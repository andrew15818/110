# Getting to know your data
When we take in data for questioning, it would be useful to do some early check
on its average values and such (e.g. mean, median, mode).

**Nominal** attributes or categorical attributes take on the values of a specific class.
These values just indicate membership in a class even if the attributes are numeric.
**Binary** attributes are just boolean nominal attributes. 
Symmetric binary attributes are equally likely to be either zero or one.

**Ordinal** attributes, similar to ordinal numbers, are those where there are a ranking.
Although they indicate rank, they don't give hints on actual differences between categories.
The meands, modes and medians are more useful for us.
These attributes tell us about the central tendency of a dataset.

The mean of a group of numbers is just the sum $\sum_{i} x_{i}$ divided over the number of 
data samples $N$.
If each of these as a different importance to our calculation, we can assign a weight to each and get 
the **weighted average** by adding the result of each $w_{i}x_{i}$ and divide it by the summation of the weights $\sum_{i=1}^{N}w_{i}$.
However, the mean can be distorted by some extremely high or low values.
To account for this, we could trim the topmost or lowermost values to get a more accurate representation.

The **median** is the middlemost value in the dataset. 
For asymmetric data, the median might be a better measure.
Given a sorted dataset, the number in the middle is the median.

The **mode** is the number that appears most frequently in the dataset.
If the dataset is symmetric, then the mean median and mode are all the same value.
Otherwise the mode might be positively skewed and be smaller than the median or
negatively skewed and be larger than the median.

There are also other methods to analyze data.
**Quantiles** are data points that can produce equal size subsets.
The $k$-th q-quantile means that $k/q$  values at most are less than a value $x$
and $q-k/q$ values are greater than $x$.
Depending on how many quantiles, we can have **quartiles** and **percentiles** based on 
4 and 100 quantiles, respectively.

