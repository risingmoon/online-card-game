from gevent.pywsgi import WSGIServer
from gevent.monkey import patch_all
from urlparse import parse_qs
from game import Game
import json
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

            headers, status, body = func(**kwargs)

        except NameError:
            headers = [("Content-type", "text/html")]
            status = "404 Not Found"
            body = "<h1>Not Found</h1>"

        except Exception:
            headers = [("Content-type", "text/html")]
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
            (r'^$', self.redirect_from_root),
            (r'^login$', self.login),
            (r'^lobby$', self.lobby),
            (r'^lobby/join$', self.lobby_join),
            (r'^lobby/vote$', self.lobby_vote),
            (r'^lobby/edit$', self.lobby_edit),
            (r'^lobby/leave$', self.lobby_leave),
            (r'^lobby/update$', self.lobby_update),
            (r'^game$', self.game_room),
            (r'^game/call$', self.game_room_call),
            (r'^game/fold$', self.game_room_fold),
            (r'^game/update$', self.game_room_update),
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
            # if re.match(r'^lobby', matchpath) and self.in_game:
            #     return self.game_room, arg

            #If the user tries to get into a game, but a game is not in
            #session, redirect them to the lobby. Hold on to the arg parsed
            #out, if applicable, so they are redirected as the appropriate
            #user.
            # if re.match(r'^game', matchpath) and not self.in_game:
            #     return self.lobby, arg

            return func, arg

        #Raise a NameError if we completely failed to map the URL.
        raise NameError

    def redirect_from_root(self, **kwargs):
        """If a user accesses the root, redirect them to either the lobby
        or the game room based on whether or not a game is in session.
        """

        if self.in_game:
            return [("Content-type", "text/html"),
                    ("Location", "%s/game" % self.base_url)], \
                "301 Redirect", ''
        else:
            return [("Content-type", "text/html"),
                    ("Location", "%s/lobby" % self.base_url)], \
                "301 Redirect", ''
            #return self.login()

    def login(self, **kwargs):
        page = """
        <center>
        <h1>Lobby</h1>
        <div>
        <form method="POST" action="/lobby/join">
            <input type="text" name="username" placeholder="Username"/>
            <input type="submit" value="Join" />
        </form>
        </div>
        </center>
        """
        return (page, None)

    def lobby_update(self, idnum=None, **kwargs):
        """Builds a json object containing information on the lobby that
        is sent to the user when their browser long polls or when they
        complete any operation that changes the state of the lobby. If
        in_game has become true since the last time this function was
        called, the json object returned instructs the javascript on the
        user's lobby page to redirect them to the game.
        """
        if self.in_game:
            info = {'redirect': "/game/%s" % idnum}

        else:
            userdata = []

            if idnum:
                userdata.append(self.users[idnum])

            for userid in sorted(self.users):
                if userid == idnum:
                    continue
                userdata.append(self.users[userid])

            info = {'users': userdata}
            if idnum:
                info.update({'idnum': idnum})

        return [("Content-type", "application/json")], \
            "200 OK", json.dumps(info)

    def lobby(self, **kwargs):
        """Answer the user's initial lobby request by reading the lobby
        html and serving it to them.
        """
        # with open('static/lobby.html') as infile:
        with open('lobby.html') as infile:
            page = infile.read()

        return [("Content-type", "text/html")], "200 OK", page

    def lobby_join(self, username="Player", **kwargs):
        """Allows the player to join the game in the lobby. Adds their new
        username and id to the game server object, then calls update_lobby
        to fetch and return a json object containing the new information
        about the lobby.
        """
        idnum = str(self.next_id)
        self.next_id += 1

        self.users[idnum] = [username, 'No']

        return self.lobby_update(idnum=idnum)

    def lobby_vote(self, idnum=None, **kwargs):
        """Function called when the player toggles their start vote in
        the lobby. It toggles their vote, then checks to see whether all
        players have voted, setting self.in_game if so. update_lobby is
        then called either to reflect their changed vote or to redirect
        them to the game room if all players have voted.
        """
        self.users[idnum][1] = \
            'Yes' if (self.users[idnum][1] == 'No') else 'No'

        votecheck = True
        for userid in self.users:
            if self.users[userid][1] == 'No':
                votecheck = False
                break

        if votecheck:
            self.in_game = True
            for userid in sorted(self.users):
                self.users[userid].append(
                    game.add_player(self.users[userid][0])
                )

        return self.lobby_update(idnum=idnum)

    def lobby_edit(self, idnum=None, username="Player", **kwargs):
        """Allows the user with the given id number to change their
        username to the username passed in.
        """
        self.users[idnum][0] = username
        return self.lobby_update(idnum=idnum)

    def lobby_leave(self, idnum=None, **kwargs):
        """Allows the user with the given id number to leave the game."""
        del self.users[idnum]
        return self.lobby_update()

    def game_room_update(self, idnum=None, **kwargs):
        """Call the game's poll_game method to get a json data dump on
        the game. If an id number is passed, it's specific to the game
        from their perspective.
        """
        return [("Content-type", "application/json")], "200 OK", \
            json.dumps(game.poll_game(player=self.users[idnum][2]))

    def game_room(self, idnum=None, **kwargs):
        """Read in and serve the game room HTML."""
        # with open('static/game.html') as infile:
        with open('game.html') as infile:
            page = infile.read()

        return [("Content-type", "text/html")], "200 OK", page

    def game_room_call(self, idnum=None, bet=0):
        """Function called when the player places a bet (whether it be a
        call or a raise).
        """
        game.update_game(bet=
            game.players_list(self.users[idnum][2]).bet(bet))

        return self.game_room_update(idnum=idnum)

    def game_room_fold(self, idnum=None):
        """Function called when the player folds."""
        game.update_game(fold=
            game.players_list(self.users[idnum][2]).fold())

        return self.game_room_update(idnum=idnum)


if __name__ == '__main__':
    game = GameRoomServer()
    patch_all()
    server = WSGIServer(('', 8080), game)
    server.serve_forever()
