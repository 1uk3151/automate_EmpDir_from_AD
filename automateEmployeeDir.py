import paramiko
import json
from html_template import HTMLTemplate
from getpass import getpass

# Active Directory Server parameters (hostname, username, password, powershell script location)

AD_SVR_HOSTNAME = "DC01"
    # Hostname of the server running Active Directory (Domain Controller)

AD_SVR_USERNAME = "luke.mosley"
    # User account on domain controller that has privileges to run Get-ADUser script

AD_SVR_PASSWORD = getpass()
    # Password of user. You will be asked for your password in the terminal after running script.

PWSH_SCRIPT = "C:\\it_files\\automateEmployeeDir\\AD_UserInfo_To_JSON.ps1"
    # Location of Get-ADUser script. This script should direct the output to a JSON formatted file. See file below:
        # param(
        #     [string]$OutFile
        # )
        #
        # Get-ADUser -Filter 'UserPrincipalName -notlike "null"' -Properties * |
        #   select Surname, GivenName, OfficePhone, Office, Department, UserPrincipalName, Title |
        #   ConvertTo-Json | Out-File $OutFile

JSON_FILE = "z:\\automateEmployeeDir\\employeedir.json"
    # Location of JSON output from the PWSH_SCRIPT

HTML_OUTPUT = "z:\\automateEmployeeDir\\employee.html"
    # Location of HTML output


# STEP 1: Run Get_ADUser script on domain controller which creates JSON file.
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=AD_SVR_HOSTNAME, username=AD_SVR_USERNAME, password=AD_SVR_PASSWORD)
stdin, stdout, stderr = client.exec_command(f"{PWSH_SCRIPT} -OutFile {JSON_FILE}")
stdin.close()
print(stdout.read().decode())
print(stderr.read().decode())
client.close()


# STEP 2: Pull user info from JSON file and place in HTML template.
htmltemplate = HTMLTemplate(html_file=HTML_OUTPUT)


with open(JSON_FILE, encoding="utf16") as json_file:
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


# ubietest = paramiko.SSHClient()
# ubietest.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ubietest.connect(hostname="ubietest", username="liason", password="Cisco123!")
# stdin, stdout, stderr = ubietest.exec_command("cp /home/luke/sharedfolder/automateEmployeeDir/employee.html /var/www/testsite")
# stdin.close()
# print(stdout.read().decode())
# print(stderr.read().decode())
# ubietest.close()


