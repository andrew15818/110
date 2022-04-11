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
    # For plottign
    uk_list = []
    f_list = []
    
    mid = (start + end) / 2
    u = np.array([0, 0]) # Minimum vector
    dims = u.shape[0]
    h = 1# Step size
    min_step = 1e-4 # Minimum step size
    du = np.zeros(u.shape) # Gradient along u
    minu = fnc2(u)          # Initial minimum value
    max_iter, i = 30, 0
    for i in range(max_iter):
        # Find best direction of increase along each dimension
        for j in range(dims):
            du[j] -= h
            fprev = fnc2(u + du)
            du[j] += 2 *h
            fnext = fnc2(u + du)
           
            if fnext < fprev and fnext < minu:
                minu = fnext

            elif fprev <= minu:
                du[j] = -h
                minu = fprev 
            # Can't further minimize along this 
            # dimension
            else:
                du[j] = 0
            print(u, du, fprev, minu, fnext)
        # Check for termination
        if np.linalg.norm(du) < tol:
            if h < min_step:
                print('Breaking')
                break
            else:
                u += du.astype(np.int64)
                h /= 2
        # Check how far we can move along u
        
        k = 0
        while k < max_iter:
            k += 1
            fm = fnc2(u + du)
            if fm < minu:
                minu = fm
                u += du
            else:
                break
          
        #u += du.astype(np.int64)
        
    '''
    # Plotting
    uk_list = np.array(uk_list)
    f_list = np.array(f_list)
    plot2(uk_list, f_list)
    '''

def plot2(uk_list, f_list):
    X, Y = np.meshgrid(uk_list[:,0], uk_list[:,1])
    Z = np.zeros(X.shape)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i,j] = fnc2(np.array([X[i,j], Y[i,j]]))
    plt.contour(X, Y, Z)

    for i in range(1, f_list.shape[0]):
        prev = uk_list[i-1]
        plt.quiver(uk_list[i,0], uk_list[i,1], prev[0], prev[1])
    plt.show()
def main():
    #plot(p1(-2, 2), 'golden section')
    #plot(quad_int(-2, 2), 'quadratic')
    p2(-5, 5)
    #plt.show()


if __name__== '__main__':
    main()
