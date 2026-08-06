words=(input().split())
weights=list(map(int, input().split()))
characters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']    
rcharacters=['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a']
fword=""
for j in range (len(words)):
    weight=0
    #print(words[j])
    for i in range (len(words[j])):
        ind=characters.index(words[j][i])
        #print("index e:" )
        #print (ind)
        #print(weights[ind])
        weight+=weights[ind]
        #print(weight)
        #print(weight)
    #print (weight)
    weight%=26
    #print (weight)
    #print("peso final e: ")
    #print (weight)
    char=rcharacters[weight]
    fword+=char

print(fword)