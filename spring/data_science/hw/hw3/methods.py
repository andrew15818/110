import numpy as np
import sklearn.impute as impute
from GAIN.gain import gain as gain_imp
#from GRAPE.models.gnn_model import get_gnn
# Need this since IterativeImputer is still experimental
from sklearn.experimental import enable_iterative_imputer
from dataclasses import dataclass, field

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

# I think we first do the missing indicator, then impute the values?
def missing_indicator(features, method='mean'):
    imputer = impute.MissingIndicator(missing_values=np.nan)
    mask = imputer.fit_transform(features).astype(float)
    # Also do regular imputation
    if method == 'mean':
        imputed = mean_imp(features)
    elif method == 'knn':
        imputed = knn(features)
    else:
        imputed = mice(features)

    # Add the missing indicators as extra columns
    return np.concatenate((imputed, mask), axis=1)

def gain(features):
    # Settings taken from GAIN/main_letter_spam.py
    # TODO: Find a way to not just use defaults?
    parameters = {'batch_size': 128,
            'hint_rate': 0.9,
            'alpha': 100,
            'iterations': 10000
            }
    return gain_imp(features, parameters)

# Because GRAPE relies on cmd args, maybe 
# we can get around it with this?
@dataclass
class GRAPEArgs:
    model_types: str = field(default='EGSAGE_EGSAGE_EGSAGE')
    norm_embs: str = field(default=None)
    post_hiddens: str = field(default=None)
    node_dim: int = field(default=64)


def grape(features):
    grapeArgs = GRAPEArgs()
    model = get_gnn(features, grapeArgs)
    pass

