import paramiko
import json
from html_template import HTMLTemplate
from getpass import getpass
import yaml

with open ("./config.yaml", "r") as yaml_file:
    config = yaml.load(yaml_file, Loader=yaml.SafeLoader)
    ad_svr_hostname = config["ad_server"]["hostname"]
    ad_svr_username = config["ad_server"]["username"]
    ad_svr_password = config["ad_server"]["password"]
    html_output = config["web_server"]["html_output"]


# STEP 1: Run Get_ADUser script on domain controller which creates JSON file.
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=ad_svr_hostname, username=ad_svr_username, password=ad_svr_password)
stdin, stdout, stderr = client.exec_command(f"""Get-ADUser -Filter 'UserPrincipalName -notlike "null"' -Properties * | 
select Surname, GivenName, OfficePhone, Office, Department, UserPrincipalName, Title | 
ConvertTo-Json""")
stdin.close()
print(stderr.read().decode())
client.close()


# STEP 2: Pull user info from JSON file and place in HTML template.
htmltemplate = HTMLTemplate(html_file=html_output)

json_data = json.load(stdout)

htmltemplate.heading()

for i in range(len(json_data)):
    employee = json_data[i]
    htmltemplate.list_employee(
        lastname=employee["Surname"],
        firstname=employee["GivenName"],
        title=employee["Title"],
        department=employee["Department"],
        office=employee["Office"],
        phone=employee["OfficePhone"],
        email=employee["UserPrincipalName"]
    )

