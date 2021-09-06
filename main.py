import wmi

c = wmi.WMI()

for os in c.Win32_OperatingSystem():
    print(os.Caption)