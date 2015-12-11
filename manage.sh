SUB_REDDITS=(askreddit funny pics videos news politics todayilearned gaming \
             gifs aww relationships showerthoughts sports iama science)
COMMENTS_DIR=comments
DATA_DIR=data
TEST_DIR=test

HELP() {
  echo "Usage: $0 {arg}"
  echo "    help   - Show this help message"
  echo "    gather - gather the comments from reddit.com"
  echo "    build  - format data from comments"
  echo "    test   - test prediction"
}

GATHER() {
  mkdir -p $COMMENTS_DIR
  for sub in ${SUB_REDDITS[@]}
  do
    if [ -f "$COMMENTS_DIR/$sub" ]
    then
      echo "Already gathered comments for $sub"
    else
      python gather.py $sub $COMMENTS_DIR/$sub
    fi
  done
}

BUILD() {
  mkdir -p $DATA_DIR
  for sub in ${SUB_REDDITS[@]}
  do
    python build.py $sub $COMMENTS_DIR $1
  done
}

TEST() {
  mkdir -p $TEST_DIR
  DUMMY=dummy.dummy
  for sub in ${SUB_REDDITS[@]}
  do
    cat $COMMENTS_DIR/$sub | shuf > $DUMMY
    COUNT=$(cat $DUMMY | wc -l)
    N=$(python -c "print $COUNT/10")
    tail -n $N $DUMMY > $TEST_DIR/$sub.test
    head -n $(python -c "print $COUNT - $N") $DUMMY > $TEST_DIR/$sub
  done
  rm $DUMMY
  COMMENTS_DIR=$TEST_DIR
  BUILD $1
  for sub in ${SUB_REDDITS[@]}
  do
    python test.py $sub $1
  done
}

while [[ $# > 0 ]]
do
  case $1 in
    gather )
      GATHER
      ;;
    build )
      shift 
      BUILD $1
      ;;
    test )
      shift
      TEST $1
      ;;
    * )
      HELP
      exit
      ;;
  esac
  shift
done
exit
