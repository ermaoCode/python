# -*- coding:utf-8 -*-
import re
import os
import urllib
import urllib2

srcurl = "http://www.gamersky.com/ent/201607/774314.shtml"
page = 1



def getPage(srcurl,pageNum):
	# 地址转换
	srcurl = "http://www.gamersky.com/ent/201607/774314.shtml"
	if pageNum==1:
		url = srcurl
	else:
		pattern = re.compile(r'(.*?\..*?\..*?)\.')
		url = re.sub(pattern,r'\1_'+str(pageNum)+'.', srcurl)
	# 获取页面html代码
	try:
		request = urllib2.Request(url)
		response = urllib2.urlopen(request)
		pageCode = response.read().decode('utf-8')
		# print u"连接gamersky第",pageNum,u"页成功"
		return pageCode
	except urllib2.URLError, e:
		if hasattr(e,"reason"):
			print u"连接gamersky第",pageNum,u"页失败,错误原因",e.reason
			return None

def getImgSrc(pageHTML):
	pattern = re.compile('<p align="center">.*?</p>',re.S)
	items = re.findall(pattern,pageHTML)
	# print items
	imgs = []
	for item in items:
		# print item
		img = []

		
		imgPattern = re.compile('(?<=src=").*?(?=")',re.S)
		picture = re.search(imgPattern,item)
		if picture == None:
			continue
		img.append(picture.group())

		textPattern = re.compile('(?<=<br>).*?(?=<)',re.S)
		text = re.search(textPattern,item)
		if text != None:
			# print re.search(textPattern,item).group()
			img.append(text.group())
		else:
			img.append("NoDescription")

		imgs.append(img)
	return imgs
	
allimg = []
while True:
	html = getPage(srcurl,page)
	if html == None:
		break
	imgs = getImgSrc(html)
	allimg.extend(imgs)
	page += 1
	


def downLoadPicFromURL(URL,dest_dir):  
	try:  
		urllib.urlretrieve(URL , dest_dir)  
	except urllib2.URLError, e:
		if hasattr(e,"reason"):
			print u"错误原因",e.reason
			return None
# 下载gif需要定义header
def downLoadGifFromURL(URL,dest_dir):  
	pageIndex = 1
	user_agent = 'Mozilla/4.0(compatible; MISE 5.5; Windows NT)'
	headers = {'User-Agent':user_agent}
	request = urllib2.Request(URL,headers = headers)
	imgData = urllib2.urlopen(request).read()
	output = open(dest_dir,'wb+')
	output.write(imgData)
	output.close()


path= r'D:\img'
imgNum = 1
for img in allimg:
	# print img[0]
	# print img[0].split('.')[-1]
	imgExtension = img[0].split('.')[-1]
	imgName = str(imgNum)+img[1].strip()+'.'+imgExtension
	# print imgName
	print u"正在下载",imgName
	dest_dir=os.path.join(path,imgName)
	if imgExtension == 'gif':
		downLoadGifFromURL(img[0],dest_dir)
	else:
		downLoadPicFromURL(img[0],dest_dir)
	imgNum += 1
