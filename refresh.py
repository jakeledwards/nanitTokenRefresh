import requests
import shutil

# Read your tokens that you got from Postman and saved in refresh.token and access.token
with open('/config/python_scripts/refresh.token', 'r') as f:
    refresh = f.read()
with open('/config/python_scripts/access.token', 'r') as f:
    access = f.read()

url = 'https://api.nanit.com/tokens/refresh'
header = {
    "nanit-api-version" : "1",
    "content-type" : "application/json",
    "authorization" : "token " + access
    }
body = {"refresh_token": refresh}

response = requests.post(url, json=body, headers = header)

data = response.json()

# Once we get the new tokens we replace the old ones
with open('/config/python_scripts/refresh.token', 'w') as f:
    f.write(data["refresh_token"])

with open('/config/python_scripts/access.token', 'w') as f:
    f.write(data["token"])

# Set up these variables
filename = "/config/secrets.yaml" # This is where your actual secrets.yaml is saved
filename2 = "secrets.yaml" # This will just create this file in your python_scripts folder
key_to_update = "nanit_access_1" # I have 2 cameras. This is camera 1
key_to_update2 = "nanit_access_2" # Camera 2
# I have 2 cameras. This is camera 1. Make sure you put your babys uid between the / and the .
new_value = '-i rtmps://media-secured.nanit.com/nanit/YOURBABYSUID.' + data["token"] 
new_value2 = '-i rtmps://media-secured.nanit.com/nanit/YOURBABYSUID.' + data["token"] 

# Read the file into a list of lines, ignoring blank lines and lines that start with "#"
# If your secrets.yaml has anything other than comments, blank lines, and properly formatted secrets.yaml entries
# this script will not work
lines = []
with open(filename, "r") as f:
    for line in f:
        if line.strip() and not line.startswith("#"):
            lines.append(line.strip())

# Find the line with the key we want to update and replace it with the updated key-value pair
for i, line in enumerate(lines):
    key, value = line.split(": ")
    if key == key_to_update:
        lines[i] = f"{key_to_update}: {new_value}"
    elif key == key_to_update2:   # If you only have one camera, you don't need this section
        lines[i] = f"{key_to_update2}: {new_value2}"

# Write the updated lines back to the file
with open(filename2, "w") as f:
    for line in lines:
        f.write(f"{line}\n")

# Why am I doing this? I don't know. Saving directly over my /config/secrets.yaml didn't work
# and this did.        
move = shutil.copy(filename2, filename)