# Classification
Machine learning just refers to a program $P$ that learns with some 
experience $E$ according to some way of measuring its performance $P$.

**Supervised** learning has labels along with the training data.
This means that durign training we can compare our guess with the 
correct answer.

**Unsupervised** data's correct answer is unknown, and here we want to 
discover the undrelying relations or clusters within the data.

## Definition
Given a set of attributes (among which there is a class label), our model
is a function of the attributes and outputs a class label.
Before we start processing the data, some data cleaning in order to 
normalize the values or fill in missing values might be required.

There are several ways of evaluating the performance of our model:
- predictive accuracy
- speed(inference, etc...)
- robustness (how does it handle missing values?)
- scalability
- interpretability (how easy is it to understand conceptually what it's doing?)
- goodness of rules (size, compactness of the representation)

some techniques include:
- Decision Trees
- Neural networks
- K-nearest neighbors
- Support Vector Machines
- Random forest

## Decision Trees
DTs are a hierarchical way of assigning class labels based on 
checking an attribute at a certain value.

The general way we build the decision trees is by having $D_{T}$ 
at some node. If the items in the dataset are all one class, we assign
the data's  label to the node. If there is data belonging to more than one
set, we use some metric to split the dataset at the node.
Some trees could be split into two features, or we could choose to have a 
multi-split approach.

If the values in a feature are continuous, how do we get a value to split on?
We could choose the average of two consecutive sorted values in the feature column.
We then have multiple different splits of data, so which is the best one?
Based on the proposed value, we need some metric of checking the 
**purity** of the resulting datasets. There are a couple of metrics:

The **gini index** measures the impurity of a node 
\begin{equation}
	\textrm{GINI}(t) = 1 - \sum_{j}[p(j|t)]^{2}
\end{equation}
where $p(j|t)$ is the relative measure of items in class $j$ in set $t$,
i.e. $|c_{j\in t}| / |t|$. 
When all the items belong to one class, the gini index is 0, so we are 
choosing the dataset that is the least "mixed".
Thus at every node, we have to calculate the gini index of both the resulting 
children nodes and subtract it from the impurity of the parent.

Another measure we could use is the **entropy**, which measures the homogeneity of a node.
\begin{equation}
	\textrm{Entropy}(t) = -\sum_{j}p(j|t)\log p(j|t)
\end{equation}

Yet another measure is the **information gain**, which measures the 
*reduction in entropy* of the resulting split.
\begin{equation}
\textrm{GAIN}_{split} = \textrm{Entropy}(p) - (\sum_{i=1}^{k} \frac{n_{i}}{n}\textrm{Entropy}(i))
\end{equation}
However, this apporach tends to prefer smaller and more numerous yet
purer partitions.

The **error** is just the probability that the label is different from 
our prediction, $E(t) = 1 - \maxP(i|t)$.

Decision trees are a popular method for classification because they are 
easy to understand, deal well with symbolic feature, relatively quick to train,
and deal well with data that is not numeric. 

## Classification Issues
When our model is too simple or too complicated, the accuracy in our 
predictions suffers. Why?
If our model is too simple, whe nwe take a look at the training data,
our error will still be relatively large when we finish training. 
This means that our model cannot entirely capture all the information
in the training data. 
The error in the training data will be large, and the testing data's error
will be even larger.

When our model is too complicated, it might focus too much on generating 
useful parameters for the testing set, but not on the testing set.
It might be getting derailed by noise in the testing data. 
Its accuracy on the training data might be very low, but it might be
very high on the testing data due to it not being general enough to handle
random noise.
It might split the space into too small areas.

How should we deal with overfitting?
**Early stopping** has the algorithm stop before convergence, (e.g.
stopping before the decision tree is completed).
Each problem is going to require us to come up with different conditions
for stopping.

We could also do the opposite and prune the tree/model once it finishes
if there are any nodes we believe are too much.

For decision trees, if we could test for multiple attributes at a single
node we could reach a consensus faster, although finding the right 
combination of attributes would be too expensive.
Another issue with DTs is that subtrees might be replicated at different
parts.

The **curse of dimensionality** refers to how quickly the dimensions of 
our data escalates.
For a simple boolean expression $(A\and B) \or (C \and D)$, there would
be $2^{param\_no}$ possible inputs.
For non-boolean data this increase would be exponentially greater.

## Instance-Based Classifiers
With these classifiers, we use the nearby attributes to classify 
each node.
**k-nearest neighbors** takes a look at the closest data points
and decides the class based on the nearby data points.

To classify the points in the test set, we need the training data's
attributes and labels, and a distance metric, and the number of the 
neighbors to check to make our decision.
**Lazy learners** such as knn do not build models explicitly during a
training phase, and instead do the classification "on the fly" for each
test point.

Choosing the value of $k$ is important because if it is too small, 
it can be influenced by noise, and if it is too big it can 
also take into account items from another class.
Since some of the values can be larger, to keep them from dominating 
the entire prediction we have to **normalize** them (e.g.
people's heights changes by couple centimeters vs. income can vary by thousands).
Another application is to normalize the input vectors to **unit length**.

## Bayes Classifier
This classifier is based on Bayes theorem
\begin{equation}
	P(C|A) = \frac{P(A|C)P(C)}{P(A)}
\end{equation}
i.e. how often an event $C$ happens given $A$ is the relationship between
how often they happen together, how likely $C$ is on its own, and 
how often $A$ happens on its own. If $A$ happens frequently,
the chance that they happen together is pretty high.

To find the chance an input $A$ belongs to class $C$, we have to find
the prob $P(a_{1}, a_{2}, \dots,a_{n}|C)$, or how likely the attributes
are given they belong to class $C$.
We can estimate that all fo the attributes are indpendent and normally distributed.

## Perceptron
This model takes in inputs, and passes them through a weighted directed graph.
The result is the collection of weights, biases and activations of the nodes 
at each previous layer. 
They all lead to the final outputs.
When we train a perceptron, we are changing the weights of the neurons
used to calculate the output of the neurons.

## Bias-Variance Tradeoff
**Bias** refers to the "offset" from otherwise the answer we would get.
The **variance** refers to how much our answers vary from the mean. 
The higher the variance, the more sporadic the values might seem.

There is a U-turn in the variance-bias relationship. First, as our model 
is more complex, the variance starts to go up.
However, the bias is more influential when the model is simpler.
The trick is making our model complex enough that we minimize the bias and the
variance just starts to increase. 
At this point, right after the variance starts picking up, is the best time
to stop our gradient descent.
When there is **high bias,low variance** our model will tend to **underfit**, 
and when there is **low bias, high variance**, our model will tend to **overfit**.

## Support Vector Machines
With SVMs, given 2-dimensional data, we ask whether there is a **hyperplane**
linearly separating the data.
There are multiple lines that linearly separate the data, which one is better?
The better line is the one that maximizes the distance between the line and
the closest point, a.k.a. the **margin**.

We would have to maximize the margin 
\begin{equation}
	\textrm{Margin} = \frac{1}{||w||^{2}}
\end{equation}

which means we want to minimize $||w||$.

However, if the data is not linearly separable or the hyperplane is not linear
this approach will not work.
In that case we would have to transform the data into a higher dimension such that
it is linearly separable with a $d-1$ dimensional hyperplane.
We would have to apply some sort of transformation to the input data to 
find the hyperplane that best separates the data.

## Ensemble methods
The ensemble here refers to a collection of other classifiers, whose consensus we 
take as the final class.
There are a couple ways of dealing with the classifiers: we can take their 
combined output.
Given an error rate $\epsilon = 0.35$, the chance that our set makes a wrong
prediction is
\begin{equation}
	E(x) = \sum_{i=13}^{25}\frac{25}{i}\epsilon^{i}(1-\epsilon)^{(25-i)}
\end{equation}

This helps when an individual classifier might have a large error rate or when
a small change in the input can have a large effect on the output. 
With **boosting**, we have a set of base classifiers which try to learn from the 
mistakes of the previous classifiers.
The samples that the previous classifier got wrong are given higher weights to make
sure they are improved on in future classifiers.
Each data sample is $(x, y, w)$ where $w$ is the weight.

## Supervised, Semi-Supervised, Unsupervised
Labeling data is expensive and time-consuming, so often we have just unlabeled
data to analyze.
The types of unsupervised learning depend on whether we have some labeled data
or not. 
Why is having unlabeled data helpful?
If we only have a few labeled samples, but we have a lot of data, those few samples
could be enough to approximate the distribution.

Even if we only have a few labeled examples, we can infer and propagate the labels
by looking at each point's similarity to the labeled data.
Even if we only have two points, give each point a label based on closest one.

**Positive examples** refer to examples of a class $P$.
**PU** learning happens when we have a combination of positive and 
unlabeled examples.
Our goal with such a classifier is to accurately classify the 
unlabeled samples, however we don't have **negative data**.

As an example to classify academic documents, the **Spy** algorithm
will use a mixture of unlabeled and positive labeled samples to build
a classifier, and try to infer the reliable negatives against the samples
we already know.
