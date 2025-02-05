#!/usr/bin/env sh
# Compute the mean image from the imagenet training lmdb
# N.B. this is available in data/ilsvrc12

EXAMPLE=/newVolume2/yaoliang/ImageSearch/example
DATA=/newVolume2/yaoliang/ImageSearch/data
TOOLS=~/tools/caffe/build/tools/

$TOOLS/compute_image_mean $EXAMPLE/image_train_lmdb \
  $DATA/imagenet_mean.binaryproto

echo "Done."
