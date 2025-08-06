n,q = map(int,input().split())
d = {}
for _ in range(n):
    name, score = input().split()
    d[name] = float(score)

for _ in range(q):
    query = input().split()
    op = query[0]
    name = query[1]
    match op:
        case "ADD":
            score = float(query[2])
            if d.get(name) == None:
                d[name] = score
        case "UPDATE":
            score = float(query[2])
            if d.get(name) != None:
                d[name] = score

        case "REMOVE":
            if d.get(name) != None:
                d.pop(name)

        case "PRINT":
            if d.get(name) == None:
                print("not exist")
            else:
                print(f"{d[name]:.2f}")

        case _:
            pass
        