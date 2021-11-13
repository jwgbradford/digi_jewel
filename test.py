a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(a)
for i in reversed(a):
    print(i)

for i in range(len(a)-1, -1, -1):
    print(i, a[i])
