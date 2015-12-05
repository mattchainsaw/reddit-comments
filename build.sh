SUB_REDDITS=(askReddit funny pics videos news politics todayilearned gaming \
             gifs aww relationships showerthoughts sports iama science)
COMMENTS_DIR=comments
DATA_DIR=data

mkdir -p $COMMENTS_DIR
for sub in ${SUB_REDDITS[@]}
do
  if [ -f "$COMMENTS_DIR/$sub" ]
  then
    echo "Already gathered comments for $sub"
  else
    python get.py $sub $COMMENTS_DIR/$sub
  fi
done
