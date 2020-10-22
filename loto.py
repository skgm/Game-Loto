import random


class LotoCard:
    def __init__(self, name):
        self.name = name
        self.amount = 91
        self.card = None
        self.cards = self.create_cards()

    def create_cards(self):
        """
        Здесь создается список списков с уникальными элементами. Затем рандомно в списках 5 цифр заменяются
        на знак '_'(означающий пустоту)
        :return: карта
        """
        self.card = [[None for i in range(1, self.amount)] for j in range(3)]
        cards = [i for i in range(1, self.amount)]
        random.shuffle(cards)
        # Делим список на равные по длине списки
        f_lam = lambda lst, sz: [lst[i:i + sz] for i in range(0, len(lst), sz)]
        ca = f_lam(cards, 30)
        # Вырезаем списки по 9 уникальных элементов в каждом
        for k in range(3):
            self.card[k] = ca[k][:9]
        b = [i.sort() for i in self.card]
        for i in range(3):
            rn = [x for x in range(1, 9)]
            random.shuffle(rn)
            # Рандомно расставляем '_' по спискам
            for j in range(5):
                self.card[i][rn[j]] = '_'
        return self.card


class LotoGame(LotoCard):
    def __init__(self, human, comp):
        self.human = human
        self.comp = comp
        self.barrel = None
        self.bool = True
        self.points_human = 0
        self.points_comp = 0

    def create_gen(self, g):
        """
        Генратор получт список из 90 элементов,
        расположенных в рандомном порядке и будет выдавать поочередно элементы этого списка
        (Для сохранности уникальности каждого элемента)
        :param g: список
        :return: элемент списка
        """
        for i in g:
            yield i

    def check(self):
        """
        Функция, которая приводит список к формату карточки из лото
        """
        a = '\n'.join([''.join(['%s\t' % i for i in row]) for row in self.human.cards])
        c = '\n'.join([''.join(['%s\t' % i for i in row]) for row in self.comp.cards])
        print('\n\tВаш счет : ', self.points_human, '\n\tСчет компьютера : ', self.points_comp)
        print('-' * 50, "\n")
        print('Ваша карта : \n', a, '\n')
        print('Карта компьютера : \n', c, '\n')

    def show_winner(self, name):
        print('Победил ', name)
        self.bool = False

    def start(self):
        print('\tПриветствую вас ', self.human.name, '\n\tПротив вас играет', self.comp.name, '\n\tНачнем!')
        z = [i for i in range(1, 91)]
        random.shuffle(z)
        # Генератор для выдачи уникальных номерков бочонков
        gen = self.create_gen(z)
        while self.bool:
            try:
                self.barrel = next(gen)
            except StopIteration:
                self.bool = False
            self.check()
            print('-' * 50, "\n")
            print('бочонок с номером : ', self.barrel)
            print('-' * 50, "\n")

            if self.barrel in self.comp.cards[0] or self.barrel in self.comp.cards[1] \
                    or self.barrel in self.comp.cards[2]:
                for i in range(len(self.comp.cards)):
                    for j in range(len(self.comp.cards[i])):
                        if self.comp.cards[i][j] == self.barrel:
                            self.comp.cards[i][j] = 'X'
                self.points_comp += 1

            ans = input('Введите "y" если такое число есть в вашей карте, или "n" если нет')
            while ans != 'n' and ans != 'y':
                ans = input('Только "y" или "n"')
            print('-' * 50, "\n")

            if ans == 'y':
                if self.barrel in self.human.cards[0] or self.barrel in self.human.cards[1] \
                        or self.barrel in self.human.cards[2]:
                    for k in range(len(self.human.cards)):
                        for n in range(len(self.human.cards[k])):
                            if self.human.cards[k][n] == self.barrel:
                                self.human.cards[k][n] = 'X'
                    self.points_human += 1
                else:
                    print('В вашей карте такого номера нет. Вы проиграли')
                    self.bool = False
            elif ans == 'n':
                if self.barrel in self.human.cards[0] or self.barrel in self.human.cards[1] \
                        or self.barrel in self.human.cards[2]:
                    print('В вашей карте был такой номер. Вы проиграли')
                    self.bool = False

            if self.points_human == 12:
                self.show_winner(self.human.name)
            if self.points_comp == 12:
                self.show_winner(self.comp.name)


Human = LotoCard(input('Введите свое имя :\n'))
Comp = LotoCard('Компьютер')
game = LotoGame(Human, Comp)
game.start()
