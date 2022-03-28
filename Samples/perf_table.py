import subprocess
import os
import pandas as pd
import glob
import matplotlib.pyplot as plt


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
    t_s = "N/A"
    for line in infos:
        count = count +1
        if("real" in line):
            assert("user" in infos[count])
            assert("sys" in infos[count+1])
            t = line.split("	")[1]
            t_s = to_time_s(t)
    return t_s

def slow(ori_file, check_file,outfile):
    with open(outfile) as f:
        lines_list = f.readlines()
        count = 0
        slowdown = "N/A"
        for line in lines_list:
            count = count + 1
            if("FPChecker Report" in line):
                with open(check_file) as time_f:
                    # try:
                    #     infos = time_f.readlines()
                    # except:
                    #     infos = "N/A"
                    # if(infos == "N/A"):
                    #     t_s = "N/A"
                    # else:
                    #     t_s = time_info(infos)
                    #e.append(t_s)
                    infos = time_f.readlines()
                    t_s = time_info(infos)
                with open(ori_file) as timeori_f:
                    # try:
                    #     infos_ori = timeori_f.readlines()
                    # except:
                    #     infos_ori = "N/A"
                    # if(infos_ori == "N/A"):
                    #     t_s_ori = "N/A"
                    # else:
                    #     t_s_ori = time_info(infos)
                    #e.append(t_s_ori) 
                    infos_ori = timeori_f.readlines()
                    t_s_ori = time_info(infos_ori)

                if(t_s == "N/A" or t_s_ori=="N/A"):
                    slowdown = "N/A"
                else:
                    print("true")
                    slowdown = t_s/t_s_ori
                    return round(slowdown,3)
            else:
                slowdown = "N/A"
    #            exist = 1
    #            e = read_report(lines_list[count+1:],[dir])
    #            break
    # print("exist is: ", exist)
    #if(exist != 0):
    
    #e.append(slowdown)
    return slowdown


           


#df = pd.DataFrame(columns = ["program","fp64_NAN", "fp64_INF", "fp64_SUB","fp64_DIV0","fp32_NAN", "fp32_INF", "fp32_SUB","fp32_DIV0","kernel","FP instructions","check_time","ori_time","slowdown"])
df = pd.DataFrame(columns = ["program","soap_slowdown","GPU-FPX_slowdown"])
#Tail=[".perf",".soap.perf"]
def create_table(dirs):
    for dir in dirs:
        print("process application: ", dir)
        with cd(dir):
            #program = dir.split("/")[-1]
            program = dir
        # run_command(["cd ",dir])
        # print(run_command([comd]))
            # for x in glob.glob("./*"):
            #     print(x)
            #for ta in Tail:
            #outfile = "stdout"+ta+".txt"
            #errfile = "stderr" + ta +".txt"
            #ori_errfile = "stderr_ori"+ta+".txt"
            #with open(outfile) as f:
            #    exist = 0
            #    lines_list = f.readlines()
            #    count = 0
            #    for line in lines_list:
            #        # print(line)
            #        count = count + 1
            #        if("FPChecker Report" in line):
            #            exist = 1
            #            e = read_report(lines_list[count+1:],[dir])
            #            break
            # print("exist is: ", exist)
            #if(exist != 0):
            e = [program]
            soap_slow = slow("stderr_ori.soap.perf.txt","stderr.soap.perf.txt","stdout.soap.perf.txt")
            gpufpx_slow = slow("stderr_ori.perf.txt","stderr.perf.txt","stdout.perf.txt")
            #print(soap_slow)
            #print(gpufpx_slow)
            if(soap_slow!="N/A" or gpufpx_slow !="N/A"):
                e.append(soap_slow)
                e.append(gpufpx_slow)
                df.loc[len(df)] = e
              #  else:
               #     e = [dir,"N/A", "N/A", "N/A", "N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A"]
                #    df.loc[len(df)] = e
        #e = [" ", " ", " ", " ", " "," "," "," "," "," "," "," "," ", " "]
        #df.loc[len(df)] = e
        cd("..")

    print(df)
    df.to_csv("performance.csv", index=False)
                #raise Exception("cannot go back to last directory")
    programs = df["program"]  
    soap_sd = df ["soap_slowdown"]
    gfpx_sd = df["GPU-FPX_slowdown"]
    # fig, ax = plt.subplots(figsize =(16, 9))
 
    # # Horizontal Bar Plot
    # ax.barh(programs, gfpx_sd)
    
    # # Remove axes splines
    # for s in ['top', 'bottom', 'left', 'right']:
    #     ax.spines[s].set_visible(False)
    
    # # Remove x, y Ticks
    # ax.xaxis.set_ticks_position('none')
    # ax.yaxis.set_ticks_position('none')
    
    # # Add padding between axes and labels
    # ax.xaxis.set_tick_params(pad = 5)
    # ax.yaxis.set_tick_params(pad = 10)
    
    # # Add x, y gridlines
    # ax.grid(b = True, color ='grey',
    #         linestyle ='-.', linewidth = 0.5,
    #         alpha = 0.2)
    
    # # Show top values
    # ax.invert_yaxis()
    
    # # Add annotation to bars
    # for i in ax.patches:
    #     plt.text(i.get_width()+0.2, i.get_y()+0.5,
    #             str(round((i.get_width()), 2)),
    #             fontsize = 10, fontweight ='bold',
    #             color ='grey')
    
    # # Add Plot Title
    # ax.set_title('Performance compared with soap paper',
    #             loc ='left', )
    
    
    # # Show Plot
    # plt.savfig(performance)

def entry(start_dir):
    dir_list = []
    for f in glob.iglob(start_dir+'/**/stdout.perf.txt',recursive=True):
        d = '/'.join(f.split('/')[:-1])
        dir_list.append(d)
    create_table(dir_list)    
        

if __name__ == "__main__":
    entry("./")
