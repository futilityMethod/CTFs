# Over the Wire - Krypton

## level 0 -> 1
The password is given as a base64 encoded string. It needs to be decoded:

`echo S1JZUFRPTklTR1JFQVQ= | base64 -D`
<details><summary>Password</summary>
	<p>	
	KRYPTONISGREAT
</p>
</details>

## level 1 -> 2
Looking for a file called 'krypton2'. It's not in the home directory. Using `find / -name "krypton2"` I was able to find it in /krypton/krypton1.

It has 4 words in it, and is a rotation cipher. Just looking at the the text, I'm guessing the third word might be 'password'. So A maps to N. If my counting is correct, that's a shift of 13. I already have a command for ROT13 decrypt from solving Bandit11.

`tr 'A-Za-z' 'N-ZA-Mn-za-m' <<< [The ROT13 encrypted string]`

Bingo.
<details><summary>Password</summary>
	<p>	
	LEVEL TWO PASSWORD ROTTEN
</p>
</details>

## level 2 -> 3
This is another rotational substitution cipher encrypted password. The password is one token, so this time I can't try to guess what one of the words is like last time. However, I am also given an encrypt binary and a keyfile. How is that useful? Well, knowing this is a caesar cipher, each letter will deterministically map to another. So if I encrypt the alphabet, I can get the mapping and decrypt the password.

OMQEMDUEQMEK equals:
<details><summary>Password</summary>
	<p>	
	CAESARISEASY
</p>
</details>

## level 3 -> 4
This is not a simple substitution cipher now. I have three files to help. It could still be a substitution cipher that is not a simple shift.

Maybe I can do a frequency analysis to help out. I found an awk command to do this:

`awk -vFS="" '{for(i=1;i<=NF;i++)w[$i]++}END{for(i in w) print i,w[i]}' found1 found2 found3`

After finding the frequencies of the characters, this was mostly trial and error. I found an ordered list of letters by frequency in english. It seemed reasonable that the most frequent character in the cipher text would be 'e', especially since it occurred much more than the second most frequent. After that, I tried some swaps, but it was definitely clear I was on the wrong track. I looked at the encrypted password file and figured the word 'password' might be in there. Knowing the relative frequencies of the characters, I was able to find a sequential chunk that could be 'password'. I replaced the characters according to this guess, and that actually got me to a point where I could deduce other letters one at a time.

Maybe there's a more automated way to do this.

<details><summary>Password</summary>
	<p>	
	BRUTE
</p>
</details>

## level 4 -> 5

This one required some programming. What we have here is a [Vignere Cipher](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher). Basically, there is a key used to encrypt the text in the following way:
* Each letter in the key represents a shift. If the first character is 'D', then the plaintext will be turned into ciphertext by shifting the letter four places forward in the alphabet.
* The first letter of the key encrypts the first letter of the plaintext, the second letter of the key encrypts the second letter of the plaintext, and so on. After using the last character in the key, you start over at the first letter of the key again. Since we know our key is 6 letters long, every sixth character will be encrypted using the same key.
* To decrypt, the ciphertext is operated on in reverse. Each letter of the ciphertext is shifted BACK by the shift value of the corresponding key position.

In this level, we get the encrypted key, plus two text files encrypted using the same key. This gives us probably enough ciphertext to try breaking it using frequency analysis in the following way:
* Split the text into 6 groups, so that each group contains all the text encrypted by the same letter in the key.
* Count the frequencies of the characters within each group.
* Assume the most frequently occuring character per group represents 'E'
* Find the distance between that most frequent character and 'E' - This is our shift
* Translate that shift to a letter for that position in the key (e.g. if the shift was 4, the letter in the key will be 'D')
* Once we've built our key, go through the texts again, this time subtracting from the ciphertext to reveal the plaintext. So if the nth-modulo-6 letter of our ciphertext is 'Y', and the nth letter of the key is 'F', 'Y' is shifted back 5 places to 'T'

If all goes well, we should see all the plaintext. Luckily, there were no shenanigans here, and the assumption that the most frequently occuring character in each group represented 'E' was correct.

I wrote a [python script](krypton5.py) to solve.

<details><summary>Password</summary>
	<p>	
	CLEARTEXT
</p>
</details>

## level 5 -> 6

The instructions for this level:
```
FA can break a known key length as well. Lets try one last polyalphabetic cipher, but this time the key length is unknown.
```

Great. Now I don't even know how long the key is. Lucky for me, something called the [Index of Coincidence](http://practicalcryptography.com/cryptanalysis/text-characterisation/index-coincidence/) should be able to help me find the key length.

Basically, the index of coincidence measures how close a frequency distribution is to a uniform distribution. For texts in english, that value is typically near 0.06. Because our ciphertext is generated using substitution ciphers, that distribution won't change. Go [here](http://practicalcryptography.com/cryptanalysis/stochastic-searching/cryptanalysis-vigenere-cipher/) for a good explanation.

The idea is to try out different key lengths, partition the text accordingly, and get the average IoC across the partitions. So for a key of length 2, we split the text into 2 groups (one for each letter of the key), and get the IoC for each group. Finally we calculate the mean IoC.

By doing this for various potential key lengths, we should be able to guess what the real key length is by seeing which one produces an average IoC that's close to 0.06.

I wrote a [python script](krypton6.py) to help, and used the third found ciphertext (since it was the longest):
```
Average ic for key length 1is 0.0408107564477
Average ic for key length 2is 0.040874315115
Average ic for key length 3is 0.0488251314946
Average ic for key length 4is 0.0405931132399
Average ic for key length 5is 0.0407136937137
Average ic for key length 6is 0.0492468684764
Average ic for key length 7is 0.0402454400087
Average ic for key length 8is 0.0405921410917
Average ic for key length 9is 0.0624730040047
Average ic for key length 10is 0.040894984326
Average ic for key length 11is 0.0407623524473
Average ic for key length 12is 0.049488108895
Average ic for key length 13is 0.0404412077371
Average ic for key length 14is 0.0401688245191
```
Looking at the output, it seems most likely that the key length is 9.

I can use my script from the previous level to try cracking the cyphertext with an assumed key length of 9:
```
block 0: 
top character: O: 63
shift is 10
Key is K
block 1: 
top character: I: 66
shift is 4
Key is KE
block 2: 
top character: C: 74
shift is 24
Key is KEY
...
...
...
Key is KEYLENGTH
```
After that, I get the decrypted message and password output.
<details><summary>Password</summary>
	<p>	
	RANDOM
</p>
</details>

## level 6 -> 7

This appears to be the final level of the challenge.

The readme gives some background on the use of randomness in cryptographic algorithms, block vs. stream ciphers, and finally introduces the challenge in this level: an XOR stream cipher. 

There is a keyfile.dat and a binary called encrypt6, which have been used to encrypt krypton7. It suggests that I look into using [cryptool](https://www.cryptool.org/en/).

And for reference, the password is encrypted as `PNUKLYLWRQKGKBE`.

So that's taking forever to download. In the meantime, I scp'd the binary off the kryptos host and loaded it up in IDA to take a look. The program has some basic checking to make sure the command line arguments are provided and that the keyfile can be opened. Aside from that, what sticks out to me is a function called 'lfsr'.

LFSR stands for Linear Feedback Shift Register, which is a method of generating bit sequences for stream ciphers. If the LFSR is big enough, the resulting bit sequence can look random, but it will actually repeat. I liked the [RIT CSCI 462 Lecture Notes](https://www.cs.rit.edu/~ark/462/module02/notes.shtml) as a reference. 

So wild guess -- this challenge uses a fairly small LFSR. I also know the key must be pretty small, too. Though I can't read it, I can see that it's 11 bytes in size.

And if I can assume the cipher is pretty weak and ends up repeating, I should be able to verify that with a chosen plaintext. I can encrypt a whole bunch of the same character and find out where the pattern starts repeating.

Ok. So I created a file of 100 A characters and encrypted it using the binary. The resulting ciphertext:
```
EICTDGYIYZKTHNSIRFXYCPFUEOCKRN EICTDGYIYZKTHNSIRFXYCPFUEOCKRN EICTDGYIYZKTHNSIRFXYCPFUEOCKRN EICTDGYIY
```
I added spaces where it repeated, which looks like is every 30 characters. So the first A is shifted to E, the second to I, and so on. 

Before I assume I can use the known ciphertext as a set of shifts, let me try again with a file of 'B's:
`FJDUEHZJZALUIOTJSGYZDQGVFPDLSOFJDUEHZJZ`
So A + 1 is B, and likewise E + 1 is F. So yes, I can use the known ciphertext as a series of shifts.

To decrypt my key, I have to reverse it. The first shift of my known ciphertext to plaintext is 'E' to 'A', which is a shift of 4. So I'll shift the first character, 'P', backwards by 4, to get 'L'.

I wrote [another python script](krypton7.py) to help:

<details><summary>Password</summary>
	<p>	
LFSRISNOTRANDOM
</p>
</details>

And yay that concludes the Krypton box! 