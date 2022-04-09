import math
import numpy as np
import matplotlib.pyplot as plt

RATIO = ( math.sqrt(5)-1)  / 2
tol = 1.0e-6
# Plot the function values of each iteration
def plot(vals, name):
    plt.scatter(range(len(vals)), vals, label = name)
    plt.legend()
# for p1
def fnc(x) -> float:
    return (x ** 3) * math.exp(-(x ** 2))

# for p2
def fnc2(vals) -> float:
    x1, x2  = vals[0], vals[1]
    return (((math.pow(x1, 2) + x2 -1)) ** 2 
            + ((x1 + x2 -7) ** 2))

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
    funcValues = []
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
        funcValues.append(min(x1, x2))
        #print(f'\tInterval between {x1}, {x2}')
    minimum = min(f1, f2)
    return funcValues
    print(f'Minimum using golden search is {minimum}.')

# Quadratic interpolation for problem 1.b
def quad_int(start, end):
    # Beginning, middle end of interval we're
    # focusing on
    funcValues = []
    al, au = start, end
    foundMin = False
    i = 0
    while not foundMin:
        am = (al + au) / 2

        xstar = 0.5 * (fnc(al)*(math.pow(am, 2) - math.pow(au, 2)) 
                    + fnc(am)*(math.pow(au, 2) -math.pow(al, 2)) 
                    + fnc(au)*(math.pow(al, 2) - math.pow(am, 2)))
        den = (fnc(al)*(am-au) + fnc(am)*(au-al) + fnc(au)*(al-am))
        den = den +1 if den == 0 else den
        xstar /= den

        num = fnc(xstar) if fnc(xstar) != 0 else q(xstar, al, am, au)
        if abs((fnc(xstar) - q(xstar, al, am, au)) / num) < tol:
            foundMin = True
            continue

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
        funcValues.append(xstar)
        i += 1
        print(f'Iter {i}: {xstar}, {al},{am},{au}')
    return funcValues

# Hooke-Jeeves method
# First use the same tol
def p2(start, end):
    mid = (start + end) / 2

    uk = np.array([mid, mid]) # Current guess
    dims = uk.shape[0]

    guk = np.zeros((dims)) # guess gradient
    h = 1e-2 # Step size
    exp = np.eye(dims) # Exploration directions
    for dim in range(dims):
        fprev = fnc2(uk + guk - (h  * exp[dim]))
        f = fnc2(uk + guk)
        fnext = fnc2(uk + guk + (h * exp[dim]))
        if fprev < f and fprev < fnext:
            guk -= (h * exp[dim])
        elif fnext < fprev and fprev < fnext:
            guk += (h * exp[dim])
        print(f'prev: {fprev} f: {f} next: {fnext}')

def main():
    #plot(p1(-2, 2), 'golden section')
    #plot(quad_int(-2, 2), 'quadratic')
    p2(-5, 5)
    #plt.show()


if __name__== '__main__':
    main()
