#Control Statement

#1 if
value = 10
if value > 10:
    print('value > 10')
elif value == 10:
    print('value == 10')
else:
    print('value < 10')

#for

values = [1, 2, 3, 4]
for var in values:
    print(var)

for i in range(1, 10):
    print(i, end=' ')
print()

#while
cur = 0
while cur < 10:
    cur = cur + 1
    print('반복 {0} 회째'.format(cur))
