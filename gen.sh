#!/bin/bash

# Must be in project root directory to use this script (i'm a bit in hurry)

cd input;
for f in *;
do
	cat $f | python ../deliver.py >../output/${f/in/out};
done
cd ..;
