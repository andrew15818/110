from easydict import EasyDict as edict

config = edict()

# Margin base softmax
config.margin_list = (1.0, 0.5, 0.0)
config.network = "efficientnet_b3"
config.resume = True  # Wer'e going to continue training 
config.save_all_states = False
config.output = "casia_effb3"

config.embedding_size = 512
config.rec = '../../CASIA-WebFace'

# Partial FC
config.sample_rate = 1
config.interclass_filtering_treshold = 0
config.fp16 = False

config.batch_size = 32
config.num_classes = 10575
config.num_image = 494414
config.warmup_epoch = 0
config.num_epoch = 12
config.val_targets = ['lfw']

#SGD
config.optimizer = 'sgd'
config.lr = 0.1
config.momentum = 0.9
config.weight_decay = 5e-4
config.verbose = 2000
config.frequent = 10
config.dali = False
config.seed = 2048
config.num_workers = 1
