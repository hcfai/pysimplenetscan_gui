from pythonping import ping
from mac_vendor_lookup import MacLookup, BaseMacLookup

import socket
# import subprocess
from re import compile
from ipaddress import IPv4Network, IPv4Address, IPv4Interface

MAC_PATTERN = compile(r'(([0-9a-fA-F]){2}[-:]){5}([0-9a-fA-F]){2}')

class Scanner():
    def __init__(self, guiconsole: None) -> None:
        if guiconsole != None:
            self.guiconsole = guiconsole
        self.scanning = False
        self.hostname = None
        self.active_interface = {}
        self.setting = { 
            'skipping': False,
            'showdetail': False, 
            'httpscan': False,
            'httpsscan': False,}
        self.reponded_hosts = []
        self.interfaces = []
        self.ip2mac_dict = dict()

    def add_interface(self, nic: dict):
        new_interface = {}
        new_interface['interface'] = nic['interface']
        new_interface['ipv4_addr'] = IPv4Interface((nic['ipv4_addr'],nic['subnet_mask']))
        new_interface['description'] = nic['description']
        new_interface['mac'] = nic['mac']
        self.interfaces.append(new_interface)

    def set_defualtinterface(self):
        self.hostname = socket.gethostname()
        ip = socket.gethostbyname(self.hostname)
        for interface in self.interfaces:
            if interface['ipv4_addr'].ip.exploded == ip:
                self.active_interface = interface
                netcls = self._scanrangelimiter(interface['ipv4_addr'].network.prefixlen)
                return interface['ipv4_addr'].ip.exploded, interface['description'], netcls

    def set_activeinterface(self, new_interface: str):
        pattern_ip = compile(r'---> ')
        index = pattern_ip.search(new_interface).end()
        for interface in self.interfaces:
            if interface['ipv4_addr'].with_prefixlen == new_interface[index:]:
                self.active_interface = interface
                netcls = self._scanrangelimiter(interface['ipv4_addr'].network.prefixlen)
                # print(f'Network Updated to {interface["ipv4_addr"]}')
                return interface['ipv4_addr'].ip.exploded, interface['description'], netcls

    def _scanrangelimiter(self, prefixlen):
        if prefixlen == 32:
            print('host ip')
            return 'ERROR'
        elif prefixlen >= 24:
            print('class C')
            return 'C'
        elif prefixlen >= 16:
            print('class B')
            return 'B'
        elif prefixlen >= 8:
            print('class A')
            return 'A'
        else:
            return 'ERROR'


    ## MAC Address lookup
    def get_mac(self) -> str:
        maclookup = MacLookup()
        BaseMacLookup.cache_path = "temp/mac-vendors.txt"
        for _ in range(len(self.reponded_hosts)):
            host = self.reponded_hosts.pop(0)
            ip = host['host']
            if ip in self.ip2mac_dict:
                mac = self.ip2mac_dict[ip]
                # print(f"try find vendor of {ip} --> {mac}")
            elif ip == self.active_interface['ipv4_addr'].ip.exploded:
                mac = self.active_interface['mac']
            else: mac = None
            self.guiconsole(f"[INFO] {ip} --> {mac}")
            vendor = self.get_vendor(mac,maclookup)
            host['mac'] = mac
            host['vendor'] = vendor
            self.reponded_hosts.append(host)

    # @staticmethod
    def get_vendor(self, mac: str, maclookup: MacLookup) -> str:
        try:
            vendor = maclookup.lookup(mac)
        except:
            self.guiconsole(f"[INFO] {mac} Vendor Not Founded")
            return "unknow"
        else:
            self.guiconsole(f"[INFO] {mac[:8]} Vendor Founded, {vendor}")
            return vendor

    # @staticmethod
    def update_vendorlist(self, maclookup: MacLookup):
        try:
            self.guiconsole("[WARN]Try Update Vendor List")
            maclookup.update_vendors()
        except:
            self.guiconsole("[WARN] Not Internet Connections; Vendors List Update Filed")
            pass
        else:
            self.guiconsole("[WARN] Vendors List Updated")
            pass
    
    ## ICMP PING
    def icmpping_ping(self, ipv4addr: IPv4Address) -> None:
        print(f"Pining {ipv4addr} ",)
        ip = ipv4addr.exploded
        if ping(ip).success():
            self.guiconsole(f"[INFO] {ipv4addr}... Responded")
            for host in self.reponded_hosts:
                if ip == host['host']: return
            self.reponded_hosts.append({"host": ip, "http": False, "https": False, "mac": None, "vendor": None})


    ## TCP PING
    def tcp_ping(self, ip: str) -> None:
        ports = []
        if self.setting['httpscan']: ports.append(80)
        if self.setting['httpsscan']: ports.append(443)
        print('Scanning TCP:', ip, ports)
        self.guiconsole(f"[INFO] Try Connect to {ip} {ports}")
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((ip, port))
                sock.settimeout(None)
            except:
                self.guiconsole(f"[INFO] {ip} {port} is DOWN")
            else:
                self.guiconsole(f"[INFO] {ip}:{port}... Replied")
                for host in self.reponded_hosts:
                    if host['host'] == ip:
                        host[self.get_portprotocol(port)] = True
                        break

    @staticmethod
    def get_portprotocol(port: int) -> str:
        dic = {80: 'http', 443: 'https'}
        if port in dic:
            protocol = dic[port]
            return protocol

if __name__ == "__main__":
    my_scanner = Scanner()
