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