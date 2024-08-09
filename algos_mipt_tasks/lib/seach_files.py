#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 100500 способов найти нужный файл
import os
from pathlib import Path
import time

def seach_exists_path(path):
    """Gets path to file
    returns path- path to parent directory wich exist
    dir_name- name of directory of file
    file_name - name of file"""
    file_name=path.name
    dir_name=path.parent.name
    while not path.exists():
        path=path.parents[0]
    return file_name,dir_name,path

def seach_dir(dir_name,start_path=Path("/usr")):
    """Recursive finds directory dir_name in start_path and subdirs using os.scandir
    gets  dir_name - name of directory
    returns list of iterators to dirs"""
    dirs_path_it=[]
    try:
        it=os.scandir(start_path)
    except PermissionError and OSError:
        return []
    for entry in it:
        try:
            if entry.is_dir():
                if dir_name in entry.name:
                    dirs_path_it.append(entry)
                else: dirs_path_it+=seach_dir(dir_name,entry)
        except PermissionError and OSError:
            continue
    return dirs_path_it

def find_file_in_dir(file_name,dir_it):
    """Recursive finds file in directory dir_it  and subdirs using os.scandir
    gets  file_name - name of file
    returns list of paths to file"""
    path_to_files=[]
    for entry in os.scandir(dir_it):
        if entry.is_file():
            if file_name.lower() in entry.name.lower():
                path_to_files.append(Path(entry))
        elif entry.is_dir():
            path_to_files+=find_file_in_dir(file_name,entry)
    return path_to_files
            
def seach_file_in_dir_rec(file_name,dir_name,start_path=Path('/usr')):
    """ NOT WORKING
    Seaches file in directory using recursive functions
    gets  file_name - name of file
    dir_name- name of directory of file -can be any parent
    (example - dir_name=c path to file - /a/b/c/d/file)
    start_path- start walk from this path
    returns list of paths to file"""
    path_to_files=[]
    for it in seach_dir(dir_name,start_path):
        path_to_files+=find_file_in_dir(file_name,it)
    return path_to_files

def seach_file_in_dir(file_name,dir_name="",start_path=Path('/')):
    """ Seaches file using os.walk in circle
    gets  file_name - name of file
    dir_name- name of directory of file -can be any parent
    (example - dir_name=c path to file - /a/b/c/d/file)
    start_path- start walk from this path
    returns list of paths to file"""
    paths_to_file=[]
    for root, dirs, files in os.walk(start_path):
        for file in files:
            if file_name.lower() in file.lower():
                if dir_name and not dir_name in root: continue
                paths_to_file.append(Path(root).joinpath(Path(file)))            
    return paths_to_file

def seach_file_in_dir2(file_name,dir_name="",start_path=Path('/')):
    """ Seaches file using 2 os.walk in circle
    gets  file_name - name of file
    dir_name- name of directory of file
    start_path- start walk from this path
    returns list of paths to file"""
    paths_to_file=[]
    for root, dirs, files in os.walk(start_path):
        for cur_dir in dirs:
            if dir_name and not dir_name in cur_dir: continue
            for dir_root,dir_dirs, dir_files in os.walk(Path(root).joinpath(Path(cur_dir))):
                for file in dir_files:
                    if file_name.lower() in file.lower():
                        paths_to_file.append(Path(dir_root).joinpath(Path(file)))            
    return paths_to_file

def test_seach_file(seach_file,file_name,dir_name,start_path):
    start_time=time.time()
    paths=seach_file(file_name,dir_name,start_path)
    end_time=time.time()
    print(end_time-start_time)
    print(*paths,sep="\n")


# In[ ]:


def start_testing_seach_files():
    s=input("Print \"yes\" to test seach files\n")
    if s!="yes":return
    path=Path("/usr/share/licenses/python/LICENSE.")
    file_name,dir_name,path=seach_exists_path(path)
    print(file_name,dir_name,path)
    test_seach_file(seach_file_in_dir,file_name,dir_name,path.parents[0])
    test_seach_file(seach_file_in_dir,file_name,dir_name,path.parents[0])
    #seach_file_in_dir(file_name,dir_name) need to test,


# In[1]:


def filter_paths_by_dir_name(paths_list,dir_name):
    """ filter paths by it's directory name"""
    f_paths_list=[]
    for path in paths_list:
        if dir_name in path.parent.name:
            f_paths_list.append(path)
    return f_paths_list

def check_open_file_to_read(path,encoding="utf-8"):
    """checks can file with path  be open to read
    gets path and encoding
    if path  not exists seachers file in its dir
    returns path to file"""
    f_paths_list=[]
    if path.exists() and path.is_file():
        paths_to_file=[path]
    else:
        f_name,dir_name,path=seach_exists_path(path)
        paths_to_file=seach_file_in_dir(f_name,dir_name,path.parent)
        f_paths_list=filter_paths_by_dir_name(paths_to_file,dir_name)
    #with path.open(mode="r", encoding="utf-8") as file:
    for new_path in f_paths_list if f_paths_list else paths_to_file :
        try:
            file=new_path.open(mode="r", encoding=encoding)
        except Exeption:
            continue
        file.close()
        return new_path

