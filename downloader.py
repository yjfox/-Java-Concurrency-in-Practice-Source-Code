import urllib
import re, os
from HTMLParser import HTMLParser

#download all java source code from http://jcip.net.s3-website-us-east-1.amazonaws.com/listings.html

class myhtmlparser(HTMLParser):
    def __init__(self):
        self.reset()
        self.newtag = []
        self.newattr = []
        self.newdata = []
    def handle_starttag(self, tag, attrs):
    	if 'a' in tag:
			self.newtag.append(tag);
			self.newattr.append(attrs);
    def handle_data(self, data):
        self.newdata.append(data)
    def clean(self):
        self.newtag = []
        self.newattr = []
        self.newdata = []
    def cleanData(self):
    	self.newdata = []

# final parameters
path = '/tmp/JavaMulThread/'
url = 'http://jcip.net.s3-website-us-east-1.amazonaws.com/'
source = urllib.urlopen('http://jcip.net.s3-website-us-east-1.amazonaws.com/listings.html')

page = source.readlines();
parser = myhtmlparser()
folderpath = ""
for line in page:
	if "puzzletitletoc" in line:
		parser.feed(line)
		if len(parser.newattr) > 0:
			for attr in parser.newattr:
				for item in attr:
					filename = item[1].split('/')[-1]
					urllib.urlretrieve(url + item[1], folderpath + filename)
					print folderpath + item[1]
		parser.clean()
	if "ChapTOC" in line:
		parser.feed(line)
		folderpath = path + parser.newdata[0].replace(" ", "_") + '/'
		print folderpath
		if not os.path.exists(folderpath):
			os.makedirs(folderpath)
		# Clean the parser
		parser.clean()

