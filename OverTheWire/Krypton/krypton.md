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
