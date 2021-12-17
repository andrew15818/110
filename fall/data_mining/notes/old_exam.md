# Practice Questions from Previous Exam
1. Please briefly describe the following terminologies:
- **F1-measure**: The harmonic mean of the precision and recall of a query.
- **specificity**: The sensitivity, also called **recall** is the percentage of the
relevant documents that were retrieved by a query. 
- **Apriori property**: When searching for frequent itemsets, this property states 
that all subsets of a frequent itemset are also frequent. So if we find a subset that 
is not frequent, all of its supersets are also not frequent.  
- **False negative**: The results that our query classifies as negatives when
they should have been positive. It's the relevant items we missed in our query.

2. What is "overfitting" and "underfitting" problem in classification modeling? Please
also descrie how to reduce their effects when you are training mdoels in DNN and decision
tree, respectively.

Overfitting refers to our model achieving a high accuracy on the testing set but not 
on the testing set. It means our mdoel memorized the training set but cannot generalize
We can remedy the problem of overfitting in DNN and DTs by performing early stopping, 
or stopping the training phase beofre the model converges.
This means that the solution might still be general enough for the testing set while
being able to model the data accurately. Overfitting also refers to splitting the 
dataset into too small areas, usally led astray by noise.

Underfitting refers to our model still having a high error rate in the training data.
This means our model has not yet learned how to accurately classify the data or how 
to capture the relevant data in our model.
Our model might be underfitting either because it hasn't trained for enough time, 
or becuase our model is too simple and cannot accurately learn the correct properties.

3. Please describe what is semi-supervised learning? if we have only positive and 
unlabeled data, how do we create a supervised classification model from this data?

Semi-supervised data means that we have a part of the dataset with its labels and 
the remaining samples are unlabeled.
To create a supervised model from this data we would need to use the labeled samples
to get a picture of the reliable negatives, of the items belonging to the other class.
Once we can get a picture of the items that don't belong to the positive class, we 
can build a classifier for the unlabeled samples.

4. Please apply the FP-growth algorithm to find large-itemsets in the following 
transaction data, if min support=3.

|TID|items bought|
|---|---|
|100|a, c, d, f, g, i, m, p|
|200|a, b, c, f, i, m, o|
|300|b, f, h, j, o|
|400| b, c,  k, s, p|
|500| a, c, e, f, l , n|


5. A simple labeled data with 4 attributes shows is on the right side.
Please use **naive bayes**method to calulate the class probability of a test 
instance with "Give birth"=no, "Can Fly"=no, "Live in water"=no, and 
have legs="yes".

The naive bayes is a classifier based on the theorem
\begin{equation}
P(C|X) = \frac{P(X|C)P(C)}{P(X)}
\end{equation}
Since the features $x_{i}$ are assumed to be independent, we calculate the 
feature for each value.

## Qualifying exam 2018
1. Please describe the following terminologies: 
- **Large itemset**: Same thing as frequent itemset, it means a particular set of items
in a transaction that appears greater than a certain threshold amount of times.
- **Apriori property**: When mining frequent itemsets, this property states that
all subsets of a frequent item are also frequent, so if we find an itemset that is not 
frequent, all its supersets are not frequent as well.
- **Information Gain**: The information gain is a criteria for choosing the 
split of a decision tree. It measures the difference in information from splitting
the dataset in a certain way.
- **Ensemble Method**: Ensemble methods use several classifiers to achieve a consensus decision.
If each individual classifier is not very accurate, a consensus of marjority classifiers could lead to 
higher accuracy.

2. For each f the following evaluation criteria, please describe and explain ONE retrieval sysetm 
in which this criterion is important.
- **R-Precision**: Measures how much of the relevant documents are retrieved by our query and 
how much of our query's results are relevant.Gkj
- **NDCG**: Useful for ordered/ranked queries.
- **P@3**: Views the precision after $k$ documents (3 here), used in search engine evaluation.
- **MRR** WTF is it good for......Quickly see when first relevant result appears, lower number means our
first relevant item is far behind.
- **Specificity**: Is the true positive over the sum of false positives and true negatives. Since the amount
of true negatives is sometimes too large, it's only useful when they're not super too much.

3. What are "overfitting" and "underfitting" problem in classification modeling? How to deal with "overfitting"?
Overfitting is when our model does well in our training but not in testing, because it splits the space into too small
pieces, usually to deal with the noise of the training data. Since the testing data has different noise values so on,
it won't be classified that well with the overly specific conclusions drawn from the training data.
We can deal with overfitting by doing early stopping, or not letting the model train to completion/convergence,
or we could do some other normalization of the data.

4. Model 2 is better, because of the many early positives, it climbs up in the roc curve quicker.
