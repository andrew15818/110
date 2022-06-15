from easydict import EasyDict as edict

config = edict()

# Margin base softmax
config.margin_list = (1.0, 0.5, 0.0)
config.network = "r50" #"effnet_b3"
config.resume = False
config.save_all_states = False
config.output = "casia_r50"

config.embedding_size = 512 # Change if too big
config.rec = "../../CASIA-WebFace"

# Partial FC
config.sample_rate = 1
config.interclass_filtering_threshold = 0
config.fp16 = False

# General
config.batch_size = 64 # Might change <128
config.num_classes = 10575 
config.num_image = 494414 
config.warmup_epoch = 0
config.num_epoch = 12 
config.val_targets = ['lfw']

# SGD
config.optimizer = "sgd"
config.lr = 0.01
config.momentum = 0.9
config.weight_decay = 5e-4

config.verbose = 2000
config.frequent = 10

config.dali = False
config.seed = 2048
config.num_workers = 1
