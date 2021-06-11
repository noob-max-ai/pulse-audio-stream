import socket
import subprocess, os

def is_port_open(ip_address, port):
    s = socket.socket()
    try:
        s.connect((ip_address, port)) 
        # originally, it was 
        # except Exception, e: 
        # but this syntax is not supported anymore. 
    except Exception as e: 
        print("something's wrong with %s:%d. Exception is %s" % (ip_address, port, e))
        return False
    finally:
        s.close()
    return True


def get_ip():
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def get_output_sources():
    cmd = ["pactl", "list"]
    tag = "Monitor Source"
    res = subprocess.run(cmd, stdout=subprocess.PIPE)
    res = res.stdout.decode('utf-8').splitlines()
    line_with_tag = []
    for line in res:
        if tag in line:
            # strip tabs
            line = line.strip()
            line = line.split(':')[-1].strip()
            line_with_tag.append(line)
            
    return line_with_tag

def service_is_running():
    TAG = "tcp"
    cmd = ["pactl", "list"]
    res = subprocess.run(cmd, stdout=subprocess.PIPE)
    res = res.stdout.decode('utf-8')
    if TAG in res:
        return True
    return False

def start_server(source, port):
    cmd = ["pactl", "load-module", 
        "module-simple-protocol-tcp", "rate=48000", "format=s16le", 
        "channels=2", f"source={source}", "record=true", f"port={port}"]
    
    res = subprocess.run(cmd, stdout=subprocess.PIPE)
    res = res.stdout.decode('utf-8')
    return res


def stop_server():
    cmd = "pactl unload-module `pactl list | grep tcp -B1 | grep M | sed 's/[^0-9]//g'`"
    return os.system(cmd)

def unload_module(module):
    cmd = f"pactl unload-module {module}"
    return os.system(cmd)

def start_mic_server(audio_file):
    cmd = f"./virtualmic {audio_file}"
    return os.system(cmd)

def mktemp():
    cmd = ["mktemp", "-u"]
    res = subprocess.run(cmd, stdout=subprocess.PIPE)
    res = res.stdout.decode('utf-8')
    return res.strip()


