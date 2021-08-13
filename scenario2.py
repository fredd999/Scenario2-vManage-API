import configparser
from IPython.display import display
import pandas as pd
import requests
from requests import session
import json
import csv
import getpass
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
vManage_ip = {""}
username = {""}
password = {""}


class SdwanAPIOBJ:
    def __init__(self):
        self.vmanage_ip = vManage_ip
        self.session = {}
        self.authenticate()

    def authenticate(self):
        base_url_str = 'https://{}:8444/'.format(vManage_ip)
        login_action = '/j_security_check'
        login_data = {'j_username': username, 'j_password': password}
        login_url = base_url_str + login_action
        url = login_url
        sess = requests.session()
        login_response = sess.post(url=login_url, data=login_data, verify=False)
        self.session[vManage_ip] = sess

    def get_device_list(self, mount_point):
        url = "https://{0}:8444/{1}".format(self.vmanage_ip, mount_point)
        response = self.session[self.vmanage_ip].get(url, verify=False)
        data = response.content
        return data

    def logout(self):
        url = "https://{}:8444/logout.html".format(self.vmanage_ip)
        return "Successfully logged out of vManage", 401


print("Viptela vManage Engine Starting...\n")

# Open up the configuration file and get all application defaults
try:
    config = configparser.ConfigParser()
    config.read('package_config.ini')
    vManage_ip = config.get("application", "serveraddress")
    username = config.get("application", "username")
    password = config.get("application", "password")
except configparser.Error:
    print("Cannot Parse package_config.ini")
    exit(-1)

vManage = SdwanAPIOBJ()
device_list = json.loads(vManage.get_device_list("dataservice/device"))
vManage_logout = vManage.logout()
table_onscreen = pd.json_normalize(device_list, record_path=['data'])
print("***" * 80)
print("Device list pulled from vManage:")
print("***" * 30)
print(table_onscreen)

table_onscreen.to_csv('device_file.csv', index=False)

print("***********************************************************************************************************")
print("CSV File Generated")
print("***********************************************************************************************************")
print(vManage_logout)
