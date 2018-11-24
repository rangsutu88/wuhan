num_list=[2,3,4,5]

a=int(len(num_list))
num=3
for i in range(1,a+1):
    if sum(num_list[:i-1]) < num <= sum(num_list[:i]):
        print(sum(num_list[:i-1]),sum(num_list[:i]))
        print(i)
        num=num-sum(num_list[:i-1])
        print(num,i)
        break

print('-------------------')
req=sum(num_list[:0])
print(req)
