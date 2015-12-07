SUB_REDDITS=(askreddit funny pics videos news politics todayilearned gaming \
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
    python get_data.py $sub $COMMENTS_DIR/$sub
  fi
done

echo 'Almost done!'
mkdir -p $DATA_DIR
for sub in ${SUB_REDDITS[@]}
do
  python build_models.py $sub
done
echo 'Done!'
