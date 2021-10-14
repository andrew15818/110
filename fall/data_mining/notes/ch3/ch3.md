# Data Preprocessing
Since some of the data in our database might be incomplete, reconstructing
or filling in missing details could be helpful in ensuring more accurate results.

## Data Cleaning
How do we do if there are missing values in the database? 
There are a couple ways:
1. Ignore the tuple. Could be necessary if the tuple is missing many fields,
but might be a waste of other potentially useful fields.
2. Fill the values in manually: Time consuming.
3. Fill values in with global constant (like inf).
4. Use mean, median or mode as the missing value.
5. Use the average/median for other members of the same class if doing classification.
6. Use some other form of inference to guess the most likely number: Bayes', decision tree, etc...

Besides missing values **noise** can also affect our data by adding small random
perturbations to the values.
There are ways to mitigate the effect of noise, such as **binning**.
Here we group the items into equally-sized bins based on the closest values.
Then we get the mean or max of the items in the bin and replace each item's value.

Regression can also be a useful way to fill missing data by getting a function that tells
us how me should expect.
Using the info gained from the metadata can also serve us: mean , median, mode, quartiles, etc...
Same data can also have different formats, as in the case with dates.
**Extraction/Transformation/Loading** tools could also help us transform the data if needed using a GUI.



