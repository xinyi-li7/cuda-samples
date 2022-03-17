export FP_EXCEPTION_HOME=/home/xinyi/nvbit_release/tools/detect_fp_exceptions
export PRELOAD_FLAG="LD_PRELOAD=${FP_EXCEPTION_HOME}/detect_fp_exceptions.so"


EXEs=$(find Samples/ -type f -executable)
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
	(time timelimit -t1200 bash run.sh) >stdout.txt 2>stderr.txt
	cd -;
done
