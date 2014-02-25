online-poker
============

Contributors:

Objects:
-Game:
    -
-Players:
    -Attributes: connection socket, connection address, username, money
    -Draw Cards
    -Call
    -Raise bets
    -Fold

Game Setup:
-Game Server:
    -Binds address and port
    -Listens for connections
    -Accepts connections (connection, address) > Player List
-Player join game room (see above)
-Players click ready button:
    -set ready to True in Player List
-Game Server:
    -Begins 15 second countdown
-Game Server:
    -Starts game.
    -Choose random player as token
    -Set big and small blinds based on token player
    Round
    -Increment Next Player: Modulus operator

-Round
    -Check Players for money/fold (need details)
    -Break when no players can play (need details)
