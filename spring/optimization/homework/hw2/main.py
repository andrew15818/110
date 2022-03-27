import math
import matplotlib.pyplot as plt

RATIO = ( math.sqrt(5)-1)  / 2
tol = 1.0e-6

def fnc(x) -> float:
    return (x ** 3) * math.exp(-(x ** 2))

# Derivative of function
def dfnc(x, a, b):
    return (2*a*x + b)
# Quadratic approixmation of f
def q(x,a, b, c):
    return a*(x ** 2) + b*x + c

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
        #print(f'\tInterval between {x1}, {x2}')
    minimum = min(f1, f2)
    print(f'Minimum using golden search is {minimum}.')


# Quadratic interpolation for problem 1.b
def quad_int(start, end):
    x1, x2 = start, end
    a, b,c  = -2, -2, 0
    x_ = 10
    while abs((fnc(x_) - q(x_, a, b, c)) / fnc(x_)) > tol:
        tmp = fnc(x1) - fnc(x2) - dfnc(x1-x2, a, b)
        a = tmp / (-(x1-x2) ** 2)
        b = dfnc(x1, a, b) + 2*x1*(tmp / ((x1-x2)**2))
        #x_ -= -b/(2*a)
        x_ = -b/(2*a)
        if fnc(x_) < fnc(x1):
            x1 = x_
        elif fnc(x_) < fnc(x2):
            x2 = x_
        print(f'\tInterval between {x1}, {x2}')
        print(q(x_,a, b,0), x_)




def main():
    p1(-2, 2)
    quad_int(-2, 2)


if __name__== '__main__':
    main()
