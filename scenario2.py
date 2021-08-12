from IPython.display import display
import pandas as pd
import requests
from requests import session
import json
import csv
import getpass
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SdwanAPIOBJ:
    def __init__(self, vmanage_ip, username, password):
        self.vmanage_ip = vmanage_ip
        self.session = {}
        self.authenticate(self.vmanage_ip, username, password)

    def authenticate(self, vmanage_ip, username, password):
        base_url_str = 'https://{}:8444/'.format(vmanage_ip)
        login_action = '/j_security_check'
        login_data = {'j_username': username, 'j_password': password}
        login_url = base_url_str + login_action
        url = login_url
        sess = requests.session()
        login_response = sess.post(url=login_url, data=login_data, verify=False)
        self.session[vmanage_ip] = sess

    def get_request(self, mount_point):
        url = "https://{0}:8444/{1}".format(self.vmanage_ip, mount_point)
        response = self.session[self.vmanage_ip].get(url, verify=False)
        data = response.content
        return data

    def logout(self):
        url = "https://{}:8444/logout.html".format(self.vmanage_ip)
        return "Successfully logged out of vManage", 401


vmanage_ip = input("Please enter vManage IP: ")
vmanage_user = input("Please enter vManage username: ")
vmanage_pass = getpass.getpass("Please enter vManage password: ")
vmanage = SdwanAPIOBJ(vmanage_ip, vmanage_user, vmanage_pass)
device_list = json.loads(vmanage.get_request("dataservice/device"))
vmanage_logout = vmanage.logout()
table_onscreen = pd.json_normalize(device_list, record_path=['data'])
print("***"* 80)
print("Device list pulled from vManage:" )
print("***"* 30)
print(table_onscreen)

table_onscreen.to_csv('device_file.csv', index=False)


print("***********************************************************************************************************")
print("CSV File Generated")
print("***********************************************************************************************************")
print(vmanage_logout)
