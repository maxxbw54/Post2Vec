# Post2Vec - Representation Learning for Stack Overflow Post

Post2Vec interface can be used to get the representation directly from the trained check point.

## Instructions

- Download the model checkpint at [Link](https://drive.google.com/file/d/1fRjmRcNLkLx4EHXU8-bKrvGuq3VdCmPu/view?usp=sharing) and store under the folder `/data/model/`.

- Get question vector by simply calling `src/interface/post2vec`

- Get full vector of a question by calling `qvec = np.concatenate([q.title, q.desc_text, q.desc_code])`

