PAGE=[1,2,3,4,5]
for num in range(1,sum(PAGE)+1):
    print(num)
    if num <= PAGE[0]:
        num = num - sum(PAGE[:0])
        print('1-',num)
    elif PAGE[0] < num <= sum(PAGE[:2]):
        num = num - sum(PAGE[:1])
        print('2-',num)
    elif sum(PAGE[:2]) < num <= sum(PAGE[:3]):

        num = num - sum(PAGE[:2])
        print('3-',num)
    elif sum(PAGE[:3]) < num <= sum(PAGE[:4]):

        num = num - sum(PAGE[:3])
        print('4-',num)

    elif sum(PAGE[:4]) < num <= sum(PAGE[:5]):

        num = num - sum(PAGE[:4])
        print('5-',num)


    else:
        print('不合法的页数：{}'.format(num))
