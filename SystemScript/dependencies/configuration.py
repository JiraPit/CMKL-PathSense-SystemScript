import json
import shutil
import os

# get link token
def LTOKEN():
    with open('dependencies/configfile', 'r') as f:
        config = json.load(f)
    return config['ltoken']

# get device id
def DID(): 
    with open('dependencies/configfile', 'r') as f:
        config = json.load(f)
    return config['did']

# set link token in config file
def set_ltoken(ltoken):
    with open('dependencies/configfile', 'r') as f:
        config = json.load(f)
    config['ltoken'] = ltoken
    with open('dependencies/configfile', 'w') as f:
        json.dump(config, f)

# set device id in config file
def set_did(did):
    with open('dependencies/configfile', 'r') as f:
        config = json.load(f)
    config['did'] = did
    with open('dependencies/configfile', 'w') as f:
        json.dump(config, f)

# clear link token in config file
def clear_ltoken():
    with open('dependencies/configfile', 'r') as f:
        config = json.load(f)
    config['ltoken'] = ''
    with open('dependencies/configfile', 'w') as f:
        json.dump(config, f)

# clear device id in config file
def clear_did():
    with open('dependencies/configfile', 'r') as f:
        config = json.load(f)
    config['did'] = ''
    with open('dependencies/configfile', 'w') as f:
        json.dump(config, f)

# backup config file
def backup():
    try:
        root = os.path.expanduser('~')
        backup_dest = os.path.join(root, 'pathsense_configfile.backup')
        shutil.copyfile('dependencies/configfile', backup_dest)
    except:
        pass

# restore config file from backup
def restore():
    try:
        root = os.path.expanduser('~')
        backup_dest = os.path.join(root, 'pathsense_configfile.backup')
        shutil.copyfile(backup_dest, 'dependencies/configfile')
    except:
        pass

# validate config file
def is_valid():

    # open config file
    with open('dependencies/configfile', 'r') as f:
        config = json.load(f)
    
    # check if link token and device id are set
    if config['ltoken'] == '' or config['did'] == '':
        return False
        
    return True