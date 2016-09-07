#input

inputVal = input('입력하세요: ')
print(inputVal)

#print

#어간에 대해 따옴표(", ')를 사용하면 문자열 합산 연산을 사용한 것과 같다
print('Life' 'is' 'Cool')
print('Life' + 'is' + 'Cool')

#쉼표를 사이에 넣으면 띄어쓰기로 적용된다
print('Life', 'is', 'Cool')

#end로 끝 문자를 지정하면 한 줄로 쓸 수 있다
for i in range(2, 10):
    for j in range(1, 10):
        print('%d X %d = %d' % (i, j, i * j), end=' ')
    print()
