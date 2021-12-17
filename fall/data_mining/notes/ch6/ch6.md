## Mining Frequent Patterns, Associations, and Correlations
When you have a set of transactions in a dataset, some of them can happen 
frequently. For a dataset $D$, there are many combinations of the items,
so how do we find the ones that happen frequently?

A **frequent itemset** is one whose **support** and **confidence** are above a 
certain threshold.
The support for a rule $A \implies B)$ is the percentage of all transactions that contain
$A \cup B$, or their intersection.
The confidence for a frequent itemset is the percentage of all transactions containing $A$ that 
also contain $B$, i.e. $P(B|A)$.

A **closed itemset** is one where for all the itemsets $X$  there is no 
proper super-itemset $Y$(X \subset Y) such that $X$ and $Y$ both have the same
support count.

## Apriori Algorithm
This algorithm uses knowledge of previous frequent itemsets to calculate the 
current one, e.g. it uses $L_{1}$ to calculate $L_{2}$, the set of frequent 2-itemsets.
The idea is that we first find all the 1-itemsets and use that to find the 2-itemsets.
Since all the 1-itemsets are proper subsets of 2-itemsets, we could build up our $L_{k}$ this way.
However, for every level of itemsets we need to scan the entire database :(

The central idea of the algorithm is that an itemset $I$ is not frequent, 
then all of its supersets will not be frequent either.
$P(I \cup A)$ cannot be more frequent than $P(a)I$ when we add an item $A$.

The first step in the algorithm is the join step.
For two subsets of $L_{k-1}$, $l_{1}$ and $l_{2}$, we join them if their first
$k-2$ elements are equal, and $l_{1}[k-1] < l_{2}[k-1]$.
This way we produce a subset that is still lexicographically ordered and contains 
one more element in it than before.

The second step is the prune step.
We generated a candidate set $C_{k}$, and maybe not every itemset here will be frequent.
If any $k-1$ itemset in $C_{k}$ is not in $L_{k-1}$, then we know it can't be frequent thus it can be removed from $C_{k}$.
(Here is where we can use a **hash tree** for quick searching of frequent itemsets)

The hash tree (from ppt) stores a hash table at each interior node and each leaf node contains a list of itemsets and their counts.

How do we efficiently generate the frequent itemsets?
We inherently have to produce a large amount of candidates, so there are a couple avenues for reducing the complexity.

1. **Hash based**: Place each candidate $k$-itemset into the ''bucket'' of a hash table.
Generate all the $k$-itemsets for each transaction, measures how much sets repeat throughout many transactions.
We also kep track of the count of items in the bucket and if at the end it's still less than the min support, they gone.

2. **Transaction reduction**: Because of the a-priori property, any non-frequent $k$-itemset will not be present 
in any $(k+1)$ frequent itemset. Thus, any transactions that do not contain any frequent $k$-itemsets can be removed.

3. **Partitioning**: In this scheme the database is partitioned into $n$ non-overlapping transactions.
Then, within that partition all the individual frequent-itemsets are found using a slightly different support measure($min\_sup \times transaction number$).
Also, any potentially frequent itemset in $D$ must be frequent in at least *one* partition (why tho?).
The frequent itemsets in each partition is a candidate for a frequent itmeset in $D$.
In the second pass through the database the support for the candidates is measured and actual frequent itemsets are determined.

4. **Sampling**: A sample of transactions in $D$ is taken, $S$, and the frequent itemsets are found there (the size is such that $S$ fits in main memory).
A slightly smaller support measure is used for items in $S$, $L^{S}$.
After frequent itemsets in $S$ are found, we can determine if there are any that we missed and scan $D$ if that is the case.

5. **Dynamic Itemset Counting**: The database is separated into blocks marked by different start points,and we again use an adjusted support equation.
Then we can measure if the itemsets occur in each block.
This method allows new blocks to be inserted during the claculation.

## Frequent Pattern Growth
Although a-priori can reduce the number of candidate sets that we search for in the dataset, two problems remain:
1. Many candidate sets still need to be generated every time.
2. Many database scans are needed to determine support for a candidate dataset.

The **frequent pattern tree** is some compressed form of the database, where relationships between the itemsets are maintained.
Then we can divide the pattern tree into *conditional databases*, where a part of a frequent itemset is stored (pattern-fragment).
The fp-tree is built by going through each transaction and ordering the items in $T$ in descending order.
The nodes can each be linked from a table where we store the support count for each item and the node link to its parent.
By following the paths of each of the itemsets, starting from the least-common one and going up, we can come up with the 
frequent itemsets involving that node.

FP is faster than a-priori and is scalable.

## Vertical Data Format
Instead of having $D$ presented as a list of transactions, we can present it as the id of the transaction and the places where it appears
in our dataset.

# Clustering
This is the ch6 slides from moodle

**Clustering** refers to grouping items togethter according to their 
labels. 
When the problem is supervised, we know the labels and the number of them,
so we can infer the label of each item this way.
With unsupervised methods we need to learn the grouping of similar 
and dissimilar items by ourselves.

A good cluster is one in which the intra-cluster similarity is high 
and the inter-cluster similarity is low.
Some of the things we should consider are dealing with non-numerical data,
requiring little domain knowledge to use such data, high dimensionality,
scalability, etc...
We also need some **similarity measure** to measure how similar two objects
are.

Clustering algorithms can be sensitive to **outliers**, a couple values
that greatly differ from the average of the cluster.
These values can drag our entire average down.
We define the cluster around some **cluster center**, so that each point
is closer to one cluster's center than closer to the center of any other
cluster.
Another definition for cluster is using the nearest neighbor and how 
how that point belongs to the same cluster as the other point.
Another type of cluster groups items in high-density areas together
and is separated from other clusters by areas of lower density.
This type of clustering can help when the data is irregular or 
intertwined.

## Partitioning based algorithms
Given a database $D$ of length $n$ and $k$ number of clusters, find the 
partition of the database items that maximizes the partition criterion.
This would require us to go through all the different partitions and evaluate 
them individually.

Some of the heuristics include $k$-means, or using the center of each 
cluster, or the $k$-mediods, where each cluster is represented by one 
item from the cluster.

**K-means** clustering tries to find $k$ clusters by first calculating 
the centroid of each partition. 
Then we relocate each object in the database to the closest item.
The centroids are often initialized randomly.
However, the initial values of the centroids play a large role in how the 
algorithm is going to split the dataset.
K-means is sensible to outliers and sensitive to items of differing sizes.
K-means is also sensitive to clusters that are not perfect spheres.

Instead of using the means of each cluster, which can be sensitive to 
outliers, we can instead use the **mediods**, or the most centrally 
located point.
PAM does not scale well to large datasets, though :(.
If we take multiple samples from the dataset, we can deal with larger
datasets instead, but the effieciency would then depend on the sample
size, and we would require a large enough sample to be representative of the 
entire dataset.

## Hierarchical Clustering
With this type of clustering we can represent clusters as a hierarhical
tree, and every time we have a new split for a new cluster
we update the tree.
We can represent any number of clusters this way depending of when we stop
the tree-building.

Using the **agglomerative** approach, we start with each point as its own 
cluster, and we continously merge the two closest clusters until only
one cluster remains. The **divisive** approach is the reverse: start with 
only one cluster, and split into two clusters until each cluster is in one 
point or we have $k$ clusters. How would we know the best cluster split though?
We would use the **proximity matrix** to know the distance b/w two points.
Each time we merge the cluster we would have to merge some entries in the 
matrix.

Defining the **inter-cluster** similarity can be challenging. We can use
either the min, max, group average, centroid distance, or some other methods.
Some of these work better with datasets of different sizes but are susc.
to outliers and vice versa.
**Ward's method** uses the sqaured error if two clusters were to be merged.
However, this is biased towards globular clusters.

With hierarchical clusters, we don't optimize a similarity metric directly, 
and the merging/splitting cannot be undone once we do it.

Other approaches involve building a **minimum spanning tree**, where for
a pair of points $(p, q)$ with $p$ in the tree and $q$ outside, find the 
closest such pair of points and add $q$ to the tree.
To build the clusters, we can split the $k$ farthest points, 
which indicate the least similarity.

## DBSCAN
This algorithm is a density-based algorithm.
The **density** of a point is the number of other points within some
specified radius.
If there are more than some predefined number of points within its radius,
this point is a **core point**.
If the point is not a core point but has a core point as one of its neighbors,
the point is a **border point**.
Otherwise, it is a **noise point**.
DBSCAN does not work well when the points are of varying density.
