###########################################################################
### Image grabbing tool to find batches of insitu images from on NEXTDB ###
###      written by E.P. Sorokin    April 2014  at UW-Madison           ###
###########################################################################
#
'''Batch downloading of in situ images from the NEXTDB database database. 
Currently searches for larval L4 and young adult in situ entries.'''

import csv 	
from bs4 import BeautifulSoup as bs
from urllib2 import urlopen
import urlparse
import os
import sys
import re

# Define variables with user input

print '\n\t--->Welcome to the insitu finder!\n' 
HOMEPAGE = raw_input("\n\t--->What HTML database to use?  (default = NEXTDB)" )
if HOMEPAGE == "":
	HOMEPAGE = 'http://nematode.lab.nig.ac.jp'
SEARCHPAGE = 'http://nematode.lab.nig.ac.jp/db2/ShowCloneInfo.php?clone='

# define DATAFILE
DATAFILE = raw_input("\n\t---> What datafile to read? (default = data.csv) ")
if DATAFILE == "":
	DATAFILE = "data.csv"

## data.csv example follows the standard for NEXTDB database entries
## formatted as a comma-delimited text file:
# clone,group,chromosome,cosmid,CDSNo.,product,gene,size,image
# 626d12,CELF00010,LGX,AH9,2,AH9.2,crn-4,1.17,in-situ
# 169c7,CELK03976,LG3,B0244,1,B0244.8,x,1.37,in-situ
# 733f10,CELK09035,LG3,B0244,1,B0244.8,x,1.83,in-situ
# 119a9,CELK01041,LG3,B0280,1,B0280.5,x,0.66,in-situ

# Read in datafile.csv
out=open(str(DATAFILE), "rb")
data = csv.reader(out)
data = [row for row in data]
out.close()
        
class Insitu:
	'''
	Methods and attributes for in situ class including get_clone.
	This is helpful when processing the data.csv file.'''
	
	def __init__(self, clone, group, lg, cosmid, cds_no, product, gene_name):
		self.clone = clone
		self.group = group
		self.lg = lg
		self.cosmid = cosmid
		self.cds_no = cds_no
		self.product = product
		self.gene_name = gene_name
	def __str__(self):
		a = "IN SITU ENTRY" + "\n"
		a += "Clone: " + str(self.clone) + "\n"
		a += "Chromosome: " + str(self.lg) + "\n"
		a += "Cosmid name: " + str(self.cosmid)
		a += "Ensembl ID: " + str(self.product)
		return a
	def get_clone (self):
		return self.clone
	def get_name (self):
		return self.gene_name
	def get_id (self):
		return self.product
		
# Define strings
worm_stage = str()
new_address = str()
image_address = str()

# PROGRAM LOGIC: Loop through the csv file to make an In Situ instance,
# then grab an image for each instance.

counter = 0
for i in range (1, len(data)):
	counter += 1
	print "\n\n\t.....NOW ON ENTRY: ", str(counter), "OF ", str(len(data)), "ENTRIES REQUESTED"
	insitu = Insitu(data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], data[i][5], data[i][6]) 
	print "\t.....Now processing images for this Ensembl ID:", insitu.get_id(), ", which is this gene :", insitu.get_name()
	
	# Read the webpage
	soup = bs(urlopen(SEARCHPAGE + insitu.get_clone()))    
	# Find all images on webpage
	counter 
	for image in soup.findAll("img"):
		
		#print "\t.....Found an image file:  %(src) s" % image 
		
		# Note the stage based on the string
		#print ".....Searching for images for this gene:", insitu.get_name()
		if str(image['src']).endswith("5-1.1.jpg"):
			worm_stage = "L1-L2"
			print "\t.....Found an image of stage", str(worm_stage),"...This animal is too young."
			pass
		elif str(image['src']).endswith("6-1.1.jpg"):
			worm_stage = "L2-L3"
			print "\t.....Found an image of stage", str(worm_stage),"...This animal is too young. "
			pass
		# Note: image files not always end with .1p (sometimes end with .2p:)
		elif str(image['src']).endswith("3-1.1.jpg") or str(image['src']).endswith("3-1.1p.jpg") or str(image['src']).endswith("3-1.2p.jpg") or str(image['src']).endswith("7-1.1.jpg") or str(image['src']).endswith("7-1.1p.jpg") or str(image['src']).endswith("7-1.2p.jpg") or str(image['src']).endswith("7-1.2.jpg"):
			worm_stage = "L3-L4"
			print "\t.....Found an image of stage", str(worm_stage),"and now retrieving image."
			image_address = re.sub('/m/', '/l/', str(image['src']))
			new_address = str(HOMEPAGE + image_address)
			resource = urlopen(new_address)
			f = open(str(insitu.get_id() + "_" + worm_stage  + '.jpg'), 'wb')
			f.write(resource.read())
			f.close()
			print "\t.....Wrote image file. "
		# Note: image files not always end with .1p: #could also be 
		elif str(image['src']).endswith("4-1.1.jpg") or str(image['src']).endswith("4-1.1p.jpg") or str(image['src']).endswith("4-1.2p.jpg") or str(image['src']).endswith("8-1.1.jpg") or str(image['src']).endswith("8-1.1p.jpg") or str(image['src']).endswith("8-1.1.1p.jpg") or str(image['src']).endswith("8-1.2p.jpg") or str(image['src']).endswith("8-1.2.jpg"):
			worm_stage = "L4-adult"
			print "\t.....Found an image of stage", str(worm_stage),"and now retrieving image."
			image_address = re.sub('/m/', '/l/', str(image['src']))
			new_address = str(HOMEPAGE + image_address)
			#print image_address, new_address
			resource = urlopen(new_address)
			f = open(str( insitu.get_id() + "_" + worm_stage + '.jpg'), 'wb')
			f.write(resource.read())
			f.close()
			print "\t.....Wrote image file. "
		else:
			pass
			
print "\n\t.....Found in situ entries you asked for. Goodbye."