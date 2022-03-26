import math
import matplotlib.pyplot as plt

RATIO = ( math.sqrt(5)-1)  / 2
tol = 1.0e-6

def fnc(x) -> float:
    return (x ** 3) * math.exp(-(x ** 2))

def p1(a, b):
    x1 = RATIO*a + (1-RATIO)*b
    x2 = (1-RATIO)*a + RATIO*b
    f1, f2  = fnc(x1), fnc(x2)

    while(b - a) > tol:
        if f1 > f2:
            a = x1
            x1 = x2
            f1 = f2
            x2 = (1 - RATIO)*a + (RATIO)*b
            f2 = fnc(x2)
        else:
            b = x2
            x2 = x1
            f2 = f1
            x1 = (RATIO)*a + (1 - RATIO)*b
            f1 = fnc(x1)
        print(f'\tInterval between {x1}, {x2}')
    minimum = min(f1, f2)
    print(f'Minimum using golden search is {minimum}.')

def main():
    p1(-2, 2)

if __name__== '__main__':
    main()
