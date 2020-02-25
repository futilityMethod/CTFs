# find key length candidates using index of coincidence 

def check_freq(x):
    freq = {}
    for c in set(x):
       freq[c] = x.count(c)
    return freq

def get_ic(text):
	frequencies = check_freq(text)
	total_count = len(text)

	sum = 0.0
	for k,v in frequencies.items():
		sum = sum + v * (v-1)
	ic = sum / (total_count * (total_count-1))
	return ic

with open ("file3", "r") as myfile:
	data = myfile.readlines()

	# test for key lengths 1 thru 15
	for i in range (1,15):
		blocks = [""] * i
		ic = [0.0] * i
		count = 0
		for ch in data[0]:
			blocks[count % i] += ch
			count = count + 1

		for j in range (0,i):
			ic[j] = get_ic(blocks[j])
			#print "ic is " + str(ic[j])
		average = sum(ic) / i

		print "Average ic for key length " + str(i) + "is " + str(average)
