from custom_filetype import *
import pypinyin
import re
import pickle
import base64
import os,shutil
import requests
import feedparser
import json
import time
from win32com.shell import shell,shellcon
from lxml import etree
import chardet


def delete_to_recyclebin(filename):
	"删除成功返回True"
	result = shell.SHFileOperation((0,shellcon.FO_DELETE,filename,None, shellcon.FOF_SILENT | shellcon.FOF_ALLOWUNDO | shellcon.FOF_NOCONFIRMATION,None,None))  #删除文件到回收站
	return not result[1]


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

def getTitle(url):
	"成功的话返回(True,title)，失败的话返回(False,Exception)"
	try:
		html=etree.HTML(getHTML(url))
		title=html.xpath("/html/head/title/text()")
		return (True,title[0])
	except:
		try:
			#YouTube的channel页面的标题竟然在body里面……
			title=html.xpath("/html/body/title/text()")
			return (True,title[0])
		except Exception as e:
			return (False,e)

def creat_net_url_file(net_url):
	"在根目录生成一个TEMP文件来制造url链接文件，如果解析成功返回(True,文件地址,error),否则返回(False,文件地址,error)"

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
		#有点网页编码不严格，这里重命名不了
		title="Unknown Page"
		DST="%s/"%DIR+title+".url"
		os.rename(SRC,DST)
	
	if title=="Unknown Page":
		return (False,DST,error)
	else:
		return (True,DST,error)



def list_difference(a,b):
	#返回两个列表的差异的合集
	c=[]
	for i in a:
		if i not in b:
			c.append(i)
	for i in b:
		if i not in a:
			c.append(i)
	return c

def encrypt_save(data,file_path):
	data_base64 = base64.b64encode(pickle.dumps(data)).decode()  # 加密，出来是个str
	with open(file_path,"wb") as f:
		pickle.dump(data_base64,f)
	return

def decrypt_load(file_path):
	with open(file_path,"rb") as f:
		data_base64=pickle.load(f)
	data = pickle.loads(base64.b64decode(data_base64.encode()))  # 解密
	return data

def encrypt(data):
	data_base64 = base64.b64encode(pickle.dumps(data)).decode()
	return data_base64

def decrypt(data_base64):
	data = pickle.loads(base64.b64decode(data_base64.encode())) 
	return data

def save_to_json(data,file_path):
	with open(file_path,"w",encoding="utf-8") as f:
		json.dump(data,f,ensure_ascii=False,indent=4)

def load_from_json(file_path):
	with open(file_path,"r",encoding="utf-8") as f:
		data=json.load(f)
	return data




def convert_to_az(c):#用unicode划分语言区
	def hanzi_to_pinyin(last_name):
		"""
		功能说明：将姓名转换为拼音首字母缩写
		参数：hanzi_to_pinyin(u'习大大')
		返回值：xdd
		"""
		rows = pypinyin.pinyin(last_name, style=pypinyin.NORMAL)  # 获取姓氏首字母
		return ''.join(row[0][0] for row in rows if len(row) > 0)   # 拼接姓名首字母字符串

	def jp_to_az(i):
		jp1=["”","“","《","》","あ","い","う","え","お","か","き","く","け","こ","さ","し","す","せ","そ","た","ち","つ","て","と","な","に","ぬ","ね","の","は","ひ","ふ","へ","ほ","ま","み","む","め","も","や","ゆ","よ","ら","り","る","れ","ろ","わ","を","ん","が","ぎ","ぐ","げ","ご","ざ","じ","ず","ぜ","ぞ","だ","ぢ","づ","で","ど","ば","び","ぶ","べ","ぼ","ぱ","ぴ","ぷ","ぺ","ぽ"]
		jp2=["”","“","《","》","ア","イ","ウ","エ","オ","カ","キ","ク","ケ","コ","サ","シ","ス","セ","ソ","タ","チ","ツ","テ","ト","ナ","ニ","ヌ","ネ","ノ","ハ","ヒ","フ","ヘ","ホ","マ","ミ","ム","メ","モ","ヤ","ユ","ヨ","ラ","リ","ル","レ","ロ","ワ","ヲ","ン","ガ","ギ","グ","ゲ","ゴ","ザ","ジ","ズ","ゼ","ゾ","ダ","ヂ","ヅ","デ","ド","バ","ビ","ブ","ベ","ボ","パ","ピ","プ","ペ","ポ"]
		az=["”","“","《","》","a","i","u","e","o","ka","ki","ku","ke","ko","sa","si","su","se","so","ta","ti","tu","te","to","na","ni","nu","ne","no","ha","hi","hu","he","ho","ma","mi","mu","me","mo","ya","yu","yo","ra","ri","ru","re","ro","wa","wo","n","ga","gi","gu","ge","go","za","ji","zu","ze","zo","da","di","du","de","do","ba","bi","bu","be","bo","pa","pi","pu","pe","po"]
		try:
			n=jp1.index(i)
			return az[n]
		except:
			try:
				n=jp2.index(i)
				return az[n]
			except:
				pass
				# print("%s	假名好像不完整\n"%i)
		return ""
	s=""
	# s+="^"#开头标识符
	for i in c:
		if re.match(r"[\u0000-\u007F]",i):#英
			s+=i.lower()
		elif re.match(r"[\u4E00-\u9FFF]",i):#中
			s+=hanzi_to_pinyin(i[0])
		elif re.match(r"[\u0800-\u4DFF]",i):#日，\u4E00是中文的一
			s+=jp_to_az(i)
		# if re.match(r"[\uAC00-\uD7FF]",c)#韩
	# s+="$"#结尾标识符
	return s




def what_day_is_today():
	"周一到周日返回1-7"
	today=int(time.strftime("%w"))
	if today==0:
		today=7
	return today

def which_icon(file_name):
	if "." not in file_name:
		icon=":/icon/folder.svg"
		return icon
	
	
	file_extension=file_name.split(".")[-1].lower()
	
	if file_extension=="url":
		icon=":/icon/globe.svg"
	elif file_extension in app_extension:
		icon=":/icon/box.svg"
	elif file_extension in audio_extension:
		icon=":/icon/music.svg"
	elif file_extension in playlist_extension:
		icon=":/icon/list.svg"
	elif file_extension in video_extension:
		icon=":/icon/film.svg"
	elif file_extension in image_extension:
		icon=":/icon/image.svg"
	elif file_extension in text_extension:
		icon=":/icon/file-text.svg"
	else:
		icon=":/icon/file.svg"
	return icon

def which_file_type(file_name):
	if "." not in file_name:
		return "folder"
	
	
	file_extension=file_name.split(".")[-1].lower()
	
	if file_extension=="url":
		return "url"
	elif file_extension in app_extension:
		return "exe"
	elif file_extension in audio_extension:
		return "audio"
	elif file_extension in playlist_extension:
		return "playlist"
	elif file_extension in video_extension:
		return "video"
	elif file_extension in image_extension:
		return "image"
	elif file_extension in text_extension:
		return "text"
	else:
		return "unknown"



def find_dict_in_string(s,name):
	"尝试在字符串中找出格式为 name:\{  \}的字典，返回一个字典，若找不到返回False"

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


class RSS_Parser():
	################################################################################
	#
	# 统一返回格式：(Status,feed_name,update_link_list)
	#
	# 统一返回的update_link_list文章列表中的每个文章字典必须包含以下两个key：[
	# 	{
	# 		"title":"",
	# 		"link":"",
	# 	}
	# ]
	# 
	# 重要！！！update_link_list中较新的文章在列表的前面，旧的在后面
	# 
	# 各自写各自的抓取方式！
	#
	# ERROR Status: Invalid 输入的url格式错误，无法匹配格式
	# ERROR Status: Failed 获取Feed信息错误
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
		"Bilibili导入格式：https://space.bilibili.com/up_ID"
		try:
			try:
				up_ID=re.findall("(?<=space\.bilibili\.com/)[\d]*",rss_url)[0]
			except:
				#不符合格式
				return ("Invalid",None,None)
			
			url_list=[]

			response=getHTML("https://api.bilibili.com/x/space/acc/info?mid="+up_ID,cookie)
			up_name=json.loads(response)["data"]["name"]

			response=getHTML("https://api.bilibili.com/x/space/arc/search?mid="+up_ID,cookie)
			video_list=json.loads(response)["data"]["list"]["vlist"]
			for video in video_list:
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
		"Bandcamp导入格式：https://NAME.bandcamp.com/"
		try:
			try:
				band_name=re.findall("(?<=https\://).+(?=\.bandcamp\.com)",rss_url)[0]
			except:
				#不符合格式
				return ("Invalid",None,None)

			url_list=[]
			response=getHTML(rss_url+"/music",cookie)
			html=etree.HTML(response)
			album_list=html.xpath('//*[@id="music-grid"]/li/a/@href')
			title_list=list(map(lambda x:x.strip(),html.xpath('//*[@id="music-grid"]/li/a/p/text()')))
			
			for i in range(len(album_list)):
				url_list.append(
					{
						"title":title_list[i],
						"link":rss_url+"/"+album_list[i]
					}
				)
			return ("Done",band_name,url_list)
		
		except:
			return ("Failed",None,None)
	
	def update_Pixiv_Illustration(self,rss_url,cookie=""):
		"Pixiv导入格式：https://www.pixiv.net/users/3371956"

		try:
			try:
				ID=rss_url.split("/")[-1]
				int(ID)
			except:
				#不符合格式
				return ("Invalid",None,None)
			
			response=json.loads(getHTML("https://www.pixiv.net/ajax/user/%s/profile/all"%ID,cookie))
			
			try:
				rss_name=response["body"]["pickup"][0]["userName"]
			except:
				#有一些用户pickup里面竟然是空的……
				#那就换一个包
				try:
					rss_name=json.loads(getHTML("https://www.pixiv.net/ajax/user/%s/profile/top"%ID,cookie))["body"]["extraData"]["meta"]["title"]
				except:
					rss_name="Unkown Feed"
			
			url_list=[]
			
			illustration_dict=response["body"]["illusts"]
			
			for i in illustration_dict.keys():
				
				url_list.append(
					{
						"title":i,
						"link":"https://www.pixiv.net/artworks/"+i
					}
				)
			
			return ("Done",rss_name,url_list)
		
		except:
			return ("Failed",None,None)
	
	def update_Pixiv_Manga(self,rss_url,cookie=""):
		"Pixiv导入格式：https://www.pixiv.net/users/3371956"

		try:
			try:
				ID=rss_url.split("/")[-1]
				int(ID)
			except:
				#不符合格式
				return ("Invalid",None,None)
			
			response=json.loads(getHTML("https://www.pixiv.net/ajax/user/%s/profile/all"%ID,cookie))

			try:
				rss_name=response["body"]["pickup"][0]["userName"]
			except:
				#有一些用户pickup里面竟然是空的……
				#那就换一个包
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
	
	def updata_Instagram(self,rss_url,cookie=""):
		"Instagram导入格式：https://www.instagram.com/ID"
		try:
			#真是刷新我的三观了，他妈的最后不带反斜线就会被反爬，加了反斜线就没问题……
			#整整两个半小时啊……
			#rss_url+"/"

			response=getHTML(rss_url+"/",cookie)
			try:
				html=etree.HTML(response)
				rss_name=html.xpath("/html/head/title/text()")[0].strip()
			except:
				rss_name="Unkown Feed"
			
			#淦！自己造的轮子，修了半天还是不能保证不出错……没用了……
			# find=find_dict_in_string(response,"edge_owner_to_timeline_media")
			
			#
			find=re.findall("(?<=window\._sharedData = ).*?(?=</script>)",response)[0][:-1]
			find=json.loads(find)["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
			
			url_list=[]
			for i in find:
				ID=i["node"]["shortcode"]
				url_list.append(
					{
						"title":ID,
						"link":"https://www.instagram.com/p/%s"%ID
					}
				)
			
			return ("Done",rss_name,url_list)
		
		except:
			return ("Failed",None,None)
		