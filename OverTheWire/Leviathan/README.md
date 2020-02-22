# Over the Wire - Leviathan

## level 0
Get in the box:
`ssh -p 2223 leviathan0@leviathan.labs.overthewire.org`

## level 0 -> 1
There's a hidden folder called .backup with an html doc. All you have to do is grep for password.
rioGegei8m

## level 1 -> 2
There is a binary called check. When run, it asks for a password. Wasn't sure what to do, so I did a hexdump:
`hexdump -C check`
Broken up throughout the ascii, I saw 4 words which will be familiar if you've ever seen the movie 'Hackers'. Combine these, and the program will execute /bin/sh.
Lucky for me, it's running as leviathan2, so you can now see the next password.
ougahZi8Ta


## level 2 -> 3
Neat. There is a file called printfile. Seems useful. `./printfile /etc/leviathan_pass/leviathan3` isn't good enough.
Things I learned:
* `strace` and `ltrace` allow you to see what system calls and library calls (respectively) are used in an executable. eg: `strace ./printfile`
* Let's say you have 3 files in a directory: 'x', 'y', and 'x y'. `cat x y` prints the contents of the first two files, while `cat "x y"` prints the file with a space in the name.
* In this hypothetical scenario, the printfile program can check whether you have access to a different file than what it ultimately cats.
* `ln -s /a/file/you/want z` creates a symbolic link to a new file z
Ahdiemoo1j

## level 3 -> 4
Ok, so I pretty quickly broke the password for the program in the directory by running it with ltrace. This made it really easy to see what string my input was compared against.
It gave me a shell. whoami? leviathan4 :)
vuH0coox6m

## level 4 -> 5
There's a hidden folder named '.trash' in wheich leviathan 5 has left an executable named bin.
It printed out a binary string. Converting it to ASCII was all that was needed.
Tith4cokei

## level 5 -> 6
There's a binary called leviathan5 that spits out a password-y looking string.
Turns out it was the password. I'm not sure what the catch was. 

I went back again later, and ran the script again. This time, it errored out because it couldn't find a file called /tmp/file.log.
Ok.. Maybe I'll just create a symlink from the password file to the file it's looking for: `ln -s /etc/leviathan_pass/leviathan6 /tmp/file.log`
UgaoFee4li

## level 6 -> 7
There's an executable that wants a 4-digit pin. I had a script to brute-force 4 digit pins from bandit, so I reused:
`
for i in `seq -f "%04g" 0 9999`;
do
	./leviathan6 $i
done
`
Eventually I was granted a shell as leviathan7.
ahy7MaeBo9

## level 7
Oh.. it's over already!
