# Evaluate our model on LFW
DATADIR='../../lfw'
MODELDIR='casia_effb3/model.pt'
#MODELDIR='ms1mv3_arcface_r50/backbone.pth' 
LABELS='../../lfw_pairs/pairsDevTest.txt'
MODELNAME='efficientnet_b3'
TARGET='lfw'
GPU=0

python my_eval.py --data-dir $DATADIR --model-name $MODELNAME --model-path  $MODELDIR \
	--label-file $LABELS
