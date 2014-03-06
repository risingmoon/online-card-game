'''This creates a game playable from the command line for testing.'''

from game import Game

the_game = Game()
the_game.add_player('Matt')
the_game.add_player('Justin')
the_game.add_player('Jordan')
the_game.add_player('Cris')

the_game.initialize_game()

while True:
    p = the_game.current_player
    if the_game.common_cards:
        print('Common cards:')
        for c in the_game.common_cards:
            print c
    your_hand = the_game.players_list[p].hand
    print('Your cards: ' + str(your_hand[0]) + ', ' + str(your_hand[1]))
    action = raw_input(
        the_game.players_list[p].name +
        ': Enter "fold" to fold, "bet" to bet:\r\n')

    if action == 'fold':
        the_game.update_game(fold=the_game.players_list[p].fold())
    elif action == 'bet':
        min_bet = the_game.min_bet - the_game.players_list[p].bet
        amount = input('Bet amount (min ' + str(min_bet) + '):\r\n')
        the_game.update_game(the_game.players_list[p].call(amount))

    if the_game.done:
        print(
            the_game.winner + ' wins ' + str(the_game.pot_won) + ' with ' +
            the_game.best_string + '!')
        the_game.done = False
