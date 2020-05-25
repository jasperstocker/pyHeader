# pyHeader
A python script for popping customisable script headers onto your C# scripts


Specifically built for adding headers to my Unity project scripts
Initially built to my very narrow use case
Mainly because there isn't this kind of functionality easily available it seems
(I'm sure a whole lot of people will correct me on this!)
Was built as part of the BuildR project
https://b.uildr.com

Simple Python script with executable bat for running the script.
You'll need to edit the BAT file though for your local system!

Script headers will be added to everything in the scripts folder defined on line 10
You can define a version file to scrape the project version from the C# script and add it into the header (line 11)

There is a header.txt file to define the main body content of the header

There is an ignore.txt file to define basic parameters for ignoreing files
These are line separated
It will affect files and folders
Ideal for making sure you don't add headers to project library source

The public key allows you to add a unique value to all the scripts
In the past, I have had issues as an Asset Store publisher where people host private code in their public repos.
I've decided a fast option will be to add this public key which you can Google (or set up a IFTTT process)
So it will be easy to track the file source being shared.

This script will endevour to not modify the modify date on scripts
It will also overwrite itself on repeat runs so you can quickly update everything with a version number change
