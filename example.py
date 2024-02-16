'''
example.py to show how to connect to devices and use textfsm
'''
from core.connect import CiscoIOS
from core.connect import CiscoNXOS
from core.connect import CiscoASA


def main_nxos() -> None:
    '''Example Call for Cisco's Nexus Devices'''
    device = CiscoNXOS('IP', 'USERNAME', 'PASSWORD', 'ENABLE')
    device.connect()
    device.run_command('show version', textfsm=True)
    device.disconnect()


def main_ios() -> None:
    '''Example Call for Cisco's Catalyst IOS Devices'''
    device = CiscoIOS('IP', 'USERNAME', 'PASSWORD', 'ENABLE')
    device.connect()
    device.run_command('show version', textfsm=True)
    device.disconnect()


def main_asa() -> None:
    '''Example Call for Cisco's ASA Devices'''
    device = CiscoASA('IP', 'USERNAME', 'PASSWORD', 'ENABLE')
    device.connect()
    device.run_command('show version', textfsm=True)
    device.disconnect()


def main():
    '''Main Fucntion to call all example functions'''
    # Example Call for Cisco's Nexus Devices
    main_nxos()

    # Example Call for Cisco's Catalyst IOS Devices
    main_ios()

    # Example Call for Cisco's ASA Devices
    main_asa()


if __name__ == '__main__':
    main()
