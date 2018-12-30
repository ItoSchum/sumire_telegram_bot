#!/usr/bin/python3
from urllib.request import urlopen as uReq
from urllib.request import urlretrieve as uRetr
from bs4 import BeautifulSoup as soup
import os

# raw_url = input("\nPlease Input the URL: (e.g. https://lineblog.me/uesaka_sumire/archives/2018-11.html)\nURL: ")
raw_url = 'https://lineblog.me/uesaka_sumire/'
# folder_dirname = input("\nPlease Input the Saving Path: (e.g. ~/[YOUR_DIRNAME])\nPath: ")

# crawler_mode = input("\nPlease Choose Mode:\n 0 --- Current Page Lateset Article Only\n 1 --- Current Page Whole\n 2 --- Current Month Whole\n 3 --- Current Page with Specific Position\nMode: ")
crawler_mode = '0'

def open_url_to_soup(url):

	# opening up connection, grabbing the page
	uClient = uReq(url)
	page_html = uClient.read()
	uClient.close()

	# html parsing
	page_soup = soup(page_html, "html.parser")

	return page_soup


def find_target_urls(raw_url):
	
	page_soup = open_url_to_soup(raw_url)
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
	
	# imgID = 0
	imgURLs = []
	for imgURL_article in imgURLs_article:
		imgURL = imgURL_article.get('href')
		imgURLs.append(imgURL)

		# folder_basename = article_name.split("\n")[2] + " " + article_name.split("\n")[1]
		# folder_basename = folder_basename.replace('/', '-')
		# folder_path = os.path.join(os.path.expanduser(folder_dirname), folder_basename)
		# mkdir(folder_path) 

		# uRetr(imgURL, folder_path + "/%03d.jpg" %imgID)
		# print(imgURL)
		# imgID = imgID + 1

	return imgURLs


def mono_article_parse(article):
	
	title_article = article.find("header", {"class":"article-header"})
	article_name = title_article.text
	imgURLs_article = article.find("div", {"class":"article-body-inner"}).find_all("a", {"target":"_blank"})
	
	imgURLs = downloadImg(imgURLs_article, article_name)

	return imgURLs


def whole_parse_and_download(target_url):

	page_soup = open_url_to_soup(target_url)
	# grabs each element
	articles = page_soup.find_all("article", {"class":"article"})

	imgURLs_webpage = []
	for article in articles:
		imgURLs_webpage.append(mono_article_parse(article))

	return imgURLs_webpage
		

def specific_parse_and_download(target_url, article_position = 0):

	page_soup = open_url_to_soup(target_url)
	# grabs each element
	articles = page_soup.find_all("article", {"class":"article"})
	
	imgURLs = mono_article_parse(articles[article_position])

	return imgURLs


# if crawler_mode == '0':
# 	specific_parse_and_download(raw_url)

# elif crawler_mode == '1':
# 	whole_parse_and_download(raw_url)

# elif crawler_mode == '2':
# 	target_urls = find_target_urls(raw_url)
# 	for target_url in target_urls:
# 		whole_parse_and_download(target_url.get('href'))

# elif crawler_mode == '3':
# 	article_position = input("\nPlease Choose the Article Position (Start with 1): ")
# 	specific_parse_and_download(raw_url, int(article_position) - 1)

	

