# A-priori algorithm

## Check the subsets of a candidate frequent-itemset
Once we generate the candidate itemsets, we need to check all of its subsets
to check if they are all frequent. If any subset is not frequent, the entire candidate
can be thrown out.

To check whether an item is frequent, we have to use a **hash tree**, where the value
of each non-leaf node is the sum of the children's hash values.
Leaf nodes have the hashed value of the items in their set as the value.

