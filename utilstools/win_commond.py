from subprocess import run,PIPE
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

def cmd_winsave(commnad: str, path: str='temp') -> str:
    if not __mkdir(path): return None
    c = commnad.split()
    filename = c[0]
    try:
        # run([commnad, ">", f"{path}/{filename}.txt"])
        with open(f"{path}/{filename}.txt", "w") as f:
            run(c, stdout=f, text=True)
        print(f"{filename} saved, will clear when progreame close")
    except:
        print('[WARN] Command Failed')
        return None
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

def check_file(filename: str,  path: str='temp') -> bool:
    try: 
        open(f"{path}/{filename}.txt", "r").read()
    except FileNotFoundError:
        return True
    except UnicodeDecodeError:
        return False
    return True

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

    
    l = sort_win_arp(cmd_winsave("arp -a"))
    print(l)
    # a = check_file("mac-vendors")
    # run(["ipconfig", "/all"])
