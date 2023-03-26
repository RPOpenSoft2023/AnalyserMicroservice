[System.Environment]::SetEnvironmentVariable('DATABASE_USER', 'postgres')
[System.Environment]::SetEnvironmentVariable('DATABASE_PASSWORD', 'demo')
[System.Environment]::SetEnvironmentVariable('DATABASE_NAME', 'analyser-db')

[System.Environment]::SetEnvironmentVariable('USER_MICROSERVICE', 'https://users-ms.apps.sandbox-m3.1530.p1.openshiftapps.com/user/api/')
[System.Environment]::SetEnvironmentVariable('BANKING_MICROSERVICE', 'https://banking-ms.apps.sandbox-m3.1530.p1.openshiftapps.com/banking/api/')
