"""
Unittests for asa plugin

Uses the mock_device.py script to test the plugin.

"""

__author__ = "Dave Wapstra <dwapstra@cisco.com>"


import os
import yaml
import unittest


import unicon
from unicon import Connection
from unicon.core.errors import SubCommandFailure
from unicon.mock.mock_device import mockdata_path

with open(os.path.join(mockdata_path, 'asa/asa_mock_data.yaml'), 'rb') as data:
    mock_data = yaml.safe_load(data.read())


class TestAsaPluginConnect(unittest.TestCase):

    def test_connect(self):
        c = Connection(hostname='ASA',
                       start=['mock_device_cli --os asa --state asa_disable'],
                       os='asa',
                       enable_password='cisco',
                       password='cisco')
        c.connect()
        v = c.execute('show version')
        self.assertEqual(v.replace('\r',''), mock_data['asa_enable']['commands']['show version'].rstrip())

    def test_connect_prio_state(self):
        c = Connection(hostname='ASA',
                       start=['mock_device_cli --os asa --state asa_disable_pri_act'],
                       os='asa',
                       enable_password='cisco',
                       password='cisco')
        c.connect()

    def test_login_connect_ssh(self):
        c = Connection(hostname='ASA',
                            start=['mock_device_cli --os asa --state connect_ssh'],
                            os='asa',
                            username='cisco',
                            tacacs_password='cisco',
                            line_password='cisco',
                            enable_password='cisco')
        c.connect()

    def test_connect_more(self):
        c = Connection(hostname='ASA',
                            start=['mock_device_cli --os asa --state asa_enable_more'],
                            os='asa',
                            username='cisco',
                            tacacs_password='cisco',
                            line_password='cisco',
                            enable_password='cisco',
                            init_exec_commands=['show version'])
        c.connect()

    def test_asa_reload(self):
        c = Connection(hostname='ASA',
                            start=['mock_device_cli --os asa --state asa_reload'],
                            os='asa',
                            series='asav',
                            username='cisco',
                            tacacs_password='cisco',
                            line_password='cisco',
                            enable_password='cisco')
        c.connect()
        c.reload()

class TestAsaPluginExecute(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = Connection(hostname='switch',
                        start=['mock_device_cli --os asa --state asa_enable'],
                        os='asa',
                        username='cisco',
                        tacacs_password='cisco',
                        init_exec_commands=[],
                        init_config_commands=[]
                        )
        cls.c.connect()

    def test_execute_error_pattern(self):
        with self.assertRaises(SubCommandFailure) as err:
          r = self.c.execute('changeto context GLOBAL')

    def test_execute_error_pattern_warning(self):
        with self.assertRaises(SubCommandFailure) as err:
          r = self.c.execute('network-object host 5.5.50.10')



if __name__ == "__main__":
    unittest.main()