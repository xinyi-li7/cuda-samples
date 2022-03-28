export FP_EXCEPTION_HOME=/home/xinyi/nvbit-exceptions/tools/detect_fp_exceptions
export PRELOAD_FLAG="LD_PRELOAD=${FP_EXCEPTION_HOME}/detect_fp_exceptions.so"


#EXEs=$(find Samples/ -type f -executable)
EXEs='Samples/5_Domain_Specific/BlackScholes/BlackScholes Samples/5_Domain_Specific/binomialOptions/binomialOptions'
for exe in ${EXEs}
do
	run=${exe##*/}
	size=${#run}
#	echo $size
#	echo ${exe::(-$size+0)}
	dir=${exe::(-$size+0)}
	cd $dir;
	echo "in ${dir}....."
	comm="eval ${PRELOAD_FLAG} ./${run}"
	echo ${comm} > run.sh
	comm2="eval ./${run}"
	echo ${comm2} > run_ori.sh
	echo "run original program"
	(time timelimit -t1200 bash run_ori.sh) >stdout_ori.perf.txt 2>stderr_ori.perf.txt
	echo "run checking program"
	(time timelimit -t1200 bash run.sh) >stdout.perf.txt 2>stderr.perf.txt
	cd -;
done
