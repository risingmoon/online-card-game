Online Poker Project
============

Contributors:

Objects:

-Game:
    
    
-Players:

* Attributes: connection socket, connection address, username, money
* Draw Cards
* Call
* Raise bets
* Fold

Game Setup (Behavior?):

1. Game Server:
    * Binds address and port
    * Listens for connections
    * Accepts connections (connection, address) > Player List

2. Player join game room (see above)

3. Players click ready button:
    * set ready to True in Player List

4. Game Server:
    * Begins 15 second countdown

5. Game Server:
    
    * Starts game.
    * Choose random player as token
    * Set big and small blinds based on token player
    * Round
    * Increment Next Player: Modulus operator

* Round
    1. Check Players for money/fold (need details)
    2. Break when no players can play (need details)
