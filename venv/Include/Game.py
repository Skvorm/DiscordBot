from Deck import Deck
from random import shuffle

class Game:
    d = Deck()
    shuffle(d.currentDeck)
    winner = ""

    def get_random_card(self):
        return self.d.peek_card()

    def get_winner(self):
        return self.winner

    def set_winner(self, player):
        self.winner = player

    # returns formatted message:
    def play(self, player_list, round_num):
        if len(player_list) == 0:
            return "No Cards Drawn"
        highest = []
        card_list = []
        winners = []
        num_winners = 0
        highest_card = ''
        msg = ''

        print(player_list)
        name_list = self.d.get_cards_names(player_list)
        for card in name_list:
            card_list.append(card)
        ret_cards = self.d.card_list_sort(card_list)
        highest = self.d.get_highest(ret_cards)
        print("Highest Card " + str(highest) + str(len(highest)))
        # winners.append(name_list.get(highest))
        num_winners = len(highest)
        if num_winners >= 2:
            if isinstance(highest, list):
                for card in highest:
                    print(card + '\n')
                winners.append(name_list[card])
            else:
                winners.append(name_list[highest])
        else:
            winners.append(name_list[highest[0]])
        self.d.resetdeck()
        shuffle(self.d.currentDeck)
        msg = (round_num * ' ') + 'Highest Card:Round ' + str(round_num) + '\n'
        for name in name_list:
            msg += '•' + name_list[name] + ':' + name + '\n'
        if len(winners) == 1:
            self.winner = str(winners[0])
            msg += (round_num * ' ') + 'Winner is ' + self.winner + ' with the ' + str(highest[0])
        else:
            msg += (round_num * ' ') + ' -Round Tie-\n '
            # for person in winners:
            for p in range(0, len(winners), 1):
                if p == (len(winners) - 1):
                    msg += f"{(round_num * ' ')} and {str(winners[p])} with the {str(highest[p])}"
                else:
                    msg += f"{(round_num * ' ')} {str(winners[p])} with the {str(highest[p])}"
            msg += (round_num * ' ') + '\n -Tie Breaker-\n'
            round_num += 1
            msg += self.play(winners, round_num)
            print(msg)

        return msg
    # if run as main, plays test game with 4 players


if __name__ == '__main__':
    g = Game()
    d1 = Deck()
    players = ['bill', 'bob', 'billy', 'larry']
    ##print(g.play(players,1))
    ##print(d1.get_cards_names(players))
    print(g.play(players, 1))
