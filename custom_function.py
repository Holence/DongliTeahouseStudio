from custom_filetype import *

import pypinyin
import re
import pickle
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os,shutil
from subprocess import Popen
from functools import partial
from random import randint
import requests
from urllib.parse import unquote
import feedparser
import json
import time
from win32com.shell import shell,shellcon
from lxml import etree
import chardet

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

def ThumbnailDirectoryFromArticleURL(article_url):
	if "www" in article_url:
		perfix=re.findall("(?<=www\.).*?(?=\.)",article_url)[0]
	else:
		perfix=re.findall("(?<=://).*?(?=\.)",article_url)[0]
	
	suffix=article_url.split("/")[-1]

	dir="./RssCache/"+perfix+suffix+".jpg"

	return dir

def textEditor_edit(textEditor_directory,text):
	
	with open("$temp","w",encoding="utf-8") as f:
		f.write(text)
	
	subprocess=Popen([textEditor_directory,"$temp"])
	subprocess.wait()

	with open("$temp","r",encoding="utf-8") as f:
		text=f.read()
	
	clear_temp_file()

	return text

def clear_temp_file():
	with open("$temp","w",encoding="utf-8") as f:
		f.write("")

def file_sort(file_list):
	file_sort_dict={}

	for file in file_list:
		file_name=file["file_name"]
		file_extension=file_name.split(".")[-1].lower()
		
		if which_file_type(file_name)=="folder":
			try:
				file_sort_dict["folder"].append(file)
			except:
				file_sort_dict["folder"]=[]
				file_sort_dict["folder"].append(file)
		elif which_file_type(file_name)=="url":
			try:
				file_sort_dict["url"].append(file)
			except:
				file_sort_dict["url"]=[]
				file_sort_dict["url"].append(file)
		else:
			try:
				file_sort_dict[file_extension].append(file)
			except:
				file_sort_dict[file_extension]=[]
				file_sort_dict[file_extension].append(file)
	
	result_list=[]
	
	try:
		for file in sorted(file_sort_dict["folder"],key=lambda x:x["file_name"]):
			result_list.append(file)
	except:
		pass
	
	for file_extension in sorted(file_sort_dict.keys()):
		if file_extension!="folder" and file_extension!="url":
			for file in sorted(file_sort_dict[file_extension],key=lambda x:x["file_name"]):
				result_list.append(file)
	
	try:
		for file in sorted(file_sort_dict["url"],key=lambda x:x["file_name"]):
			result_list.append(file)
	except:
		pass
	
	return result_list

def generate_key(password):
	"""
	??????password?????????????????????salt??????salt????????????PBKDF2??????PBKDF2???password??????key
	???????????????????????????password???????????????????????????key???
	"""
	salt=password.encode()[::-1]
	password=password.encode()
	kdf=PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=100000,backend=default_backend())
	key=base64.urlsafe_b64encode(kdf.derive(password))
	return key

def Fernet_Encrypt_Save(password,data,file_path):
	try:
		data=pickle.dumps(data)
		key=generate_key(password)

		fer=Fernet(key)
		encrypt_data=fer.encrypt(data)

		with open(file_path,"wb") as f:
			f.write(encrypt_data)
		
		return True
	except:
		return False

def Fernet_Decrypt_Load(password,file_path):
	try:
		key=generate_key(password)
	
		with open(file_path,"rb") as f:
			data=f.read()
		
		fer=Fernet(key)
		decrypt_data=fer.decrypt(data)
		decrypt_data=pickle.loads(decrypt_data)

		return decrypt_data
	except:
		return False

def Fernet_Encrypt(password,data):
	try:
		data=pickle.dumps(data)
		key=generate_key(password)

		fer=Fernet(key)
		encrypt_data=fer.encrypt(data)
		
		return encrypt_data
	except:
		return False

def Fernet_Decrypt(password,data):
	try:
		key=generate_key(password)
		
		fer=Fernet(key)
		decrypt_data=fer.decrypt(data)
		decrypt_data=pickle.loads(decrypt_data)

		return decrypt_data
	except:
		return False

def delay_msecs(msecs):
	"??????int????????????????????????msecs"
	dieTime= QTime.currentTime().addMSecs(msecs)
	while QTime.currentTime() < dieTime:
		QCoreApplication.processEvents(QEventLoop.AllEvents, 100)


def generate_color():
	return QColor(randint(50,256),randint(50,256),randint(50,256))


def delete_to_recyclebin(filename):
	"??????????????????True"
	result = shell.SHFileOperation((0,shellcon.FO_DELETE,filename,None, shellcon.FOF_SILENT | shellcon.FOF_ALLOWUNDO | shellcon.FOF_NOCONFIRMATION,None,None))  #????????????????????????
	return result[0]==0


def getHTML(url,cookie=""):

	head={}

	if cookie!="":
		head["cookie"]=cookie
	
	head['User-Agent']='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 YaBrowser/21.2.3.73 (beta) Yowser/2.5 Safari/537.36'
	

	# response=requests.get(url,headers=head,timeout=3)#
	response=requests.get(url,headers=head)#
	
	if response.encoding!="GB2312" and response.encoding!="GBK":
		response.encoding='utf-8'
	else:
		response.encoding="GBK"
	
	return response.text

def getPic(url,cookie="",referer=""):
	head={}

	if cookie!="":
		head["cookie"]=cookie
	if referer!="":
		head["referer"]=referer
	
	head['User-Agent']='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 YaBrowser/21.2.3.73 (beta) Yowser/2.5 Safari/537.36'

	# response=requests.get(url,headers=head,timeout=3)#
	response=requests.get(url,headers=head)#
	return response.content

def getTitle(url):
	"??????????????????(True,title)?????????????????????(False,Exception)???????????????Title?????????url???????????????|????????????%7C?????????????????????utf-8??????"
	try:
		html=etree.HTML(getHTML(url))
		title=html.xpath("/html/head/title/text()")
		title=unquote(title[0],'utf-8')
		return (True,title)
	except:
		try:
			#YouTube???channel????????????????????????body????????????
			title=html.xpath("/html/body/title/text()")
			title=unquote(title[0],'utf-8')
			return (True,title)
		except Exception as e:
			return (False,e)

def creat_net_url_file(net_url):
	"????????????????????????TEMP???????????????url???????????????????????????????????????(True,????????????,error),????????????(False,????????????,error)"

	DIR=os.getcwd().replace("\\","/")
	error=""
	
	result=getTitle(net_url)
	if result[0]==True:
		title=result[1]
		error="No Error"
	else:
		title="Unknown Page"
		error="Connecting Error"

	SRC="%s/TEMP"%DIR
	DST="%s/"%DIR+title+".url"

	with open(SRC,"w",encoding="utf-8") as f:
		temp="[InternetShortcut]\nURL=%s"%net_url
		f.write(temp)
	
	try:
		os.rename(SRC,DST)
	except:
		error="Naming Error for %s"%title
		#???????????????????????????????????????????????????
		title="Unknown Page"
		DST="%s/"%DIR+title+".url"
		os.rename(SRC,DST)
	
	if title=="Unknown Page":
		return (False,DST,error)
	else:
		return (True,DST,error)

def list_difference(a,b):
	#????????????????????????????????????
	c=[]
	for i in a:
		if i not in b:
			c.append(i)
	for i in b:
		if i not in a:
			c.append(i)
	return c

def encrypt_save(data,file_path):
	data_base64 = base64.b64encode(pickle.dumps(data)).decode()  # ?????????????????????str
	with open(file_path,"wb") as f:
		pickle.dump(data_base64,f)
	return

def decrypt_load(file_path):
	with open(file_path,"rb") as f:
		data_base64=pickle.load(f)
	data = pickle.loads(base64.b64decode(data_base64.encode()))  # ??????
	return data

def encrypt(data):
	data_base64 = base64.b64encode(pickle.dumps(data)).decode()  # ?????????????????????str
	return data_base64

def decrypt(data_base64):
	data = pickle.loads(base64.b64decode(data_base64.encode()))  # ??????
	return data

def save_to_json(data,file_path):
	with open(file_path,"w",encoding="utf-8") as f:
		json.dump(data,f,ensure_ascii=False,indent=4)

def load_from_json(file_path):
	with open(file_path,"r",encoding="utf-8") as f:
		data=json.load(f)
	return data

def QDate_transform(Date):
	return (QDate.year(Date),QDate.month(Date),QDate.day(Date))

def convert_to_az(c):
	#???unicode???????????????
	def hanzi_to_pinyin(last_name):
		"""
		??????????????????????????????????????????????????????
		?????????hanzi_to_pinyin(u'?????????')
		????????????xdd
		"""
		rows = pypinyin.pinyin(last_name, style=pypinyin.NORMAL)  # ?????????????????????
		return ''.join(row[0][0] for row in rows if len(row) > 0)   # ??????????????????????????????

	def jp_to_az(i):
		jp1=["???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???"]
		jp2=["???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???","???"]
		az=["???","???","???","???","a","i","u","e","o","ka","ki","ku","ke","ko","sa","si","su","se","so","ta","ti","tu","te","to","na","ni","nu","ne","no","ha","hi","hu","he","ho","ma","mi","mu","me","mo","ya","yu","yo","ra","ri","ru","re","ro","wa","wo","n","ga","gi","gu","ge","go","za","ji","zu","ze","zo","da","di","du","de","do","ba","bi","bu","be","bo","pa","pi","pu","pe","po"]
		try:
			n=jp1.index(i)
			return az[n]
		except:
			try:
				n=jp2.index(i)
				return az[n]
			except:
				pass
				# print("%s	?????????????????????\n"%i)
		return ""
	s=""
	# s+="^"#???????????????
	for i in c:
		if re.match(r"[\u0000-\u007F]",i):#???
			s+=i.lower()
		elif re.match(r"[\u4E00-\u9FFF]",i):#???
			s+=hanzi_to_pinyin(i[0])
		elif re.match(r"[\u0800-\u4DFF]",i):#??????\u4E00???????????????
			s+=jp_to_az(i)
		# if re.match(r"[\uAC00-\uD7FF]",c)#???
	# s+="$"#???????????????
	return s

def what_day_is_today():
	"?????????????????????1-7"
	today=int(time.strftime("%w"))
	if today==0:
		today=7
	return today


# def which_icon(file_name):
# 	if "." not in file_name:
# 		icon=":/icon/folder.svg"
# 		return icon

# 	file_extension=file_name.split(".")[-1].lower()
	
# 	if file_extension=="url":
# 		icon=":/icon/globe.svg"
# 	elif file_extension in app_extension:
# 		icon=":/icon/box.svg"
# 	elif file_extension in audio_extension:
# 		icon=":/icon/music.svg"
# 	elif file_extension in playlist_extension:
# 		icon=":/icon/list.svg"
# 	elif file_extension in video_extension:
# 		icon=":/icon/film.svg"
# 	elif file_extension in image_extension:
# 		icon=":/icon/image.svg"
# 	elif file_extension in text_extension:
# 		icon=":/icon/file-text.svg"
# 	else:
# 		icon=":/icon/file.svg"
# 	return icon

def which_file_type(file_url):
	#????????????
	if "|" in file_url:
		return "url"
	#??????????????????
	else:
		
		file_name=file_url.split("/")[-1]

		file_extension=file_name.split(".")[-1].lower()
		
		if file_extension in app_extension:
			return "exe"
		elif file_extension in image_extension:
			return "image"
		elif file_extension in text_extension:
			return "text"
		elif file_extension in audio_extension:
			return "audio"
		elif file_extension in video_extension:
			return "video"
		elif file_extension in playlist_extension:
			return "playlist"
		else:
			return "folder"
		
		#?????????????????????.???????????????
		# if "." not in file_name:
		# 	return "folder"
		# else:

def find_dict_in_string(s,name):
	"???????????????????????????????????? name:\{  \}???????????????????????????????????????????????????False"

	index_head=s.find(name)

	if index_head==-1:
		return False
	
	index_tail=index_head-1
	num_big=0
	num_middle=0
	in_quote=True
	start=0
	for i in s[index_head:]:
		index_tail+=1

		if num_big==0 and num_middle==0 and start==1:
			break
		
		if i=="\"" and in_quote==False:
			in_quote=True
			
		if i=="\"" and in_quote==True:
			in_quote=False
		
		if in_quote==True:
			continue
		else:
			if i=="{":
				start=1
				num_big+=1
				continue
			if i=="}":
				num_big-=1
				continue
			if i=="[":
				start=1
				num_middle+=1
				continue
			if i=="]":
				start=1
				num_middle-=1
				continue
		
	
	if num_big!=0 or num_middle!=0:
		return False

	find="{\""+s[index_head:index_tail]+"}"
	
	return json.loads(find)

class MarkdownNode():
	"""
	???????????????#?????????????????????level(int)???name??????
	???gnerate_markdown_tree_from_text??????text
	???generate_text_from_markdown_tree?????????
	"""
	def __init__(self,name,level,index):
		self.__name=name#???????????????
		self.__level=level#???????????????
		self.__index=index#???node_list???????????????
		self.__text=""#????????????????????????
		self.__pos=0#???????????????????????????????????????????????????
		self.__line=0#?????????????????????????????????????????????
		self.__parent=None#?????????
		self.__child=[]#?????????

	def addText(self,text):
		self.__text=self.__text+text
	
	def setPos(self,pos):
		self.__pos=pos
	
	def setLine(self,line):
		self.__line=line
	
	def addChild(self,node):
		self.__child.append(node)
	
	def clearChild(self):
		self.__child=[]
	
	def setParent(self,node):
		self.__parent=node
	
	def name(self):
		return self.__name
	
	def level(self):
		return self.__level
	
	def setLevel(self,level):
		self.__level=level
	
	def index(self):
		return self.__index
	
	def text(self):
		return self.__text
	
	def pos(self):
		return self.__pos
	
	def line(self):
		return self.__line
	
	def child(self):
		return self.__child
	
	def parent(self):
		return self.__parent

def gnerate_markdown_tree_from_text(text,parent):
	"??????markdown text?????????node_list???????????????????????????Head???????????????node.child()???????????????????????????"
	node_list=[]

	#Head??????
	index=0
	current_name="Head"
	current_level=0
	current_node=MarkdownNode(current_name,current_level,index)
	node_list.append(current_node)
	
	pos=0
	line=0
	
	for i in text.split("\n"):
		pos+=len(i)+1

		if i:
			if i[:2]=="| " and i[:3]!="| -":
				line+=i.count("|")-1
			elif i=="> " or i==">":
				pass
			else:
				line+=1
		
		post_level=current_level
		
		try:
			current_level=len(re.match("^#+(?= )",i).group())
			current_name=re.findall("(?<=# ).*",i)[0]

			#???????????????
			if current_level>post_level:
				if current_level-post_level>1:
					QMessageBox.warning(parent,"Warning","???????????????\n\n%s"%i)
					return []
				parent_node=current_node
			
			elif current_level==post_level:
				parent_node=current_node.parent()
			
			elif current_level<post_level:
				parent_node=current_node
				for j in range(post_level-current_level+1):
					parent_node=parent_node.parent()
			
			index+=1
			current_node=MarkdownNode(current_name,current_level,index)
			parent_node.addChild(current_node)
			current_node.setParent(parent_node)
			current_node.setPos(pos)
			current_node.setLine(line)
			node_list.append(current_node)

		except:
			#?????????
			current_node.addText(i+"\n")
			pass
	
	return node_list

def generate_text_from_markdown_tree(node_list):
	def deep_append_text(node):
		temp=""
		for child in node.child():
			temp+="#"*child.level()+" "+child.name()+"\n\n"+child.text()+"\n\n"

			temp+=deep_append_text(child)
		
		return temp
		
	text=""
	text=deep_append_text(node_list[0])
	text=re.sub("\n\n\n+","\n\n",text)
	return text

class RSS_Parser():
	################################################################################
	#
	# ?????????????????????(Status,feed_name,update_link_list)
	#
	# ???????????????update_link_list????????????????????????????????????????????????????????????key???[
	# 	{
	# 		"title":"",
	# 		"link":"",
	# 	}
	# ]
	# 
	# ???????????????update_link_list??????????????????????????????????????????????????????
	# 
	# ?????????????????????????????????
	#
	# ERROR Status: Invalid ?????????url?????????????????????????????????
	# ERROR Status: Failed ??????Feed????????????
	#
	################################################################################
	
	def __init__(self):
		
		pass

	def update_normal_rss(self,rss_url,cookie=""):
		try:
			rss=feedparser.parse(rss_url)
			if "title" in rss.feed and rss.entries!=[]:
				return ("Done",rss.feed.title,rss.entries)
			else:
				return ("Invalid",None,None)
		except:
			return ("Failed",None,None)

	def update_BiliBili_Video(self,rss_url,cookie=""):
		"Bilibili???????????????https://space.bilibili.com/up_ID"
		try:
			try:
				up_ID=re.findall("(?<=space\.bilibili\.com/)[\d]*",rss_url)[0]
			except:
				#???????????????
				return ("Invalid",None,None)
			
			url_list=[]

			response=getHTML("https://api.bilibili.com/x/space/acc/info?mid="+up_ID,cookie)
			up_name=json.loads(response)["data"]["name"]

			response=getHTML("https://api.bilibili.com/x/space/arc/search?mid="+up_ID,cookie)
			video_list=json.loads(response)["data"]["list"]["vlist"]

			for video in video_list:
				
				thumbnail_file="./RssCache/"+"bilibili"+video["bvid"]+".jpg"
				if not os.path.exists(thumbnail_file):
					Pic=getPic(video["pic"],"","")
					with open(thumbnail_file,"wb") as f:
						f.write(Pic)
				
				url_list.append(
					{
						"title":video["title"],
						"link":"https://www.bilibili.com/video/"+video["bvid"]
					}
				)

			return ("Done",up_name,url_list)
		
		except:
			return ("Failed",None,None)

	def updata_Bandcamp(self,rss_url,cookie=""):
		"Bandcamp???????????????https://NAME.bandcamp.com/"
		try:
			try:
				band_name=re.findall("(?<=https\://).+(?=\.bandcamp\.com)",rss_url)[0]
			except:
				#???????????????
				return ("Invalid",None,None)

			url_list=[]
			response=getHTML(rss_url+"/music",cookie)
			html=etree.HTML(response)
			album_list=html.xpath('//*[@id="music-grid"]/li/a/@href')
			title_list=list(map(lambda x:x.strip(),html.xpath('//*[@id="music-grid"]/li/a/p/text()')))

			index=0
			Thumbnail_url_list1=html.xpath('//*[@id="music-grid"]/li/a/div/img/@src')
			Thumbnail_url_list2=html.xpath('//*[@id="music-grid"]/li/a/div/img/@data-original')
			
			
			for thumbnail_url in Thumbnail_url_list1[:len(Thumbnail_url_list1)-len(Thumbnail_url_list2)]:
				thumbnail_file="./RssCache/"+band_name.lower()+title_list[index].replace(" ","-").replace("---","-").lower()+".jpg"
				try:
					if not os.path.exists(thumbnail_file):
						Pic=getPic(thumbnail_url,"","")
						with open(thumbnail_file,"wb") as f:
							f.write(Pic)
				except:
					pass
				index+=1

			for thumbnail_url in Thumbnail_url_list2:
				thumbnail_file="./RssCache/"+band_name.lower()+title_list[index].replace(" ","-").replace("---","-").lower()+".jpg"
				try:
					if not os.path.exists(thumbnail_file):
						Pic=getPic(thumbnail_url,"","")
						with open(thumbnail_file,"wb") as f:
							f.write(Pic)
				except:
					pass
				index+=1
			
			for i in range(len(album_list)):
				url_list.append(
					{
						"title":title_list[i],
						"link":rss_url+album_list[i]
					}
				)
			return ("Done",band_name,url_list)
		
		except:
			return ("Failed",None,None)
	
	def update_Pixiv_IllustrationS(self,cookie):
		"?????????Pixiv Cookie?????????????????????????????????Feed?????????https://www.pixiv.net/bookmark_new_illust.php"
		try:
			rss_name=None
			
			url="https://www.pixiv.net/bookmark_new_illust.php"
			response=getHTML(url,cookie)
			
			ss=re.findall('(?<=js-mount-point-latest-following"data-items="\[).*?(?=\]")',response)[0]
			ID_list=re.findall("(?<=&quot;illustId&quot;:&quot;).*?(?=&quot;,)",ss)
			Title_list=re.findall("(?<=&quot;illustTitle&quot;:&quot;).*?(?=&quot;,)",ss)
			Thumbnail_url_list=re.findall("(?<=&quot;url&quot;:&quot;).*?(?=&quot;,)",ss)

			#???????????????
			for i in range(len(ID_list)):
				ID=ID_list[i]
				thumbnail_file="./RssCache/"+"pixiv"+ID+".jpg"
				if not os.path.exists(thumbnail_file):
					thumbnail_url=Thumbnail_url_list[i].replace("\\","")
					Pic=getPic(thumbnail_url,cookie,"https://www.pixiv.net/")
					with open(thumbnail_file,"wb") as f:
						f.write(Pic)
			
			url_list=[]
			
			for i in range(len(ID_list)):
				
				try:
					title=Title_list[i].encode('utf-8').decode('unicode_escape')
				except:
					title=Title_list[i]
				
				link="https://www.pixiv.net/artworks/"+ID_list[i]
				url_list.append(
					{
						"title":title,
						"link":link
					}
				)
			return ("Done",rss_name,url_list)
		
		except:
			return ("Failed",None,None)

	def update_Pixiv_Illustration(self,rss_url,cookie=""):
		"Pixiv???????????????https://www.pixiv.net/users/3371956"

		try:
			try:
				ID=rss_url.split("/")[-1]
				int(ID)
			except:
				#???????????????
				return ("Invalid",None,None)
			
			response=json.loads(getHTML("https://www.pixiv.net/ajax/user/%s/profile/all"%ID,cookie))
			
			try:
				rss_name=response["body"]["pickup"][0]["userName"]
			except:
				#???????????????pickup???????????????????????????
				#??????????????????
				try:
					rss_name=json.loads(getHTML("https://www.pixiv.net/ajax/user/%s/profile/top"%ID,cookie))["body"]["extraData"]["meta"]["title"]
				except:
					rss_name="Unkown Feed"
			
			url_list=[]
			
			illustration_dict=response["body"]["illusts"]
			
			#??????????????????
			# https://www.pixiv.net/ajax/user/2922722/profile/illusts?ids[]=47896781&ids[]=47896782&work_category=illust&is_first_page=1
			# ?????????????????????
			extraInfoList=[]
			for i in illustration_dict.keys():
				
				thumbnail_file="./RssCache/"+"pixiv"+i+".jpg"
				if not os.path.exists(thumbnail_file):
					extraInfoList.append(i)
				
				#????????? ???????????? ??????????????????
				if len(extraInfoList)==20:
					extraInfoUrl="https://www.pixiv.net/ajax/user/%s/profile/illusts?"%ID
					for i in extraInfoList:
						extraInfoUrl+="ids[]="+i+"&"
					extraInfoUrl+="work_category=illust&is_first_page=1"
					
					extraInfo=json.loads(getHTML(extraInfoUrl,cookie))

					#???????????????
					for i in extraInfo["body"]["works"].values():
						id=i["id"]
						illustration_dict[id]=i["title"]
						Pic=getPic(i["url"],cookie,"https://www.pixiv.net/")
						thumbnail_file="./RssCache/"+"pixiv"+id+".jpg"
						with open(thumbnail_file,"wb") as f:
							f.write(Pic)
					
					extraInfoList=[]
			
			extraInfoUrl="https://www.pixiv.net/ajax/user/%s/profile/illusts?"%ID
			for i in extraInfoList:
				extraInfoUrl+="ids[]="+i+"&"
			extraInfoUrl+="work_category=illust&is_first_page=1"
			
			extraInfo=json.loads(getHTML(extraInfoUrl,cookie))

			#???????????????
			for i in extraInfo["body"]["works"].values():
				id=i["id"]
				illustration_dict[id]=i["title"]
				Pic=getPic(i["url"],cookie,"https://www.pixiv.net/")
				thumbnail_file="./RssCache/"+"pixiv"+id+".jpg"
				with open(thumbnail_file,"wb") as f:
					f.write(Pic)

			# Extra??????????????????
			#
			for i in illustration_dict.keys():
				if i==None:
					i="Unkown..."
				url_list.append(
					{
						"title":illustration_dict[i],
						"link":"https://www.pixiv.net/artworks/"+i
					}
				)
			
			return ("Done",rss_name,url_list)
		
		except:
			return ("Failed",None,None)
	
	def update_Pixiv_Manga(self,rss_url,cookie=""):
		"Pixiv???????????????https://www.pixiv.net/users/3371956"

		try:
			try:
				ID=rss_url.split("/")[-1]
				int(ID)
			except:
				#???????????????
				return ("Invalid",None,None)
			
			response=json.loads(getHTML("https://www.pixiv.net/ajax/user/%s/profile/all"%ID,cookie))

			try:
				rss_name=response["body"]["pickup"][0]["userName"]
			except:
				#???????????????pickup???????????????????????????
				#??????????????????
				try:
					rss_name=json.loads(getHTML("https://www.pixiv.net/ajax/user/%s/profile/top"%ID,cookie))["body"]["extraData"]["meta"]["title"]
				except:
					rss_name="Unkown Feed"
			
			url_list=[]
			
			manga_dict=response["body"]["manga"]
			
			for i in manga_dict.keys():
				url_list.append(
					{
						"title":i,
						"link":"https://www.pixiv.net/artworks/"+i
					}
				)
			
			return ("Done",rss_name,url_list)
		
		except:
			return ("Failed",None,None)
	
	def update_Instagrams(self,cookie):
		"Instagram???????????????Feed??????"
		# Instagram???????????????????????????????????????????????????????????????????????????????????????????????????????????????
		url="https://www.instagram.com/"
		response=getHTML(url,cookie)
		find=re.findall("(?<=>window\.__additionalDataLoaded\('feed',).*?(?=\);</script>)",response)[0]
		for i in find["user"]["edge_web_feed_timeline"]["edges"]:
			pass

	def updata_Instagram(self,rss_url,cookie=""):
		"Instagram???????????????https://www.instagram.com/ID"
		try:
			#???????????????????????????????????????????????????????????????????????????????????????????????????????????????
			#??????????????????????????????
			#rss_url+"/"

			response=getHTML(rss_url+"/",cookie)
			try:
				html=etree.HTML(response)
				rss_name=html.xpath("/html/head/title/text()")[0].strip()
			except:
				rss_name="Unkown Feed"
			
			#???????????????????????????????????????????????????????????????????????????????????????
			# find=find_dict_in_string(response,"edge_owner_to_timeline_media")

			#
			find=re.findall("(?<=window\._sharedData = ).*?(?=</script>)",response)[0][:-1]
			find=json.loads(find)["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
			
			url_list=[]
			for i in find:
				ID=i["node"]["shortcode"]

				thumbnail_file="./RssCache/"+"instagram"+ID+".jpg"
				thumbnail_url=i["node"]["thumbnail_resources"][0]["src"]
				Pic=getPic(thumbnail_url,"","")
				with open(thumbnail_file,"wb") as f:
					f.write(Pic)
				
				url_list.append(
					{
						"title":ID,
						"link":"https://www.instagram.com/p/%s"%ID
					}
				)
			
			return ("Done",rss_name,url_list)
		
		except:
			return ("Failed",None,None)