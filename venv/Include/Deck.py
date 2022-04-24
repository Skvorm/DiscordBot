from random import randrange


class Deck:
    suit = ["Clubs", "Diamonds", "Spades", "Hearts"]
    rank = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
    rank_aces_high=rank[1:13]
    rank_aces_high.append("Ace")
    currentDeck = []
    size = 52
    aces_high=True

    def cmp_cards(self, card_1, card_2, aces_high=True):
        card_list1 = card_1.split()
        card_list2 = card_2.split()
        if aces_high:
            card1_rank_index = self.rank_aces_high.index(card_list1[0])
            card2_rank_index = self.rank_aces_high.index(card_list2[0])
        else:
            card1_rank_index = self.rank.index(card_list1[0])
            card2_rank_index = self.rank.index(card_list2[0])
        if card1_rank_index == card2_rank_index:
            return 0
        if card2_rank_index > card1_rank_index:
            return 1
        else:
            return -1

    def card_list_sort(self, card_list, aces_high=True):
        if aces_high:
            sorted_list = sorted(card_list, key=lambda x: self.rank_aces_high.index(x.split()[0]))
        else:
            sorted_list = sorted(card_list, key=lambda x: self.rank.index(x.split()[0]))
        return sorted_list

    def get_highest(self, card_list, aces_high=True):
        sorted_list = self.card_list_sort(card_list, aces_high)
        print("list:"+str(sorted_list))
        highest_rank = ""
        highest_cards = []
        if len(sorted_list) == 0:
            return "No Highest Card"
        elif len(sorted_list) == 1:
            return sorted_list
        elif len(sorted_list) >= 2:
            if aces_high:
                highest_rank = max(sorted_list, key=lambda x: self.rank_aces_high.index(x.split()[0]))
            else:
                highest_rank = max(sorted_list, key=lambda x: self.rank.index(x.split()[0]))
        else:
            return "No Highest Card"
        highest_rank = highest_rank.split()[0]
        highest_cards = [card for card in sorted_list if highest_rank in card]
        if isinstance(highest_cards, str):
            temp = highest_cards
            highest_cards = [temp]
        return highest_cards

    def resetdeck(self):
        self.currentDeck = []
        self.size = 52
        for x in list(self.suit):
            for y in list(self.rank):
                self.currentDeck.append(y + " of " + x)

    def __init__(self,aces_high=True):
        self.aces_high=aces_high
        self.resetdeck()

    def get_card(self):
        self.size-=1
        return self.currentDeck.pop()

    def peek_card(self):
        card = f'{self.rank[randrange(0, 13)]} of {self.suit[randrange(0, 4)]}'
        return str(card)

    def get_card_num(self):
        return self.size

    def get_cards(self, number):
        card_list = []
        if number < 0:
            number = 0
        if number > self.size:
            number = self.size
        print("getting " + str(number) + " cards")
        for i in range(number):
            card_list.append(self.get_card())
        #self.size = self.size - number
        return card_list

    def get_cards_names(self, names):
        name_dict = {}
        drawn = self.get_cards(len(names))
        for index, card in enumerate(drawn, start=0):
            name_dict[card] = names[index]
        return name_dict
if __name__ == '__main__':
    d = Deck()
    print(d.rank)
    print(d.rank_aces_high)
