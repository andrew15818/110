import numpy as np
import torch
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

# Sample random numbers within standard deviation
def std(features):
    phi = np.std(features, axis=1)
    imputer = impute.SimpleImputer(missing_values=np.nan, 
                                    fill_value=phi[0]*np.random.sample()
                                    )
    arr = imputer.fit_transform(features[:,0].reshape(-1,1))
    for idx in range(1, features.shape[1]):
        col = features[:,idx]
        imputer = impute.SimpleImputer(missing_values=np.nan, 
                                        fill_value=(col.mean() + phi[idx]*np.random.sample()))
        imputed = imputer.fit_transform(features[:,idx].reshape(-1,1))
        arr = np.concatenate((arr, imputed),  axis=1)
    return arr 
        

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

    out = np.concatenate((imputed, mask), axis=1)
    return out
def gain(features, missingRatio=0.1):
    # Using batch_size=128 gave me dimension error on one dataset?
    # This batch_size works
    parameters = {'batch_size': 93,
            # missing data = 1 - hint_rate
            'hint_rate': 1-missingRatio,
            'alpha': 100,
            'iterations': 1
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


def grape(features, dataset):
    print(dataset)
    load_path = './GRAPE/uci/mdi_results/results/gnn_mdi_v1/{}/0/impute_model.pt'\
        .format(dataset)
    #model = torch.nn.Module.load_state_dict(torch.load(load_path))
#    grapeArgs = GRAPEArgs()
    #model = get_gnn(features, grapeArgs)
    pass

