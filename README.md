#Reddit Comments

**Matthew Meyer**

**Saint Louis University**

###Usage

Running `./manage.sh help` will show available options. 
gather will collect all of the comments on the top posts (Hot Filter) 
defined by `$SUB_REDDITS`. All of the downloaded data will go into the 
directory `comments/`. Alternatively, you can run `python gather.py <sub> 
<out_file> for an individual subreddit, then build the model with 
`python build.py <sub> <score>` where score is the threshold for 
comment points.

