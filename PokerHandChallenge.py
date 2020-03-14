from collections import defaultdict
from itertools import combinations
import unittest


# Pokerhand é a classe aonde é criada a lista com os valores e naipes das cartas, assim como os métodos necessários
# para a lógica do algoritmo

class Pokerhand:
    values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13,
              "A": 14}
    suits = {'S': 'spades', 'H': 'hearts', 'D': 'diamonds', 'C': 'clubs'}

    # método para ordenar as cartas

    def __init__(self, cards):
        self.cards = sorted(cards, key=lambda x: self.values[x[0]], reverse=True)
        self.values = [self.values[card[0]] for card in self.cards]
        self.suits = [card[1] for card in self.cards]

        # Método que retorna um score para cada possível mão de poker baseada em suas regras padrão, com um total de
        # 10 possibilidades

    def check_hand_score(self):
        if self.check_royal_straight_flush():
            return 10
        if self.check_straight_flush():
            return 9
        if self.check_four_of_a_kind():
            return 8
        if self.check_full_house():
            return 7
        if self.check_flush():
            return 6
        if self.check_straight():
            return 5
        if self.check_three_of_a_kind():
            return 4
        if self.check_two_pairs():
            return 3
        if self.check_one_pairs():
            return 2
        return 1

    card_order_dict = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12,
                       "K": 13, "A": 14}

    # Métodos que checam cada possibilidade de mão de poker

    def check_royal_straight_flush(self):
        if self.check_straight_flush() and self.values == list(range(14, 9, -1)):
            return True
        else:
            return False

    def check_straight_flush(self):
        if self.check_flush() and self.check_straight():
            return True
        else:
            return False

    def check_four_of_a_kind(self):
        values = [i[0] for i in self.cards]
        value_counts = defaultdict(lambda: 0)
        for v in values:
            value_counts[v] += 1
        if sorted(value_counts.values()) == [1, 4]:
            return True
        return False

    def check_full_house(self):
        values = [i[0] for i in self.cards]
        value_counts = defaultdict(lambda: 0)
        for v in values:
            value_counts[v] += 1
        if sorted(value_counts.values()) == [2, 3]:
            return True
        return False

    def check_flush(self):
        suits = [i[1] for i in self.cards]
        if len(set(suits)) == 1:
            return True
        else:
            return False

    def check_straight(self, card_order_dict=None):
        values = [i[0] for i in self.cards]
        value_counts = defaultdict(lambda: 0)
        for v in values:
            value_counts[v] += 1
        card_values = [card_order_dict[i] for i in values]
        value_range = max(card_values) - min(card_values)
        if len(set(value_counts.values())) == 1 and (value_range == 4):
            return True
        else:
            # check straight with low Ace
            if set(values) == set(["A", "2", "3", "4", "5"]):
                return True
            return False

    def check_three_of_a_kind(self):
        values = [i[0] for i in self.cards]
        value_counts = defaultdict(lambda: 0)
        for v in values:
            value_counts[v] += 1
        if set(value_counts.values()) == set([3, 1]):
            return True
        else:
            return False

    def check_two_pairs(self):
        values = [i[0] for i in self.cards]
        value_counts = defaultdict(lambda: 0)
        for v in values:
            value_counts[v] += 1
        if sorted(value_counts.values()) == [1, 2, 2]:
            return True
        else:
            return False

    def check_one_pairs(self):
        values = [i[0] for i in self.cards]
        value_counts = defaultdict(lambda: 0)
        for v in values:
            value_counts[v] += 1
        if 2 in value_counts.values():
            return True
        else:
            return False

        # Classe que compara as mão dentre dois jogadores e pontualiza, a mão com maior somatório de pontos vence


class Comparehands:
    poker_hand_1 = []
    poker_hand_2 = []
    poker_hand_score_1 = 0
    poker_hand_score_2 = 0
    result = 0

    def __init__(self, cards):
        cards = cards.split()
        self.poker_hand_1 = Pokerhand(cards[0:5])
        self.poker_hand_2 = Pokerhand(cards[5:10])
        self.compare_with();

    def compare_with(self):
        self.poker_hand_score_1 = self.poker_hand_1.check_hand_score();
        self.poker_hand_score_2 = self.poker_hand_2.check_hand_score();

        if self.poker_hand_score_1 > self.poker_hand_score_2:
            Result = "WIN"
        else:
            Result = "LOSS"

        # Conjunto de teste unitários para validação do código

        self.assertTrue(Pokerhand("TC TH 5C 5H KH").compare_with(Pokerhand("9C 9H 5C 5H AC")) == Result.WIN)
        self.assertTrue(Pokerhand("TS TD KC JC 7C").compare_with(Pokerhand("JS JC AS KC TD")) == Result.LOSS)
        self.assertTrue(Pokerhand("7H 7C QC JS TS").compare_with(Pokerhand("7D 7C JS TS 6D")) == Result.WIN)
        self.assertTrue(Pokerhand("5S 5D 8C 7S 6H").compare_with(Pokerhand("7D 7S 5S 5D JS")) == Result.LOSS)
        self.assertTrue(Pokerhand("AS AD KD 7C 3D").compare_with(Pokerhand("AD AH KD 7C 4S")) == Result.LOSS)
        self.assertTrue(Pokerhand("TS JS QS KS AS").compare_with(Pokerhand("AC AH AS AS KS")) == Result.WIN)
        self.assertTrue(Pokerhand("TS JS QS KS AS").compare_with(Pokerhand("TC JS QC KS AC")) == Result.WIN)
        self.assertTrue(Pokerhand("TS JS QS KS AS").compare_with(Pokerhand("QH QS QC AS 8H")) == Result.WIN)
        self.assertTrue(Pokerhand("AC AH AS AS KS").compare_with(Pokerhand("TC JS QC KS AC")) == Result.WIN)
        self.assertTrue(Pokerhand("AC AH AS AS KS").compare_with(Pokerhand("QH QS QC AS 8H")) == Result.WIN)
        self.assertTrue(Pokerhand("TC JS QC KS AC").compare_with(Pokerhand("QH QS QC AS 8H")) == Result.WIN)
        self.assertTrue(Pokerhand("7H 8H 9H TH JH").compare_with(Pokerhand("JH JC JS JD TH")) == Result.WIN)
        self.assertTrue(Pokerhand("7H 8H 9H TH JH").compare_with(Pokerhand("4H 5H 9H TH JH")) == Result.WIN)
        self.assertTrue(Pokerhand("7H 8H 9H TH JH").compare_with(Pokerhand("7C 8S 9H TH JH")) == Result.WIN)
        self.assertTrue(Pokerhand("7H 8H 9H TH JH").compare_with(Pokerhand("TS TH TD JH JD")) == Result.WIN)
        self.assertTrue(Pokerhand("7H 8H 9H TH JH").compare_with(Pokerhand("JH JD TH TC 4C")) == Result.WIN)
        self.assertTrue(Pokerhand("JH JC JS JD TH").compare_with(Pokerhand("4H 5H 9H TH JH")) == Result.WIN)
        self.assertTrue(Pokerhand("JH JC JS JD TH").compare_with(Pokerhand("7C 8S 9H TH JH")) == Result.WIN)
        self.assertTrue(Pokerhand("JH JC JS JD TH").compare_with(Pokerhand("TS TH TD JH JD")) == Result.WIN)
        self.assertTrue(Pokerhand("JH JC JS JD TH").compare_with(Pokerhand("JH JD TH TC 4C")) == Result.WIN)
        self.assertTrue(Pokerhand("4H 5H 9H TH JH").compare_with(Pokerhand("7C 8S 9H TH JH")) == Result.WIN)
        self.assertTrue(Pokerhand("4H 5H 9H TH JH").compare_with(Pokerhand("TS TH TD JH JD")) == Result.LOSS)
        self.assertTrue(Pokerhand("4H 5H 9H TH JH").compare_with(Pokerhand("JH JD TH TC 4C")) == Result.WIN)
        self.assertTrue(Pokerhand("7C 8S 9H TH JH").compare_with(Pokerhand("TS TH TD JH JD")) == Result.LOSS)
        self.assertTrue(Pokerhand("7C 8S 9H TH JH").compare_with(Pokerhand("JH JD TH TC 4C")) == Result.WIN)
        self.assertTrue(Pokerhand("TS TH TD JH JD").compare_with(Pokerhand("JH JD TH TC 4C")) == Result.WIN)


if __name__ == '__main__':
    unittest.main()
