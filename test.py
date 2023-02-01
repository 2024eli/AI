#print a dictionary in reverse
dict = {1: "one", 2: "two", 3: "three", 4: "four"}
def dictRev(dict):
    return {dict[i] : i for i in dict.keys()}
print(dictRev(dict)) 

#print all unique words in a string 
#"three two two" -> ["three"]
def unique(s):
    return " ".join([i for i in s.split(" ") if s.split(" ").count(i)==1])
print(unique("Java is great Grails is also great"))

def inv(s):
    return sum([sum([s[i]>s[j] for j in range(i+1,len(s))]) for i in range(len(s))])
print(inv("ABCDEHFG"))