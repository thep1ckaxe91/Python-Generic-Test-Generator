n,q = map(int, input().split())
d = {}
for _ in range(n):
    username, password = input().split()
    d[username] = password

for _ in range(q):
    query = input().split()
    match query[0]:
        case "REGISTER":
            username, password = query[1:]
            if username not in d:
                d[username] = password
        case "LOGIN":
            username, password = query[1:]
            if username in d:
                if d[username] == password:
                    print("success")
                else:
                    print("wrong password")
            else:
                print("not exist")
        case "CHANGE":
            username, old_password, new_password = query[1:]
            if username in d and d[username] == old_password:
                d[username] = new_password
        case _:
            pass
