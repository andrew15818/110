import numpy as np
import sklearn.impute as impute

def mean_imp(features):
    imputer = impute.SimpleImputer(missing_values=np.nan,
                                    strategy='mean')
    return imputer.fit_transform(features)


