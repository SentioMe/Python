
#abs(number) : 전달된 수치 값의 절대값 반환
print(abs(-4))

#all(iterable) : 전달된 값이 모두 iterable 값이라면 true, 아니면 false
print(all([1, 2, 0]))

#any(iterable) : 전달된 값 중 하나라도 iterable 값이라면 true, 아니면 false
print(any([1, 2, 0]))

#chr(i)  : 전달된 정수값에 대한 ASCii값 반환
print(chr(40))

#dir(object) :  #전달된 객체 내부의 내장 함수 및 변수 반환
print(dir(1))

#divmode(x, y) : x / y를 행하여 몫과 나머지를 튜플로 반환
print(divmod(8, 6))

#enumrate(iterable) : Container의 index와 값을 반환
for i, name in enumerate(['body', 'head', 'neck']):
    print(i, name)

#eval(args, kwargs) : c#의 reflection처럼 실행 가능한 문자열을 실행시킨다
print(eval('divmod(4, 3)'))


#filter(function_or_None, iterable) : 두 번째 인자(값들) 중 첫 번째 인자(함수)의 반환값이 참인 것만 걸러서 묶어 반환한다

def positive(li):
    result = []
    for i in li:
        if i > 0:
            result.append(i)
    return  result

def positive2(x):
    return x > 0

print(positive([1, -3, 2, 0, 5, -7, 8]))
print(list(filter(positive2, [1, -3, 2, 0, 5, -7, 8])))
print(list(filter(lambda x : x > 0, [1, -3, 2, 0, 5, -7, 8])))

#hex(number) : 전달한 값의 16진수 값 반환
print(hex(10))

#id(object) : 객체의 레퍼런스를 반환한다, 아래의 반환값은 모두 같다
a = 3
print(id(3))
print(id(a))
b = a
print(id(b))

#input(args, kwargs) : 사용자 입력을 받는다
#input()

#int(x) : 전달된 문자열 형태의 숫자나 소수점 있는 숫자를 정수로 반환한다
print(int('3'))

#int(x, radix) : radix 진수로 표현된 문자열 x를 10진수로 변환하여 반환한다
print(int('111', 2))

#isinstance(object, class) : 해당 object가 해당 class의 instance인지 판별한다

#lambda : 무명 함수를 만든다

#len(object) : 입력값 object의 길이를 반환한다
len([1, 2, 3])
len('python')

#list(iterable) : 반복가능한 자료형을 받아 리스트로 반환한다
listVal = list('python')
print(listVal)

#map(function, iterable) : iterable자료들이 전달한 함수를 실행한 결과를 반환한다
print(list(map(lambda x : x * x, [1, 2, 3, 4])))

#max(iterable) : 반복 가능한 자료형 중 가장 큰 값을 반환한다
#min(iterable) : 반복 가능한 자료형 중 가장 작은 값을 반환한다

#oct(x)     : 정수 형태의 숫자를 8진수 문자열로 바꿔 반환한다

#open(fileName, [mode]) : 지정 모드로 경로의 파일을 연다 (w, r, a, b)

#ord(c)    : 문자의 아스키 코드값 반환

#pow(x, y) : x의 y 제곱값 반환

#range(a)       : 0부터 a직전까지의 값의 묶음 반환
#range(a, b)    : a부터 b직전까지의 값의 묶음 반환
#range(a, b, c) : a부터 b직전까지 c만큼 건너 뛴 값의 묶음 반환

#sorted(args, kwargs) : iterable 자료들을 정렬하여 반환한다

#str(object) : 문자열로 변환하여 반환

#tuple(iteralbe) : 반복 가능한 자료형을 튜플로 바꿔 리턴
#type(object) : 입력값의 자료형 반환
`
#zip(iterable) : 동일한 개수를 가진 자료형을 묶는다
print(list(zip([1,2,3], [4,5,6], [7,8,9])))