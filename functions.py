def sum(a,b):
    return a+b

def greet(name,msg="Hello"):
    print(f"{msg} {name}")

def value(val):
    
    lst.append(val)
    return lst

def ff(*args):
    return args

def bb(**kwargs):
    return kwargs

print(f"Sum of 10 & 15 is {sum(10,15)}\n")
greet("Divjot")
greet("Divjot","Heyo")

lst=[]
for i in range(1,101):
    if(i%5==0):
        lst=value(i)
print(lst)

print(f"Arguments :",ff(1,2,3)) #Arbitrary Positional Arguments
print(f"Arguments :",bb(a=1,b=2,c=3)) #Arbitrary Keyword Arguments
