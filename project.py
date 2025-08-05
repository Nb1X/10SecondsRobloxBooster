import os
import subprocess
import shutil
import psutil
import winreg
import time


def disable_sysmain():
    print("Disabling SysMain...")
    try:
        import wmi
        c = wmi.WMI()
        for disk in c.Win32_DiskDrive():
            if "SSD" in disk.MediaType:
                subprocess.run('sc stop SysMain', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run('sc config SysMain start=disabled', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print("Success")
                return
            else:
                print("Failed: You have an HDD (Hard Drive)")
                return
        print("Failed: Disk info not found")
    except Exception as e:
        print(f"Failed: {e}")


def launch_disk_cleanup():
    print("Launching Disk Cleanup...")
    try:
        subprocess.run("cleanmgr /sagerun:1", shell=True)
        print("Success")
    except Exception as e:
        print(f"Failed: {e}")


def delete_temp_files():
    print("Deleting the %temp% not-used files...")
    temp_path = os.getenv('TEMP')
    deleted_files = 0
    deleted_folders = 0
    try:
        for root, dirs, files in os.walk(temp_path):
            for name in files:
                try:
                    os.remove(os.path.join(root, name))
                    deleted_files += 1
                except:
                    continue
            for name in dirs:
                try:
                    shutil.rmtree(os.path.join(root, name))
                    deleted_folders += 1
                except:
                    continue
        print(f"Success, {deleted_files + deleted_folders} files have been deleted")
    except Exception as e:
        print(f"Failed: {e}")


def enable_game_mode():
    print("Game mode:", end=' ')
    try:
        key_path = r"Software\Microsoft\GameBar"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS) as key:
            value, _ = winreg.QueryValueEx(key, "AllowAutoGameMode")
            if value == 1:
                print("already activated")
            else:
                winreg.SetValueEx(key, "AllowAutoGameMode", 0, winreg.REG_DWORD, 1)
                print("true")
    except Exception as e:
        print(f"Failed: {e}")


def launch_roblox_fullscreen():
    print("Launching Roblox...")
    try:
        roblox_versions_path = os.path.expandvars(r"%LOCALAPPDATA%\Roblox\Versions")
        found = False
        for folder in os.listdir(roblox_versions_path):
            full_path = os.path.join(roblox_versions_path, folder)
            roblox_exe = os.path.join(full_path, "RobloxPlayerBeta.exe")
            if os.path.exists(roblox_exe):
                found = True
                subprocess.Popen([roblox_exe], shell=True)
                print("Success")
                return
        if not found:
            print("Failed: Roblox not found")
    except Exception as e:
        print(f"Failed: {e}")


disable_sysmain()
print("-" * 40)
launch_disk_cleanup()
print("-" * 40)
delete_temp_files()
print("-" * 40)
enable_game_mode()
print("-" * 40)
launch_roblox_fullscreen()
print("-" * 40)

print("Script finished. Press ENTER to exit.")
input()
