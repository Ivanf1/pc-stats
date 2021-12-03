# PC Stats from OpenHardwareMonitor to ESP32

Use [OpenHardwareMonitor](https://github.com/openhardwaremonitor/openhardwaremonitor) to retrieve stats about the host pc, apply custom filtering and formatting and send them via UART to an ESP32.

## Usage

OpenHardwareMonitor needs to be running. Clone or download the repo and run

```bash
python main.py
```

## Customization

OpenHardwareMonitor publishes data to WMI classes. You can run queries on those classes to get the data you need.

[What is WMI](https://docs.microsoft.com/en-us/windows/win32/wmisdk/about-wmi)  
[How OpenHardwareMonitor data is published on WMI](http://openhardwaremonitor.org/wordpress/wp-content/uploads/2011/04/OpenHardwareMonitor-WMI.pdf)  
[How to write WQL to get the OpenHardwareMonitor data](https://docs.microsoft.com/en-us/windows/win32/wmisdk/wql-sql-for-wmi)
