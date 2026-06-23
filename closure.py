def outer(x):
    def inner(y):
        return x+y
    return inner

def mul(n):
    return lambda x:x**n

a=outer(2)
print(f"a : {a(5)}")
print(f"a : {a(8)}")

double=mul(2)
triple=mul(3)
print(f"double : {double(5)}")
print(f"triple : {triple(5)}")