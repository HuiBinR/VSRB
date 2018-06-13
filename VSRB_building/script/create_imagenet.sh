#!/usr/bin/env sh
# Create the imagenet lmdb inputs
# N.B. set the path to the imagenet train + val data dirs
set -e

#EXAMPLE=/newVolume2/yaoliang/ImageSearch/example
TOOLS=~/tools/caffe/build/tools

#user defined params,should be revised when directory changes
ALL_DATA_ROOT=/home/zhangjiashuo/smallpic/  # where image datasets are stored, here is wikipedia images..
ALL_DATA_LIST=/home/zhangjiashuo/train.txt/  # wiki images list...
ALL_DATA_EXP=/newVolume2/yaoliang/ImageSearch/script/zhangjiashuo/img_train_lmdb  # formatted wiki images

# Set RESIZE=true to resize the images to 256x256. Leave as false if images have
# already been resized using another tool.
RESIZE=true
if $RESIZE; then
  RESIZE_HEIGHT=256
  RESIZE_WIDTH=256
else
  RESIZE_HEIGHT=0
  RESIZE_WIDTH=0
fi

if [ ! -d "$ALL_DATA_ROOT" ]; then
  echo "Error: DATA_ROOT is not a path to a directory: $ALL_DATA_ROOT"
  echo "Set the DATA_ROOT variable in create_imagenet.sh to the path" \
       "where the ImageNet training data is stored."
  exit 1
fi

echo "Creating train lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    $ALL_DATA_ROOT \
    $ALL_DATA_LIST \
    $ALL_DATA_EXP

