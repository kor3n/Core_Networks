'''Docstring'''
import os
from netmiko import ConnectHandler
from netmiko import NetMikoTimeoutException
from netmiko import NetMikoAuthenticationException


class Network_Device():
    '''docstring for Network_Device'''

    def __init__(self, ip, username, password, secret, port=22):
        self.ip = ip
        self.username = username
        self.password = password
        self.secret = secret
        self.port = port
        self.connected = None
        templates = f"{os.path.dirname(os.path.abspath(__file__))}" \
            "\\modules\\textfsm\\templates\\"
        os.environ['NET_TEXTFSM'] = templates

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


class Base_Commands(Network_Device):
    """docstring for Base_Commands"""

    def __init__(self, *args):
        super().__init__(*args)

    def disconnect(self):
        '''Docstring'''
        super()._disconnect_network_device()

    def find_device_prompt(self):
        '''Docstring'''
        super()._find_prompt()


class Cisco_IOS(Base_Commands):
    """docstring for Cisco_IOS"""

    def __init__(self, *args):
        super().__init__(*args)
        self.device_type = 'cisco_ios'  # 'cisco_nxos'

    def connect(self):
        '''Docstring'''
        switch = {
            'device_type': self.device_type,
            'ip': self.ip,
            'username': self.username,
            'password': self.password,
            'secret': self.secret,
            'port': self.port
        }
        super()._connect_network_device(switch)

    def run_command(self, command, textfsm=False):
        '''Docstring'''
        if textfsm is False:
            return self.connected.send_command(command, expect_string='#')
        elif textfsm is True:
            return self.connected.send_command(command, use_textfsm=True)

    def run_command_set(self, commands):
        '''Docstring'''
        return self.connected.send_config_set(commands)

    def interface_running_config(self, interface, output='str'):
        '''Docstring'''
        command = f'show run int {interface}'
        if output.lower() == 'str':
            return self.connected.send_command(command)
        elif output.lower() == 'list':
            return self.connected.send_command(command).splitlines()


class Cisco_NXOS(Base_Commands):
    """docstring for Nexus_Switch"""

    def __init__(self, *args):
        super().__init__(*args)
        self.device_type = 'cisco_nxos'  # 'cisco_nxos'

    def connect(self):
        '''Docstring'''
        switch = {
            'device_type': self.device_type,
            'ip': self.ip,
            'username': self.username,
            'password': self.password,
            'secret': self.secret,
            'port': self.port
        }
        super()._connect_network_device(switch)

    def run_command(self, command, textfsm=False):
        '''Docstring'''
        if textfsm is False:
            return self.connected.send_command(command) #, expect_string='#')
        elif textfsm is True:
            return self.connected.send_command(command, use_textfsm=True)

    def run_command_set(self, commands):
        '''Docstring'''
        return self.connected.send_config_set(commands)

    def switch_vdc(self, vdc):
        '''Docstring'''
        command = [f'switchto vdc {vdc}',
                   'terminal width 511',
                   'terminal length 0']
        return self.connected.send_config_set(command)


class Cisco_ASA(Base_Commands):
    """docstring for Cisco_ASA"""

    def __init__(self, *args):
        super().__init__(*args)
        self.device_type = 'cisco_asa'  # 'cisco_nxos'

    def connect(self):
        '''Docstring'''
        switch = {
            'device_type': self.device_type,
            'ip': self.ip,
            'username': self.username,
            'password': self.password,
            'secret': self.secret,
            'port': self.port
        }
        super()._connect_network_device(switch)

    def run_command(self, command, textfsm=False):
        '''Docstring'''
        if textfsm is False:
            return self.connected.send_command(command)
        elif textfsm is True:
            return self.connected.send_command(command, use_textfsm=True)

    def run_command_set(self, commands):
        '''Docstring'''
        return self.connected.send_config_set(commands)

    def interface_running_config(self, interface, output='str'):
        '''Docstring'''
        command = f'show run int {interface}'
        if output.lower() == 'str':
            return self.connected.send_command(command)
        elif output.lower() == 'list':
            return self.connected.send_command(command).splitlines()
