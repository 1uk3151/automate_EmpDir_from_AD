param(
    [string]$OutFile
)

Get-ADUser -Filter 'UserPrincipalName -notlike "null"' -Properties * | select Surname, GivenName, OfficePhone, Office, Department, UserPrincipalName, Title | ConvertTo-Json | Out-File $OutFile