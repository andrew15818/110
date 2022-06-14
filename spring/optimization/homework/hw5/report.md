# Optimization Homework 5

## Q1
So far we have learned two ways to deal with linear programming problems. One way is using the simplex algorithm, and the other is using
interior point methods. Pick any two LP problems. Perform optimization
with both kinds of approaches. For each test problem, comment on the accuracy and convergence speed of the two approaches.

For the first problem, we solve problem 3.45 from the textbook by Rao.
\begin{equation}
	f(\boldsymbol{x})=240x_1 + 104x_2 + 60x_3 + 19x_4
\end{equation}
subject to 
$$20x_1 + 9x_2 + 6x_3 + x_4\leq 20$$
$$10x_1 + 4x_2 + 2x_3 + x_4\leq 10$$
$$x_i \geq 0, i=1,\dots,4$$

We compare both the simplex and Positive Affine Scaling algorithm.
The implementations for these algorithms were obtained online.
We find that the simplex algorithm needs to run only 3 times, while the PAS needs around 100 iterations to obtain an answer.
The answer we get with the simplex method is $\{0, 2, 0, 2, 0, 0\}$.

### Q1b
We also choose a problem from the textbook, this time 3.14 from the book by Rao again.
\begin{equation}
f(x, y)  = 19x + 7y
\end{equation}

subject to
$$7x + 6y \leq 42$$
$$5x + 9y \leq 45$$
$$x - y \leq 4$$
$$x\geq 0, y\geq 0$$

When we run the simplex and PAS methods, we obtain the solution
$\{0, 5, 12, 0, 9, 0\}$ using the simplex method.
Similar to the previous section, the simplex algorithm takes many times
less to terminate, only 1 iteration compared to 98 with the PAS implementation used.

Both these problems highlight the overall efficiency of the simplex algorithm for linear problems even today.
The simplex implemenation we used had accuracy comparable to other solvers online.
We are unsure if this is an error specific to our implementation or a general feature of these algorithms.
For dealing with linear problems, the simplex algorithm seems a very strong candidate.

## Q2
So far we have learned two ways to deal with constrained nonlinear optimizatino problems. One way is the indirect approach (e.g. penalty functions) and the other is the direct approach (e.g. Sequential Quadratic Programming, SQP). Pick any two test functions (neither linear nor quadratic functions) with constraints. Perform optimization with both direct and indirect approaches.

For the first section, we estimate
\begin{equation}
f(x, y) = \sin(x+y)
\end{equation}
subject to 
$$x + y \leq 2$$
$$x + y \leq -2$$
which effectively means $x$ and $y$ are bounded in this region.
We use the `scipy.optimize.minimize` library in python which contains 
a quadratic programming minimizer.
We also implement our own interior method by minimizing the function $f$
with an added interior penalty method $\min(0, h_i(x))$.

Using the quadratic solver, the minimizer evaluates the function 15 times
and iterates 5 times through the algorithm.
The interior penalty method uses 10 iterations for this problem.
The quadratic was more efficient.
We obtain the answer $\{-0.78, -0.78\}$.

### Q2b
For the last section, we use the function 
\begin{equation}
f(x, y) = x\sin(x + \sin(y))
\end{equation}
subject to 
$$x + y \leq 1$$

We can pass the constraints along to the `scipy` minimizer and
obtain $\{2.9, -1.57\}$ as our answer.
The quadratic approach took 10 iterations with 33 function evaluations,
while the interior method used 10 iterations also with 31 function evaluations.


In general, the quadratic approach seemed more accurate while taking less iterations
and function evaluations than the interior penalty method.
This makes sense since the interior penalty might require larger numbers as penalties
and incur more iterations.
The results between the two approaches were a little different, but the quadratic programming
approach seemed to yield slightly more accurate results compared to other online solvers.
This was the case for both equations.

## Conclusion
In conclusion, we were able to test many of the methods learned in the 
last few weeks of class.
From the methods we tested, the simplex algorithm and quadratic were generally faster
since they required less iterations or function evaluations.

