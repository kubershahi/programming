import math

l = []
def pow5(x):
    if x == 1:
        l.append(x)
        return x
    else: 
        k = pow5(math.floor(x/2))
        e = k + k 
        l.append(e)
        return e
    
print(pow5(33))
print(l)