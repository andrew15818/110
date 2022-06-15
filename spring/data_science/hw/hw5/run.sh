
##CUDA_VISIBLE_DEVICES=0 python -m torch.distributed.launch \
#--nproc_per_node=1 \
#--nnodes=1 \
#--node_rank=0 \
#--master_addr="127.0.0.1" \
#--master_port=12345 train.py $@
#CONFIG="configs/casia_wf_r50.py"
CONFIG="configs/casia_wf_effb3.py"
RATIO=0.25
python my_train.py --local_rank 0 $CONFIG --ratio $RATIO

ps -ef | grep "train" | grep -v grep | awk '{print "kill -9 "$2}' | sh
