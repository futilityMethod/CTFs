# Over The Wire - Bandit

## level 0 
	All you need to do is to ssh into the host.
	`ssh -p <port> user@hostname`


## level 0 -> 1 
	Once logged into the host, simply cat the file which contains the password.

## level 1 -> 2
	The problem here is that the file is called '-', which cat/vim interprets as stdin. You have to `cat ./-`

## level 2 -> 3
	The password filename has spaces. Just tab complete and the shell escapes it for you.

## level 3 -> 4 
	The file is hidden, so you have to `ls -a` to see it.

## level 4 -> 5
	It's pretty easy to find the password file by just using cat.

## level 5 -> 6 
	You have to search through 20 directories to find the 1033 byte file that is not executable and is human readable.
	Using 'find' helped, but don't forget about hidden files!
	`find . -type f -size 1033c -exec ls -l {} \;`

## level 6 -> 7
	`find` is your friend again here.
	`find / -type -f -size 33c -group bandit6 -user bandit7 -exec ls -l {} \;`

## level 7 -> 8
	Here you have a big file, but are told exactly where it is. Use `grep`. 
	`grep data.txt | grep -A 2 'millionth'`

## level 8 -> 9 
	Looking for a non-repeated token, which is easy to find by chaining a few commands: 
	`cat data.txt | sort | uniq -u`

## level 9 -> 10
	The catch here is that the file is in binary format, so you need to tell `grep` to treat it as text. 
	`cat data.txt | grep -a '==='`

## level 10 -> 11
	All you need to do is base64-decode the file: 
	`base64 -d data.txt`

## level 11 -> 12
	Here you have an ROT13 encrypted string (each letter is shifted 13 places). You can use the `tr` utility to translate.
	Wikipedia actually tells you the command: 
	`tr 'A-Za-z' 'N-ZA-Mn-za-m' <<< [The ROT13 encrypted string]`

## level 12 -> 13 
	This one is a wild goose chase. The key is recognizing that the text file is a compressed hexdump, and needs to be turned back into a binary.
	The `xxd` utility creates hexdumps, but can also reverse them: 
	`xxd -r data.txt data.bin`
	Now we can use `file` to see what type of compressed file it is. Once you unzip the file and inspect the type, you'll see it's *another* compressed file. You have to repeat the decompress-inspect-decompress steps multiple times until you finally end up with a text file. The intermediate files are compressed using 'gzip', 'bzip2', and 'tar'. 

## level 13 -> 14
	There's an ssh key on the server. Copy it and save it locally. You need to change the permissions on the file before you can use it:
	`chmod 400 <sshkey>`
	 Then you use `ssh` with `-i <sshkey>`

## level 14 -> 15
	Now you can access the password for bandit14 at /etc/bandit_pass/bandit14. You need to use netcat to submit the password to the specified port in order to get the next password:
	`echo <pw> | nc localhost 30000`

## level 15 -> 16
	You need to use `openssl` to open an encrypted connection to the port before entering the password.
	`openssl s_client -connect localhost:30001`

## level 16 -> 17
	Finding the opem port was straigtforward using `nmap -p31000-32000 localhost` to specify the port range. But adding the  `-sV` flag showed that the port was 'tcpwrapped'.
	You're supposed to echo the password to the port using openssl s_client (as in the previous level) to get an ssh key. However, I wasn't able to get the port to return an ssl key. I cheated and stole the key from the internet. I am sorry. 

## level 17 -> 18
	Use `diff` to see the changed portion between the files.

## level 18 -> 19
	So when you attempt to ssh in, the .bashrc logs you right back out. The trick is to add `bash --noprofile --norc` to the end of the ssh command, so that you can log in without loading the profile.

## level 19 -> 20
	The binary file allows you to run commands as bandit20, so you just pass the command `cat /etc/bandit_pass/bandit20` as arguments.

## level 20 -> 21
	You'll need to open two terminals to get the password. On the first terminal, use netcat to listen on a tcp port:
	`netcat -l -p <some port>`
	In the second terminal, run the binary: 
	`./suconnect <some port>`
	Go back to the first terminal and enter the password.

## level 21 -> 22 
	Find the cron job and then inspect the script it runs. You'll see that the script writes the password to a specific file. You might have to wait for it to run, but after that, you can just cat the file.

## level 22 -> 23
	This level involves another cron job. The script it runs generates a md5 hash of "I am user bandit23" to use as a directory name. This is the catch. You can't just run the command in the script to get the hash, because you are a different user. You need to generate the correct hash in order to find the directory.

## level 23 -> 24
	This time, the cron job runs a script that executes whatever scripts are in var/spool/bandit24. However, you can't see what these scripts are. So I wrote a wrapper script to call the script and redirect the output to a file. See bandit24.sh

## level 24 -> 25
	You have to brute-force try all the 4-digit pins, so I wrote a script to do it. See bandit25.sh

## level 25 -> 26
	So I found an ssh key and a pin on the host. I saved both, but didn't actually need the pin for anything. The problem here is that the default shell for the user will log you out after printing some ASCII art on the screen. I spent a lot of time trying to force the use of another shell when logging in, but this was the wrong approach. It turns out that you can exploit the fact that the log-in script uses `more`. If you make the terminal window really tiny before you ssh in, the text file won't fit on the screen. `more` will allow you to scroll through the text. But don't. You can go into edit mode by typing `v`. This opens a text editor (vi or vim). Once you're in the text editor, you can open another file (namely, the password file):
	`:e /etc/bandit_pass/bandit26` 

## level 26 -> 27
	OK so now that you are bandit26, you can reset your own shell.	Get into vi mode like before and `:set shell=/bin/bash`. This will allow you to open a *normal* shell by entering `:shell`. Once you're in, there's a script in the home directory that lets you run commands as the next user:
	`./bandit27-do cat /etc/bandit_pass/bandit27`

## level 27 -> 28
	This level is just looking to see if you can clone a repo:
	`git clone ssh://bandit27-git@bandit.labs.overthewire.org:2220/home/bandit27-git/repo`
	You'll find the password.

## level 28 -> 29
	Clone the repo and check the commit history! You will have to check out a previous commit.

## level 29 -> 30
	Another git repo. This time, the password you want will be on another branch.

## level 30 -> 31
	This is another git repo, but this one is a bit tricky. There is only one commit on one branch, but by looking around, I found a tag in packed-refs inside the .git directory. I tried to checkout the tag, but it wasn't something that could be checked out. Had to read some documentation about tags to find out that you can un-hash the SHA-1 to see the original tagged content:
	`git cat-file -p <SHA-1>`

## level 31 -> 32
	Yet another git repo! You have to create the file specified with the correct content. The file name, however, is listed in the .gitignore. You'll have to force add, then commit.
	There's a hook that will print the password, but reject the commit.

## level 32 -> 33
	This level is running something that announces itself as UPPERCASE SHELL. None of the normal commands work, because it uppercases them and linux file system is case-sensitive. I did find that entering environment variables (i.e `$PATH`) will print the resolved value (uppercased, of course). What you have to know is that you can type `$0`, which is a special variable that expands to the name of the shell. Once entered, you are back to a useable shell, and it turns out you have permissions to view bandit33's password. 

## level 33 -> 34
	Once you log in as bandit33, you are done.
	


