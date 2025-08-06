n, q = map(int, input().split())
a = list(map(int,input().split()))
d = {}
for v in a:
    if v in d:
        d[v]+=1
    else:
        d[v]=1
for _ in range(q):
    print(d.get(int(input()), 0))
