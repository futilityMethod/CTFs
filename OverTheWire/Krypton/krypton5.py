# Key length determines how many blocks of text we break our files into
key_len = 9
files = ["file1", "file2", "file3", "file4"]
blocks = [""] * key_len

def check_freq(x):
    freq = {}
    for c in set(x):
       freq[c] = x.count(c)
    return freq

for f in files:
	with open(f) as fileObj:
		count = 0
		for line in fileObj:
			for ch in line:
				blocks[count % key_len] += ch
				count = count + 1

# For each string, calculate the character frequencies
key = {}
keyStr = ""
count = 0
for b in blocks:
	frequencies = check_freq(b);
	print "block " + str(count) + ": "
	#print frequencies

	# Get most frequent character 
	v, k = max((v, k) for k, v in frequencies.items())
	print "top character: " + k + ": " + str(v)
	
	# Calculate shift between character and e 
	shift = ((ord(k) - ord('E')) % 26) 
	print "shift is " + str(shift)

	# Check key - map shift to a character (Eg if shift is 4, key is 'd')
	key[count] = shift -1
	keyStr += chr(((ord('A') + shift) % 65) + 65)
	count = count + 1


	print "Key is " + keyStr

# loop through text subtracting shift
for f in files:
	with open(f) as fileObj:
		count = 0
		newText = ""
		for line in fileObj:
			for ch in line:
				newChar = chr(((ord(ch) - ord(keyStr[count % key_len])) % 26) + 65)
				newText += newChar
				count = count + 1		
		print newText