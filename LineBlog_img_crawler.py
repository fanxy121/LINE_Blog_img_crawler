#!/usr/bin/python3
from urllib.request import urlopen as uReq
from urllib.request import urlretrieve as uRetr
from bs4 import BeautifulSoup as soup
import os

raw_url = input("Please input the url:\n(e.g. https://lineblog.me/uesaka_sumire/archives/2018-11.html)\n\n")
# e.g.
# raw_url = "https://lineblog.me/uesaka_sumire/archives/2018-11.html?p=1"
folder_dirname = input("Please input the path:\n(e.g. ~/[YOUR_DIRNAME])\n\n")

def find_target_urls(raw_url):
	
	uClient = uReq(raw_url)
	page_html = uClient.read()
	uClient.close()

	# html parsing
	page_soup = soup(page_html, "html.parser")

	paging_number = page_soup.find("ol", {"class":"paging-number"})
	target_urls = paging_number.find_all("a")

	return target_urls


def mkdir(path):
	
	folder = os.path.exists(path)
	if not folder:                   
		os.makedirs(path)            
		print("---  Made New Dir  ---")
	else:
		print("---  Alredy Exsits  ---")
		

def downloadImg(imgURLs_article, article_name):
	
	imgID = 0
	for imgURL_article in imgURLs_article:
		imgURL = imgURL_article.get('href')
		
		folder_basename = article_name.split("\n")[2] + " " + article_name.split("\n")[1]
		folder_basename = folder_basename.replace('/', '-')
		folder_path = os.path.join(os.path.expanduser(folder_dirname), folder_basename)
		mkdir(folder_path) 

		uRetr(imgURL, folder_path + "/%03d.jpg" %imgID)
		print(imgURL)
		imgID = imgID + 1


def parse_and_download(target_url):

	# opening up connection, grabbing the page
	uClient = uReq(target_url)
	page_html = uClient.read()
	uClient.close()

	# html parsing
	page_soup = soup(page_html, "html.parser")

	# grabs each element
	articles = page_soup.findAll("article", {"class":"article"})

	for article in articles:
		title_article = article.find("header", {"class":"article-header"})
		article_name = title_article.text
		imgURLs_article = article.find("div", {"class":"article-body-inner"}).find_all("a", {"target":"_blank"})
		downloadImg(imgURLs_article, article_name)


target_urls = find_target_urls(raw_url)

parse_and_download(raw_url)
for target_url in target_urls:
	parse_and_download(target_url.get('href'))
	

