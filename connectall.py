import subprocess
import time
import re
from lcd_display import LCDDisplay

def parse_midi_ports(output):
    ports = []
    ignore_ports = [0,14]
    lines = output.strip().splitlines()
    for line in lines:
        port_info = line.strip().split(' ')
        if len(port_info) >= 3 and port_info[0] == 'client':
            port_num = int(port_info[1].replace(":",""))
            port_name = ' '.join(port_info[2:])
            port_name = re.sub(r"\[.*?\]", "", port_name)
            port_name = port_name.replace("'","")
            if port_num not in ignore_ports:
                ports.append((port_num, port_name))
    return ports

def list_midi_ports():
    result = subprocess.run(["aconnect", "-l"], capture_output=True, text=True)
    if result.returncode == 0:
        output = result.stdout
        ports = parse_midi_ports(output)
        if ports:
            print("Available MIDI Ports:")
            for port_num, port_name in ports:
                print(f"{port_num}: {port_name}")
        else:
            print("No MIDI ports found.")
    else:
        print("Error listing MIDI ports.")

def connect_midi_ports(source, dest):
    subprocess.run(["aconnect", str(source[0]), str(dest[0])])
    print(f"Connected {source[1]} to {dest[1]}")

def lcd_send(lcd, port_names):
    '''Write ports to lcd'''
    port_names.insert(0, "Midi Connections:")
    lines = list(range(0,len(port_names)))
    lcd.write_lines(lines, port_names)

def check_and_connect_new_ports(lcd=None):
    previous_ports = set()

    while True:
        result = subprocess.run(["aconnect", "-l"], capture_output=True, text=True)
        if result.returncode == 0:
            output = result.stdout
            current_ports = set(parse_midi_ports(output))
            # Show current ports to LCD
            lcd_send(lcd, [x[1] for x in current_ports])
            new_ports = current_ports - previous_ports

            if not previous_ports:     #First time
                for p1 in current_ports:
                    for p2 in current_ports:
                        if p1[0] != p2[0]:
                            connect_midi_ports(p1, p2) 
            elif len(new_ports) != 0: # Find new ports that are not present in the previous set
                print("New ports found")
                for p1 in new_ports:
                    for p2 in previous_ports:
                        if p1[0] != p2[0]:
                            connect_midi_ports(p1,p2)
                            connect_midi_ports(p2,p1)
            #Set previous to be current
            previous_ports = current_ports
        # Wait for 1 second before checking again
        time.sleep(1)


if __name__ == "__main__":
    list_midi_ports()
    lcd = LCDDisplay()
    check_and_connect_new_ports(lcd)
