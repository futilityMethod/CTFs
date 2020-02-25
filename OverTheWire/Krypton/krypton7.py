secret = "PNUKLYLWRQKGKBE"
known_text = 'EICTDGYIYZKTHNSIRFXYCPFUEOCKRN'

decrypted = ""

for i in range(0, len(secret)):
	# Find the shift amount between the current position
	# of the known ciphertext and 'A'
	shift = ord(known_text[i]) - ord('A')
	# subtract the shift from the current position of the encrypted key
	# and fit within alphabet range
	new_ch = ((ord(secret[i]) - shift) - 65) % 26
	# move back to ASCII capital range
	ch = chr(new_ch + 65)
	decrypted += ch

print decrypted