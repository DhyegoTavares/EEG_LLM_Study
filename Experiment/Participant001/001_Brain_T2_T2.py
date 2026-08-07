s = "jackee"
l = len(s)

vocals = ["a", "e", "i", "o", "u"]

for i in range(0, l):
    r = l-i-1
    c = s[r]
    if c in vocals:
        s = s[0:r]
    else:
        break

print(s)
    