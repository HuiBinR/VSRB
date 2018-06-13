######## Pre-runing scripts for Image-Image Search Engine########
######## write by yaoliang   ########
 
### This Scripts is used for checking corrupted images which can't  		####
### recognized by image feature extraction system.., we remove unrecognized ####
### images from image list after the scripts be excuted...				    ####

#user defined params
ALL_DATA_DIR=/newVolume1/dingsiyuan/WIKI_Crwal/ 	# where the real images are stored
QUERY_DATA_DIR=/newVolume2/yaoliang/WMT16Img/ 		# where the real query images are stored		
ALL_DATA_LIST=$1		# wiki images list file...(contains image path and label, label default set to zero)
QUERY_DATA_LIST=$2      # query images list file...(contains image path and label, label default set to zero)

TOOLS=~/tools/caffe/build/tools
BASE_PATH="/newVolume2/yaoliang/ImageSearch/"
EXAMPLE=$BASE_PATH"example/"
TEMP_DIR=$BASE_PATH"tmp_dir/"                  #temporal directory
DATA_DIR=$BASE_PATH"data/"    #valid image data
ALL_DATA_EXP=$EXAMPLE"wiki_lmdb"
QUERY_DATA_EXP=$EXAMPLE"image_query_lmdb"

mkdir -p ${TEMP_DIR}
if [ ! $ALL_DATA ]; then
	echo "not given enough parameters... "
	exit
fi
if [ ! $QUERY_DATA ]; then
	echo "not given enough parameters..."
	exit
fi

####resize picture and convert to lmdb format..####
echo "convert image format..."
nohup bash create_imagenet.sh $ALL_DATA_DIR $ALL_DATA_LIST $ALL_DATA_EXP > "$TEMP_DIR/log" 2>&1 &
echo "waiting..."
wait

####find the corrputed images..####
echo "find the corrputed images..."
grep "Could not"  "$TEMP_DIR/log"  >  "$TEMP_DIR/failed"

####remove unvalid image name...####
python removeUnvalidImg.py $ALL_DATA $DATA_DIR"train_data_valid" "$TEMP_DIR/failed"


### we assume all query images are valid ###
nohup bash create_imagenet.sh $QUERY_DATA_DIR $QUERY_DATA_LIST $QUERY_DATA_EXP > "$TEMP_DIR/log.query" 2>&1 &
wait

# move the query images list to data directory...
cp $QUERY_DATA_LIST $DATA_DIR"query_data" 

#remove 
/bin/rm -r $ALL_DATA_EXP

