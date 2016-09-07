#class

#class ClassName[(Parent Class)]
#      <Variable>
#      <Variable>
#      ...
#      def Function(self, params...)
#           func statement
#
#      def Function(self, params...)
#           func statement
#      ...
#...
#note : 필요에 따라 __init__(self, params...), 을 통해 초기값 초기화

class Calculator:
    def __init__(self):
        self.result = 0

    def add(self, num):
        self.result += num
        return self.result

    def mul(self, num):
        self.result *= num
        return self.result

    def sub(self, num):
        self.result -= num
        return self.result

    def div(self, num):
        self.result /= num
        return  self.result


cal1 = Calculator()
cal2 = Calculator()
print(type(cal1))
print(type(cal2))

print('1번 계산기 값 : %d' % cal1.add(4))
print('1번 계산기 값 : %d' % cal1.mul(3))

print('2번 계산기 값 : %d' % cal2.add(1))

print('1번 계산기 값 : %d' % cal1.add(2))

print('2번 계산기 값 : %d' % cal2.mul(2))