export GPUFPX_OBJ=/home/xinyi/nvbit-exceptions/tools/detect_fp_exceptions/detect_fp_exceptions.so
export BINFPE_OBJ=/home/xinyi/nvbit-exceptions/tools/detect_fp_exceptions_ori/detect_fp_exceptions.so


export GPUFPX_PRELOAD_FLAG="LD_PRELOAD=${GPUFPX_OBJ}"
export BINFPE_PRELOAD_FLAG="LD_PRELOAD=${BINFPE_OBJ}"

EXEs=$(find Samples/ -type f -executable)
#EXEs='Samples/5_Domain_Specific/MonteCarloMultiGPU/MonteCarloMultiGPU Samples/5_Domain_Specific/FDTD3d/FDTD3d Samples/5_Domain_Specific/dxtc/dxtc Samples/4_CUDA_Libraries/cuSolverRf/cuSolverRf Samples/4_CUDA_Libraries/cuSolverSp_LinearSolver/cuSolverSp_LinearSolver Samples/4_CUDA_Libraries/cuSolverSp_LowlevelQR/cuSolverSp_LowlevelQR Samples/4_CUDA_Libraries/cuSolverDn_LinearSolver/cuSolverDn_LinearSolver Samples/4_CUDA_Libraries/cuSolverSp_LowlevelCholesky/cuSolverSp_LowlevelCholesky Samples/2_Concepts_and_Techniques/interval/interval'
for exe in ${EXEs}
do
	run=${exe##*/}
	size=${#run}
#	echo $size
#	echo ${exe::(-$size+0)}
	dir=${exe::(-$size+0)}
	cd $dir;
	echo "in ${dir}....."

	comm_plain="eval ./${run}"
	echo ${comm_plain} > run_plain.sh
	echo "run plain program"
	(time timelimit -t2000 bash run_plain.sh) >stdout.plain.txt 2>stderr.plain.txt
	
	comm_gpufpx="eval ${GPUFPX_PRELOAD_FLAG} ./${run}"
	echo ${comm_gpufpx} > run_gpufpx.sh
	echo "run gpu-fpx on program"
	(time timelimit -t2000 bash run_gpufpx.sh) >stdout.gpufpx.txt 2>stderr.gpufpx.txt

	comm_binfpe="eval ${BINFPE_PRELOAD_FLAG} ./${run}"
	echo ${comm_binfpe} > run_binfpe.sh
	echo "run binfpe on program"
	(time timelimit -t2000 bash run_binfpe.sh) >stdout.binfpe.txt 2>stderr.binfpe.txt
	#comm="eval ${PRELOAD_FLAG} ./${run}"
	#echo ${comm} > run.sh
	#comm2="eval ./${run}"
	#echo ${comm2} > run_ori.sh
	#echo "run original program"
	#(time timelimit -t2000 bash run_ori.sh) >stdout_ori.perf.txt 2>stderr_ori.perf.txt
	#echo "run checking program"
	#(time timelimit -t2000 bash run.sh) >stdout.perf.txt 2>stderr.perf.txt
	
	# comm_binfpe="eval ${BINFPE_PRELOAD_FLAG} ./${run}"
	# echo ${comm_binfpe} > run_binfpe.sh
	#comm2_soap="eval ./${run}"
	#echo ${comm2_soap} > run_ori_soap.sh
	#echo "run original soap program"
	#(time timelimit -t2000 bash run_ori_soap.sh) >stdout_ori.soap.perf.txt 2>stderr_ori.soap.perf.txt
	#echo "run checking soap program"
	#(time timelimit -t2000 bash run_soap.sh) >stdout.soap.perf.txt 2>stderr.soap.perf.txt
	cd -;
done
