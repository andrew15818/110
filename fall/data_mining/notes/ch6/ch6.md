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


