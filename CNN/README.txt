code usage:
1. All the code with T is used for 2-way Temporal relation classification.
2. All the code with C is used for 3-way classification.
3. All the code with cause is used for 2-way Causal relation classification.

data usage:
1. TERB_Train: the training data builded on TERB, used by the Temporal classification and the 3-way classification.
2. Cause_Train: the training data builed on TERB used by the 2-way Causal relation classification.
2. Test_cause_network: the test data for causal relation.
3. Test_network: the test data used by the Temporal classification and the 3-way classification.

matters need attention:
1. We divide the predicting and evalution into 2 parts. Use the predicting files we recorded in the "results" file, and evaluate the PRF score with the codes in the "evaluation" file.