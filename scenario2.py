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
        base_url_str = 'https://%s:8444/' % vmanage_ip
        login_action = '/j_security_check'
        login_data = {'j_username': username, 'j_password': password}
        login_url = base_url_str + login_action
        url = login_url
        sess = requests.session()
        login_response = sess.post(url=login_url, data=login_data, verify=False)
        self.session[vmanage_ip] = sess

    def get_request(self, mount_point):
        url = "https://%s:8444/%s" % (self.vmanage_ip, mount_point)
        response = self.session[self.vmanage_ip].get(url, verify=False)
        data = response.content
        return data

    def logout(self):
        url = "https://%s:8444/logout.html" % self.vmanage_ip
        return "Your session was closed", 401



vmanage_ip = input("Please enter vManage IP: ")
vmanage_user = input("Please enter vManage username: ")
vmanage_pass = getpass.getpass("Please enter vManage password: ")
vmanage = SdwanAPIOBJ(vmanage_ip, vmanage_user, vmanage_pass)
device_list = json.loads(vmanage.get_request("dataservice/device"))
vmanage_logout = vmanage.logout()

data_header = device_list['data']
device_file = open('device_file.csv', 'w')

csv_writer = csv.writer(device_file)

count = 0

for device in data_header:
    if count == 0:
        header = device.keys()
        csv_writer.writerow(header)
        count += 1

    csv_writer.writerow(device.values())

device_file.close()


print("***********************************************************************************************************")
print("CSV File Generated")
