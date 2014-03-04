from gevent.pywsgi import WSGIServer
from gevent.monkey import patch_all
from urlparse import parse_qs
from game import Game
import re


class GameRoomServer(object):
    """The game room server. This class is callable, and handles dispatch
    to the various functions of the game room based on its internal state.
    """

    def __init__(self):
        """Initialize the game room with a game object."""
        self.game = Game()

        #Each user can be tied with a Player object in the game.
        self.users = {}

        #We start in the lobby, and go to the game when all players are
        #ready to start.
        self.in_game = False

        #Keep track of the next id number that can be allocated.
        self.next_id = 1

        #For asbolute redirects. Leave blank to redirect by relative URL.
        self.base_url = ''

    def __call__(self, environ, start_response):
        """When called, the GameRoomServer class behaves as a dispatcher."""

        headers = [("Content-type", "text/html")]
        try:
            path = environ.get('PATH_INFO', None)
            if path is None:
                raise NameError

            #Parse out POST request information.
            request_size = int(environ.get('CONTENT_LENGTH', 0))
            request_body = environ['wsgi.input'].read(request_size)
            kwargs = parse_qs(request_body)

            #By default, parse_qs returns lists of values that were passed
            #for each keyword in the query string. We're expecting only one
            #value for each, so here we pull the first (and only) value
            #out of the list and assign it directly to the keyword in kwargs.
            for key, val in kwargs.iteritems():
                kwargs[key] = val[0]

            func, arg = self._resolve_path(path)

            #Overwrite idnum argument with corresponding argument parsed
            #out of the url, if present.
            if arg:
                kwargs['idnum'] = str(arg)

            body, header = func(**kwargs)

        except NameError:
            status = "404 Not Found"
            body = "<h1>Not Found</h1>"
            header = None

        except Exception:
            status = "500 Internal Server Error"
            body = "<h1>Internal Server Error</h1>"
            header = None

        finally:
            if header:
                status = "301 Redirect"
                headers.append(header)
            else:
                status = "200 OK"

            headers.append(('Content-length', str(len(body))))
            start_response(status, headers)
            return [body]

    def _resolve_path(self, path):
        """Private method that resolves the url received when the class
        is called. The url is mapped onto one of the class methods."""

        urls = [
            (r'^$', self.redirect_from_root),
            (r'^lobby$', self.lobby),
            (r'^lobby/(\d+)$', self.lobby),
            (r'^lobby/join$', self.lobby_join),
            (r'^lobby/vote$', self.lobby_vote),
            (r'^lobby/edit$', self.lobby_edit),
            (r'^lobby/leave$', self.lobby_leave),
            (r'^game$', self.game_room),
            (r'^game/(\d+)$', self.game_room),
            (r'^game/call$', self.game_room_call),
            (r'^game/raise$', self.game_room_raise),
            (r'^game/fold$', self.game_room_fold),
        ]

        matchpath = path.lstrip('/')

        for regexp, func in urls:
            match = re.match(regexp, matchpath)

            if match is None:
                continue

            arg = match.groups([])
            arg = arg[0] if arg else None

            #If the user tries to get into the lobby, but a game is in
            #session, redirect them to the game. Hold on to the arg parsed
            #out, if applicable, so they are redirected as the appropriate
            #user.
            if re.match(r'^lobby', matchpath) and self.in_game:
                return self.game_room_redirect, arg

            #If the user tries to get into a game, but a game is not in
            #session, redirect them to the lobby. Hold on to the arg parsed
            #out, if applicable, so they are redirected as the appropriate
            #user.
            if re.match(r'^game', matchpath) and not self.in_game:
                return self.lobby_redirect, arg

            return func, arg

        #Raise a NameError if we completely failed to map the URL.
        raise NameError

    def redirect_from_root(self, **kwargs):
        """If a user accesses the root, redirect them to either the lobby
        or the game room based on whether or not a game is in session.
        """

        if self.in_game:
            return self.game_room_redirect()
        else:
            return self.lobby_redirect()

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
        <form method="POST" action="/lobby/edit">
            <input type="text" name="username" value="%s"/>
            <input type="submit" value="Change Username" />
            <input type="hidden" name="idnum" value="%s" />
        </form>
        <form method="POST" action="/lobby/vote">
            <input type="submit" value="Change Vote" />
            <input type="hidden" name="idnum" value="%s" />
        </form>
        <form method="POST" action="/lobby/leave">
            <input type="submit" value="Leave Game" />
            <input type="hidden" name="idnum" value="%s" />
        </form>
    </div>""" % (self.users[idnum][0], idnum, idnum, idnum)

        #Otherwise, the player gets a form that allows them to join the
        #game. No hidden input with id is included: the game is not keeping
        #track of them yet.
        else:
            page += """
    <div>
        <form method="POST" action="/lobby/join">
            <input type="text" name="username" placeholder="Username"/>
            <input type="submit" value="Join" />
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
    <form method="POST" action="/lobby%s">
        <input type="submit" value="Update" />
    </form>
</center>""" % (('/%s' % idnum) if idnum else '')

        return (page, None)

    def lobby_redirect(self, idnum=None, **kwargs):
        """Redirect the player to the lobby."""

        if idnum:
            return ('', ('Location', "%s/lobby/%s" % (self.base_url, idnum)))
        else:
            return ('', ('Location', "%s/lobby" % self.base_url))

    def lobby_join(self, username="Player", **kwargs):
        """Allows the player to join the game in the lobby. Adds their new
        username and id to the game server object, then returns a redirect
        to a version of the lobby page that is tailored to that id.
        """

        idnum = str(self.next_id)
        self.next_id += 1

        self.users[idnum] = [username, 'No']

        return self.lobby_redirect(idnum=idnum)

    def lobby_vote(self, idnum=None, **kwargs):
        """Function called when the player toggles their start vote in the
        lobby. If all players have voted to start, it returns a redirect
        to the game room and changes the status of the game server object
        to reflect that we're now ingame. Otherwise, it returns a redirect
        to a version of the lobby that reflects the changed vote.
        """

        self.users[idnum][1] = \
            'Yes' if (self.users[idnum][1] == 'No') else 'No'

        votecheck = True
        for userid in self.users:
            if self.users[userid][1] == 'No':
                votecheck = False
                break

        if votecheck:
            self._initialize_game_room()
            return self.game_room_redirect(idnum=idnum)
        else:
            return self.lobby_redirect(idnum=idnum)

    def lobby_edit(self, idnum=None, username="Player", **kwargs):
        """Allows the user with the given id number to change their username
        to the username passed in.
        """

        self.users[idnum][0] = username
        return self.lobby_redirect(idnum=idnum)

    def lobby_leave(self, idnum=None, **kwargs):
        """Allows the user with the given id number to leave the game."""

        del self.users[idnum]
        return self.lobby_redirect()

    def _initialize_game_room(self):
        """When the game starts, this function is called to set up the game
        and all players in the game.
        """

        for userid in self.users:
            self.users[userid].append(
                self.game.add_player(self.users[userid][0]))

        self.game.run_game()

        #Change self.in_game last so that players don't get into the game
        #room while the game is still setting up.
        self.in_game = True

    def game_room(self, idnum=None, **kwargs):
        """Builds the html for the game room. If an id number is given,
        the user gets back a version that is tailored to that id number.
        If not, the player gets a version of the page that allows them only
        to spectate and update the room.
        """
        return "<h1>We are in-game.</h1>", None

    def game_room_redirect(self, idnum=None, **kwargs):
        """Redirect the player to the game room."""
        if idnum:
            return ('', ('Location', "%s/game/%s" % (self.base_url, idnum)))
        else:
            return ('', ('Location', "%s/game" % self.base_url))

    def game_room_raise(self, idnum=None, amount=None, **kwargs):
        """Function called when the player places a bet or raises a bet."""

        self.users[idnum][2].raise_bet(int(amount))
        return self.game_room_redirect(idnum=idnum)

    def game_room_call(self, idnum=None, amount=None, **kwargs):
        """Function called when the player calls."""

        self.users[idnum][2].call(int(amount))
        return self.game_room_redirect(idnum=idnum)

    def game_room_fold(self, idnum=None, **kwargs):
        """Function called when the player folds."""

        self.users[idnum][2].fold()
        return self.game_room_redirect(idnum=idnum)


if __name__ == '__main__':
    game = GameRoomServer()
    patch_all()
    server = WSGIServer(('', 8080), game)
    server.serve_forever()
