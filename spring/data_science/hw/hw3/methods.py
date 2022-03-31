import numpy as np
import sklearn.impute as impute
# Need this since IterativeImputer is still experimental
from sklearn.experimental import enable_iterative_imputer

def mean_imp(features):
    imputer = impute.SimpleImputer(missing_values=np.nan,
                                    strategy='mean')
    return imputer.fit_transform(features)

def knn(features, n=5):
    imputer = impute.KNNImputer(missing_values=np.nan, 
                                    n_neighbors=n)
    return imputer.fit_transform(features)

def mice(features):
    imputer = impute.IterativeImputer(missing_values=np.nan)
    return imputer.fit_transform(features)


