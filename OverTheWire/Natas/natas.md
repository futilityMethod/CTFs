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

That is not useful. But yo, I can navigate the file system.


