# Post2Vec - Representation Learning for Stack Overflow Post

Post2Vec interface can be used to get the representation directly from the trained check point.

## Instructions

- Get question vector by simply calling `src/interface/post2vec`

- Get full vector of a question by calling `qvec = np.concatenate([q.title, q.desc_text, q.desc_code])`

## How to Run with Docker Container

- Download the Docker Image (around 11G) from [here](https://drive.google.com/file/d/1F49komWwuq7b0BQpCFZZjYji171f_r4v/view?usp=sharing)

- Clone the repo under the folder `[LOCAL_FILE_DIR]` via:

```
cd [LOCAL_FILE_DIR]
git clone https://github.com/maxxbw54/Post2Vec.git
```

- Add your data to be converted to vectors by Post2vec under the folder `[LOCAL_FILE_DIR]/data/input`


- Create a Docker Container:

```docker run -it --gpus '"device=[GPU(s)]"' --name post2vec -v [LOCAL_FILE_DIR]:/post2vec post2vec-interface```

- Download the model checkpint at [Link](https://drive.google.com/file/d/1fRjmRcNLkLx4EHXU8-bKrvGuq3VdCmPu/view?usp=sharing) and store under the folder `[LOCAL_FILE_DIR]/data/model`.


- Configure the main file `Post2Vec/src/interface/post2vec.py` in the container accordingly, and then set up the environment by using virtual environemnt with `pip3 installl -r requirement.txt`. And then run the main file again to produce the corresponding vectors in `.pkl` format.

```
cd /post2vec/Post2Vec
source .env/bin/activate
export PYTHONPATH="${PYTHONPATH}:/post2vec/Post2Vec/src"
CUDA_VISIBLE_DEVICES=3 .env/bin/python3 src/interface/post2vec.py
```
