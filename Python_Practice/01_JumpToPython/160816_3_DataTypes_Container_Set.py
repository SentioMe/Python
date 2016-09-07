#Container - Set

#note : 중복을 허용하지 않고, 순서가 없는 자료구조

s1 = set([1, 2, 3, 4, 5, 6])
s2 = set([4, 5, 6, 7, 8, 9])

print('set s1 = {0}'.format(s1))
print('set s2 = {0}'.format(s2))

print('s1과 s2의 교집합 : {0}'.format(s1 & s2)) #or, s1.intersection(s2)
print('s1과 s2의 합집합 : {0}'.format(s1 | s2)) #or. s1.union(s2)
print('s1과 s2의 차집합 : {0}'.format(s1 - s2)) #or, s1.difference(s2)


#note
#add : 1개의 값 추가
#udpate : 복수의 값 추가
#remove : 값 제거