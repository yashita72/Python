squares=[i**2 for i in range(1,5)]
print(squares)

result=["even" if i%2==0 else "odd" for i in range(10)]
print(result)

evens=[i for i in range(10) if i%2==0]
print(evens)

sq={k:k**2 for k in range(1,6)}
num={k%4 for k in range(20)}
print(num)
print(sq)
b=[x*y for x in range(3) for y in range(3) if x != y]
print(b)