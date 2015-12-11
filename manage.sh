SUB_REDDITS=(askreddit funny pics videos news politics todayilearned gaming \
             gifs aww relationships showerthoughts sports iama science)
COMMENTS_DIR=comments
DATA_DIR=data

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
  echo 'Almost done!'
  mkdir -p $DATA_DIR
  for sub in ${SUB_REDDITS[@]}
  do
    python build.py $sub
  done
  echo 'Done!'
}

TEST() {

}

while [[ $# > 0 ]]
do
  case $1 in
    gather )
      GATHER
      ;;
    build )
      BUILD
      ;;
    test )
      TEST
      ;;
    * )
      HELP
      exit
      ;;
  esac
  shift
done
exit
