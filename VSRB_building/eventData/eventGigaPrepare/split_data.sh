path=$1 #vsrb file , has three column, which part | position | path id
awk -F '|' '{if($1=="0") print $0}' $path | sort -t '|' -k2 -n > vsrb_data_00
awk -F '|' '{if($1=="1") print $0}' $path | sort -t '|' -k2 -n > vsrb_data_01
awk -F '|' '{if($1=="2") print $0}' $path | sort -t '|' -k2 -n > vsrb_data_02
awk -F '|' '{if($1=="3") print $0}' $path | sort -t '|' -k2 -n > vsrb_data_03
awk -F '|' '{if($1=="4") print $0}' $path | sort -t '|' -k2 -n > vsrb_data_04
awk -F '|' '{if($1=="5") print $0}' $path | sort -t '|' -k2 -n > vsrb_data_05
awk -F '|' '{if($1=="6") print $0}' $path | sort -t '|' -k2 -n > vsrb_data_06
awk -F '|' '{if($1=="7") print $0}' $path | sort -t '|' -k2 -n > vsrb_data_07
awk -F '|' '{if($1=="8") print $0}' $path | sort -t '|' -k2 -n > vsrb_data_08
awk -F '|' '{if($1=="9") print $0}' $path | sort -t '|' -k2 -n > vsrb_data_09
awk -F '|' '{if($1=="10") print $0}' $path | sort -t '|' -k2 -n > vsrb_data_10
awk -F '|' '{if($1=="11") print $0}' $path | sort -t '|' -k2 -n > vsrb_data_11
awk -F '|' '{if($1=="12") print $0}' $path | sort -t '|' -k2 -n > vsrb_data_12
awk -F '|' '{if($1=="13") print $0}' $path | sort -t '|' -k2 -n > vsrb_data_13
awk -F '|' '{if($1=="14") print $0}' $path | sort -t '|' -k2 -n > vsrb_data_14
awk -F '|' '{if($1=="15") print $0}' $path | sort -t '|' -k2 -n > vsrb_data_15

cat vsrb_data_* > VSRB_train_data_tmp
awk '{print $0" 0"}' VSRB_train_data_tmp > VSRB_train_data
