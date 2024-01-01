data=$1
postfix=$2
log_dir=exp_logs/${data}_${postfix}
mkdir -p $log_dir

iters=10
va_set=../data/$data/va.ffm
tr_set=../data/$data/tr.ffm
params="-t ${iters} -s 1 -p ${va_set} ${tr_set} ${log_dir}/last_model"

task(){

train_cmd="./ffm-train"

for lr in 0.2
do
    for l in 0
    do
        for k in 4
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
task | xargs -0 -d '\n' -P 1 -I {} sh -c {}
