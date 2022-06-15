from easydict import EasyDict as edict

config = edict()

# Margin base softmax
config.margin_list = (1.0, 0.5, 0.0)
config.network = "efficientnet_b3" #"effnet_b3"
config.resume = False
config.save_all_states = False
config.output = "lfw_arcface_effnetb3"

config.embedding_size = 512 # Change if too big
config.rec = "../../lfw"

# Partial FC
config.sample_rate = 1
config.interclass_filtering_threshold = 0
config.fp16 = False

# General
config.batch_size = 32 # Might change <128
config.num_classes = 5749
config.num_image = 13233
config.warmup_epoch = 0
config.num_epoch = 12 
config.val_targets = ['lfw']

# SGD
config.optimizer = "sgd"
config.lr = 0.1
config.momentum = 0.9
config.weight_decay = 5e-4

config.verbose = 2000
config.frequent = 10

config.dali = False
config.seed = 2048
config.num_workers = 1
