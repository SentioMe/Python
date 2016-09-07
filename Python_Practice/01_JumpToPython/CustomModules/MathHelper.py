def sum(*args):
    ret = 0
    for arg in args:
        ret = ret + arg
    return ret

def safe_mul(a, b):
    if type(a) != type(b):
        print('Is not same type a and b!')
        return
    else:
        return a * b

class CircleMath:
    PI = 3.141592
    def ToRadian(self, angle):
        return angle * (self.PI / 180)

#이 아래부터의 구문은 모듈이 직접 실행됐을 때만 기능한다
if __name__ == "__main__":
    print(sum(0, 1, 2, 3, 4))

    cm = CircleMath()
    print(cm.ToRadian(90))