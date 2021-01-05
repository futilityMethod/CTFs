# HackerOne Hacker101 CTF

## A little something to get you started
<details><summary>Read More</summary>
A simple page with a message: `Welcome to level 0. Enjoy your stay.`

Opening the browser dev tools, you can see that an image called background.png has been loaded. Opening that image in a new tab, the flag is revealed.

<details><summary>Flag</summary>
	<p>	
^FLAG^9933f2b9362ed67cb07736d3c58fa8f0df309e517836266caadc1ef75536331f$FLAG$
</p>
</details>
<p>
</details>

## Micro-CMS v1
<details><summary>Read More</summary>
This one has 4 flags to capture.

The web page has three links: Testing, Markdown Test, and Create a new page. Visiting the links, the site appears to let you create pages using Markdown. On the create page, there is a note that Markdown is supported, but scripts are not. 

We shall see about that.

### XSS #1

Sure enough, simply including a `<scrpit>` tag doesn't work.
Taking a look at the [OWASP xss attacks page](https://owasp.org/www-community/attacks/xss/) provides some alternatives. One in particular works:
```
<b onmouseover=alert('Wufff!')>click me!</b>
```

So the alert pops up with the message. Was half expecting the flag. Taking a look at the raw response payload in the browser dev tools reveals something interesting. The flag has been added to the mouseover.
<details><summary>Flag 1</summary>
	<p>	
^FLAG^2a5c351ae314aa8524200fd2a2c9024eb891c3422c1af883bdc65a5e19f22265$FLAG$
</p>
</details>

### XSS #2
I just get a feeling I should try something similar in the title. Going back to edit the page and adding the same payload to the title results in...uri encoded characters. Hm.

But when I navigate back to home, the title is used as the link text for my page! And an alert pops up with the 2nd flag:
<details><summary>Flag 2</summary>
	<p>	
^FLAG^43ae863005e42e2d57b617fa862d533df75788fdca51a024621e63f59c948616$FLAG$
</p>
</details>

Two down, two to go.

### Gaining Access to Page 4
Taking a look at the existing 'Markdown Test' page, I see text that says adorable kitten. But I don't see any adorable kitten... I click on edit, and see that it's supposed to load an image from a url, that apparently doesn't exist. The OWASP xss page had examples using images. So I replace the url with one of the examples:
```
![adorable kitten]("http://url.to.file.which/not.exist" onerror=alert(document.cookie);)
```
Well. Now the page says 'adorable kitten)'. But it did change. Inspecting the network tab, I see my GET request for page 2, but then another GET for the file `not.exist" flag=` which of course 404s. flag??? Better check the raw response for page 2. And yep, actually the flag has been inserted into the img src. It's broken, but it's there. Unfortunately, it's flag 1 again.


In the meantime, I've noticed that the existing links direct to urls of 'page/1' and 'page/2'. When I create a test page, it's assigned to 'page/6'. Well, what about pages 3, 4, and 5? 

Page 3 and 5 return 404s. But page 4 returns a 403! 

Can I import page 4 into my own page? Html seems somewhat supported by Markdown, so I'll try to use an iframe:
`<iframe src="=4" ></iframe>`

The iframe loads! But it's still the Forbidden message. 

Ok, but what if I try accessing page 4 from the edit page? If I navigate to a page I can access, click the edit link, the url is '/page/edit/2'. Can I change it to a 4? 

Oh, turns out I can. And there is a flag:
<details><summary>Flag 3</summary>
	<p>	
^FLAG^1732e1ff3fab8cfd7cca9a26e8a6061b57a0a1953e88dc24191c6dfa5b4635e7$FLAG$ 
</p>
</details>

And then I found the last flag by accident, on the edit page. I fat-fingered the enter key and added a single quote to the end of the url. The page that loaded was flag number 4. I don't really understand this one.

<details><summary>Flag 4</summary>
	<p>	
^FLAG^2adb864946c28bd69723ed9f4694551e4319896dd70e827d8a66ef299f8971ea$FLAG$
</p>
</details>
<p>
</details>

## Micro-CMS v2 
<details><summary>Read More</summary>

### Initial Once-Over
Another Micro CMS site, this time with three flags to find. 

Visiting the changelog page, I am informed that auth has been added, and only admin users can add or edit pages. When I click the 'edit' link, I am directed to a login page. I'm not so lucky as to get in using admin/admin, but can see that the username and password are send as request params in the POST request.

Also found that there is a forbidded page 3.

### Running an Automated Scan

Decided to give [OWASP ZAP](https://www.zaproxy.org/) a try, since I hadn't used it before. Just ran the automated scan to see if anything came up.

#### XSS Strikes Again
Turns out that the scan found one of the flags for me. So while attempting to navigate to an edit page in the browser, I'm redirected to the login page. But as ZAP has discovered, requesting the edit page while using the POST verb and including values for 
username and password in the request body will generate a response containing a flag:

<details><summary>Flag 1</summary>
	<p>	
^FLAG^844e7cfe80058456158057d1e62fc271aa2e525b9b2a871ce55c7c1b3f4fee1b$FLAG$
</p>
</details>

ZAP tried some xss injection payloads for username and password, but trying it out myself shows that any arbitrary values will do. For instance:
```
POST /8cbf00c8e2/page/edit/1 HTTP/1.1
username=aaaa&password=bbbb
```

#### SQL Injection Vulnerability
Anything else in the scan results? Uh yea, got a pretty great error message from the login page with request parameters of `username=%27%22%3Cscript%3Ealert%281%29%3B%3C%2Fscript%3E&password=`:

```
Traceback (most recent call last):
  File "./main.py", line 145, in do_login
    if cur.execute('SELECT password FROM admins WHERE username=\'%s\'' % request.form['username'].replace('%', '%%')) == 0:
  File "/usr/local/lib/python2.7/site-packages/MySQLdb/cursors.py", line 255, in execute
    self.errorhandler(self, exc, value)
  File "/usr/local/lib/python2.7/site-packages/MySQLdb/connections.py", line 50, in defaulterrorhandler
    raise errorvalue
ProgrammingError: (1064, 'You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near \'"<script>alert(1);</script>\'\' at line 1')

```

This tells me that the web server is accessing a MariaDB (MySQL) database. More specifically, there is a table named admins, with username and password columns. Also get some full system paths. 
But most importantly, we have a SQL injection vulnerability.

The unescaped username param was `'"<script>alert(1);</script>`. Tried again with just `'` as the username (uri encoded the param as `%27` first), and was able to get the same error message.

### Scripting SQLi Payloads to Discover Credentials

Trying `username=%27%20OR%201%3D1%3B&password=` comes back with a new message on the login page: invalid password. So forcing a true conditional statement shows that there is a different message for a successful query on users in the admin table. I can probably use this to harvest a username.

I have some python scripts I'd put together for a previous CTF challenge which injects LIKE statements to brute force a password match one character at a time. Looking at the error message, looks like `%` characters will be a problem though. Some browsing of the MariaDB docs reveals the REGEXP operator may help. With a bit of trial and error, I arrive at the following payload to pass as the username:
```
' OR username REGEXP 'a';
```
This gives me the Unknown user message. However, changing the 'a' to 'e', I now see the invalid password message. So there is a username that contains an 'e', but not a username containing an 'a'.

Now I can modify my existing script (which I'll include in this folder). First, I iterate through lowercase characters and numbers (REGEXP is case insensitive, but so are usernames usually (fingers crossed)) and collect a set of characters matched in the table's usernames. Then I modify the payload a bit to `' OR username REGEXP '^(test_string)';`, which looks for matches at the beginning of the username. This will put the characters in order.

Running the script, I get:
```
('Found char ', 'e')
('Found char ', 'i')
('Found char ', 'm')
('Found char ', 't')
('Username so far:', 'e')
('Username so far:', 'em')
('Username so far:', 'emm')
('Username so far:', 'emmi')
('Username so far:', 'emmit')
('Username so far:', 'emmitt')
('Username:', 'emmitt')
```
Trying out the username 'emmitt' on the page with whatever password gives me the 'invalid password' message.

Ok. Now what do I do with the username? I can use it to modify the sql injection payload in order to brute force the password in a similar manner. Changing the username to `emmitt' AND password REGEXP '{0}.';` (where {0} is replaced by the test string), I should be able to reuse my script to find the characters in the password and the order in which they appear.

A few things I'll need to keep in mind: 
1. Passwords are probably case sensitive, but the REGEXP will return a match for either case. 
2. The password may not be stored in plain text. So what I get may not be the final result.

Result:
```
('Found char ', 'b')
('Found char ', 'e')
('Found char ', 'k')
('Found char ', 'o')
('Found char ', 'r')
('password so far:', 'b')
('password so far:', 'br')
('password so far:', 'bro')
('password so far:', 'broo')
('password so far:', 'brook')
('password so far:', 'brooke')
('password:', 'brooke')
```
Lucky for me, the password was actually all lower case, so I didn't have to go through the exercise of trying all case variants. Logging in with the credentials yields a flag:
<details><summary>Flag 2</summary>
	<p>	
^FLAG^2c28140afa9597a8d90aba72ad4e4708599f2e5aeee0f6e2efaca2227ccc57c7$FLAG$
</p>
</details>

There is one more flag to find, and I'm guessing that it's to be found on the restricted page 3. Using the credentials on the site didn't appear to leave me logged in, so I'll have to find another way to access page 3. 

### A Little Help from sqlmap 
One tool that was mentioned in the [PayloadsAllTheThings SQL Injection cheatsheet](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection) I've been referencing is [sqlmap](https://github.com/sqlmapproject/sqlmap). It's a command line tool that automates discovery and exploitation of SQL Injection vulnerabilities. Figure I may as well test it out, and see if I can get any more information. It's likely page content is also stored in the database. After cloning the repo and rtfm, I go with the following command:
```
python sqlmap.py -v -u http://[target]/login --method=POST --data="username=emmitt&password=brooke" --skip=password -a
```
This skips attempting to inject the password param since it's not injectable. The -a option is to dump EVERYTHING.
And it does. The admins table is dumped, followed by the pages table. Which includes the content for the forbidden page three. The flag is found:
<details><summary>Flag 3</summary>
	<p>	
^FLAG^3a4381fac9b9ea1150d772204981463d1724c56b9ab3fc0dd6ce4adcb94d15c3$FLAG$
</p>
</details>
<p>
</details>

## Encrypted Pastebin
<details><summary>Read More</summary>
Here we have a website called 'Encrypted Pastebin', with a message that reads:
```
We've developed the most secure pastebin on the internet. Your data is protected with military-grade 128-bit AES encryption. The key for your data is never stored in our database, so no hacker can ever gain unauthorized access.
```
The page also contains a form. And a 1x1 gif named 'tracking.gif'

### Messing With URL Query Params
Creating a test post results in a page ?post=4XgTu!iq7bU2Stw1W0vz5PZlM!VnkcmwQzJal95surrf!owYF-o-4rhMSomkVsYUrmpoN6OObkbmfiy4rlidibiQF0wAyyBhtJz3O164GMJLIP3ek1IcPIj0U2GG2rL7k3-oo5Q1tKU-Ey2WiwkcgliR9Y0eT3QuwfJfsJlcUoJm12bK0epc5oMzJBjTgytI5O5M!PkGQRKNoZ9HH3JVSw~~

Obvious thing to do is try navigating to a different post using the query params. Attempting to load post=1 results in the 
<details><summary>Flag 1</summary>
	<p>	
^FLAG^dedbcfb7edfbc14940b66e684c5fca7d6e2646da1c1a1e55bba7df6cf6b6d46e$FLAG$
</p>
</details>

And a cool error message...

### Follow the Error Messages

```
Traceback (most recent call last):
  File "./main.py", line 69, in index
    post = json.loads(decryptLink(postCt).decode('utf8'))
  File "./common.py", line 46, in decryptLink
    data = b64d(data)
  File "./common.py", line 11, in <lambda>
    b64d = lambda x: base64.decodestring(x.replace('~', '=').replace('!', '/').replace('-', '+'))
  File "/usr/local/lib/python2.7/base64.py", line 328, in decodestring
    return binascii.a2b_base64(s)
Error: Incorrect padding
```
That's helpful. So the post is decoded into json via sending a variable `postCt` to decryptLink in the file common.py. In decryptLink, at some point some `data` is base64 decoded. This b64d function replaces the `~` character with `=`, `-` with `+`, and '!' with '/' before calling python's base64.py. And this is where it barfs, upon attempting to base64 decode '1'.

Ok so now if I create a post with no title and no content, I still get a string:
`BNEwZagYCJgVuUg7iiZK5jvo7HZ7t7TiP0DfVR5B9xjnn5e6X4I5g8FIsY4nS2DR3ut-zpf4pCNXx030CS2Dbb-ScHANkAPjQSNO6776AdpWqp0l6S5Fcu7bGYN7QY0ra8aF239CTyTSE0Olxuw8Cq4HtE52FGu4a-jfKgqsfE6OVRoLjEB5jr8OZov99ViI4J5FIKE!beua3lpoOSFLlg~~`

I get a different string if I try again:
`ED1BnZaT3y4eVHR3XBaNiuYTL9zDkBsHPgOqrfN-qpiXE2atEraCwqg7EklTaLj9WuFDx!eSacgVtVZ4srfPFQZ3yB3JwJiYS!ZrRZQYN31NGt6L5lUBRnlTrlbR8pLPljsI1fFwtTQidqxBSNRt3cBfLe5z5kLJUD9tJe91DzixJytLM1SglWcs1T7t4-E2XRLLdm5XyqtlThTKAcVArA~~`

So I don't get the same cipher text each time, which lowers my chances that the site is just lying about using AES.

Since I can get raw error message info simply by supplying query params, maybe I get get more errors. What if I ask for a post that is valid base64 encoding?

for `?post=d2hvYW1p` I do get a new error message:
```
Traceback (most recent call last):
  File "./main.py", line 69, in index
    post = json.loads(decryptLink(postCt).decode('utf8'))
  File "./common.py", line 48, in decryptLink
    cipher = AES.new(staticKey, AES.MODE_CBC, iv)
  File "/usr/local/lib/python2.7/site-packages/Crypto/Cipher/AES.py", line 95, in new
    return AESCipher(key, *args, **kwargs)
  File "/usr/local/lib/python2.7/site-packages/Crypto/Cipher/AES.py", line 59, in __init__
    blockalgo.BlockAlgo.__init__(self, _AES, key, *args, **kwargs)
  File "/usr/local/lib/python2.7/site-packages/Crypto/Cipher/blockalgo.py", line 141, in __init__
    self._cipher = factory.new(key, *args, **kwargs)
ValueError: IV must be 16 bytes long
```

Some more information is leaked:
* AES is indeed being used here. 
* It's being used in CBC mode. 
* There is a static key. 
* The initialization vector must be 16 bytes long. However, since I am seeing this stack trace, my input must have an influence on how the IV is determined.

A question:
* Is there a database where the post content is stored? Or is it all contained in the post name?

If the form content is encrypted and used as the post name, then the post name length should be reflective of this. So I tested the tokens generated for an empty form, body with 1 character, 16 characters, 17 characters. The base64-decoded token length was 160 bytes each time. But maybe the tile is used? Testing similar plaintext titles also resulted in a constant size post token.

So it seems that some other name must be assigned to a post. Whatever this is is encrypted, but is not the content itself. There is a variable called postCt, which could stand for post count. But I would need to be able find the right encrypted payload for any number in order to use this to my advantage.

The website says that the keys aren't stored in the database. But the key could very well be in the source code. Or an env variable. 

I should be able to get at least one additional error case to leak. I know the length of the tokens now, so I can cobble something together that is "valid" in the sense that it will be decrypted, but doesn't refer to any known post. First, I will create a post and get a token (I just submit a blank form). Next I'll create a second post (just a body of 'a'). I base64 decode to hex, swap in the first 16 bytes of the 2nd token into the 1st, re-encode, and set it as the post query param. I do get a new error:
```
Traceback (most recent call last):
  File "./main.py", line 69, in index
    post = json.loads(decryptLink(postCt).decode('utf8'))
  File "/usr/local/lib/python2.7/encodings/utf_8.py", line 16, in decode
    return codecs.utf_8_decode(input, errors, True)
UnicodeDecodeError: 'utf8' codec can't decode byte 0x88 in position 0: invalid start byte
```
Or if I place the first 16 bytes from another encoded token into the one for 'a':
```
Traceback (most recent call last):
  File "./main.py", line 69, in index
    post = json.loads(decryptLink(postCt).decode('utf8'))
  File "/usr/local/lib/python2.7/encodings/utf_8.py", line 16, in decode
    return codecs.utf_8_decode(input, errors, True)
UnicodeDecodeError: 'utf8' codec can't decode byte 0xd2 in position 2: invalid continuation byte
```

Looks like whatever the plaintext is, it should be both utf-8 encoded and valid json. I have no way of divining what that json might look like, so I think it's time to read up on AES.

### Diving into AES CBC Mode

I like books, and I have a lot of them. Sometimes, they come in handy. This is one of those times. [Serious Cryptography](https://nostarch.com/seriouscrypto) not only has a chapter on block ciphers, but goes into the details of the AES implementation, its various modes of operation (including CBC), and my personal favorite section called 'How Things Can Go Wrong'.

This section describes the Padding Oracle Attack, which seems relevant, as it targets AES in CBC mode. In summary, the idea is this:
* AES encryption is a block cipher, so the plaintext is broken up into blocks to be processed by the algorithm. For AES-128, with a 128-bit key, these blocks are 128 bits long (16 bytes).
* CBC stands for Cipher Block Chaining. Each block of plaintext is XORed with the previous block of ciphertext before being encrypted, so the result at each step depends on the output of the step before.
* Since the first block of plaintext has nothing to be XORed with, an Initialization Vector is used. 
* If the plaintext is not a multiple of 16 bytes, it needs to be padded before the algorithm is applied. This works as follows: 
  * If the last block of plaintext fills 15 bytes, the last byte is set to 0x1
  * If the last block fills 14 bytes, the last 2 bytes are set to 0x2
  * etc..
 * The Padding Oracle Attack takes two consecutive blocks of ciphertext, C1C2, and attempts to find the plaintext (P2) of C2 by changing C1 one bit at a time.
 * If C1 XOR P2 ends with a valid padding byte, the ciphertext will be successfully decrypted.
 * The feasibility of this attack relies on the target behaving differently in a success or failure scenario.

I'm in luck, because this site just dumps all the error messages at me.

I wrote up a script in python, which I'll add to this repository. I give it one of the blobs of ciphertext that appears in the site url after creating a page. It base64 decodes it and breaks it up into 16 byte chunks. Then, taking two blocks at a time, it modifies the first block one at a time, sends a GET request to the site with the modified post param, and checks the response. I had to cycle through the various possible errors received and separate out the ones indicative of failed decryption. Errors that occur after the decrypt step are fine -- they mean decryption succeeded. When a 'good' response is encountered, that means we've found the value for that particular byte of C1 that when XORed with P2 produces a valid padding. We store this value for each byte, until all 16 bytes have been processed. When all the blocks are finished, they are XORed with the original ciphertext blocks to reveal the plaintext.

This takes a a bit of time, and involves spamming the server with tens of thousands of requests, but it doesn't seem to mind.

Eventually, I do get a plaintext, which includes a flag:
<details><summary>Flag 2</summary>
	<p>	
`{"flag": "^FLAG^9aa5a923f6a1d21368e406edc1aee5d7ef4dcb03266d40513d91fb5af22dec04$FLAG$", "id": "2", "key": "AyWeSm9qBGOo3IMqw8zSHA~~"}\n\n\n\n\n\n\n\n\n\n`
</p>
</details>

So yes, the post ids are numbered. And there's a key?! 

Another lovely error message was also revealed while my script ran:
```
Traceback (most recent call last):
  File "./main.py", line 71, in index
    if cur.execute('SELECT title, body FROM posts WHERE id=%s' % post['id']) == 0:
TypeError: 'int' object has no attribute '__getitem__'
```

Great. More SQL injection...

### To Be Continued...
<p>
</details>