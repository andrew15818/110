# Homework 5
Modified code of ArcFace, mostly taken from their repo [here](https://github.com/deepinsight/insightface/tree/master/recognition/arcface_torch).

The `config` directory stores the options for the different models. 
The ones I used were `casia_wf_effb3.py` and `casia_wf_r50.py`.

To run the training script, edit `run.sh` with the path to the config file you need and type

```sh
sh run.sh
```
and watch the (hopefully) magic happen :D

To run the evaluation, change the path to the model you want to use in `run_eval.sh` and again

```sh
./run_eval.sh
```

I modified the dataloader slightly and rewrote the training and evaluation scripts `my_eval.py` and `my_train.py`.
