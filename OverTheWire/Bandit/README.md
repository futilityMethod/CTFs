# Over The Wire - Bandit

## level 0 
All you need to do is to ssh into the host.

`ssh -p <port> user@hostname`


## level 0 -> 1 
Once logged into the host, simply cat the file which contains the password.
<details><summary>Password</summary>
	<p>
		boJ9jbbUNNfktd78OOpsqOltutMc3MY1
	</p>
</details>

## level 1 -> 2
The problem here is that the file is called '-', which cat/vim interprets as stdin. You have to `cat ./-`
<details><summary>Password</summary>
	<p>
	CV1DtqXWVFXTvM2F0k09SHz0YwRINYA9
	</p>
</details>

## level 2 -> 3
The password filename has spaces. Just tab complete and the shell escapes it for you.
<details><summary>Password</summary>
	<p>
	UmHadQclWmgdLOKQ3YNgjWxGoRMb5luK
	</p>
</details>

## level 3 -> 4 
The file is hidden, so you have to `ls -a` to see it.
<details><summary>Password</summary>
	<p>	
	pIwrPrtPN36QITSp3EQaw936yaFoFgAB
	</p>
</details>

## level 4 -> 5
It's pretty easy to find the password file by just using cat
<details><summary>Password</summary>
	<p>	
	koReBOKuIDDepwhWk7jZC0RTdopnAYKh
	</p>
</details>

## level 5 -> 6 
You have to search through 20 directories to find the 1033 byte file that is not executable and is human readable.
Using 'find' helped, but don't forget about hidden files!

`find . -type f -size 1033c -exec ls -l {} \;`
<details><summary>Password</summary>
	<p>	
	DXjZPULLxYr17uwoI01bNLQbtFemEgo7
	</p>
</details>

## level 6 -> 7
`find` is your friend again here.

`find / -type f -size 33c -group bandit6 -user bandit7 -exec ls -l {} \;`
<details><summary>Password</summary>
	<p>	
	HKBPTKQnIay4Fw76bEy8PVxKEDQRKTzs
	</p>
</details>

## level 7 -> 8
Here you have a big file, but are told exactly where it is. Use `grep`. 

`cat data.txt | grep -A 2 'millionth'`
<details><summary>Password</summary>
	<p>	
	cvX2JJa4CFALtqS87jk27qwqGhBM9plV
	</p>
</details>

## level 8 -> 9 
Looking for a non-repeated token, which is easy to find by chaining a few commands: 

`cat data.txt | sort | uniq -u`
<details><summary>Password</summary>
	<p>	
UsvVyFSfZZWbi6wgC7dAFyFuR6jQQUhR
	</p>
</details>

## level 9 -> 10
The catch here is that the file is in binary format, so you need to tell `grep` to treat it as text. 
	
`cat data.txt | grep -a '==='`
<details><summary>Password</summary>
	<p>	
	truKLdjsbJ5g7yyJ2X2R0o3a5HQJFuLk
	</p>
</details>

## level 10 -> 11
All you need to do is base64-decode the file: 

`base64 -d data.txt`
<details><summary>Password</summary>
	<p>	
	IFukwKGsFW8MOq3IRFqrxE1hxTNEbUPR
	</p>
</details>

## level 11 -> 12

Here you have an ROT13 encrypted string (each letter is shifted 13 places). You can use the `tr` utility to translate.

Wikipedia actually tells you the command: 

`tr 'A-Za-z' 'N-ZA-Mn-za-m' <<< [The ROT13 encrypted string]`
<details><summary>Password</summary>
	<p>	
	5Te8Y4drgCRfCx8ugdwuEX8KFC6k2EUu
	</p>
</details>

## level 12 -> 13 
This one is a wild goose chase. The key is recognizing that the text file is a compressed hexdump, and needs to be turned back into a binary.
The `xxd` utility creates hexdumps, but can also reverse them: 

`xxd -r data.txt data.bin`

Now we can use `file` to see what type of compressed file it is. Once you unzip the file and inspect the type, you'll see it's *another* compressed file. You have to repeat the decompress-inspect-decompress steps multiple times until you finally end up with a text file. The intermediate files are compressed using 'gzip', 'bzip2', and 'tar'. 
<details><summary>Password</summary>
	<p>		
	8ZjyCRiBWFYkneahHwxCv3wb2a1ORpYL
	</p>
</details>

## level 13 -> 14
There's an ssh key on the server. Copy it and save it locally. You need to change the permissions on the file before you can use it:

`chmod 400 <sshkey>`

Then you use `ssh` with `-i <sshkey>`

<details><summary>Password</summary>
	<p>		
		4wcYUJFw0k0XLShlDzztnTBHiqxU3b3e
	</p>
</details>

## level 14 -> 15
Now you can access the password for bandit14 at /etc/bandit_pass/bandit14. You need to use netcat to submit the password to the specified port in order to get the next password:
	
`echo <pw> | nc localhost 30000`
<details><summary>Password</summary>
	<p>	
	BfMYroe26WYalil77FoDi9qh59eK5xNr
	</p>
</details>

## level 15 -> 16
You need to use `openssl` to open an encrypted connection to the port before entering the password.

`openssl s_client -connect localhost:30001`
<details><summary>Password</summary>
	<p>		
	cluFn7wTiGryunymYOu4RcffSxQluehd
	</p>
</details>

## level 16 -> 17
Finding the open port was straigtforward using `nmap -p31000-32000 localhost` to specify the port range. But adding the  `-sV` flag showed that the port was 'tcpwrapped'.

You're supposed to echo the password to the port using openssl s_client (as in the previous level) to get an ssh key.

## level 17 -> 18
Use `diff` to see the changed portion between the files.

<details><summary>Password</summary>
	<p>		
```
	diff passwords.new passwords.old 
	42c42
	< kfBf3eYk5BPBRzwjqutbbfE887SVc5Yd
	---
	> hlbSBPAWJmL6WFDb06gpTx1pPButblOA
```
	</p>
</details>

## level 18 -> 19
So when you attempt to ssh in, the .bashrc logs you right back out. The trick is to add `bash --noprofile --norc` to the end of the ssh command, so that you can log in without loading the profile.
<details><summary>Password</summary>
	<p>			
	IueksS7Ubh8G3DCwVzrTd8rAVOwq3M5x
	</p>
</details>

## level 19 -> 20
The binary file allows you to run commands as bandit20, so you just pass the command `cat /etc/bandit_pass/bandit20` as arguments.
<details><summary>Password</summary>
	<p>			
	GbKksEFF4yrVs6il55v6gwY5aVje5f0j
	</p>
</details>

## level 20 -> 21
You'll need to open two terminals to get the password. On the first terminal, use netcat to listen on a tcp port:
	
`netcat -l -p <some port>`

In the second terminal, run the binary: 

`./suconnect <some port>`

Go back to the first terminal and enter the password.
<details><summary>Password</summary>
	<p>	
	gE269g2h3mw3pwgrj0Ha9Uoqen1c9DGr
	</p>
</details>

## level 21 -> 22 
Find the cron job and then inspect the script it runs. You'll see that the script writes the password to a specific file. You might have to wait for it to run, but after that, you can just cat the file.
<details><summary>Password</summary>
	<p>		
	Yk7owGAcWjwMVRwrTesJEwB7WVOiILLI
	</p>
</details>

## level 22 -> 23
This level involves another cron job. The script it runs generates a md5 hash of "I am user bandit23" to use as a directory name. This is the catch. You can't just run the command in the script to get the hash, because you are a different user. You need to generate the correct hash in order to find the directory.
<details><summary>Password</summary>
	<p>	
	jc1udXuA1tiHqjIsL8yaapX5XIAI6i0n
	</p>
</details>

## level 23 -> 24
This time, the cron job runs a script that executes whatever scripts are in var/spool/bandit24. However, you can't see what these scripts are. So I wrote a wrapper script to call the script and redirect the output to a file. 

See [script here](bandit24.sh)
<details><summary>Password</summary>
	<p>	
	UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ
	</p>
</details>

## level 24 -> 25
You have to brute-force try all the 4-digit pins, so I wrote a script to do it. 

See [script here](bandit25.sh)
<details><summary>Password</summary>
	<p>	
	uNG9O58gUE7snukf3bvZ0rxhtnjzSGzG
	</p>
</details>

## level 25 -> 26
So I found an ssh key and a pin on the host. I saved both, but didn't actually need the pin for anything. The problem here is that the default shell for the user will log you out after printing some ASCII art on the screen. I spent a lot of time trying to force the use of another shell when logging in, but this was the wrong approach. It turns out that you can exploit the fact that the log-in script uses `more`. If you make the terminal window really tiny before you ssh in, the text file won't fit on the screen. `more` will allow you to scroll through the text. But don't. You can go into edit mode by typing `v`. This opens a text editor (vi or vim). Once you're in the text editor, you can open another file (namely, the password file):

`:e /etc/bandit_pass/bandit26` 
<details><summary>Password</summary>
	<p>	
	5czgV9L3Xx8JPOyRbXh6lQbmIOWvPT6Z
	</p>
</details>

## level 26 -> 27
OK so now that you are bandit26, you can reset your own shell.	Get into vi mode like before and `:set shell=/bin/bash`. This will allow you to open a *normal* shell by entering `:shell`. Once you're in, there's a script in the home directory that lets you run commands as the next user:

`./bandit27-do cat /etc/bandit_pass/bandit27`
<details><summary>Password</summary>
	<p>	
	3ba3118a22e93127a4ed485be72ef5ea
	</p>
</details>

## level 27 -> 28
This level is just looking to see if you can clone a repo:

`git clone ssh://bandit27-git@bandit.labs.overthewire.org:2220/home/bandit27-git/repo`

You'll find the password easily.
<details><summary>Password</summary>
	<p>	
	0ef186ac70e04ea33b4c1853d2526fa2
	</p>
</details>

## level 28 -> 29
Clone the repo and check the commit history! You will have to check out a previous commit.
<details><summary>Password</summary>
	<p>	
	bbc96594b4e001778eee9975372716b2
	</p>
</details>

## level 29 -> 30
Another git repo. This time, the password you want will be on another branch.
<details><summary>Password</summary>
	<p>		
	5b90576bedb2cc04c86a9e924ce42faf
	</p>
</details>

## level 30 -> 31
This is another git repo, but this one is a bit tricky. There is only one commit on one branch, but by looking around, I found a tag in packed-refs inside the .git directory. I tried to checkout the tag, but it wasn't something that could be checked out. Had to read some documentation about tags to find out that you can un-hash the SHA-1 to see the original tagged content:

	`git cat-file -p <SHA-1>`
<details><summary>Password</summary>
	<p>		
	47e603bb428404d265f59c42920d81e5
	</p>
</details>

## level 31 -> 32
Yet another git repo! You have to create the file specified with the correct content. The file name, however, is listed in the .gitignore. You'll have to force add, then commit. There's a hook that will print the password, but reject the commit.
<details><summary>Password</summary>
	<p>		
	56a9bf19c63d650ce78e6ec0354ee45e
	</p>
</details>

## level 32 -> 33
This level is running something that announces itself as UPPERCASE SHELL. None of the normal commands work, because it uppercases them and linux file system is case-sensitive. I did find that entering environment variables (i.e `$PATH`) will print the resolved value (uppercased, of course). What you have to know is that you can type `$0`, which is a special variable that expands to the name of the shell. Once entered, you are back to a useable shell, and it turns out you have permissions to view bandit33's password.
<details><summary>Password</summary>
	<p>	
	c9c3199ddf4121b10cf581a98d51caee
	</p>
</details>

## level 33 -> 34
Once you log in as bandit33, you are done.
	


