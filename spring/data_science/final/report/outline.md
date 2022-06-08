1. Introduction
- Explain the usefulness of visual search, when to use
- Explain the idea of the competition
- Stress some of the challenges in such a competition

2. Competition Description
- Motivated by need for fine-grained visual search
- Large number of different products can still belong to same class
- How the hierarchy is laid out, how many images
- Difference b/w train, test sets 

3. Related Methods
	- Why didn't we use these methods?

Describe these methods and why we didn't use them.
4. Method description
- More than just image classification, fine-grained differences
- Use ResNet50 for feature learning
	- How do we mix in hierarchical structure into training?
	- Model tries to predict meta, level2, subclass
	- Figure of model
- Locality sensitive hashing, math background
	- How do we find related images in a hash table using model embedding?
	
5. Training, experiments
- Algorithm
- Show an example of why my algorithm did so poorly
	- Show query image and some of the matched images
Reasons for poor performance:
1. The paper we based our results on used far fewer classes, task slightly different.
2. Querying many individual hash tables
3. Compounding of errors during training, it propagates during building hash tables.
4. Long evaluation time, hard to measure changes.
5. Too many similar images, too high distance measure.
