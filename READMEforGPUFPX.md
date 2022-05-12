### File introduction
##### `run.sh`
This file is the script to run all the codes in the `./Samples`. There are several cases:
1. Run with GPU-FPX
We need to change  `GPUFPX_OBJ` as the shared object of GPU-FPX
2. Run with BINFPE
We need to change  `BINFPE_OBJ` as the shared object of GPU-FPX
3. Other runs like `check_wo_channel`, `wo_check_wo_channel`
Just modify the shared object's path

##### 