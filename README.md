#Reddit Comments

**Matthew Meyer**

**Saint Louis University**

###Usage

**Building:**     
Running `bash build.sh` will build collect all of the comments on 
the top 25 posts (Hot Filter) defined by `$SUB_REDDITS`. All of the 
downloaded data will go into the directory `comments/`.
Alternatively, you can run `python get_data.py <sub> <out_file> for an
individual subreddit, then build the model with 
`python build_model.py <sub>`


**Running:**     
After the data has been pulled from the web, you can run 
`python guess.py`. You will enter in a subreddit (by default,
the program will look for it in the data/ directory) and comment,
and will recieve a karma rating, predicting the score of the comment.

