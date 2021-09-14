from serial.tools import list_ports

def get_serial_ports():
    """Return a list of all serial ports found"""
    return sorted(list_ports.comports())