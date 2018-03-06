from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse


class LinkParser ( HTMLParser ):
	
	def handle_starttag(self , tag , attrs ):
		# link like <a href="www.link.com"></a>
		if tag == 'a' :
			for(key , value) in attrs :
				if key == 'href' :
					if ( value.startswith("http") or value.startswith("www") ) :
						self.links = self.links  + [value] ;
					else :
						if not value.startswith("/"):
							value = "/"+value
						newUrl = parse.urljoin(self.baseUrl, value) ;
						self.links = self.links + [newUrl]
	
	
	def getLinks(self,url):
		self.links = []
		
		if not ( url.startswith("http") | url.startswith("www") ):
			url = "http://" + url ;
		if url.endswith("/") :
			url = url[:-1]
			
		self.baseUrl = url
		
		response = urlopen(url)
		
		#print(response.getheader)
		
		#if response.getheader('Content-Type') == 'text/html' :
		if True:
			htmlBytes = response.read()
			
			htmlString = htmlBytes.decode("utf-8")
			
			self.feed(htmlString)
			
			return htmlString, self.links
		#else: 
		#	print("Not html page")
		#	return "",[]
			
def spider( url, word ):
	
	#if not ( url.startswith("http") | url.startswith("www") ):
	#	url = "http://" + url ;
	#if url.endswith("/") :
	#	url = url[:-1]
	
	pagesToVis = [url]
	
	foundWord = False
	
	while pagesToVis != [] and not foundWord :
		
		url = pagesToVis[0]
		pagesToVis = pagesToVis[1:]
		
		try:
			print("Visiting : ", url)
			
			parser = LinkParser()
			
			data, links = parser.getLinks(url)
			
			pagesToVis = pagesToVis + links
			
			if( data.find(word) > -1 ) :
				foundWord = True
				
				print("** Success! **")
				
		except :
			print(" ** Not found **")
		


url = input("Enter url :")

word = input("Enter word to find :")

#n = input("Enter no of pages to crawl :")

spider(url,word)

