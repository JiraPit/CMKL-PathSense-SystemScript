import subprocess
import argparse

def install():
    subprocess.run(["chmod", "+x", "setup_sh/install.sh"])
    subprocess.run(["sudo setup_sh/install.sh"])

def update():
    subprocess.run(["chmod", "+x", "setup_sh/update.sh"])
    subprocess.run(["sudo setup_sh/update.sh"])

def remove_from_boot():
    subprocess.run(["chmod", "+x", "setup_sh/remove-from-boot.sh"])
    subprocess.run(["sudo setup_sh/remove-from-boot.sh"])

def main(command):
    if command == "install":
        install()
    elif command == "update":
        update()
    elif command == "remove-from-boot":
        remove_from_boot()
    else:
        print("Invalid command. Please use install or uninstall.")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="install / update / remove-from-boot")
    args = parser.parse_args()
    main(args.command)