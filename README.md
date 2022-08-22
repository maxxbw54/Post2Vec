# Post2Vec - Representation Learning for Stack Overflow Post

Note: This is the branch Post2Vec interface for easy use, means you can get the learned representation directly from the trained check point. If you want to check the orignal training and test data, please checkout the `main` branch and you should have them.


## Instructions

- Get question vector by simply calling `src/interface/post2vec`

- Get full vector of a question by calling `qvec = np.concatenate([q.title, q.desc_text, q.desc_code])`

## How to Run with Docker Container

1. GitHub Repo

1.1 Clone the repo under the folder `[LOCAL_FILE_DIR]` via:

```
cd [LOCAL_FILE_DIR]
git clone https://github.com/maxxbw54/Post2Vec.git
```

2. Docker

2.1 Download the Docker Image (around 11G) from [here]()

2.2 Import the image via:

```
cat [LOCAL_FILE_DIR]/post2vec-interface.tar | docker import - post2vec-interface:latest
```

2.3 Create a Docker Container:

```docker run -it --gpus '"device=[GPU(s)]"' --name post2vec -v [LOCAL_FILE_DIR]:/post2vec post2vec-interface```

3. Model checkpoint

3.1 Download the model checkpint at [Link](https://drive.google.com/file/d/1QmB2SCcrw4t6mrgPXKgvKz9PFtozeKby/view?usp=sharing) and store under the folder `[LOCAL_FILE_DIR]/data/model`.

4. Input/Query data

4.1 Add your data to be converted to vectors by Post2vec under the folder `[LOCAL_FILE_DIR]/data/input`

5. Configuration (Input & Output Data File Path)

Configure the main file `Post2Vec/src/interface/post2vec.py` in the container accordingly, and then set up the environment by using virtual environemnt with `pip3 installl -r requirement.txt`. And then run the main file again to produce the corresponding vectors in `.pkl` format.

6. Run to collect the output data

```
cd /post2vec/Post2Vec
source .env/bin/activate
export PYTHONPATH="${PYTHONPATH}:/post2vec/Post2Vec/src"
CUDA_VISIBLE_DEVICES=3 .env/bin/python3 src/interface/post2vec.py
```
