def fact(n):
    if(n==0):
        return 1
    return fact(n-1)*n
n=int(input("Enter Number for factorial:"))
print(f"Factorial of {n} : {fact(n)}")

def fib(n):
    if(n==0):
        return 0
    if(n==1):
        return 1
    return fib(n-1) + fib(n-2)

m=int(input("Enter Number for Fibonacci:"))
print(f"Fibonacci of {m} : {fib(m)}")
