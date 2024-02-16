"""Docstring"""
import os
from netmiko import ConnectHandler
from netmiko import NetMikoTimeoutException
from netmiko import NetMikoAuthenticationException


class NetworkDevice:
    """docstring for Network_Device"""

    def __init__(self, ip, username, password, secret, port=22):
        self.ip = ip
        self.username = username
        self.password = password
        self.secret = secret
        self.port = port
        self.connected = None
        templates = (
            f"{os.path.dirname(os.path.abspath(__file__))}"
            "\\modules\\textfsm\\templates\\"
        )
        os.environ["NET_TEXTFSM"] = templates

    def _connect_network_device(self, switch):
        try:
            self.connected = ConnectHandler(**switch)
            self.connected.enable()
            return True
        except (NetMikoTimeoutException) as e:
            raise e
        except (NetMikoAuthenticationException) as e:
            raise e

    def _disconnect_network_device(self):
        try:
            self.connected.disconnect()
            self.connected = None
            return True
        except Exception as e:
            raise e

    def _find_prompt(self):
        try:
            return self.connected.find_prompt()
        except Exception as e:
            raise e


class BaseCommands(NetworkDevice):
    """docstring for Base_Commands"""

    def __init__(self, *args):
        super().__init__(*args)

    def disconnect(self):
        """Docstring"""
        super()._disconnect_network_device()

    def find_device_prompt(self):
        """Docstring"""
        super()._find_prompt()


class CiscoIOS(BaseCommands):
    """docstring for Cisco_IOS"""

    def __init__(self, *args):
        super().__init__(*args)
        self.device_type = "cisco_ios"  # 'cisco_nxos'

    def connect(self):
        """Docstring"""
        switch = {
            "device_type": self.device_type,
            "ip": self.ip,
            "username": self.username,
            "password": self.password,
            "secret": self.secret,
            "port": self.port,
        }
        super()._connect_network_device(switch)

    def run_command(self, command, textfsm=False):
        """Docstring"""
        if textfsm is False:
            return self.connected.send_command(command, expect_string="#")
        elif textfsm is True:
            return self.connected.send_command(command, use_textfsm=True)

    def interface_running_config(self, interface, output="str"):
        """Docstring"""
        command = f"show run int {interface}"
        if output.lower() == "str":
            return self.connected.send_command(command)
        elif output.lower() == "list":
            return self.connected.send_command(command).splitlines()


class CiscoNXOS(BaseCommands):
    """docstring for Nexus_Switch"""

    def __init__(self, *args):
        super().__init__(*args)
        self.device_type = "cisco_nxos"

    def connect(self):
        """Docstring"""
        switch = {
            "device_type": self.device_type,
            "ip": self.ip,
            "username": self.username,
            "password": self.password,
            "secret": self.secret,
            "port": self.port,
        }
        super()._connect_network_device(switch)

    def run_command(self, command, textfsm=False):
        """Docstring"""
        if textfsm is False:
            return self.connected.send_command(command)
        elif textfsm is True:
            return self.connected.send_command(command, use_textfsm=True)

    def switch_vdc(self, vdc):
        """Docstring"""
        command = [f"switchto vdc {vdc}",
                   "terminal width 511", "terminal length 0"]
        return self.connected.send_config_set(command)


class CiscoASA(BaseCommands):
    """docstring for Cisco_ASA"""

    def __init__(self, *args):
        super().__init__(*args)
        self.device_type = "cisco_asa"

    def connect(self):
        """Docstring"""
        switch = {
            "device_type": self.device_type,
            "ip": self.ip,
            "username": self.username,
            "password": self.password,
            "secret": self.secret,
            "port": self.port,
        }
        super()._connect_network_device(switch)

    def run_command(self, command, textfsm=False):
        """Docstring"""
        if textfsm is False:
            return self.connected.send_command(command)
        elif textfsm is True:
            return self.connected.send_command(command, use_textfsm=True)

    def interface_running_config(self, interface, output="str"):
        """Docstring"""
        command = f"show run int {interface}"
        if output.lower() == "str":
            return self.connected.send_command(command)
        elif output.lower() == "list":
            return self.connected.send_command(command).splitlines()


class PaloPANOS(BaseCommands):
    """docstring for palo"""

    def __init__(self, *args):
        super().__init__(*args)
        self.device_type = "paloalto_panos"

    def connect(self):
        """Docstring"""
        switch = {
            "device_type": self.device_type,
            "ip": self.ip,
            "username": self.username,
            "password": self.password,
            "port": self.port,
        }
        super()._connect_network_device(switch)

    def run_command(self, command, set_command=False, textfsm=False):
        """Docstring"""
        if textfsm is False:
            if set_command is True and isinstance(command, list) is True:
                return self.connected.send_config_set(
                    command, expect_string=r">")
            else:
                return self.connected.send_command(command, expect_string=r">")
        elif textfsm is True:
            return self.connected.send_command(command, use_textfsm=True)
