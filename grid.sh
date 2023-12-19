#data=criteo
data=libffm_toy
log_dir=exp_logs/$data
mkdir -p $log_dir

iters=20
va_set=../data/$data/va.ffm
tr_set=../data/$data/tr.ffm
#params="-t ${iters} -s 16 --auto-stop --no-norm -p ${va_set} ${tr_set} ${log_dir}/best_model"
params="-t ${iters} -s 1 --no-norm -p ${va_set} ${tr_set} ${log_dir}/best_model"

task(){

train_cmd="./ffm-train"

for lr in 0.2
do
    for l in 0 #.00002
    do
        for k in 4 #1 2 4 8
        do
            cmd="${train_cmd} -r $lr"
            cmd="${cmd} -l $l"
            cmd="${cmd} -k $k"
            cmd="${cmd} ${params} | tee $log_dir/${lr}_${l}_${k}.log"
            echo "${cmd}"
        done
    done
done

}

# Check command
task
wait

# Run
task | xargs -0 -d '\n' -P 2 -I {} sh -c {}
