import os
from netmiko import ConnectHandler
from netmiko import ssh_exception


class Network_Device():
    '''docstring for Network_Device'''

    def __init__(self, ip, username, password, secret, port=22):
        self.ip = ip
        self.username = username
        self.password = password
        self.secret = secret  # if secret is not '' else password
        self.port = port
        # place holder
        self.connected = None
        templates = f"{os.path.dirname(os.path.abspath(__file__))}" \
            "\\modules\\textfsm\\templates\\"
        os.environ['NET_TEXTFSM'] = templates

    def _connect_network_device(self, switch):
        try:
            self.connected = ConnectHandler(**switch)
            self.connected.enable()
            return True
        except (ssh_exception.NetMikoTimeoutException) as e:
            raise e
        except (ssh_exception.NetMikoAuthenticationException) as e:
            raise e

    def _disconnect_network_device(self):
        try:
            self.connected.disconnect()
            self.connected = None
            return True
        except Exception as e:
            raise e


class Base_Commands(Network_Device):
    """docstring for Base_Commands"""
    def __init__(self, *args):
        super().__init__(*args)

    def disconnect(self):
        super()._disconnect_network_device()


class Cisco_IOS(Base_Commands):
    """docstring for Cisco_IOS"""

    def __init__(self, *args):
        super().__init__(*args)
        self.device_type = 'cisco_ios'  # 'cisco_nxos'

    def connect(self):
        switch = {
            'device_type': self.device_type,
            'ip': self.ip,
            'username': self.username,
            'password': self.password,
            'secret': self.secret,
            'port': self.port
        }
        super()._connect_network_device(switch)


class Cisco_NXOS(Base_Commands):
    """docstring for Nexus_Switch"""

    def __init__(self, *args):
        super().__init__(*args)
        self.device_type = 'cisco_nxos'

    def connect(self):
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
        if textfsm is False:
            return self.connected.send_command(command)
        elif textfsm is True:
            return self.connected.send_command(command, use_textfsm=True)


class Cisco_ASA(Base_Commands):
    """docstring for Cisco_ASA"""

    def __init__(self, *args):
        super().__init__(*args)
        self.device_type = 'cisco_asa'  # 'cisco_nxos'

    def connect(self):
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
        if textfsm is False:
            return self.connected.send_command(command)
        elif textfsm is True:
            return self.connected.send_command(command, use_textfsm=True)
