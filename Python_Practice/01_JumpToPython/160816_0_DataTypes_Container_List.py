#03. Container - List

testList = []
print('1 : {0}'.format(testList))
testList = [1, 2, 3]
print('2 : {0}'.format(testList))
testList = ['test', 'list']
print('3 : {0}'.format(testList))
testList = [1, 2, 3, 'test', 'list']
print('4 : {0}'.format(testList))
testList = [1, 2, 3, ['test', 'list']]
print('5 : {0}'.format(testList))

testList = [1, 2, 3]
print('시작 : {0}'.format(testList[0]))
print('끝   : {0}'.format(testList[-1]))

testList = [1, 2, ['a', 'b', 'c']]
print('testList[-1][0] : {0}'.format(testList[-1][0]))


#Operation
listA = [1, 2, 3]
listB = [4, 5, 6]
print('listA + listB = {0}'.format(listA + listB))
print('listA * 3 = {0}'.format(listA * 3))

#Indexing
testList = [1, 2, 3, 4]
testList[1] = 4
print(testList)
testList[1:3] = [6, 7, 8]
print(testList)
testList[2] = ['a', 'b']
print(testList)
testList[2:4] = []
print(testList)
del testList[1]
print(testList)

#Funtion
#append     : 뒤로 추가
#sort       : 정렬
#reverse    : 순서 뒤집기
#index      : 위치 값 반환 (범위 밖이면 에러)
#insert     : 지정 위치로 값 추가
#remove     : 지정 값 제거
#pop        : 위치 값 반환 및 삭제 (Default = 마지막)
#count      : 지정 값 갯수 체크
#extend     : 리스트에 리스트를 추가