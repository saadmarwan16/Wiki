from re import IGNORECASE, search

x = "it"
y = ["It Is", "he"]
res = []

# print(x in y)

# print(search(x in (name for name in y), IGNORECASE))
# print(search(x, y, IGNORECASE))
for string in y:
    if search(x, string, IGNORECASE):
        res.append(string)

print(res)