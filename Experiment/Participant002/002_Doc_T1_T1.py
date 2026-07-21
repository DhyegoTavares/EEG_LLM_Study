

def relaciona_pesos(words,weights):
    letters = []

    for word in  words:
        for letter in word:
            letters.append(letter)

    dict = {letter: weight for letter, weight in zip(letters, weights)}

    for word in words:
        total_weight = 


words = ["abcd","def","xyz"]
weights = [5,3,12,14,1,2,3,2,10,6,6,9,7,8,7,10,8,9,6,9,9,8,3,7,7,2]

relaciona_pesos(words,weights)