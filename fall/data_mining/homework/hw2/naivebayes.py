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
        
        final = norm.pdf(val, mu, sig)
        #print(f'\tparams to normal function : {final} = {val, mu, sig}' )
        return final

    # Prior class probability P(Ci)
    def _class_prior_prob(self, data:pd.DataFrame, label:str) -> float:
        # Name of the last column with class label
        colname = data.columns[-1]
        return (data[colname] == label).sum() / len(data)


    # main entry point
    def run(self, data):
        classes = [] 
        attribs = data.columns[:-1]
        for item in data.itertuples(): # item[0] is the index
            featvalues = item[1:-1]
            best_prob = 0
            best_class = ""
            for ci in self.labels:
                class_prior = self._class_prior_prob(data, ci)
                posterior = 1
                for attribute, value in zip(attribs, featvalues):
                    posterior *=  self._posterior_prob(data, ci, attribute, value)
                #print(class_prior, posterior)
                if posterior * class_prior > best_prob:
                    best_prob = posterior
                    best_class = ci
                    #print(f'best_class {best_class} ')
            classes.append(best_class)
        return classes
        # DEBUG: check the accuracy on the training set
        # Check if this is best prob

