## This script used for get test image list ##
testDir=$1
for file in $testDir/*
do
	awk -F "|" '{for(i=1;i<=NF;++i) if($i==""){} else{print $i}}' $file >> "image_list"

done

sort -u "image_list" > "image_uniq"

