left = 30
right = 20

if left < right * 2 :
    print('right * 1.5 over left : ', left, right)
elif left == right / 2 :
    print('right / 2 equal left : ', left, right)
else :
    print('left, right value : ', left, right)


left = 10
right = 15

if left + right > 20 and left < 20 :
    print('left + right > 20 and left < 20 : ', left)
else :
    print('none')