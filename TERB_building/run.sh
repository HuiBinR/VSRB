
# Step1: split mention file into separating file...
inputPath=$1  #train or test file root dir
mentionPath=$2 #where mention1 mention2 are stored
searchResult=$3 #search result path
mkdir -p $searchResult
mkdir -p $mentionPath

echo 'split mention file...'
for file in ${inputPath}/*
do
	baseName=${file##*/}
	echo $baseName
	if [[ "${file}" =~ txt$ ]];
	then
		awk -F "\\|\\|\\|" '{print $1}' ${file} > $mentionPath/${baseName}_mention1
		awk -F "\\|\\|\\|" '{print $2}' ${file} > $mentionPath/${baseName}_mention2
	fi

done
# Step2: using lucene to retrieval image caption..
libPath=/data/yhong/yaoliang/Lucene/lib
lucenePath=/data/yhong/yaoliang/Lucene/lucene
# compile
javac -cp .:${libPath}/* ${lucenePath}/*.java

cd ${lucenePath}
wikiCapPath=/data/hongyu/yaoliang/Lucene/data/caption.txt
wikiSepPath=/data/yhong/yaoliang/Lucene/data/sep/
indexPath=/data/yhong/yaoliang/Lucene/indexDir/

#/bin/rm -r $searchResult/*
echo 'convert captions file into separated file...'
#java -cp .:${libPath}/* RetrieveDataPrepare ${wikiCapPath} ${wikiSepPath}

echo 'build index and search similar captions for each mention...'
java -cp .:${libPath}/* Main ${wikiSepPath} ${indexPath} ${mentionPath} ${searchResult} 100

#creat image pair
for file in $searchResult/*
do
	if [[ "$file" =~ txt_mention1$ ]];
	then
		baseName=${file%_*}
		echo $baseName
		sed -i 's/[0-9]*#//g' $file #remove source_id			
		sed -i 's/[0-9]*#//g' "$baseName"_mention2 #remove source_id		
		paste -d '' $file "$baseName"_mention2 > "$baseName"\#merge
		sed -i 's/|||$//g' "$baseName"\#merge
	fi
done
