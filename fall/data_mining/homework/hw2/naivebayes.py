import pandas as pd
from scipy.stats import norm

class NaiveBayes:
    def __init__(self,labels=None):
        self.labels = labels
        pass

    def set_labels(self, labels):
        self.labels = labels

    # Posterior probability P(X|Ci)
    def _posterior_prob(self, data:pd.DataFrame, label:str, attribute:str,val:float) -> float:
        # Get the sum, standard dev of class values
        classcol = data.columns[-1]
        # All the rows in given class
        D = data[data[classcol] == label]
        mu = D[attribute].mean()
        sig = D[attribute].std()
        
        return norm.pdf(val)

    # Prior class probability P(Ci)
    def _class_prior_prob(self, data:pd.DataFrame, label:str) -> float:
        # Name of the last column with class label
        colname = data.columns[-1]
        return (data[colname] == label).sum()


    # main entry point
    def run(self, data):
        classes = [] 
        for item in data.itertuples(): # item[0] is the index
            featvalues = item[1:-1]
            attribs = item._fields[1:-1]
            best_prob = 0
            best_class = ""
            for ci in self.labels:
                class_prior = self._class_prior_prob(data, ci)
                posterior = 1
                for attribute, value in zip(attribs,featvalues):
                    posterior *=  self._posterior_prob(data, ci, attribute, value)
                if posterior * class_prior > best_prob:
                    best_prob = posterior
                    best_class = ci
            classes.append(best_class)
        print(classes)
                # Check if this is best prob

