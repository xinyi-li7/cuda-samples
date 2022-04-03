import subprocess
import os
import pandas as pd
import glob

def setup_module(module):
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    os.chdir(THIS_DIR)

def teardown_module(module):
    cmd = ["make clean"]
    cmdOutput = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)

def run_command(cmd):
    try:
        cmdOutput = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.output)
        exit()
    return cmdOutput

from contextlib import contextmanager
import os

@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)
    
def read_report(report, data_list):
    assert(len(report) >= 10)
    for line in report:
        #print(line)
        if("NaN found" in line or "INF found" in line):
            line_set = line.split("              ")
        elif("underflow (subnormal)" in line):
            line_set = line.split("  ")
        elif("Total Division by 0" in line):
            line_set = line.split("          ")
        elif("Kernels" in line):
            line_set = line.split("      ")
        elif("FP Inst. count" in line):
            line_set = line.split("  ")
        elif("Inst. count" in line):
            line_set = line.split("  ")
        else:
            line_set = []
        #print(line_set)
        if(len(line_set)==2):
            num = line_set[1].split("\n")[0]
            data_list.append(num)
    #print(report)
    print(len(data_list))
    #assert(len(data_list) == 9)
    return data_list

def to_time_s(t):
    time_list = t.split('m')
    return float(time_list[0])*60+float(time_list[1].split('s')[0])

def time_info(infos):
    count = 0
    for line in infos:
        count = count +1
        if("real" in line):
            assert("user" in infos[count])
            assert("sys" in infos[count+1])
            t = line.split("	")[1]
            t_s = to_time_s(t)
    return t_s

def slow_time(errfile,ori_errfile):
    with open(errfile) as time_f:
        infos = time_f.readlines()
        t_s = time_info(infos)
    with open(ori_errfile) as timeori_f:
        infos_ori = timeori_f.readlines()
        t_s_ori = time_info(infos_ori)
    slowdown = t_s/t_s_ori
    return round(slowdown,3)


df = pd.DataFrame(columns = ["program","fp64_NAN", "fp64_INF", "fp64_SUB","fp64_DIV0","fp32_NAN", "fp32_INF", "fp32_SUB","fp32_DIV0","kernel","FP instructions","Num of excps","gpu-fpx slowdown","soap slowdown"])
#df = pd.DataFrame(columns = ["program","fp64_NAN", "fp64_INF", "fp64_SUB","fp64_DIV0","fp32_NAN", "fp32_INF", "fp32_SUB","fp32_DIV0","kernel","check_time"])
#Tail=[".perf",".soap.perf"]
def create_table(dirs):
    for dir in dirs:
        exist = 0
        exist2 = 0
        print("process application: ", dir)
        with cd(dir):
        # run_command(["cd ",dir])
        # print(run_command([comd]))
            # for x in glob.glob("./*"):
            #     print(x)
        
            outfile_gp = "stdout.perf.txt"
            errfile_gp = "stderr.perf.txt"
            ori_errfile_gp = "stderr_ori.perf.txt"
            outfile_soap = "stdout.soap.perf.txt"
            errfile_soap = "stderr.soap.perf.txt"
            ori_errfile_soap = "stderr_ori.soap.perf.txt"
            e = []
            with open(outfile_gp) as f:
                exist = 0
                lines_list = f.readlines()
                count = 0
                for line in lines_list:
                    # print(line)
                    count = count + 1
                    if("FPChecker Report" in line):
                        exist = 1
                        e = read_report(lines_list[count+1:],[dir])
                        break
            with open(outfile_soap) as f:
                exist2 = 0
                lines_list = f.readlines()
                count = 0
                for line in lines_list:
                    # print(line)
                    count = count + 1
                    if("FPChecker Report" in line):
                        exist2 = 1
                        if(exist == 0):
                            e = [dir,"N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A"]
                        break
            excps = 0;
            for in in range(1, len(e)-2)
               excps+= e[i]
            e.append(excps)
            if(exist != 0 or exist2!=0):
                slowdown_gp = slow_time(errfile_gp,ori_errfile_gp)
                slowdown_soap = slow_time(errfile_soap,ori_errfile_soap)
                e.append(slowdown_gp)
                e.append(slowdown_soap)
                #if(ta == ".soap.perf"):
                #    print("true")
                #    e.insert(4, "N/A")
                #    e.insert(8, "N/A")
                df.loc[len(df)] = e
            #  else:
            #     e = [dir,"N/A", "N/A", "N/A", "N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A"]
            #    df.loc[len(df)] = e
        #e = [" ", " ", " ", " ", " "," "," "," "," "," "," "," "," ", " "]
        #df.loc[len(df)] = e
        cd("..")

    print(df)
    df.to_csv("excp_perf.csv", index=False)
                #raise Exception("cannot go back to last directory")

def entry(start_dir):
    dir_list = []
    for f in glob.iglob(start_dir+'/**/stdout_ori.perf.txt',recursive=True):
        d = '/'.join(f.split('/')[:-1])
        dir_list.append(d)
    create_table(dir_list)    
        

if __name__ == "__main__":
    entry("./")
