#!/usr/bin/env python
# coding: utf-8

# In[2]:


from pathlib import Path
def make_dirs_to_file(path):
    path_to_dir=path.parent
    if not path_to_dir.exists():
        path_to_dir.mkdir(parents=True)
        
def write_to_file(text,path,rewrite=False):
    make_dirs_to_file(path)
    if not rewrite and path.exists():
        print("file {} exists".format(path.name))
        return
    with path.open(mode='w') as f:
        f.write(text)
        print("file {} is written".format(path.name))


# In[3]:


def try_to_open_file(file_name,mode="r"):
    try:
        file=open(file_name,mode)
    except FileNotFoundError:
        print("No such file or directory %s" %(file_name))
        return 0
    except PermissionError:
        print("No permition to the file {}".format(file_name))
        return 0
    except Exception:
        mode_name=""
        if mode=="r":
            mode_name="read"
        elif mode=="w":
            mode_name="write"
        else:
            mode_name="open"
        print("File {} cann't be {}".format(file_name,mode_name))
        return 0
    return file
    
def input_numbers(*,n_type=float,str_count:int=0,end_symbol="",n_count:int=0,sep=" ",
                  first_is_str_count:bool=False,file_name=""):
    """ Reads numeric data from keybord input or file
    returns list of numbers if only 1 symbol in string
        elif  list of tuples of numbers,tuple is one string
        -1 if can't be read
    Parametrs:
    n_type - type of numbers float or int
    str_count - number of strings to read, inf if not defined
    end_symbol- string read to (not including)
    n_count - number of numbers in one string, not define, if we doesn't know
    sep - separator between values
    first_is_str_count - is first string an str_count parametr
    file_name - name of file to read if it defined, if not read from input
    """
    result=[]
    my_input=input
    if not (n_type is int or n_type is float):
        print("Types of numbers can be only float or int")
        return -1
    if file_name:
        file=try_to_open_file(file_name,'r')
        if not file: return -1
        my_input=file.readline
    if first_is_str_count:
        try:
            str_count= int(my_input())
        except ValueError:
            print("In first string must be a natural number of strings to read")
            return -1
        
    str_number=1
    string= my_input().rstrip('\n')
    while string and string!=end_symbol:
        numbers=string.split(sep)
        n_len=len(numbers)
        if n_count and n_count!=n_len:
            print("In string must be %d values separated with '%s'" % (n_count,sep))
            return -1
        try:
            numbers= tuple(map(n_type,numbers)) if n_len>1 else n_type(*numbers)
        except ValueError:
            print("Numbers must be %s type separated with '%s'" %(str(n_type),sep))
            return -1
        result.append(numbers)
        str_number+=1
        if str_count and str_number>str_count: break
        string= my_input().rstrip('\n')
    if file_name: file.close()
    return result


# In[4]:


def write_numbers_to_file(numbers,file_name:str,*,n_type=float,str_count:int=0,end_symbol="",
                          n_count:int=0,sep_w=" ",sep_r=" ",
                          first_is_str_count:bool=False, create_new_file=False):
    """ Writes numeric data to file
    returns file name or -1 if can't be written
    Parametrs:
    numbers- list of numbers or strings with numbers or list of lists of numbers
    str_count - number of strings to write, inf if not defined
    end_symbol- last string
    n_count - number of numbers in one string, not define, if we doesn't know
    sep - separator between values
    first_is_str_count - is first string an str_count parametr
    file_name - name of file to write
    create_new_file - new file will be created if the file doesn't exist
    """
    if create_new_file:
        file=open(file_name,"w")
    else:
        try:
            file = open(file_name,'r')
        except FileNotFoundError:
            print("File does not exist, do you want to ceate a new one?")
            answer=input("print yes or no \n")
            if answer =='yes':
                file=open(file_name,"w")
            elif answer=='no':
                print("The file %s doesn't exist" %(file_name))
                return -1
            else:
                print("Wrong answer,bye!")
                return -1
        file.close()
        file=open(file_name,"w")
    if first_is_str_count:
        if str_count:
            file.write(str(str_count)+"\n")
        else:
            file.write(str(len(numbers))+"\n")
    str_number=1
    for string in numbers:
        if str_count and str_number>str_count: break
        type_s=type(string)
        if type_s is int or type_s is float:
            file.write(str(string)+"\n")
            continue
        elif type_s is str or type_s is list:
            if n_count and len(string)>n_count:
                string=string[:n_count]
            if type_s is str :
                string.replace(sep_r,sep_w)
            else:
                string=sep_w.join(map(str,string))
        elif type_s is tuple:
            string=sep_w.join(map(str,string))
        else:
            print("Wrong data" )
            return -1
        #print(string)
        file.write(string+"\n")
        str_count+=1
    if end_symbol:
        file.write(end_symbol)
    file.close()
    return file_name


# In[5]:


from contextlib import redirect_stdout
import io
#from python_shell import Shell
import os
import sys

def wrong_test(test_number,answer,n_type=int, str_count:int=0, end_symbol="",n_count:int=0,
               sep=" ", first_is_str_count:bool=False ,file_name='test.txt'):
    print("Wrong test {}:".format(test_number))
    f = io.StringIO()
    with redirect_stdout(f):
        res=input_numbers(n_type=n_type,str_count=str_count,end_symbol=end_symbol,n_count=n_count,
                         sep=sep,first_is_str_count=first_is_str_count,file_name=file_name)
    s=f.getvalue()
    print("OK" if s==answer and res==-1 else "Fail\nwrite answer:\n"+answer +s,res,"\n")
    return test_number+1

def right_test(test_number,answer,n_type=int, str_count:int=0, end_symbol="",n_count:int=0,
               sep=" ", first_is_str_count:bool=False ,file_name='test.txt'):
    print("Right test {}:".format(test_number))
    res=input_numbers(n_type=n_type,str_count=str_count,end_symbol=end_symbol,n_count=n_count,
                      sep=sep,first_is_str_count=first_is_str_count,file_name=file_name)
    print("OK\n" if res==answer else "Fail\nwrite answer:\n",answer,"\nresult:\n",res,"\n")
    return test_number+1
    
    
def test_input_numbers():
    
    test_count=0
    
    print("Test file_name")
    answer="No such file or directory {}\n".format("rer")
    test_count=wrong_test(test_count,answer,file_name="rer")
    
    blocked_file="blocked_file.txt"
    f=open(blocked_file,"w")
    f.close()
    os.system("chmod u-r {}".format(blocked_file))
    test_count=wrong_test(test_count,"No permition to the file {}\n".format(blocked_file),file_name="blocked_file.txt")
    os.system("chmod u+r blocked_file.txt")
    os.remove("blocked_file.txt")
    
    A=[5,5,5,5,5,5,5,5]
    file_name='test.txt'
    write_numbers_to_file(A,file_name)
    
    print("Test n_type")
    test_count=wrong_test(test_count,"Types of numbers can be only float or int\n",n_type=str)
    test_count=right_test(test_count,A,file_name='test.txt')
    A=list(map(float,A))
    write_numbers_to_file(A,file_name)
    test_count=right_test(test_count,A,n_type=float,file_name='test.txt')
    
    print("Test first is str_count")
    write_numbers_to_file("q123",'test.txt')
    answer="In first string must be a natural number of strings to read\n"
    test_count=wrong_test(test_count,answer,first_is_str_count=True)
    write_numbers_to_file("51234567",'test.txt')
    test_count=right_test(test_count,[1,2,3,4,5],first_is_str_count=True)
    
    print("Test n_count")
    n_count=5
    sep=' '
    a=[1,2,3,4,5,6]
    A=[a,a,a]
    write_numbers_to_file(A,file_name,n_count=4)
    answer="In string must be %d values separated with '%s'\n" % (n_count,sep)
    test_count=wrong_test(test_count,answer,n_count=n_count)
    write_numbers_to_file(A,file_name,n_count=5)
    a.pop()
    A=[tuple(a) for i in range(3)]
    test_count=right_test(test_count,A,n_count=n_count)
    
    print("Test numbers type")
    a=(1.1,2.2,3.3)
    A=[a,a,a]
    write_numbers_to_file(A,file_name)
    answer="Numbers must be %s type separated with '%s'\n" %(str(int),' ')
    test_count=wrong_test(test_count,answer,n_type=int)
    test_count=right_test(test_count,A,n_type=float)
    
    print("Test separator")
    a=(0,1,2,3,4)
    A=[a,a,a]
    write_numbers_to_file(A,file_name,sep_w=',')
    answer="Numbers must be %s type separated with '%s'\n" %(str(int),' ')
    test_count=wrong_test(test_count,answer,n_type=int)
    test_count=right_test(test_count,A,sep=",")
    
    print("Test str_count and end symbol")
    write_numbers_to_file(A,file_name)
    test_count=right_test(test_count,[a,a],str_count=2)
    write_numbers_to_file(A,file_name,end_symbol='0')
    test_count=right_test(test_count,[a,a,a],end_symbol='0')
    A=[i+1 for i in range(6)]
    write_numbers_to_file(A,file_name)
    test_count=right_test(test_count,[1,2],str_count=4,end_symbol='3')
    
    print("Test all")
    A="3\n1.1,1.2,1.3\n2.2,2.3,2.4\n3.3,3.4,3.5\n4.4,4.5,4.6\n#\n5.5,5.6,5.7"
    f=open(file_name,"w+")
    f.write(A)
    f.close()
    A=[(1.1, 1.2, 1.3),(2.2, 2.3, 2.4),(3.3, 3.4,3.5)]
    test_count=right_test(test_count,A,n_type=float,str_count=4,end_symbol='#',
                          n_count=3,sep=",",first_is_str_count=True,file_name=file_name)
    os.remove(file_name)
#test_input_numbers()


# In[6]:


#input_numbers(n_type=float,str_count=4,end_symbol='#',n_count=3,sep=",",first_is_str_count=True)

