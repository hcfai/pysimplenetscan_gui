import threading
from time import sleep,localtime,strftime
from os import _exit

from gui import mainctk
from nettools import scanner
from utilstools import win_commond, ipv4_helper

## getipconfig
def get_all_interface() -> list:
    filename = win_commond.cmd_winsave('ipconfig -all')
    nic_list = win_commond.sort_win_ipconfig(filename)

    for _ in range(len(nic_list)):
        nic = nic_list.pop(0)
        if 'ipv4_addr' in nic: app.add_interface(nic)

    nic_opntion = []
    for nic in app.interfaces:
        nic_opntion.append(f"{nic['description']}  ---> {nic['ipv4_addr']}")
        gui.console_textbox_2_addnewline(f"[INFO] New Interface: {nic['interface']} ---> {nic['description']}")
    gui.setting_om_int.configure(values=nic_opntion)

## Custom Scan range
def get_ScanningRangebyActiveInterface():
    scanNetwork = app.active_interface['ipv4_addr'].network
    fristAddr = ipv4_helper.ipv4_addone(scanNetwork.network_address)
    lastAddr = ipv4_helper.ipv4_devone(scanNetwork.broadcast_address)
    gui.setting_customscan.update_iprangeEntry(fristAddr, lastAddr)


## function for gui
def scanner_isrunning() -> None:
    gui.progressbar_show()
    while app.scanning:
        sleep(1)
    gui.progressbar_hide()

def popupwindows_close():
    gui.destroy()

def killall():
    ## shell is true so becareful
    win_commond.cleanup(filename='ipconfig')
    win_commond.cleanup(filename='arp')
    gui.destroy()
    sleep(1)
    _exit(0)

## ICMP Echo Threading
def start_std_icmpping():
    for ip in app.active_interface['ipv4_addr'].network.hosts():
        thread = threading.Thread(target=app.icmpping_ping, args=(ip,))
        thread.start()
        threadhandling.append(thread)
        sleep(0.01)
    for thread in threadhandling: thread.join()
    for host in app.reponded_hosts: print(f"{host['host']} is UP")

def start_custom_icmpping():
    start_ip = gui.setting_customscan.ip_input_1.get()
    end_ip = gui.setting_customscan.ip_input_2.get()
    scantargets = ipv4_helper.ipv4_rangecheck(start_ip, end_ip)
    if not isinstance(scantargets, ipv4_helper.GeneratorType):
        gui.console_textbox_addnewline(scantargets)
        app.setting['correctiprange'] = False
        return
    else: app.setting['correctiprange'] = True
    for ip in scantargets:
        thread = threading.Thread(target=app.icmpping_ping, args=(ip,))
        thread.start()
        threadhandling.append(thread)
        sleep(0.01)
    for thread in threadhandling: thread.join()
    for host in app.reponded_hosts: print(f"{host['host']} is UP")

## scanning
def start_maclookup():
    filename = win_commond.cmd_winsave('arp -a')
    ip2mac_dict = win_commond.sort_win_arp(filename)
    app.ip2mac_dict = ip2mac_dict
    app.get_mac()

def start_tcpping():
    for host in app.reponded_hosts:
        thread = threading.Thread(target=app.tcp_ping, args=(host['host'],))
        thread.start()
        threadhandling.append(thread)
    for thread in threadhandling: thread.join()

## Scanning Thread
def start_scanning():
    app.scanning = True

    if app.setting['skipping']:
        gui.console_textbox_addnewline(f"[INFO] new scanning started at {strftime('%Y/%m/%d - %H:%M:%S', localtime())} | Skipping Ping, Try Connect to {len(app.reponded_hosts)} Hosts")
        pass
    elif app.setting['customscantarget']:
        gui.console_textbox_addnewline(f"[INFO] new scanning started at {strftime('%Y/%m/%d - %H:%M:%S', localtime())} | Scanning from {gui.setting_customscan.ip_input_1.get()} to {gui.setting_customscan.ip_input_2.get()}")
        icmp_thread = threading.Thread(target=start_custom_icmpping)
        icmp_thread.start()
        icmp_thread.join()
    else:
        gui.console_textbox_addnewline(f"[INFO] new scanning started at {strftime('%Y/%m/%d - %H:%M:%S', localtime())} | Interface: {app.active_interface['ipv4_addr']} | {app.active_interface['ipv4_addr'].network.num_addresses-2} hosts to scan")
        icmp_thread = threading.Thread(target=start_std_icmpping)
        icmp_thread.start()
        icmp_thread.join()
    
    if app.setting['correctiprange'] == False: 
        app.scanning = False
        return

    if app.setting['showdetail']:
        gui.console_textbox_2_addnewline("[WARN] Start getting mac address and vendor")
        maclookup_thread = threading.Thread(target=start_maclookup)
        maclookup_thread.start()
        maclookup_thread.join()

    for host in app.reponded_hosts:
        if app.setting['showdetail']:
            gui.console_textbox_addnewline(f"[ICMP] {host['host']} is UP --> {host['mac']} --> {host['vendor']}")
        else:
            gui.console_textbox_addnewline(f"[ICMP] {host['host']} is UP")

    if app.setting['httpscan'] or app.setting['httpsscan']:
        gui.console_textbox_2_addnewline("[WARN] Start Pinging TCP Ports")
        tcp_thread = threading.Thread(target=start_tcpping)
        tcp_thread.start()
        tcp_thread.join()

    for host in app.reponded_hosts:
        if host['http']:
            gui.console_textbox_addnewline(f"[HTTP] webpage founded: http://{host['host']}:80")

    for host in app.reponded_hosts:
        if host['https']:
            gui.console_textbox_addnewline(f"[HTPS] webpage founded: https://{host['host']}:443")

    app.scanning = False

## Button Funcktion
def buttonFunc_startPing():
    print("Starting Pining")
    threading.Thread(target=start_scanning).start()
    threading.Thread(target=scanner_isrunning).start()

def buttonFunc_popupcomfrim():
    get_all_interface()
    set_default_interface()
    gui.popupwindow.withdraw()
    gui.deiconify()

def buttonFunc_getnetowrk():
    app.interfaces.clear()
    get_all_interface()
    set_default_interface()

def buttonFunc_clean():
    gui.console_textbox_clear()
    gui.console_textbox_2_clear()
    app.reponded_hosts.clear()

def cboxFunc_enableCustomScanTarget():
    gui.cbox_customscan.configure(state='normal')
    gui.setting_customscan.change_entrystate(gui.setting_customscan.ip_input_1, gui.cbox_customscan)
    gui.setting_customscan.change_entrystate(gui.setting_customscan.ip_input_2, gui.cbox_customscan)
    gui.changesetting(gui.cbox_customscan, app, 'customscantarget')

def set_infobox(ip, description,netcls):
    gui.console_textbox_2_addnewline(f'[WARN] Active Interface: {description} ---> {app.active_interface["ipv4_addr"].with_prefixlen}')
    if netcls == 'C': 
        gui.console_textbox_2_addnewline(f'[WARN] Scanning Range set to {app.active_interface["ipv4_addr"].with_prefixlen} ({app.active_interface["ipv4_addr"].network.num_addresses-2} hosts will be scan)')
        gui.setting_om_int.configure(fg_color='#3a7ebf')
    elif netcls == 'B' or 'A': 
        gui.console_textbox_2_addnewline(f"[WARN] This Interface's network is too big, it will take long time to scan! ({app.active_interface['ipv4_addr'].network.num_addresses-2} hosts will be scan!!!!)")
        gui.setting_om_int.configure(fg_color='#BF3A7E')
    elif netcls == 'ERROR': 
        gui.console_textbox_2_addnewline('[WARN] Scan Target error')
        gui.setting_om_int.configure(fg_color='red')
    gui.cconsole_infobox_addnewline('clear')
    gui.cconsole_infobox_addnewline("Host:")
    gui.cconsole_infobox_addnewline(f"{app.hostname}")
    gui.cconsole_infobox_addnewline("Name:")
    gui.cconsole_infobox_addnewline(f"{app.active_interface['interface']}")
    gui.cconsole_infobox_addnewline("Adapter:")
    gui.cconsole_infobox_addnewline(f"{app.active_interface['description']}")
    gui.cconsole_infobox_addnewline("IP Address:")
    gui.cconsole_infobox_addnewline(f"{app.active_interface['ipv4_addr']}")
    gui.cconsole_infobox_addnewline("MAC:")
    gui.cconsole_infobox_addnewline(f"{app.active_interface['mac']}")
    get_ScanningRangebyActiveInterface()

def optionmenu_interface(new_interface: str):
    ip, description, netcls= app.set_activeinterface(new_interface)
    set_infobox(ip, description, netcls)

def set_default_interface():
    print("Geting Network Infomation")
    ip, description, netcls = app.set_defualtinterface()
    set_infobox(ip, description, netcls)
    gui.setting_om_int.set(f"{description}  ---> {ip}") 

def buttonFunc_testing():
    print(app.interfaces)
    pass

## defualt labels
def gui_defualttext():
    gui.confirm_popup(NOTE)
    gui.button_startPing.configure(text="Start Scan")
    gui.button_getNetwork.configure(text="Refresh Network")
    gui.button_cleanConsole.configure(text="Clean All")
    gui.button_savetxt.configure(text="Save to .txt") 
    gui.setting_label_int.configure(text="Interface Info") 
    gui.setting_label_intchange.configure(text="Change Interface") 
    gui.setting_om_int.configure(values=["Scan Interfaces"], command=optionmenu_interface) 
    gui.cbox_customscan.configure(text='Custom Scan Range')
    gui.setting_om_int.set("Scan Interfaces") 
    gui.cbox_detail.configure(text="MAC Lookup")
    gui.cbox_http.configure(text="HTTP Scan")
    gui.cbox_https.configure(text="HTTPS Scan")
    gui.cbox_skipping.configure(text="Skip Ping")
    gui.console_label.configure(text="Output")
    gui.setting_customscan.label.configure(text="Scaner Target Range")

## Link Button to function
def gui_linkbutton():
    gui.button_startPing.configure(command=buttonFunc_startPing)
    gui.button_getNetwork.configure(command=buttonFunc_getnetowrk)
    gui.button_popup.configure(command=buttonFunc_popupcomfrim)
    gui.button_cleanConsole.configure(command=buttonFunc_clean)
    gui.button_savetxt.configure(command=gui.button_savefile)
    gui.cbox_detail.configure(command=lambda: gui.changesetting(gui.cbox_detail, app, 'showdetail'))
    gui.cbox_http.configure(command=lambda: gui.changesetting(gui.cbox_http, app, 'httpscan'))
    gui.cbox_https.configure(command=lambda: gui.changesetting(gui.cbox_https, app, 'httpsscan'))
    gui.cbox_skipping.configure(command=lambda: gui.changesetting(gui.cbox_skipping, app, 'skipping'))
    gui.cbox_customscan.configure(command=cboxFunc_enableCustomScanTarget)
    gui.popupwindow.protocol("WM_DELETE_WINDOW", popupwindows_close)
    gui.protocol("WM_DELETE_WINDOW", killall)


NOTE = """Simple Network Scanner for AV Technician BATE v0.82
Please DO NOT use it in any pulbic network!!!
USE IT WITH YOUR OWN RISK!!!

Included Moduls:
TomSchimansky/CustomTkinter
alessandromagg/pythonping
bauerj/mac_vendor_lookup

Regards,

Version 0.82
Add optional scan target
Version 0.72
Clean temp file when quite
Add interfaces option
Change to using subprocess get arp table
Version 0.6
Add support for mac address lookup
Version 0.5
Add support for disabling http or https scan
Version 0.4
Add support for http and https scan
"""


if __name__ == "__main__":
    threadhandling, nic_list = [], []
    gui = mainctk.GuiApp(title="Simple Network Scanner for AV Technician BATE v0.82")
    app = scanner.Scanner(guiconsole=gui.console_textbox_2_addnewline)
    gui_defualttext()
    gui_linkbutton()
    gui.mainloop()