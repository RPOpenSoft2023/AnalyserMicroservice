[System.Environment]::SetEnvironmentVariable('DATABASE_USER', 'postgres')
[System.Environment]::SetEnvironmentVariable('DATABASE_PASSWORD', 'demo')
[System.Environment]::SetEnvironmentVariable('DATABASE_NAME', 'analyser-db')

[System.Environment]::SetEnvironmentVariable('USER_MICROSERVICE', 'http://34.105.83.175:80/user/api/')
[System.Environment]::SetEnvironmentVariable('BANKING_MICROSERVICE', 'http://34.82.249.105:80/banking/api/')
