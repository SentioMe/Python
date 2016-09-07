#Container - Dictionary

dic = {'name':'Kim', 'Age':25, 'birth':921207}
print(dic)
dic['Job'] = 'GameProgrammer'
print(dic)

print(dic['name'])
print('dic keys = {0}'.format(dic.keys()))
print('dic values = {0}'.format(dic.values()))
print('dic infos = {0}'.format(dic.items()))

for value in dic.keys():
    print(dic[value])

job = dic.get('Job')
dic.clear()

print(job)
