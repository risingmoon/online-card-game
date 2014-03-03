from gevent.pywsgi import WSGIServer
from gevent.monkey import patch_all
from urlparse import parse_qs
import re


class GameRoomServer(object):
    """The game room server. This class is callable, and handles dispatch
    to the various functions of the game room based on its internal state.
    """

    def __init__(self):
        """Initialize the game room with a game object."""
        #self.game = game_placeholder.Game()

        #Each user can be tied with a Player object in the game.
        self.users = {}

        #We start in the lobby, and go to the game when all players are
        #ready to start.
        self.in_game = False

        #Keep track of the next id number that can be allocated.
        self.next_id = 1

    def __call__(self, environ, start_response):
        """When called, the GameRoomServer class behaves as a dispatcher."""

        headers = [("Content-type", "text/html")]
        try:
            path = environ.get('PATH_INFO', None)
            if path is None:
                raise NameError
            request_size = int(environ.get('CONTENT_LENGTH', 0))
            request_body = environ['wsgi.input'].read(request_size)
            kwargs = parse_qs(request_body)
            func = self._resolve_path(path)
            body = func(**kwargs)
            status = "200 OK"
        except NameError:
            status = "404 Not Found"
            body = "<h1>Not Found</h1>"
        except Exception:
            status = "500 Internal Server Error"
            body = "<h1>Internal Server Error</h1>"
        finally:
            headers.append(('Content-length', str(len(body))))
            start_response(status, headers)
            return [body]

    def _resolve_path(self, path):
        """Private method that resolves the url received when the class
        is called. The url is mapped onto one of the class methods."""

        urls = [
            (r'^$', self.poll_lobby_status),
            (r'^lobby$', self.lobby),
            (r'^lobby/join$', self.lobby_join),
            (r'^lobby/vote$', self.lobby_vote),
            (r'^lobby/edit$', self.lobby_edit),
            (r'^lobby/update$', self.poll_lobby_status),
            (r'^game$', self.game_room),
        ]

        matchpath = path.lstrip('/')
        for regexp, func in urls:
            match = re.match(regexp, matchpath)
            if match is None:
                continue
            return func
        raise NameError

    def poll_lobby_status(self, **kwargs):
        """Determines whether we're in-game or in the lobby and returns
        the appropriate callable. Used by the dispatcher to determine
        where to send the user.
        """

        if self.in_game:
            return self.game_room(**kwargs)
        else:
            return self.lobby(**kwargs)

    def lobby(self, idnum=None, **kwargs):
        """Builds the html for the lobby. If an id number is given, the
        user gets back a version that is tailored to that id number. If
        not, the player gets a version of the page that allows them only
        to join and view the list of players.
        """
        page = """
<center>
    <h1>Lobby</h1>"""

        #If this player has an id number, they get forms that allow them
        #to change their username and toggle their vote. The forms also
        #contain a hidden input that keeps track of their id number.
        if idnum:
            page += """
    <div>
        <form method="POST" action="edit">
            <input type="text" name="username" value="%s"/>
            <input type="submit" name="submit" value="Change Username" />
            <input type="hidden" name="idnum" value="%s" />
        </form>
        <form method="POST" action="vote">
            <input type="submit" value="Change Vote" />
            <input type="hidden" value="%s" />
        </form>
    </div>""" % (self.users[idnum][0], idnum, idnum)

        #Otherwise, the player gets a form that allows them to join the
        #game. No hidden input with id is included: the game is not keeping
        #track of them yet.
        else:
            page += """
    <div>
        <form method="POST" action="lobby/join">
            <input type="text" name="username" placeholder="Username"/>
            <input type="submit" name="submit" value="Join" />
        </form>
    </div>"""

        page += """
    <table>
        <tr>
            <td>Players</td>
            <td>Vote</td>
        </tr>"""

        #If the lobby is being accessed by a user with an ID number, format
        #the lobby so that their username, labeled, appears at the top of
        #the list of players.
        if idnum:
            page += """
        <tr>
            <td>{0} (You)</td>
            <td>{1}</td>
        </tr>""".format(*self.users[idnum])

        for userid in sorted(self.users):
            if userid == idnum:
                continue

            page += """
        <tr>
            <td>{0}</td>
            <td>{1}</td>
        </tr>""".format(*self.users[userid])

        page += """
    </table>
    <form method="POST" action="update">
        <input type="submit" value="Update" />
    </form>
</center>"""

        return page

    def lobby_join(self, username="Player", **kwargs):
        """Allows the player to join the game in the lobby. Adds their new
        username and id to the game server object, then returns a
        version of the lobby page that is tailored to that id.
        """

        idnum = self.next_id
        self.next_id += 1

        self.users[idnum] = [username, 'No']

        return self.lobby(idnum)

    def lobby_vote(self, idnum=None, **kwargs):
        """Function called when the player toggles their start vote in the
        lobby. If all players have voted to start, it returns the game room
        and changes the status of the game server object to reflect that
        we're now ingame. Otherwise, it returns a version of the lobby
        that reflects the changed vote.
        """

        self.users[idnum][1] = \
            'Yes' if self.users[idnum][1] == 'No' else 'No'

        votecheck = True
        for userid in self.users:
            if self.users[userid][1] == 'No':
                votecheck = False
                break

        if votecheck:
            self.in_game = True
            return self.game_room(idnum)
        else:
            return self.lobby(idnum)

    def lobby_edit(self, idnum=None, username="Player", **kwargs):
        """Allows the user with the given id number to change their username
        to the username passed in.
        """

        self.users[idnum][0] = username
        return self.lobby(idnum)

    def game_room(self, idnum=None, **kwargs):
        return "<h1>We are in-game.</h1>"


if __name__ == '__main__':
    game = GameRoomServer()
    patch_all()
    server = WSGIServer(('', 10101), game)
    server.serve_forever()
