######## Image-Image Search System ########
######## write by yaoliang   ########

BASE_PATH="/newVolume2/yaoliang/ImageSearch/"
DATA=$BASE_PATH"data/" 
EXAMPLE=$BASE_PATH"example/"

WIKI_IMG_DIR=/	#where images are stored
TEMP_DIR=$BASE_PATH"tmp_dir/"
TOOLS=~/tools/caffe/build/tools
mkdir -p ${TEMP_DIR}

:<<mark
#### Step1: resize picture and convert to lmdb format... ####
echo "convert image format..."
for file in $DATA/*
do
	if [[ "$file" =~ wikiTrain[01]+ ]];
	then
		name=${file##*/}
		echo "name:"$name
		nohup bash create_imagenet.sh $WIKI_IMG_DIR $file $EXAMPLE"$name" > $TEMP_DIR"/log"$name 2>&1 &
		wait
		echo "ok"
	fi
done	
mark

##### step2 extract image feature #######

echo "done of format conversion..."
PROTO_FILE=$BASE_PATH"proto/wikiProto"
BATCH_SIZE=32   # BATCH SIZE in proto file
DATA_SIZE=80000 # the size of each train data 
NUM_BATCH=$(expr $DATA_SIZE / $BATCH_SIZE)
echo $NUM_BATCH

echo "extract features using trained deep CNN neural work..."
array=("00" "01" "02" "03" "04" "05" "06" "07" "08" "09" "10")
for element in ${array[@]}
do
	if [ -r $BASE_PATH"feature_extraction/wikiTrain"$element ]; then
		echo "remove ..."
		rm -r $BASE_PATH"feature_extraction/wikiTrain"$element
	fi

	echo "extract part "$element	
	$TOOLS/extract_features.bin 	\
		$BASE_PATH"model/VGG_ILSVRC_16_layers.caffemodel" 		\
		$PROTO_FILE"_"$element  						\
		fc7 				\
		$BASE_PATH"feature_extraction/wikiTrain"$element \
		$NUM_BATCH 		\
		leveldb 			\
		GPU
done 

::<<mark
# query image feature extraction...
QUERY_PROTO=$BASE_PATH"proto/query_proto" 
QUERY_BATCH=`cat $BASE_PATH"data/query_data" | wc -l`

if [ -r $BASE_PATH"feature_extraction/query_features" ]; then
	rm -r $BASE_PATH"feature_extraction/query_features"
fi

$TOOLS/extract_features.bin \
	"$BASE_PATH"model/VGG_ILSVRC_16_layers.caffemodel \
	$QUERY_PROTO        \
	fc7                 \
	$BASE_PATH"feature_extraction/query_features"     \
	$QUERY_BATCH   	    \
	leveldb             \
	GPU

echo "save features..."

ALL_DATA_FEATURES=$BASE_PATH"data/all_data_features"
QUERY_FEATURES=$BASE_PATH"data/all_query_features"
mark
#python readFeat.py feature_extraction/all_features $ALL_DATA_FEATURES
#python readFeat.py feature_extraction/query_features $QUERY_FEATURES
#python compute_distance.py "data/all_query_features" "data/query_data" "data/all_data_features" "data/all_valid_data"
