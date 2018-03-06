import requests
import re
from urllib import parse

# e-mail regexp:
# letter/number/dot/comma @ letter/number/dot/comma . letter/number
emailRe = re.compile( r'([\w\.,]+@[\w\.,]+\.\w+)' )

# HTML <a> regexp
# Matches href="" attribute

linkRe = re.compile( r'href="(.*?)"' )

def crawl( url , level ):
	print("visiting: ", url )
	
	if( level == 0 ):
		return
	
	#get webpage
	req = requests.get( url );
	result = []
	
	#check
	if( req.status_code != 200 ) :
		return []
	
	#get all links
	links = linkRe.findall( req.text );
	
	for link in links :
		#get absolute url
		link = parse.urljoin(url,link)
		
		if link.endswith("/"):
			link = link[:-1]
		
		if not link.startswith("http") and not link.startswith("www") :
			#discard link
			continue;
		
		print(link);
		
		#result += crawl( link , level-1 )
	
	#get all emails	
	result += emailRe.findall( req.text )
	return result
	
url = input("Enter url :")

if not ( url.startswith("http") | url.startswith("www") ):
	url = "http://" + url ;
if url.endswith("/") :
	url = url[:-1]

emails = crawl(url , 2);

print("Scrapped e-mails :")
for e in emails:
	print(e)
	
print("Done")
	

