
def f1( num):
    PAGE=[1,2,3,4]



    for i in range(1, int(len(PAGE)) + 1):

        if sum(PAGE[:i - 1]) < num <= sum(PAGE[:i]):
            num = num - sum(PAGE[:i - 1])
            is_useful = 0
            print(num,i)
            break

    if 'is_useful' not in locals():
        print('页数不合法%d' % num)
        return


f1(1)