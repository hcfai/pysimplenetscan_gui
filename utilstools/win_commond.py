from subprocess import check_output, run
from os import mkdir

from functools import wraps
from time import time
def timer_cont(org_func):
    @wraps(org_func)
    def wrapper(*args, **kwargs):
        t1 = time()
        resulat = org_func(*args, **kwargs)
        t2 = time() - t1
        print(f"{org_func.__name__} ran in :{t2} sec.")
        return resulat
    return wrapper

def cmd_pysave(commnad: str, path: str='temp') -> str:
    if not __mkdir(path):
        return 
    filename = commnad.split()[0].strip() + '.txt'
    try:
        proc = check_output(commnad).decode('utf-8')
    except FileNotFoundError:
        print('[WARN] Command Failed')
        return
    else:
        print('[INFO] Commnad Run Sucessed')
        with open(f'{path}/{filename}', 'w') as file:
            file.write(proc)
        return filename

def cmd_winsave(commnad: str, path: str='temp', shell=True, *args, **kwargs) -> str:
    if not __mkdir(path):
        return 
    filename = commnad.split()[0].strip()
    try:
        run(f'{commnad} > {path}/{filename}.txt', shell=shell, *args, **kwargs)
    except:
        print('[WARN] Command Failed')
        return
    else:
        print('[INFO] Commnad Run Sucessed')
        return filename

def __mkdir(path: str) -> bool:
    try:
        mkdir(path)
    except FileExistsError:
        return True
    except OSError:
        print("[WARN] Can't access file(ppl don't have promssion)")
        return False
    else:
        return True

def cleanup(filename: str=None, path: str='temp'):
    if filename == None: return
    with open(f'{path}/{filename}.txt', 'w') as file:
        file.write('')
    

@timer_cont
def sort_win_ipconfig(filename: str='ipconfig', path: str='temp') -> list:
    import re
    re_name, re_ip, re_subnet, re_mac = re.compile(r'Description'), re.compile(r'IPv4 Address'), re.compile(r'Subnet Mask'), re.compile(r'Physical Address')
    nic_list = []
    nic_dict = {}
    with open(f'{path}/{filename}.txt', 'r') as file:
        lines = file.readlines()
    for line in lines[5:]: 
        line = line.rstrip()
        if len(line) < 1: continue
        if not line.startswith(' '):
            if len(nic_dict) > 0: nic_list.append(nic_dict)
            nic_dict = {}
            nic_dict['interface'] = line.replace(':' ,'')
            continue
        if bool(re_name.search(line)): 
            nic_dict['description'] = line.split(' :')[1].strip()
            continue
        if bool(re_ip.search(line)): 
            nic_dict['ipv4_addr'] = line.split(' :')[1].strip().replace('(Preferred)', '')
            continue
        if bool(re_subnet.search(line)): 
            nic_dict['subnet_mask'] = line.split(' :')[1].strip()
            continue
        if bool(re_mac.search(line)): 
            nic_dict['mac'] = line.split(' :')[1].strip().lower()
            continue
    print('Done')
    nic_list.append(nic_dict)
    return nic_list


def sort_win_arp(filename: str='arp', path: str='temp') -> dict:
    import re
    ip2mac_dict = dict()
    re_macpattern = re.compile(r'(([0-9a-fA-F]){2}[-:]){5}([0-9a-fA-F]){2}')
    re_ippattern = re.compile(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}")
    re_mactpye = re.compile(r'dynamic')
    with open(f'{path}/{filename}.txt', 'r') as file:
        lines = file.readlines()
    for line in lines:
        if bool(re_mactpye.search(line)): 
            ip = re_ippattern.search(line).group()
            if bool(re_macpattern.search(line)): mac = re_macpattern.search(line).group()
            else: mac = None
            ip2mac_dict[ip] = mac 
    return ip2mac_dict

if __name__ == '__main__':

    filename = cmd_winsave('ipconfig /all')
    nic_list = sort_win_ipconfig(filename)
    for nic in nic_list:
        print(nic)
    print('***')
    for _ in range(len(nic_list)):
        nic = nic_list.pop(0)
        if 'ipv4_addr' in nic: print(nic)
    
    input()