import abc


class Mammal(abc.ABC):
    @abc.abstractmethod
    def move(self):
        pass


class Dolphin(Mammal):
    def move(self):
        print('I am swimming!')


class Bat(Mammal):
    pass


d = Dolphin()
d.move()

b = Bat()

