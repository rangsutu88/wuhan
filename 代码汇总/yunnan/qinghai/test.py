from collections import namedtuple,deque,OrderedDict,defaultdict,Counter


d1=dict([[3,4],[1,2],[5,6]])
# print(d1.keys())


d2=OrderedDict([[3,4],[1,2],[5,6]])
# print(d2.keys())


p=namedtuple('p','def y',rename=True)
p1=p(1,2)
# print(p1)


print('========================================')


emp1 = ('Pankaj', 35, 'Editor')
emp2 = ('David', 40, 'Author')

for p in [emp1, emp2]:
    print(p)



for p in [emp1, emp2]:
    print(p[0], 'is a', p[1], 'years old working as', p[2])

# pythonic way
for p in [emp1, emp2]:
    print('%s is a %d years old working as %s' % p)

print('==============================')





