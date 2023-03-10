from ipaddress import IPv4Address
from types import GeneratorType

## IP
def ipv4_rangecheck(startip: str, endip: str):
    try: start_ipv4_addr = IPv4Address(startip)
    except Exception as e: 
        return f'[ERRO] Incorrect format of Start IP: {e}'

    try: end_ipv4_addr = IPv4Address(endip)
    except Exception as e: 
        return f'[ERRO] Incorrect format of End IP: {e}'

    if start_ipv4_addr.is_private and end_ipv4_addr.is_private:
        if ipv4_conpare(start_ipv4_addr, end_ipv4_addr):
            return gen_ipv4range(start_ipv4_addr, end_ipv4_addr)
        else:
            return '[ERRO] Start IP is Smaller then End IP'
    else:
        return '[ERRO] Start or End IP is NOT Private IP'

def gen_ipv4range(startip: IPv4Address, endip: IPv4Address):
    while startip != endip:
        yield startip
        startip = ipv4_addone(startip)
        if not startip.is_private: break
    if startip.is_private: yield startip

def ipv4_addone(ip: IPv4Address) -> IPv4Address:
    ip_bytes = bytearray(ip.packed)

    if ip_bytes[3] == 255:
        ip_bytes[3] = 0
        if ip_bytes[2] == 255:
            ip_bytes[2] = 0
            if ip_bytes[1] == 255:
                ip_bytes[1] = 0
                ip_bytes[0] += 1
            else: ip_bytes[1] += 1
        else: ip_bytes[2] += 1
    else: ip_bytes[3] += 1

    ip_bytes = bytes(ip_bytes)
    new_ip = IPv4Address(ip_bytes)
    return new_ip

def ipv4_devone(ip: IPv4Address) -> IPv4Address:
    ip_bytes = bytearray(ip.packed)

    if ip_bytes[3] == 0:
        ip_bytes[3] = 255
        if ip_bytes[2] == 0:
            ip_bytes[2] = 255
            if ip_bytes[1] == 0:
                ip_bytes[1] = 255
                ip_bytes[0] -= 1
            else: ip_bytes[1] -= 1
        else: ip_bytes[2] -= 1
    else: ip_bytes[3] -= 1

    ip_bytes = bytes(ip_bytes)
    new_ip = IPv4Address(ip_bytes)
    return new_ip

def ipv4_conpare(self: IPv4Address, other: IPv4Address) -> bool:
    self = self.packed
    other = other.packed
    if self[0] > other[0]: return False
    elif self[1] > other[1]: return False
    elif self[2] > other[2]: return False
    elif self[3] > other[3]: return False
    else: return True

if __name__ == '__main__':
    start_ip = IPv4Address('192.168.255.200')
    end_ip = IPv4Address('192.168.1.210')
    id_iprange = gen_ipv4range(startip=start_ip, endip=end_ip)
    isinstance(id_iprange, GeneratorType)