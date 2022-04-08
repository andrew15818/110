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
def q(x,al, am, au):
    num = ((fnc(al)*(x-am)*(x-au))/((al-am)*(al-au))
            + (fnc(am)*(x-al)*(x-au))/((am-al)*(am-au))
            + (fnc(au)*(x-al)*(x-am))/ ((au-al)*(au-am)))
    return num

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
    # Beginning, middle end of interval we're
    # focusing on
    al, au = start, end
    am = (al + au) / 2
    print(al, am, au)
    maxiter = 10
    for i in range(maxiter):
        xstar = 0.5 * (fnc(al)*(math.pow(am, 2) - math.pow(au, 2)) 
                    + fnc(am)*(math.pow(au, 2) -math.pow(al, 2)) 
                    + fnc(au)*(math.pow(al, 2) - math.pow(am, 2)))
        den = (fnc(al)*(am-au) + fnc(am)*(au-al) + fnc(au)*(al-am))
        xstar /= den

        num = fnc(xstar) if fnc(xstar) != 0 else q(xstar, al, am, au)
        if abs((fnc(xstar) - q(xstar, al, am, au)) / num) < tol:
            print('FOund the minimum')
            return xstar 

        # Adjust the new points
        elif xstar <= am:
            if fnc(am) >= fnc(xstar):
                am = xstar
                au = am
            else:
                al = xstar
        
        elif xstar > am:
            if fnc(am) >= fnc(xstar):
                al = amam = xstar
            else:
                au = xstar
        print(f'Iter {i}: {xstar}')


def main():
    p1(-2, 2)
    quad_int(-2, 3)


if __name__== '__main__':
    main()
