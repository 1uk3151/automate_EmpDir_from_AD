import paramiko
import json
from html_template import HTMLTemplate


# Run script on domain controller. Script should output AD users in json format.
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname="TESTSERVER", username="luke.mosley", password="Cisco123!")
stdin, stdout, stderr = client.exec_command("C:\\sharedfolder\\automateEmployeeDir\\ad_to_json.ps1")
stdin.close()
print(stdout.read().decode())
print(stderr.read().decode())
client.close()


htmltemplate = HTMLTemplate(html_file="./employee.html")


with open("/home/luke/sharedfolder/automateEmployeeDir/employeedir.json", encoding="utf16") as json_file:
    json_data = json.load(json_file)

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


ubietest = paramiko.SSHClient()
ubietest.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ubietest.connect(hostname="ubietest", username="liason", password="Cisco123!")
stdin, stdout, stderr = ubietest.exec_command("cp /home/luke/sharedfolder/automateEmployeeDir/employee.html /var/www/testsite")
stdin.close()
print(stdout.read().decode())
print(stderr.read().decode())
ubietest.close()


