from core.connect import Cisco_IOS
from core.connect import Cisco_NXOS
from core.connect import Cisco_ASA


def main_NXOS():
    # Example Call for Cisco's Nexus Devices
    device = Cisco_NXOS('IP', 'USERNAME', 'PASSWORD', 'ENABLE')
    device.connect()
    device.run_command('show version', textfsm=True)
    device.disconnect()


def main_IOS():
    # Example Call for Cisco's Catalyst IOS Devices
    device = Cisco_IOS('IP', 'USERNAME', 'PASSWORD', 'ENABLE')
    device.connect()
    device.run_command('show version', textfsm=True)
    device.disconnect()


def main_ASA():
    # Example Call for Cisco's ASA Devices
    device = Cisco_ASA('IP', 'USERNAME', 'PASSWORD', 'ENABLE')
    device.connect()
    device.run_command('show version', textfsm=True)
    device.disconnect()


def main():
    # Example Call for Cisco's Nexus Devices
    main_NXOS()

    # Example Call for Cisco's Catalyst IOS Devices
    main_IOS()

    # Example Call for Cisco's ASA Devices
    main_ASA()


if __name__ == '__main__':
    main()
