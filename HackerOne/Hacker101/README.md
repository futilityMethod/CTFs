# HackerOne Hacker101 CTF

## A little something to get you started
A simple page with a message: `Welcome to level 0. Enjoy your stay.`

Opening the browser dev tools, you can see that an image called background.png has been loaded. Opening that image in a new tab, the flag is revealed.

<details><summary>Flag</summary>
	<p>	
^FLAG^9933f2b9362ed67cb07736d3c58fa8f0df309e517836266caadc1ef75536331f$FLAG$
</p>
</details>

## Micro-CMS v1
This one has 4 flags to capture.

The web page has three links: Testing, Markdown Test, and Create a new page. Visiting the links, the site appears to let you create pages using Markdown. On the create page, there is a note that Markdown is supported, but scripts are not. 

We shall see about that.

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

I just get a feeling I should try something similar in the title. Going back to edit the page and adding the same payload to the title results in...uri encoded characters. Hm.

But when I navigate back to home, the title is used as the link text for my page! And an alert pops up with the 2nd flag:
<details><summary>Flag 2</summary>
	<p>	
^FLAG^43ae863005e42e2d57b617fa862d533df75788fdca51a024621e63f59c948616$FLAG$
</p>
</details>

Two down, two to go.

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

## Micro-CMS v2 

Another Micro CMS site, this time with three flags to find. 

Visiting the changelog page, I am informed that auth has been added, and only admin users can add or edit pages. When I click the 'edit' link, I am directed to a login page. I'm not so lucky as to get in using admin/admin, but can see that the username and password are send as request params in the POST request.

Also found that there is a forbidded page 3.

Decided to give [OWASP ZAP](https://www.zaproxy.org/) a try, since I hadn't used it before. Just ran the automated scan to see if anything came up.

Turns out that the scan found one of the flags for me. So while attempting to navigate to an edit page in the browser, I'm redirected to the login page. But as ZAP has discovered, requesting the edit page while using the POST verb and including values for username and password in the request body will generate a response containing a flag:
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
