# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：		file_util
   Description :	
   Author :			bowenxu
   Create date：		12/9/18
   Update date:		12/9/18
-------------------------------------------------
"""

import os
import shutil
from subprocess import call


def read_kth_line_of_file(file_path, k):
    '''
    read kth line from a file, k start from 0
    :param file_path:
    :param k:
    :return:
    '''
    with open(file_path) as fp:
        for i, line in enumerate(fp):
            if i == k:
                return str(line).strip()


def write_file(file_path, obj):
    write_str = ''
    if type(obj) == list:
        write_str = ('\n'.join(obj))
    elif type(obj) == str:
        write_str = obj
    else:
        write_str = obj
    file_object = open(file_path, 'wb')
    file_object.write(write_str.encode('utf-8').strip())
    file_object.close()


def insert_str_at_end(file_path, str):
    my_open = open(file_path, 'a')
    my_open.write(str)
    my_open.close()


def clean_dir(dir_path):
    import os
    if os.path.exists(dir_path):
        import shutil
        shutil.rmtree(dir_path)
    os.mkdir(dir_path)


def get_par_path(path):
    import os.path
    return os.path.abspath(os.path.join(path, os.pardir))


def cp_dir(src_dir, dst_dir, new_dir_name=None):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    call(['cp', '-r', src_dir, dst_dir])
    if new_dir_name is not None:
        src_dir_name = src_dir.split(os.sep)[-1]
        src_cp_dir = os.path.join(dst_dir, src_dir_name)
        new_dir = os.path.join(dst_dir, new_dir_name)
        os.rename(src_cp_dir, new_dir)


def delete_dir(source):
    call(['rm', '-rf', source])


def cp_file(source, target):
    call(['cp', source, target])


def write_str2file(w_str, file_path):
    fdir = os.sep.join(file_path.split(os.sep)[0:-1])
    if not os.path.exists(fdir):
        os.makedirs(fdir)
    with open(file_path, 'w') as the_file:
        the_file.write(str(w_str))


def write_byte2file(file_path, w_byte):
    with open(file_path, 'wb') as the_file:
        the_file.write(w_byte)


def write_list2file(file_path, w_list):
    if os.path.exists(file_path):
        os.remove(file_path)
    with open(file_path, "a+") as f:
        for item in w_list:
            f.write(str(item) + "\n")


def read_file_to_str(file_path):
    with open(file_path, 'r') as myfile:
        data = myfile.read()
    return data


def read_file_into_line_list(file_path, if_strip=False):
    if not os.path.exists(file_path):
        print("File {} not exists!".format(file_path))
        return None
    with open(file_path) as f:
        content = f.readlines()
    if if_strip:
        content = [x.strip() for x in content]
    else:
        content = [x for x in content]
    return content


def list_files(dir):
    import os
    dir_list = [dir]
    file_list = []
    while len(dir_list) != 0:
        cur_dir = dir_list[0]
        for f in os.listdir(cur_dir):
            if os.path.isdir(cur_dir + os.sep + f):
                dir_list.append(cur_dir + os.sep + f)
            elif os.path.isfile(cur_dir + os.sep + f):
                file_list.append(cur_dir + os.sep + f)
        dir_list.pop(0)
    return file_list


def move_files(src, dst):
    shutil.move(src, dst)


def remove_file(file_path):
    os.remove(file_path)


def clear_folder(dir_path):
    for item in os.listdir(dir_path):
        itemsrc = os.path.join(dir_path, item)
        shutil.rmtree(itemsrc)


def copy_file(fpath, dst):
    from shutil import copyfile
    try:
        copyfile(fpath, dst)
    except Exception as e:
        import subprocess
        cmd = "cp -f {} {}".format(fpath, dst)
        subprocess.call(cmd, shell=True)


def create_dir_for_fpath(fpath, remove_if_exist):
    from pathlib import Path
    dir = Path(fpath).parent
    if os.path.exists(dir) and not remove_if_exist:
        print("{} exists!".format(dir))
        exit(0)
    if os.path.exists(dir) and remove_if_exist:
        remove_dir(dir)
    os.makedirs(dir, mode=0o777)


def remove_dir(dir_path):
    import shutil
    try:
        shutil.rmtree(dir_path)
    except Exception as e:
        import subprocess
        cmd = "rm -rf {}".format(dir_path)
        subprocess.call(cmd, shell=True)


if __name__ == '__main__':
    create_dir_for_fpath("/data/bowen/data/post2vec/data/relPred/tagcnn/02-26-19_05-53-dsdfs59/tagcnn_all_qvec_dict.pkl", True)
