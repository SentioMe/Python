#Function

def sum_and_mul(a, b):
    return a + b, a * b

def variableParamFunc(*args):
    ret = 0
    for arg in args:
       ret = ret + arg
    return  ret

def defaultParamFunc(name, age, isMan = True):
    sexual = '남자' if isMan else '여자'
    print('''이름은 {0}이고, 나이는 {1} 살입니다
성별은 {2} 입니다'''.format(name, age, sexual))


#global을 선언하면 외부 변수를 가져와 사용할 수는 있으나
#외부 변수 의존적이므로 사용하지 않음
def usedGlobalValue():
    global value
    value = value + 1


result = sum_and_mul(1, 2)
print('returned tuple : {0}'.format(result))

result1, result2 = sum_and_mul(3, 4)
print('returned sum : {0}'.format(result1))
print('returned mul : {0}'.format(result2))


print('1 to 5 sum : %d' % variableParamFunc(1, 2, 3, 4, 5))

defaultParamFunc('Kim', 25)

value = 0
print('Non called usedGlobalValue() function : %d' % value)
usedGlobalValue()
print('Called usedGlobalValue() function : %d' % value)