#class Inheritance and override

class Animal:
    name = '동물'

    def __init__(self, leg):
        self.leg = leg

    def desc(self):
        print('%s (은)는 %d 발 달린 동물이다' %(self.name, self.leg))

    def action(self):
        print('%s (은)는 뛸 수 있다' % self.name)

class Bat(Animal):
    name = '박쥐'

    def action(self):
        print('%s (은)는 날 수 있다' % self.name)

class Cat(Animal):
    name = '고양이'


bat = Bat(2)
bat.desc()
bat.action()

cat = Cat(4)
cat.desc()
cat.action()