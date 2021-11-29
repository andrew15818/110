# Data Mining Homework 2
The main purpose of this assignment was to evaluate different classification models and 
their performance.
Then, we analyzed how the amounts of features in our data affected model's performance.

The relevant python files are `main.py` which reads the input data and calls the other models,
`decisiontree.py`, `naivebayes.py`, and `model.py`.

The main options for `main.py` are:
- `-f --file`: the file used for training and testing.
- `-a --algorithm`: either `decisiontree`, `neural`, or `naivebayes`.

## Data
The data files used here are in `.csv` format, with the attribute 
names at the first row of the file.
The last column is the class label.

