---
titlepage: false,
title: "Data Mining Homework 1 Report"
Author: [Andr\'es Ponce, P76107116]
---

# Introduction
Finding patterns in large, unstructured data such as a transaction database
might at first seem too computationally expensive to perform.
Our goal is to find items that occur often together and make inferences about them.
At the end, those subsets which appear more than a certain threshold
(called its **support**) are considered frequent itemsets.
From frequent itemsets we can generate **association rules** by calculating
how often the subsets of frequent itemsets occur together.

If we wanted to find frequent patterns in a set of transactions, a naive
approach would be to go through each transaction of the database, and count
the appearance of all the subsets in each transaction.
Such an approach would be prohibitive in terms of memory and time.
It also misses a key insight: all subsets of a frequent itemset are themselves frequent.
This is called the **a-priori** property, and it is the basis of the two algorithms 
compared in this report.
Using this property, if at any point we encounter a set that is not frequent, 
we know that all its supersets are also not frequent.

After frequent itemsets are calcualted, association rules are generated which 
measure the chance of two sets of items occurring together.
For instance, the rule A \Rightarrow B means that whenever $A$ occurs, $B$ also occurs 
with a certain probability $p$, called the rule's **confidence**.

To generate association rules from frequent itemsets, various algorithms have been proposed.
The focus of this report is comparing the **a-priori** algorithm and the **FP-Growth** algorithm.

## A-priori Algorithm
The a-priori algorithm uses the a-priori property to build up the frequent itemsets.
First, the $1$-itemsets are found by scanning the dataset $D$ and getting the support count for each
item; only the items with high enough support are kept.

Next, until the frequent itemsets $L$ is empty, we keep finding the new candidate set $C_{k+1}$.
From the set of frequent itemsets $L_{k}$, we combine each element $l_{1}$ with an element from $l_{2}$
if $l_{2}$'s last element is greater than the one $l_{1}$. 
Having this requirement preserves the lexicographical order of the itemsets.

We maintain a structure called a **hash tree**, whose leaf nodes contain the itemsets and their counts and 
the internal nodes contain the hashes of the children nodes.
To insert a new item, we check the hash of a certain index of the item, then insert the item to the corresponding
bucket in the node.

When the length of a bucket exceeds a certain amount, we have to split the items in the node's buckets
into different children corresponding to its hash value.
By recursively inserting items and splitting the nodes, eventually by following the hash of each index of the itemset
we reach the leaf node that contains its count or where it should be inserted.
The hash tree structure allows us to maintain a count and insert items in a more efficient way.

To get the frequent itemsets, we check all the leaf nodes in the hash table that contain a support count greater than 
the minimum support.
The frequent itemsets are the $k$-itemsets $L_{k}$.
We repeat this process until there are no more new frequent itemsets, or $L_{k} = \emptyset$.

## FP-Growth Algorithm
The FP-Growth algorithm addresses some of the potential drawbacks of the a-priori algorithm. 
The first algorithm requires several scans of the database to determine the support count
of datasets.
Furthermore, for large databases the space required to store the hash tree might be prohibitive as well.
For large, datasets, these several scans might be prohibitive.

The FP-Growth algorithm uses a compressed form of the database to determine support counts for the itemsets,
and avoids the candidate generation approach which might produce a large amount of itemsets without enough support.
First we determine the support for the $1$-itemsets in the same way as in a-priori: by scanning the database and
maintaining the support count of each element in the transactions.

After we determine $L_{1}$, we proceed to build the **fp-tree** as follows. 
First, we loop again through the dataset, sort each transaction in decreasing order according to its support count in $L_{1}$ and insert them into the tree.
If the item at a given index in the transaction is present in the node's children, we increase its count and recurse
on that node, checking increasing the index. 
In the end, we are left with a tree of the most common items close to the root and less common items closer to the leaves.
Since there might be more than one node with the item "1" for example, we keep a table where we maintain a reference to all the 
nodes for "1", as well as for all the other items.

The header table becomes useful in the next step which involves building the **conditional pattern bases**.
For each item, e.g. "1", we build the set of all the paths from these nodes to the roots. 
We then make smaller fp-tree, called the **conditional fp-tree**, for each element and insert the items in the 
conditional pattern base to the conditional fp-tree, and maintain the support count.
Once we build the conditional pattern tree for an item $i$, we prune the nodes who do not meet the minimal support count.
The remaining items in the tree are the items that comprise the frequent itemsets involving item $i$.

The overall set of frequent itemsets is thus the concatenation of the frequent itemsets for each item $i$.

## Experiment
To test the differnce between the two algorithms, we test several transitional datasets and compare the execution time 
and results.
There are a couple of datasets we are using: a 9-item file with the textbook example, used to check for correct itemset generation;
a 100-item `.data` file produced by the IBM dataset generator; and the provided `ibm-5000.txt` file.
The results are the average of three runs.

The testing results for the a-priori with a support count of 2 and rule confidence of 0.8 algorithm are as follows

| Trans. Number| Memory Usage(Mb) | Time(s) |
|----|----------------|--------|
| **9** | 12.95 | .000253 |
|**100**| 152,190 | 164.098 |
|**4798**|||

## Rules

## Answer:
1. High Support/ high confidence
2. High Support/ low confidence
3. Low Support/ High confidence
4. Low Support/ low confidence
