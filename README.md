# VSRB

The purpose of this repository is to share the code and the data for the paper:  Incorporating Image Captioning and Matching Into Knowledge Acquisition for Event-Oriented Relation Recognition.

## Data building
#### 1 Train/Test data building
We use the code in Train_Test_build to build the test data on the ACE-R2 dataset, and the training data on TERB and PDTB.

- Code usage:
    - divide_dataset.py: Divide the dataset into development dataset and test dataset.
    - cnt_temp_during_equal.py: Compute the number of the relation we want to combine
    - delete_other_relation.py: Delete the relation we won't use for classification in this time
    - score_prf.py: Compute the prf score

- Matters need attention:

    - We can't provide PDTB, but you can get it from: https://catalog.ldc.upenn.edu/LDC2008T05

#### 2 TERB building
Use the code in TERB_building to build the TERB.

- Code usage:
    - Use Step1 in run.sh to divide the Gigaword data.
    - Use the RetrieveDataPrepare to prepare the caption data in file sep.
    - Use the Main to build index and seatch similar captions for each mention in the extracted Gigaword corpus (in the file train).
    - Use code in run.sh to concatenate the retrieve results of each mention.
- Data usage:
    - test.zip: The test data extracted from ACE-R2.
    - train.zip: The extract Gigaword data. (The train.zip is too big to share here, we will update the link to get it in the future.)
    - sep.zip: Storing the id of image captions for index building and retrieval. (The sep.zip is too big to share here, we will update the link to get it in the future.)


#### 3 VSRB building
The code in ImageSearch is used to build the VSRB.

- Code usage:
    - create_imagenet.sh: Resize images and convert them to lmdb format.
    - removeUnvalidImg.py: Remove unvalid image name
    - run.sh: Search similiar image.
- Data usage:
    - data.zip: Record the storage path and the id of each images. (The data.zip is too big to share here, we will update the link to get it in the future.)

- Matters need attention:
    - The image dataset is too big to upload here, which contains about 740,000 images, so we provide the result of the VSRB construction: GigaVSRB_Result_top100.
    - The image dataset will be shared on the figshare later, and the webpage link will be shared here. So you can reproduce VSRB.

## Holmes
The code in file Holmes is used to construct Holmes.

- Code usage:
    - IISVSRBPRF_record: Use the test data to retrieve the VSRB and save the result of the predicition.
    - score_the_add_cnt_*.py: Tune the model and compute the PRF score.
- Data usage:
    -  GigaVSRB_Result_top100 (VSRB): The id pairs of the simi image searched by image similarity.
    -  Test_cause: The test date for 2-way contingent relation classification
    -  Test_count: The test data for 3-way classification and 2-way temporal classification.

## Bi-LSTM
The code in file LSTM is used to train the Bi-LSTM model.

- Code usage:
	- data_helpers_*.py: Data preparing.
	- train_*.py: Train the classification model.
	- Text_BiRNN.py: Build the BiRNN.
	- Eval_*.py: Evaluate the model.
- Data usage:
	- TERB_Train: The training data builded on TERB, used by the Temporal classification and the 3-way classification.
	- Cause_Train: The training data builed on TERB used by the 2-way Causal relation classification.
	- Test_cause_network: The test data for causal relation.
	- Test_network: The test data used by the Temporal classification and the 3-way classification.

## CNN
The code in file CNN is used to train the CNN model.
- Code usage:
	- data_helpers_*.py: Data preparing.
	- train_*.py: Train the classification model.
	- text_cnn.py: Build the CNN.
	- Eval_*.py: Evaluate the model.
- Data usage:
	- TERB_Train: the training data builded on TERB, used by the Temporal classification and the 3-way classification.
	- Cause_Train: the training data builed on TERB used by the 2-way Causal relation classification.
	- Test_cause_network: the test data for causal relation.
	- Test_network: the test data used by the Temporal classification and the 3-way classification.




---
The data are shared on figshare: https://figshare.com/s/cf3869dcde770b58d4df
- sep.zip: The files named with each ids which store the captions of each images.
- train.zip: The extracted Gigaword data for VSRB building.
- data.zip: The training data for all the neural network (Bi-LSTM and CNN).
- data_VSRB.zip: The data for VSRB building.

---

There are .sh/.shell files in most of the code file, you can use the code according to it.
