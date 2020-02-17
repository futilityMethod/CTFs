# Over The Wire - Natas

## level 0
Just log in to the webpage

## level 0 -> 1
View source to find password
gtVrDuiDfck831PqWsLEZy5gyDz1clto

## level 1 -> 2
You can't right click, but you can save the html and open it in a text editor.
ZluruAthQk7Q2MqmDeTiUij2ZvWy2mBi

## level 2 -> 3
If you inspect the page source, you'll see an image is loaded on the page. The image is stored in a directory named 'files'. You can visit the url for that directory and view all the files it contains.
sJIJNW6ucpu6HPZ1ZAchaDtwd7oGrD14

## level 3 -> 4
So this one has a hint when you view the source. A comment that says "not even Google will find it this time..." The ellipsis made me suspicious, so I tried to see if anything came up when I added /robots.txt to the url. And yeah...there's a directory named there. Visit that directory and you'll find it.
Z9tkRkWmpt9Qr7XrR5jWRkgOU901swEZ

## level 4 -> 5
A message which says I am visiting from "" instead of "http://natas5.natas.labs.overthewire.org/", plus a link to refresh the page. That link points to a php page. The div id is called viewsource. I opened the dev console before clicking the link. The page reloaded and the the "" was this time replaced by the current url. I took a look at the HTTP headers for the GET, and found that the referrer key contained the same value. By editing this header to contain the value specified in the message, I was able to resubmit the request and get the password.
iX6IOfmpN7AYOQGPwtn3fXpbaJVJcHfq

## level 5 -> 6
Logging in got me "Access disallowed. You are not loged in". Inspecting the HTTP response, I noticed there was a cookie named 'loggedin' which was set to 0. I edited the cookie to be 1 and refreshed the page.
aGoY4q2Dc6MgDq4oL4YtoKtyAg9PeHa1

## level 6 -> 7
This one has an input field. The view source link gives you the source. It includes a file. This file has a variable called secret - FOEIUWGHFEEUHOFUOIU
Now if you input that secret, you can get the password.
7z3hEENjQtflzgnT29q7wAvMNfZdh0i9

## level 7 -> 8
Two links. Home and About. On the About page, there is a helpful comment to tell you where the password is.
DBfUBfqQG69KvJvJ1iAbMoIpwSNQ9bWe

## level 8 -> 9
Back to the input secret again. Now there is an encoded secret. The user input is base64 encoded, reversed, and then converted from binary to hex. So I will convert to binary, reverse, and base64_decode. I used an online php sandbox to do this because it was easy.
oubWYf2kBq
W0mMhUcRRnG8dcghE4qvk3JA9lGt8nDl

## level 9 -> 10
This level has another input field that lets you search for words containing input. It greps through some dictionary.txt file...which doesn't appear to have anything interesting. 
But it uses passthru which executes an arbitrary command and directly passes the output to the user.
So I input: `dictionary.txt; ls -a; grep -i "2" `
That printed the directory for me. There are two files interesting.
.htpasswd with
natas9:$1$p1kwO0uc$UgW30vjmwt4x31BP1pWsV.
natas9:$1$H1h4/vhv$sGSIWyboB82roKx9lNLlE/
natas9:$1$G56GGLB5$XS1TpsdfDa8t4tvOx.V660

Wait. didn't read the insturctions. Should be able to look at level 10's password directly. Have to wait until the site is back up :(
`dictionary.txt; cat /etc/natas_webpass/natas10 `
nOpp1igQAkUzaI1GUUjzn1bFVj7xCNzu

## level 10 -> 11
Now there is some attempt at client-side input validation. The characters [,],|,&,; are removed. 
You can still hijack the use of grep though:
`"." /etc/natas_webpass/natas11`
U82q5TCMMQ9xuFoI3dYX61s7OZD9JKoK

## level 11 -> 12
A cookie is generated server-side which is json-endoded, xor_encrypted with some unknown key, and then base-64 encoded. This cookie contains two fields - the background color as specified by the user, and a show-password flag. When you submit a request with a new background color, there is a script that checks that the 'bgcolor' key exists and that the value matches a regex. It then assigns that raw value to the array -- not the match. I thought this might be the hint, but I couldn't find a way to trick the regex and sneak in anything useful.

So looking back at XOR encryption. We have a value XOR'd with a key. But we can get around not knowing the key! Let's take an example:
`     1 0 1 0
  xor 0 0 1 1
  -----------
      1 0 0 1
`
 Imagine `0011` is our key. What happens when we XOR our input and output:
 `    1 0 1 0
  xor 1 0 0 1
  -----------
      0 0 1 1
 `

 We get our key! Great. Now we can forge a cookie.
 I wrote a php script that slightly modifies the xor_encrypt function to take the key as a parameter. By passing it our base64-decoded default cookie as `$in` and the default value array as the `$key`, the actual key is revealed.
 Now, I can pass in the array I want to submit (where showpassword is set to yes), and encode it with the true key. This should get me in.
 EDXp0pS26wLKHZy1rDBPUZk0RKfLGIR3

## level 12 -> 13
Now I'm allowed to upload a jpeg. What could go wrong here?
So looking at the source, when a file is uploaded, a filename is randomly generated and returned back to you. While you're instructed to upload a jpeg, the file type isn't actually enforced. If you upload another type of file, you'll get a link returned to you that ends in a .jpeg extension. Where does the extension come from? Well it's not hardcoded in the php script. It's actually set in a hidden html tag. This gets passed up in the request, and is then used to specifiy the extension for the uploaded file. 

So I can change the extension in the hidden field to php. And then upload a php script (see natas12.php) that prints the contents of the password file when I load the document.
jmLTY0qiPZBbaKc9341cqPQZBJv7MQbY

## level 13 -> 14
K, now they only accept image files. 
They are doing this by checking that `exif_imagetype(..)` does not return false. So basically, any type of image file can pass this check. More specifically, any file that has a header of a valid image type will pass. 
I did a google search on embedding php into an image, and quickly found some information about adding php to gifs. I found a very tiny gif, opened it in a text editor, and basically pasted the same php code into it as used for the prevous level (changed the file to print, of course). I also changed the hidden element extension to gif.php (which is the extension I gave my file). Don't know if that's actually necessary (could have just named it .php). I've included the gif/php file in this repo.
Lg96M10TdfaPyVBkJdjymbllQ5L6qdl1

## level 14 -> 15
Now there is a username and password to enter. Viewing the source, I see that it's accessing a mysql database to check the login. I'm betting this is a sql injection vulnerability. For a quick refresher, I checked out the w3schools page on sql injection (https://www.w3schools.com/sql/sql_injection.asp).
Literally the second example works.
AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J

## level 15 -> 16
This level has a username input box and a button labeled "check existence". When a username is entered, a query is executed against a mysql database to check if the user exists.  If you enter 'natas16', the output shows that this user exists in the table. I can try to inject input to change the query, no part of the result will be output to me. So basically, you're limited to knowing whether or not a query produced any results.

The password can still be brute forced. At most, the password is 64 characters long (based on the schema revealed in the source file). If I can get a query that checks for username=natas16 and password=<the correct password>, I'll get a response that indicates the entry exists. 

I had to figure out how to generate the url to make this http request in order to write a script for the brute force attack. The key here is using the sql 'LIKE' operator, to figure out what characters the password contains, and in what order. 

The script ran for at least 10 minutes, but brute-forcing is slow. With patience, the password was got.
WaIHEacj63wnNIBROHeqi3p9t0m5nhmh

## level 16 -> 17
Now we are back at searching for text in 'dictionary.txt'. This time, [], ;,|,\`,and ' are filtered out.
But you know what's cool? If you enter `$0` into the box, you get a list of words that contain 'sh'. So shell variables are expanded. I can run something like `$(grep x /etc/natas_webpass/natas17)` and the result is used by the wrapping grep command as search text. This in itself isn't usefull since the password isn't going to match anything in dictionary.txt. But I could append the output to another search string. For example, 'apples' returns 3 results. If I run `apples$(grep x /etc/natas_webpass/natas17)` , I get the same results, because there is no 'x' in the password, so the expression just evaluates to apples. But if I run `apples$(grep b /etc/natas_webpass/natas17)`, I get no results. This must be the case because the password contains a b, so the expression evaluates to applesb, which is not a word in dictionary.txt.

So I've modified the script I used in the last level to perform a similar brute force attack. By trying all the characters in the expression, I can find out which are contained in the password. Then, I can start building the password one character at a time until finally I have it.
8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw

## level 17 -> 18
On this level, looks like we are back to SQL injection. From the source, it appears mostly the same as level 15, but this time, you get no output either way. So I don't even know if the user exists or not. I had no idea where to start with this one, so I browsed through a few other people's write-ups for hints (trying to only read as far as needed to get a clue). And this is how I learned about time-based attacks.

Apparently, you can add a sleep into a sql command. Remember in level 15, I was able to use the 'LIKE' comparison operator to test whether characters were contained in the password of interest. Well, I can combine these two tools in the following way: I can craft a query that sleeps if the password comparison check succeeds: ` select * from users where username=natas18 and password like binary <test value> and sleep(5)` 
If the first two conditions are true, the sleep executes. Otherwise, the boolean expression evaluation short-circuits after the first false.
So instead of checking my queries against some text I expect in the response, I can check if my queries take a long time to complete to determine what's stored in natas18's password.

See natas18.py for the script.
xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP

## level 18 -> 19
This level has a login form, which directs me to log in with admin credentials to receive natas19's password.
By viewing the source provided I found out that this page is using Sessions to manage logged in user's state. When I log in with natas18's credentials, I can verify that I am assigned a PHPSESSID cookie. 
On the server, the \_SESSION array has a key called 'admin', which is set to 1 if the user is admin. When a page loads and a valid PHPSESSID cookie is included in the http request, the code just checks to see if the 'admin' variable for the session has the correct value before deciding to print natas19's password in the response.
So it seems that I can just try passing different PHPSESSID values along with my requests to see if an active session for admin already exists on the server. Bonus for me, I can see that the max session id possible is 640, so I know I won't be brute forcing forever.
See the attached natas19.py script for the solution.
Lo and behold, it works.
4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs

## level 19 -> 20
Instructions say this level uses mostly the same code as the previous level, except session IDs are no longer sequential.
So I log in to see what my session id looks like: `PHPSESSID:"3237332d6e617461733139"`
First guess was that it was base-64 encoded, but there were no printable characters found (at least for UTF-8 charset). Maybe it's hex? Sure, just a really big number.
Can I just brute force all day? Seems annoying.
I thought maybe it's a hash, so I tried putting it in crackstation.net which claims to have a massive set of rainbow tables, but there was no match found.
PHPSESSID:"3237332d6e617461733139" - 273-natas19
PHPSESSID:"  37372d6e617461733139" -  77-natas19
PHPSESSID:"3630372d6e617461733139" - 607-natas19
PHPSESSID:"3237392d6e617461733139" - 279-natas19
PHPSESSID:"3430382d6e617461733139" - 408-natas19
PHPSESSID:"3334352d6e617461733139" - 345-natas19
PHPSESSID:"3434312d6e617461733139" - 441-natas19

So the end bit stays the same. That means it's probably not a hash of something. It's not base64. But actually, it's hex representation of ascii.
Converting 2d6e617461733139 from hex to ascii reveals '-natas19'

Let's say that the number in front of -natas19 is still constrained within the range 0-640 and try editing the last script to work...

I ran it the first time, and got no hits. I looked closely at the wording on the page -- it says to login as 'admin' to get the credentials for natas20. So I altered my script so that the suffix was -admin and ran it again. That was a good guess.
eofm3Wsshxc5bwtVnEuGIlr7ivb9KABF

## level 20 -> 21
This level also requires you to login as an admin to retrieve the next password, but also has an input field that allows you to change your name.
Source code is provided again, and this time I have to learn a little bit about how session data can be managed with php. There's a function `session_set_save_handler` which takes a set of callbacks for opening, closing, reading, writing, and destroying sessions. In this example, only read and write handlers seem to be functional.

I can also see that session ids are only allowed to contain letters, numbers, -, and spaces. My assigned session id is `PHPSESSID:"qj3reabo65f24jvsg50d0008r6"`
The session's data is stored in a file located at <Session Save Path>/mysess_{session id}. This file has permissions set to 0600.

When you set a name, this gets saved to the session array, and is reflected back into the input field. Maybe there is a way to inject something here. 

Going back to the code where the session data is saved, each key-value pair is saved into the file:
name joe
key value

When it's read back out, it splits lines out by detecting \n, and then each line is broken into key and value based on encountering a whitespace character.
Maybe I can set a name such that when it is read back from the file, it's read as an additional key-value pair. I will have to hide a \n in there. It doesn't look like 

Using the developer tools in the browser, I was able to modify the previous POST request to send params of:
`%0Aadmin%201`

When I loaded the page again, I was admin.


## level 21 -> 22
Loggin into this page, I'm told again to login as admin, but also that the page is "colocated" with another url. Following the link, I have to log in again to see some kind of css style experimenter form. I have source code to both pages.
I'm going to assume that 'colocated' probably means that sessions are somehow shared between both sites. So if I can set admin in the css form site, which takes input, I might be able to hijack that session from the other page.

Looking at the source code, I see that it restricts keys received in the POST request to those expected on the form. I also see that if a 'submit' key is in the request, it will store each key-value pair in the request to the SESSION array. 

Again, I used the dev tools in the browser to modify the request params. I tried adding 'admin=1' in addition to the existing params, but that didn't work. I tried resubmitting the POST with just `submit=Update&admin=1` as the request body. I then copied the session id cookie after the request completed, went back to the natas21.natas.labs.overthewire.org page, and overwrote that session id. I resumbitted the GET with this new session ID, and that did the trick.

chG9fbe1Tq2eWVMgjYYD1MsfIvN461kJ

## level 22 -> 23
This is a blank page, except for a view sourcecode link. 

The source code checks for an array key of "revelio" in the GET request. If it exists, it should print the credentials. However, there is also some logic executed right after session_start() that calls `header("Location: /");` if there is no admin=1 stored in the session array. What does this do?

Reading up on php.net - "Location:" is one of two special case header calls. It sends the header to the browser along with a REDIRECT(302) status code. 
I can confirm that when I add "revelio" as a param in the url, I get a 302 back from the server, followed by a second GET without any params (the browser redirected). 

Another thing that I noticed in the documentation for header Location was that exit should be called after setting the location to prevent the rest of the code from being executed. This is absent in the source code example. So hypothetically, the rest of the php should be executed, meaning credentials will be displayed as long as 'revelio' in in the request.

While the browser seemed to automatically redirect once receiving a 302 response code in the header, curl does not automatically follow redirects. So a simple curl command revealed the password:
`curl -u natas22:chG9fbe1Tq2eWVMgjYYD1MsfIvN461kJ http://natas22.natas.labs.overthewire.org?revelio`

D0vlad33nQF0Hz2EP255TP5wSW9ZsRSE

## level 23 -> 24
Here we have an input box labelled 'Password' with a Login button. And a view sourcecode link.
This one has nothing to do with sessions. It looks for a passwd request parameter and checks that it contains the substring 'iloveyou' and also that it is greater than 10.
There is also a comment `//morla / 10111`. The total length of the input is constrained to 20 characters.
I literally just took a wild guess and added `?passwd=10111iloveyou` to the url and that was all I needed to do.

OsRmXFguozKpTZZ5X14zNO43379LZveg

## level 24 -> 25
This looks almost exactly like the previous level, except this time, the string that passwd value is compared against is censored. That morla comment is still there.

This uses strcmp() to check the value of passwd against some censored value. It's a weird check. strcmp returns 0 if equal, or a negative/positive integer in other cases. The source checks for !(strcmp(val1, val2))...which is a weird way of checking for a 0 return value. 
Reading the comments on the php.net documentation for the strcmp() function are interesting. There are ways certain comparisons that return unexpected NULLs or errors. One interesting comment showed a problem with using strcmp on a query param:

```
<?php
if (strcmp($_POST['password'], 'sekret') == 0) {
    echo "Welcome, authorized user!\n";
} else {
    echo "Go away, imposter.\n";
}
?>

$ curl -d password=sekret http://andersk.scripts.mit.edu/strcmp.php
Welcome, authorized user!

$ curl -d password=wrong http://andersk.scripts.mit.edu/strcmp.php
Go away, imposter.

$ curl -d password[]=wrong http://andersk.scripts.mit.edu/strcmp.php
Welcome, authorized user!
```

So I tried this out...altered the query param of passwd to be passwd[]. Resubmitted the request and got a funny response:
```
Warning: strcmp() expects parameter 1 to be string, array given in /var/www/natas/natas24/index.php on line 23

The credentials for the next level are:

Username: natas25 Password: GHF6X7YwACaYYssHVY05cFq83hRktl4c
```

PHP is...special.

## level 25 -> 26
Ok, I'm presented with some weird long quote about God. There's a language drop-down, and good ol' view source code link.
Looks like session ids are back, and lang is a query string. The available options are 'en' and 'de'.
Viewing the source, I see that the code uses the lang param to access a file stored at language/en. It's passes to a function called safeinclude() which strips out `../` and blocks anything containing the substring "natas_webpass", which is where the password is stored.

One thing to note, is that if a directory traversal or password file access is attempted, this is logged in a file at /var/www/natas/natas25/logs/natas25_{session_id}.
The log contains a timestamp, the http user agent, and the message. There is no input validation on the user agent, so maybe this is a place to inject some php.

Using [php include](https://www.php.net/manual/en/function.include.php), I might be able to include the password file in the log.
I'll try this by setting the user agent in the request to 
`
<? include "/etc/natas_webpass/natas26" ?>
`
Also, there's a little bug in the safeinclude function. It detects directory traversal by looking for ../ and then logs the attempt before stripping out the characters. But then it continues to check for the file's existence and include it. So if I use ....// in place of ../ , the "corrected" string will still contain ../ which allows me to traverse.

So I should be able to print the log file (which now hopefully includes the password) by letting the lang param to `....//logs/natas25_{session_id}.log`

My edited request looks like this:
`
GET /?lang=....//logs/natas25_mysess.log HTTP/1.1
Host: natas25.natas.labs.overthewire.org
User-Agent: <? include "/etc/natas_webpass/natas26" ?>
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
DNT: 1
Authorization: Basic bmF0YXMyNTpHSEY2WDdZd0FDYVlZc3NIVlkwNWNGcTgzaFJrdGw0Yw==
Connection: keep-alive
Cookie: PHPSESSID=mysess
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0
`

And the server responds with:
```
[10.02.2020 14::09:04] oGgWAJ7zcGT28vYazGo4rkhOPDhBu34T
 "Directory traversal attempt! fixing request."
 ```

oGgWAJ7zcGT28vYazGo4rkhOPDhBu34T

## level 26 -> 27

Oh great. This level has four input boxes! It commands me to draw a line by entering values for x1, y1, x2, and y2. 
I tried entering 4 values and it returned a black png...hmm.

Let's read the given source:
There is a Logger class that handles writing to a log file for the duration of the session. 
There is a showImage function which builds an img tag out of the given file name.
There is a drawImage function which creates a png and writes it to the given file .
There is a drawFromUserdata function which gets the coordinates from the request and also reads any drawings stored as cookies.
Finally, there is a storeData function that gets the values from the request and serializes them before setting as the "drawing" cookie.

I don't see the log class actually being used by the other parts of the code, interestingly. 

So I don't know that I can trick the showImage to generate something other than an image. But the storeData function looks like it just reads the coordinates straight into a cookie that's base64 encoded. Maybe I can try injecting php similar to the previous level as a coordinate, and get the password included, and then decode the base64 blob that's returned as a cookie.
 
I tried url-encoding `<? include "/etc/natas_webpass/natas27" ?>` as the x1 value, and then base64 decoding the drawing cookie:
`
a:3:{i:0;a:4:{s:2:"x1";s:1:"1";s:2:"y1";s:1:"2";s:2:"x2";s:1:"5";s:2:"y2";s:1:"6";}i:1;a:4:{s:2:"x1";s:1:"7";s:2:"y1";s:1:"5";s:2:"x2";s:1:"4";s:2:"y2";s:1:"3";}i:2;a:4:{s:2:"x1";s:42:"<? include "/etc/natas_webpass/natas27" ?>";s:2:"y1";s:1:"5";s:2:"x2";s:1:"4";s:2:"y2";s:1:"3";}}
`

So my php is set in there, but not resolved. I also get the following error displayed:
`Warning: imageline() expects parameter 2 to be long, string given in /var/www/natas/natas26/index.php on line 66`

The decoded cookie looks a little weird, so upon closer inpection of the source, I see that php serialize() is used before it is encoded. I looked up the docs for serialize, and then also [unserialize](https://www.php.net/manual/en/function.unserialize.php) which has a big warning about not trusting user input while unserializing as it could result in code loading and execution.

So I think I'm on the right track by trying to get code loaded from the drawing cookie.

I need to be able to write to a file that I can access later somehow. There's still this unused Logger class in the source code, which writes messages to a file. At this point, I needed a hint. Searching around, I learned about php object injection, which is related to the vulnerability in unserialize loading and executing arbitrary code. From my understanding, if the php code on the server uses a class that implements a method like "\__wakeup" or "\__destruct" (Logger implements one of these!), and this class has already been declared by the time unserialize() has been called, you have a good case for an object injection attack.

Looking at the examples on [OWASP.org](https://owasp.org/www-community/vulnerabilities/PHP_Object_Injection), I see that the idea is to write some code that overrides the existing class's implementation, serialize it and base64 encode it, and pass it up as a cookie.

I have a php script (Natas26.php) included in the repository that redefines the initialization of the Logger class's private members so it writes the contents of the password file to a location of my choosing. I picked the img/ directory, since the code clearly already has the ability to read and write to this location.
Finally, the script encodes and serializes the object.

I use the blob that is output and replace the "drawing" cookie value before submitting the request.
The page reloads with an image, but also with this error message:
`
Fatal error: Cannot use object of type Logger as array in /var/www/natas/natas26/index.php on line 105
`

Ok, but is my file there? I go to natas26.natas.labs.overthewire.org/img/myfile.php and:

55TBjpPZUUJgVP5b3BnbG6ON9uDPVzCJ 

## level 27 -> 28

This is another user name and password page. Entering 'natas27' and the level password doesn't log me in. Taking a look at the source, there's a comment:
`//morla / 10111`
This seems to work, as the page displays a message: User morla was created!

There is also a comment stating that the database is cleared every 5 minutes. Guessing this will be important -- potentially there will be a time window during which I must complete my attack.

Starting from the bottom of the source code (to see what happens once a request is received), it's now clear why morla/10111 worked. First, a mysql database is accessed using the natas27 credentials. Then the credentials passed into the request are tested. If they are valid, a welcome message is displayed along with some data. If the user exists but the password is invalid, a message is returned stating the password is wrong. However, if the user doesn't exist in the table, it creates one using the credentials provided. So Morla did not exist in the table, but Natas27 did.


I'm going to look athe createUser function first. It takes a link to the DB, and the request username and password values. Both username and password are passed through a function called mysql_real_escape_string before being substituted into a prepared query. 

Time to read the [docs](https://www.php.net/manual/en/function.mysql-real-escape-string.php). First there is a nice big red warning box, saying this extension was deprecated in PHP 5.5.0. Let's see why. So apparently, the function prepends backslashes to `\x00, \n, \r, \, ', ", \x1a`. This info is immediately followed by a big security caution box, stating that the character set much be set at the serverl level or by mysql_set_charset in order to affect mysql_real_escape_string. Ok...

Ok, there is a note that the method does not escape % or _ which are wildcards in mysql w/ LIKE, GRANT, or REVOKE. I'll put that in the back of my mind for now.

Now let's take a look at validUser, which takes the DB link and the requested username. That seems to be a straightforward check to see if any matching rows come back from querying the DB with the user name.

The checkCredentials function takes DB link, username, and password. Escapes the input, and queries the DB for entries where both fields match.

Now the last method, dumpData. This only takes the username and a link to the DB. And it just does a SELECT * on the username. So you'd get all the data for that user.

So I think my first approach should be to craft a sql injection payload for the password field that circumvents the checkCredentials function. If that works, I should be able to get the password for Natas28.

After spending a lot of time reading up on how mysql_real_escape_string works, I started to feel like I was banging my head against the wall. Especially after running into [this post](https://www.sqlinjection.net/advanced/php/mysql-real-escape-string/) on sql injection avenues for the function. It looked like there were two potential avenues: exploiting an unsanitized numeric parameter (where the value isn't wrapped in single quotes), or slipping in a wild card character in a LIKE query. The code had neither of these vulnerabilities. 

Maybe I should look for another way. 

I know that Natas28 is a valid user name. I could always brute force the password. I know the max length is 64 characters. Examing the characters used in the previous passwords, I could constrain the characterset to 66 (a-z + A-Z + 0-9). That's a stupidly huge number of passwords to try (ie 66^0 + 66^1 + ... + 66^64). Even if I assume the password will be 32 characters exactly (as the previous ones seem to have been), that's still way too many passwords to try.

Ugh. What if I try to create a username or password with more than 64 characters?
I tried entering 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaz' (64 a + 1 z), with no password, and it reflected it back to me as being created.
If I try entering it again, I again see a message that the user was created. Hmmm.
Ok so what if I enter exactly 64 a characters? Now I see my user data. So somehow the truncated user is what actually gets stored. 

I found this quote from the [mysql docs](https://dev.mysql.com/doc/refman/8.0/en/char.html)
```
For those cases where trailing pad characters are stripped or comparisons ignore them, if a column has an index that requires unique values, inserting into the column values that differ only in number of trailing pad characters will result in a duplicate-key error. For example, if a table contains 'a', an attempt to store 'a ' causes a duplicate-key error. 
```

So this means that I can't try to create a user 'natas28 ' or 'natas28 [+ 60 spaces]' because the whitespace is ignored when comparing against 'natas28'. BUT. If I pad it with enough whitespace AND put a character after that, I can get past the comparison when trying to create a new user. And as I've seen with my experiment above, the username will be truncated to 64 characters when it's stored.

The next query that checks for username='natas28', BOTH results will be returned, because my now-truncated fake-Natas28 won't have its trailing whitespaces counted in the comparison.

When I put this to the test (1. create an "evil" natas28 with no password, 2. Log in as regular Natas28 with no password), I get this result: 

Welcome natas28!<br>Here is your data:<br>Array
(
    [username] =&gt; natas28
    [password] =&gt; JWwR438wkgTsNKBbcJoowyysdM82YjeF
)

## Level 28 -> 29

The situation just got real -- no source available in this level. I'm presented with a "Joke Database" with a text input box and search button.
Just to check, I took a look at the page html source. The only thing interesting is the following comment:
`<!-- 
    morla/10111 
    y0 n0th!
-->`

If I hit search without entering any text, The response comes back with the following location: 
` search.php/?query=G%2BglEae6W%2F1XjA7vRm21nNyEco%2Fc%2BJ2TdR0Qp8dcjPLof%2FYMma1yzL2UfjQXqQEop36O0aq%2BC10FxP%2FmrBQjq0eOsaH%2BJhosbBUGEQmz%2Fto%3D`
The browser then redirects to this page, and displays some jokes.

Url decoded, this is `G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPLof/YMma1yzL2UfjQXqQEop36O0aq+C10FxP/mrBQjq0eOsaH+JhosbBUGEQmz/to=`
Which looks like base64 encoding. 

I tried with the query 'cow', and got redirected to `G%2BglEae6W%2F1XjA7vRm21nNyEco%2Fc%2BJ2TdR0Qp8dcjPIpuCdGvo%2FlSLmvzc7sI%2Bm6mi4rXbbzHxmhT3Vnjq2qkEJJuT5N6gkJR5mVucRLNRo%3D`
Which apparently has no jokes.

So I'm unsure what these strings of characters are, but I notice the url decoded forms have several forward slashes. I tried removing everything after the first slash and resubmitting the request. I get the following error:
`Incorrect amount of PKCS#7 padding for blocksize`

PKCS7 is a standard defined in [RFC 2315 - Cryptographic Message Syntax](https://tools.ietf.org/html/rfc2315). So basically, this query string is encrypted. 
I tried a number of various search queries, and one thing that stood out to me is that the beginning part of the encrypted query param was always the same. 
I also tried reapeatedly prefixing a query (cow) with successively larger numbers of the character 'a', and was able to find a few additional patterns.
With every additional 16 a's, the length of the encrypted string increases. This suggests the encryption scheme is a block cipher with a block size of 16 bytes. 
I think this reveals that the cipher is using ECB mode, since I can show that identical pieces of plaintext result in the same ciphertext.

I spent some time prepending successive numbers of 'a's before my query, and found that after 10, one more block becomes fixed:
G%2BglEae6W%2F1XjA7vRm21nNyEco%2Fc%2BJ2TdR0Qp8dcj PJcgFy9Kftj4uxTZFMlx6iW Awjck%2BiODOmY8IWnZPcoVG IjoU2cQpG5h3WwP7xz1O3YrlHX2nGysIPZGaDXuIuY 10 b's plus cow
G%2BglEae6W%2F1XjA7vRm21nNyEco%2Fc%2BJ2TdR0Qp8dcj PLAhy3ui8kLEVaROwiiI6Oe Awjck%2BiODOmY8IWnZPcoVG IjoU2cQpG5h3WwP7xz1O3YrlHX2nGysIPZGaDXuIuY 10 a's plus cow

So that means the beginning of the encrypted query takes of part of that block. It's also clear that there is some text appended to the end of the input query.
I'm guessing this is some sql query to get jokes LIKE the input text. I was able to confirm this by entering 9 a's so that the last character in that encrypted block is the first character appended to the input.
Then I had to try adding a 10th character to my input to see which resulted in the same encrypted character. Turns out it's '%', which gives more evidence that the encrypted query is a sql LIKE statement.

This trick can actually help get past the escaping of single-quote characters. If I enter 9 characters + single quote, the 10th character of the encrypted result will be the backslash escaping the quote. So the next block will contain the encrypted value of single quote.
In this way, I can get an encrypted sql query starting on a fresh block.

For the query: Previous levels had a users table with username and password columns. I'm just going to take a wild guess that the same table is available. So let's say `‘  UNION ALL SELECT password FROM users;#` will be a good candiate.

So the idea:
1. Find my encrypted sql payload by entering 9 characters followed by the single quote and query (so the escape character fills up the block). The plaintext payload is 40 characters, so it will be contained in 3 16-byte blocks.
2. Grab those three encrypted blocks after the first three encrypted blocks.
3. Generate another encrypted query string using 10 characters.
4. Slip the encrypted text from step 2 in the middle of the cyphertext obtained in step 3, right after the first 3 blocks.

If it works, the resulting query string should return the next password.

(Spoiler: it does. See natas28.py)

airooCaiseiyee8he8xongien9euhe8b

## Level 29 -> 30
