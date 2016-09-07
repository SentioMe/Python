#02. String

#string
str = "Python's very easy!"
print(str)
str = 'He said, "Python\'s very easy!"'
print(str)

#파이썬의 문자열 지시자는 ('), (")가 있다
#각각 문맥에서 해당 표기가 필요할 때 다른 지시자로 문자열을 감싸거나
#역슬래시(\)를 앞에 추가하여 문자형으로 인식시켜야한다

#multi line string
strMulti = 'Life is cool\nWoo Woo Woo\nLife is so cool~'
print(strMulti)

strMulti = '''Life is cool
Woo Woo Woo
Life is so cool~'''
print(strMulti)

#문자열 지시자 ', "를 나란히 3개를 입력하면 이스케이프 코드 없이도 인식이 된다


#Operation
print('Python' + ' ' + 'string test')
print('=' * 20)
print('Python string operation')
print('=' * 20)

#Indexing
str = 'Python is simple'
print(str[3])
print(str[-1])
print(str[2:10])

#Formating
valueA = 20
valueB = 10.56789
print('valueA = %d, valueB = %.3f' %(valueA, valueB))

#Alignment
print('Hi, %50s Word' % 'Right Align')
print('Hi, %-50s Word' % 'Left Align')

#Function
str = 'Test string'
print('Test string 문자열 내, t 문자의 개수 : %d' %str.count('t'))
print('Test string 문자열 내, e 문자의 위치 : %d' %str.find('e'))
print('Test string 문자열 내, e 문자의 위치 : %d' %str.index('e')) #note : find는 없는 문자라면 -1을 리턴하고, index는 오류를 리턴한다
print(str.join('join'))
print('대문자 화 : ' + str.upper())
print('소문자 화 : ' + str.lower())

strStrip = ' test test '
print('오른쪽 공백 제거 : ' + strStrip.rstrip())
print('왼  쪽 공백 제거 : ' + strStrip.lstrip())
print('양  쪽 공백 제거 : ' + strStrip.strip())

print('Life is cool'.replace('Life', 'Game'))

str = 'Game is amazing'
splitVal = str.split()
print(splitVal)
splitVal = 'a,b,c,d'.split(',')
print(splitVal)