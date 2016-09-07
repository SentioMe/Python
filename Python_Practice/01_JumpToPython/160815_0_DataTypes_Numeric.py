#01. Numeric

#Integer
numVal = 123
print(numVal)
numVal = -123
print(numVal)

#Floating-point
numVal = 1.233
print(numVal)
numVal = 1.23E-10
print(numVal < 1)

#Octal and Hexadecimal
numVal = 0o177
print(numVal)
numVal = 0x8ff
print(numVal)

#Complex number
numVal = 1+2j
print('Complex number : ', numVal)
print('Complex number.real : ', numVal.real)
print('Complex number.imag : ', numVal.imag)
print('Complex number.conjugate : ',numVal.conjugate())

#Operation
a = 4.5
b = 2

print('a : ', a, ' b : ', b)

print('a + b = ', a + b)            #sum
print('a - b = ', a - b)            #diff
print('a * b = ', a * b)            #multi
print('a / b = ', a / b)            #divide
print('a // b = ', a // b)          #divide return point upper
print('a % b = ', a % b)            #divide return remain
print('a ** b = ', a ** b)          #square