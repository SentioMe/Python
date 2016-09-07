#class Operator overloading

class House:
    def __init__(self, size):
        self.size = size

    def __add__(self, other):
        self.size = self.size + other.size
        return self

    def __sub__(self, other):
        self.size = self.size - other.size
        return self

    def desc(self):
        if self.size < 2:
            print('일반 집이다')
        elif self.size < 4:
            print('적당한 집이다')
        elif self.size < 10:
            print('은수저다')
        else:
            print('금수저다')


kimHouse = House(2)
kimHouse.desc()

parkHouse = House(2)
parkHouse.desc()

newHouse = kimHouse + parkHouse
newHouse.desc()

kimHouse = newHouse + parkHouse
kimHouse = kimHouse + parkHouse
kimHouse = kimHouse + parkHouse
kimHouse.desc()

kimHouse -= parkHouse
kimHouse.desc()