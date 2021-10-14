---
Author: "Andres Ponce"
Title: "Introduction to Data Mining"
---
# Introduction to Data Mining
Data mining refers to the methods by which we gain information from data.
It is related to machine learning and statistics.
With hardware advanced in recent years extracting patterns from data has become both easier and cheaper.

A **data warehouse** is a single site where multiple different data sources are aggregated to facilitate
management.

Similar to regular mining, data mining attempts to find useful pieces of information from large amounts of raw material
or not so useful data.
Gaining useful information then has a couple of stages, such as preprocessing.
In preprocessing we filter any noise from the data an may aggregate data from different sources.

A **data cube** is a way of visualizing data where each dimension is an attribute or set of attributes and each individual
cell is a value such as a count, etc...
**Online analytical processing** operations can allow us to view data at different *levels of abstraction*.
For example, if we break down the sales of each quarter to view by month, we are **drilling down**, and if we 
combine data points into a larger one we are **rolling up**.
If we take all the results of a row or column from a data cube or multidimensional data cube, we can arrive at useful data pieces.

A **transactional data base** is one where each entry is a transaction such as a purchase or rental.
Databases just represent the relations between items with different **attributes**.
When we find relations between different data points, we try and find some characteristic rules.

There are many types of occurrences of similar data that would be of importance, such as frequent itemsets, or frequent subsequences.
Recommendation systems would try to recommend products that often get bought together by people of certain demographics.
A value indicating the **confidence** of the association would indicate how likely it is that the items occur together.
The **support** value indicates the percentage of transactions involve similar itemsets.
The attribute that we're looking for in our conditions (e.g. customer *buys* item) would be a single dimension in our data cube.
(e.g. if 2% of all customers purchased a laptop and a camera, there is 60% chance they also buy memory).
If we had more we would perform **multi-dimensional analysis**.

In a system there might be a minimum threshold for support and confidence in order to use a certain association rule.
When we present a **model** for classifying the data, it could be a lot of if-then rules or a decision tree.

