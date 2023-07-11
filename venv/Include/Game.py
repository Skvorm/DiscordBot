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
    def play(self, player_list, round_num=1):
        if len(player_list) == 0:
            return "No Cards Drawn"
        highest = []
        winners = []
        card_list=[]
        num_winners = 0
        highest_card = ''
        msg = ''
        indent = 2 * " "
        name_list = self.d.get_cards_names(player_list)
        for card in name_list:
            card_list.append(card)
        ret_cards = self.d.card_list_sort(card_list)
        highest = self.d.get_highest(ret_cards)
        num_winners = len(highest)
        if num_winners >= 2:
            if isinstance(highest, list):
                for card in highest:
                    winners.append(name_list[card])
            else:
                winners.append(name_list[highest])
        else:
            winners.append(name_list[highest[0]])
        self.d.resetdeck()
        shuffle(self.d.currentDeck)
        for name in name_list:
            msg += f"•{name_list[name]} - {name}\n"
        if num_winners ==1:
            self.winner = str(winners[0])
            if len(highest)==1:
                highest=highest[0]
            highest=str(highest)
            msg += f"---Winner---\n**{self.winner}** with the {highest}"
        else:
            msg += f"---Winners---\n"
            # for person in winners:
            for p in range(0, len(winners), 1):
                msg+=f"•**{winners[p]}** - {highest[p]}\n"

        return msg
    # if run as main, plays test game with 4 players


if __name__ == '__main__':
    g = Game()
    d1 = Deck()
    players = ['bill', 'bob', 'billy', 'larry']
    msg=g.play(players, 1)
    print(msg)
    print(len(msg))
