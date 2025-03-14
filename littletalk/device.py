from serial.tools import list_ports
from serial import Serial

def Find_USB_Device(VID_PID):
    enmu_ports = enumerate(list_ports.comports())
    for n, (p, descriptor, hid) in enmu_ports:
        if hid.find(VID_PID) >= 0:
            print("Find device at " + p)
            print("Info : " + hid)
            return p
    print("ERROR : Can't find target USB device in any COM port.")
    return None

def Get_Serial_Device(com_port, baud_rate):
    serial_device = Serial(com_port, baud_rate)
    return serial_device

def Kill(serial_device : Serial):
    serial_device.close()
