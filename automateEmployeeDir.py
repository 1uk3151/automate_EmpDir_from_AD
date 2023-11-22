import paramiko
import json
from html_template import HTMLTemplate
from getpass import getpass

# Active Directory Server parameters (hostname, username, password, powershell script location)

AD_SVR_HOSTNAME = "TESTSERVER"
    # Hostname of the server running Active Directory (Domain Controller)

AD_SVR_USERNAME = "liason"
    # User account on domain controller that has privileges to run Get-ADUser script

AD_SVR_PASSWORD = getpass()
    # Password of user. You will be asked for your password in the terminal after running script.

HTML_OUTPUT = "/var/www/testsite/employee.html"
    # Location of HTML output on web server


# STEP 1: Run Get_ADUser script on domain controller which creates JSON file.
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=AD_SVR_HOSTNAME, username=AD_SVR_USERNAME, password=AD_SVR_PASSWORD)
stdin, stdout, stderr = client.exec_command(f"""Get-ADUser -Filter 'UserPrincipalName -notlike "null"' -Properties * | 
select Surname, GivenName, OfficePhone, Office, Department, UserPrincipalName, Title | 
ConvertTo-Json""")
stdin.close()
print(stderr.read().decode())
client.close()


# STEP 2: Pull user info from JSON file and place in HTML template.
htmltemplate = HTMLTemplate(html_file=HTML_OUTPUT)

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

