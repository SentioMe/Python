#FileStream

path = 'SampleData/160817_3_File_sample001.txt'


#Write
f = open(path, 'w')

for i in range(1, 11):
    line = '%d 번째 Line\n' % i
    f.write(line)

f.close()


#Read
f = open(path, 'r')

print('한 줄씩 읽기')
while True:
    line = f.readline()
    if not line: break
    print(line)

f.close()

print('여러 줄 읽기')
f = open(path, 'r')

lines = f.readlines()
for line in lines:
    print(line)

f.close()

print('파일 문자열 통째로 읽기')
f = open(path, 'r')
print(f.read())
f.close()

#Append

f = open(path, 'a')
f.write('11 번째 Line')
f.close()

f = open(path, 'r')
print(f.read())
f.close()

#Auto close == C# using
with open(path, 'r') as file:
    print('used with : %s' % file.readline())

