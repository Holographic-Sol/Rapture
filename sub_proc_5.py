import os
import sys
import os.path
import shutil
import subprocess

cfg_f = './config.txt'
data_file = './tmp/sub_proc_data_5.tmp'

src_path = ''
dest_path = ''
src_bool = False
dest_bool = False

debug_enabled = False
output_verbosity = 1
compare_bool = None

# Set Counters For Output Summary
cp0_count = 0
cp0_fail_count = 0
cp1_count = 0
cp1_fail_count = 0

if os.path.exists(data_file):
    with open(data_file, 'r') as fo:
        for line in fo:
            line = line.strip()
            if line is '0':
                compare_bool = False
            elif line is '1':
                compare_bool = True
    fo.close()
    print('-- compare_bool:', compare_bool)

if os.path.exists(cfg_f) and compare_bool != None:
    with open(cfg_f, 'r') as fo:
        for line in fo:
            line = line.strip()
            if line.startswith('SOURCE 5: '):
                line = line.replace('SOURCE 5: ', '')
                if os.path.exists(line):
                    print('config source path exists:', line)
                    src_path = line
                    src_bool = True
                elif not os.path.exists(line):
                    print('config source path does not exist', line)
                    src_bool = False
            if line.startswith('DESTINATION 5: '):
                line = line.replace('DESTINATION 5: ', '')
                if os.path.exists(line):
                     print('config destination path exists:', line)
                     dest_bool = True
                     dest_path = line
                elif not os.path.exists(line):
                     print('config destination path does not exist', line)
                     dest_bool = False

if compare_bool != None and src_bool is True and dest_bool is True and os.path.exists(src_path) and os.path.exists(dest_path):
    for dirname, subdirlist, filelist in os.walk(src_path):
        for fname in filelist:
            fullpath = os.path.join(dirname, fname)
            t_path = fullpath.replace(src_path, '')
            t_path = dest_path + t_path
            if not fullpath.endswith('.ini'):

                # Mode 0: Write Missing Files Only
                if not os.path.exists(t_path):
                    change_var = True
                    try:
                        shutil.copy2(fullpath, t_path)
                    except Exception as e:
                        if debug_enabled is True:
                            print('-- exception:', str(e).strip().encode('utf8'))
                        try:
                            os.makedirs(os.path.dirname(t_path))
                            shutil.copy2(fullpath, t_path)
                        except Exception as e:
                            if debug_enabled is True:
                                print('-- exception:', str(e).strip().encode('utf8'))

                    # Mode 0: Check File
                    if os.path.exists(t_path) and os.path.exists(fullpath):
                        siz_src = str(os.path.getsize(fullpath))
                        siz_dest = str(os.path.getsize(t_path))
                        if siz_src == siz_dest:
                            if output_verbosity is 0:
                                output_str = str('copied new: ' + t_path).strip().encode('utf8')
                                print(output_str)
                            elif output_verbosity is 1:
                                output_str = str('copied new: (' + siz_dest + '/' + siz_src + ' bytes) ' + t_path).strip().encode('utf8')
                                print(output_str)
                            cp0_count += 1
                        elif siz_src != siz_dest:
                            output_str = str('failed to copy new (failed bytes check, possible false negative as file exists): (' + siz_dest + '/' + siz_src + ' bytes) ' + t_path).strip().encode('utf8')
                            print(output_str)
                            cp0_fail_count += 1
                    elif not os.path.exists(t_path):
                        output_str = str('failed to copy new (file does no exist in destination): ' + t_path).strip().encode('utf8')
                        print(output_str)
                        cp0_fail_count += 1

                # Mode 1: Write Missing & Write Predicated Upon Time Stamp Comparison Results
                elif os.path.exists(t_path):
                    if compare_bool is True:
                        ma = os.path.getmtime(fullpath)
                        mb = os.path.getmtime(t_path)
                        if mb < ma:
                            change_var = True
                            try:
                                shutil.copy2(fullpath, t_path)
                            except Exception as e:
                                if debug_enabled is True:
                                    print('-- exception:', str(e).strip().encode('utf8'))
                                try:
                                    os.makedirs(os.path.dirname(t_path))
                                    shutil.copy2(fullpath, t_path)
                                except Exception as e:
                                    if debug_enabled is True:
                                        print('-- exception:', str(e).strip().encode('utf8'))
                                    output_str = str('error: ' + t_path).strip().encode('utf8')
                                    print(output_str)

                            # Mode 1: Check File
                            if os.path.exists(t_path) and os.path.exists(fullpath):
                                mb = os.path.getmtime(t_path)
                                ma_str = str(ma)
                                mb_str = str(mb)
                                siz_src = str(os.path.getsize(fullpath))
                                siz_dest = str(os.path.getsize(t_path))
                                if mb >= ma and siz_src == siz_dest:
                                    if output_verbosity is 0:
                                        output_str = str('updated new: ' + t_path).strip().encode('utf8')
                                        print(output_str)
                                    elif output_verbosity is 1:
                                        output_str = str('updated new: (' + siz_dest + '/' + siz_src + ' bytes) ' + t_path).strip().encode('utf8')
                                        print(output_str)
                                    cp1_count += 1
                                elif mb < ma or siz_src != siz_dest:
                                    if siz_src != siz_dest:
                                        output_str = str('failed to copy new (failed bytes check, possible false negative as file exists): (' + siz_dest + '/' + siz_src + ' bytes) ' + t_path).strip().encode('utf8')
                                        print(output_str)
                                        cp1_fail_count += 1
                                    elif mb < ma:
                                        output_str = str('failed to copy new (failed timestamp check): (Source: ' + ma_str + ' Destination:' + mb_str + ') ' + t_path).strip().encode('utf8')
                                        print(output_str)
                                        cp1_fail_count += 1
                            elif not os.path.exists(t_path):
                                output_str = str('failed to update file (file does no exist in destination): ' + t_path).strip().encode('utf8')
                                print(output_str)
                                cp1_fail_count += 1

# Output Summary
cp0_count_str = str(cp0_count)
cp0_fail_count_str = str(cp0_fail_count)
cp1_count_str = str(cp1_count)
cp1_fail_count_str = str(cp1_fail_count)
output_sum =  str('copied new: (' + cp0_count_str + ') | failed to copy new: (' + cp0_fail_count_str + ') | updated: (' + cp1_count_str + ')  | failed to update: (' + cp1_fail_count_str + ')').strip()
print('-- ThreadClass5: ' + output_sum)
