from custom_function import *
from custom_widget import *

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from mytabwidget_form import Ui_mytabwidget_form
from setting_dialog import Ui_setting_dialog
from file_check_dialog import Ui_file_check_dialog
from rss_feed_edit_dialog import Ui_rss_feed_edit_dialog
from diary_search_dialog import Ui_diary_search_dialog


class RSS_Updator_Threador(QThread):
	"""
	更新文章列表的threador，传入你要更新的rss_url列表，
	每帮你更新完一个就emit一个带有rss_url的progress信号，
	你就要回去拿这里new_article_list去更新rss_data中对应的rss_url的文章，
	注意要正序插入到最前面
	"""

	progress = Signal(str)
	def setdata(self,parent,updating_url_list):
		#这里传进来的rss_data竟然是指针……因为它是列表……
		self.parent=parent
		self.updating_url_list=updating_url_list#需要更新的url_list
		
		self.tray=QSystemTrayIcon()
		self.tray.setContextMenu(self.parent.qmenu)
		self.tray.setIcon(QIcon(":/icon/holoico.ico"))
		self.need_to_quit=False

		#一个rss feed的新文章列表，每更新了一个就会emit一个带有rss_url的信号，回去了就对应rss_url，把new_article_list append进去
		self.new_article_list=[]

		self.rss_parser=RSS_Parser()
	
	def rss_feed_update(self,rss_url):
		
		# 统一返回格式：(Status,feed_name,update_link_list)
		#
		# 统一返回的update_link_list文章列表中的每个文章字典必须包含以下两个key：[
		# 	{
		# 		"title":"",
		# 		"link":"",
		# 	}
		# ]

		################################################################################
		################################################################################
		################################################################################

		#普通RSS
		if self.parent.rss_data[rss_url]["type"]=="Standard":
			# print("RSS",rss_url)
			
			(Status,feed_name,update_link_list)=self.rss_parser.update_normal_rss(rss_url)
			
		elif self.parent.rss_data[rss_url]["type"]=="Bilibili Video":
			# print("BILIBILI",rss_url)

			(Status,feed_name,update_link_list)=self.rss_parser.update_BiliBili_Video(rss_url)



		################################################################################
		################################################################################
		################################################################################

		if Status=="Invalid":
			self.tray.hide()
			self.tray.show()
			self.tray.showMessage("Infomation","RSS更新失败:\n%s"%self.parent.rss_data[rss_url]["feed_name"],QIcon(":/icon/holoico.ico"))
			return

		#超时了，或者
		if Status=="Failed":
			self.tray.hide()
			self.tray.show()
			self.tray.showMessage("Infomation","RSS更新失败:\n%s"%self.parent.rss_data[rss_url]["feed_name"],QIcon(":/icon/holoico.ico"))
			return

		################################################################################

		if Status=="Done":
			
			#先把之前所有的link列出来，塞进去的应该是之前没有的link
			alreay_have_list=[i[1] for i in self.parent.rss_data[rss_url]["article_list"]]

			updated=False

			
			#清空单位更新列表
			self.new_article_list=[]
			
			#一般的feed都是新发布的在前，所以这里倒序插入到首位
			#这里直接把最新的扔到更新列表的最后面，出去的时候再正序遍历更新列表，append到rss_data中时，最新的就回到最前面了
			for article in update_link_list:
				
				if article["link"] not in alreay_have_list:
					# 手动更新和每日自动更新在这里是不会冲突的，因为外面有qlock锁死着呢
					# print(self.parent.rss_data[rss_url]["feed_name"],article["title"])
					self.new_article_list.append([article["title"],article["link"],False,int(time.time())])
					updated=True

			

			if updated==True:
				#只有更新了，才出去把rss_data保存到外存
				self.progress.emit(rss_url)

				self.tray.hide()
				self.tray.show()
				self.tray.showMessage("Infomation","RSS更新成功:\n%s"%self.parent.rss_data[rss_url]["feed_name"],QIcon(":/icon/holoico.ico"))

			return



	def rss_data_update(self):
		
		for rss_url in self.updating_url_list:
			

			self.parent.qlock.lock()

			if self.need_to_quit==True:
				return
			
			self.rss_feed_update(rss_url)
			

			if self.need_to_quit==True:
				return


			self.parent.qlock.unlock()

			time.sleep(5)

		
	def run(self):
		self.rss_data_update()


class RSS_Adding_Getor_Threador(QThread):
	"添加新feed的threador，全部结束后应该回收这里的successed（添加成功的rss）字典和failed（解析失败的rss_url）列表"
	
	progress=Signal(int)

	def setdata(self,parent,adding_rss_url_list,update_type):
		self.parent=parent
		
		self.adding_rss_url_list=adding_rss_url_list

		self.temp_tree_item_list=[]

		self.update_type=update_type

		self.tray=QSystemTrayIcon()
		self.tray.setContextMenu(self.parent.qmenu)
		self.tray.setIcon(QIcon(":/icon/holoico.ico"))
		self.tray.show()


		self.successed={}#临时存放成功解析到的rss_data，所有都弄完后再被主线程并入self.rss_data中去
		self.failed=[]#解析失败的rss_url列表
		self.need_to_quit=False

		self.rss_parser=RSS_Parser()
	
	def rss_feed_add(self,rss_url):
		#淦这里的操作不能写在run()的for循环里面，为什么写在run里面就会在第二次的时候卡死？？
		#又是捉了快两个小时的虫子才捉出来……
		
		
		# 统一返回格式：(Status,feed_name,update_link_list)
		#
		# 统一返回的update_link_list文章列表中的每个文章字典必须包含以下两个key：[
		# 	{
		# 		"title":"",
		# 		"link":"",
		# 	}
		# ]

		################################################################################

		#普通RSS
		if self.update_type=="Standard":
			# print("RSS")
			(Status,feed_name,update_link_list)=self.rss_parser.update_normal_rss(rss_url)
			
		elif self.update_type=="Bilibili Video":
			# print("BILIBILI")
			(Status,feed_name,update_link_list)=self.rss_parser.update_BiliBili_Video(rss_url)

		################################################################################

		#parse出来的是个怪物
		if Status=="Invalid":
			self.failed.append(rss_url)
			self.tray.hide()
			self.tray.show()
			self.tray.showMessage("Infomation","RSS不符合标准:\n%s"%rss_url,QIcon(":/icon/holoico.ico"))
			return Status
			

		#超时了，或者
		if Status=="Failed":
			self.failed.append(rss_url)
			self.tray.hide()
			self.tray.show()
			self.tray.showMessage("Infomation","RSS解析失败:\n%s"%rss_url,QIcon(":/icon/holoico.ico"))
			return Status
		
		################################################################################
		
		if Status=="Done":
			
			
			
			if self.update_type=="Standard":
				#新建feed容器
				self.successed[rss_url]={
					"type":"Standard",
					"feed_name":feed_name,
					"unread":0,
					"frequency":[1,2,3,4,5,6,7],
					"article_list":[]
				}
			
			elif self.update_type=="Bilibili Video":
				#新建feed容器
				self.successed[rss_url]={
					"type":"Bilibili Video",
					"feed_name":feed_name,
					"unread":0,
					"frequency":[1,2,3,4,5,6,7],
					"article_list":[]
				}

		
							############################################################
			

			for article in update_link_list:
				#一般的feed都是新发布的在前，所以新建的时候可以从前往后直接append在list里面
				self.successed[rss_url]["article_list"].append([article["title"],article["link"],False,int(time.time())])
				self.successed[rss_url]["unread"]+=1
			
			

			feed_unread=str(self.successed[rss_url]["unread"])

			#树的信息中不区分RSS是Standard还是Custom，只区分Folder和RSS！这东西只是用于建树以及判断rss树的合法性的
			temp=QTreeWidgetItem(["[%s]|"%feed_unread+feed_name,"RSS",rss_url])
			temp.setIcon(0,QIcon(":/icon/rss.svg"))
			self.temp_tree_item_list.append(temp)
			#temp要传回去建树的
			


			self.tray.hide()
			self.tray.show()
			self.tray.showMessage("Infomation","RSS添加成功:\n%s"%rss_url,QIcon(":/icon/holoico.ico"))
			return Status
	
	def run(self):
		
		i=0
		for rss_url in self.adding_rss_url_list:
			
			self.parent.qlock.lock()
			
			if self.need_to_quit==True:
				return
			
			status=self.rss_feed_add(rss_url)
			
			if self.need_to_quit==True:
				return
			
			i+=1
			#只有成功的时候，返回更新treewidget的信号
			if status=="Done":
				self.progress.emit(i)
			
			self.parent.qlock.unlock()
			
			time.sleep(1)



class MyTabWidget(QWidget,Ui_mytabwidget_form):

	clicked=Signal(int)
	
	def __init__(self,parent,tab_selection_id,tab_selection_depth):
		super().__init__()
		self.setupUi(self)

		self.tab_selection_depth=tab_selection_depth
		self.tab_selection_id=tab_selection_id
		self.parent=parent

		#用来出去显示concept内容的
		self.current_select_ID=None

		
		#点击更新文件列表并且显示concept内容
		self.treeWidget.itemClicked.connect(self.update_file_list_and_show_parent_concept)

		self.listWidget_file_root.itemDoubleClicked.connect(self.root_file_open)
		self.listWidget_file_root.dropped.connect(self.concept_linked_file_add)
		self.listWidget_file_leafs.itemDoubleClicked.connect(self.leafs_file_open)

		self.tab_update()

	def concept_linked_file_add(self,links):
		"""
		从file library中进来的直接添加到当前日期，（如果带有内部路径，报错！）
		从concept或者tab root进来的判断是否为内部文件，
			如果是外部文件那就放到当前日期，
			如果是内部文件，先按照ymd查filedata中有没有，
				如果有就只做链接操作，
				如果没有，那就说明熊孩子在乱搞，明明可以用file check来添加他非得手拖进来，报出警告！
		diary区只允许从内部拖入，只链接文件
		"""

		if self.parent.file_saving_base=="":
			QMessageBox.warning(self,"Warning","如果要使用File Library，请先到Setting中设置File Library的基地址。（所有拖进File Library中的文件都会被移动到基地址下）")
			return
		
		#当日路径在不在
		if not os.path.exists(self.parent.file_saving_today_dst):
			os.makedirs(self.parent.file_saving_today_dst)
		else:
			pass
		
		#存不存在当日文件的容器
		try:
			self.parent.file_data[self.parent.y][self.parent.m][self.parent.d]
		except:
			self.parent.file_data[self.parent.y][self.parent.m][self.parent.d]={}

		adding_file=[]

		#移动文件到当日路径
		for i in links:
			
			#拥有内部路径
			try:
				date=list(map(lambda x:int(x),i.split("/")[-4:-1]))
				y=date[0]
				m=date[1]
				d=date[2]
				#检查file
				#如果拥有内部路径
				if self.parent.file_saving_base in i:
					if y in range(1970,2170) and m in range(1,13) and d in range(1,32):
						
						#如果filedata中已经存在，就只做链接操作
						try:
							file_name=os.path.basename(i)
							self.parent.file_data[y][m][d][file_name]

							file_icon=which_icon(file_name)
							adding_file.append(
								{
									"y":y,
									"m":m,
									"d":d,
									"file_name":file_name,
									"file_icon":file_icon
								}
							)
						#如果不存在，那就说明熊孩子在乱搞，明明可以用file check来添加他非得手拖进来
						except:
							QMessageBox.warning(self,"Warning","禁止从内部路径导入文件（可以用File Chack功能添加abundant文件）")
							return

			#拥有外部路径，移动到当日的文件库
			except:

				#如果是网址的话要预处理一下，生成一个url文件
				if i[:4]=="http" or i[:5]=="https":
					url_file_result=creat_net_url_file(i)
					if url_file_result[0]==False:
						QMessageBox.critical(self,"Error","导入网址失败:\n%s\n%s\n\n网络连接正常吗？\n网页编码标准吗？\n网页标题有没有文件名不允许出现的字符？\n\n请及时更改url文件名，否则第二次会被覆盖掉"%(url_file_result[2],i))
					
					i=url_file_result[1]
				
				file_name=os.path.basename(i)
				file_dst=self.parent.file_saving_today_dst+"/"+file_name
				shutil.move(i,file_dst)
				#文件链接concept置空
				self.parent.file_data[self.parent.y][self.parent.m][self.parent.d][file_name]=[]

				file_icon=which_icon(file_name)
				adding_file.append(
					{
						"y":self.parent.y,
						"m":self.parent.m,
						"d":self.parent.d,
						"file_name":file_name,
						"file_icon":file_icon
					}
				)
		
		#链接concept与文件的信息

		ID=int(self.parent.lineEdit_id.text())

		already_have=self.parent.concept_data[ID]["file"]

		for file in adding_file:
			file_name=file["file_name"]
			y=file["y"]
			m=file["m"]
			d=file["d"]
			if file not in already_have:
				self.parent.concept_data[ID]["file"].append(file)
			if ID not in self.parent.file_data[y][m][d][file_name]:
				self.parent.file_data[y][m][d][file_name].append(ID)
		
		#按照文件名排序
		self.parent.concept_data[ID]["file"].sort(key=lambda x:x["file_name"])

		#更新事物界面
		self.parent.concept_show(ID)
		self.parent.window_title_update()
		self.parent.file_library_list_update()

		for tab in self.parent.custom_tabs_shown:
			tab.tab_update()

	def concept_linked_file_remove(self):
		
		ID=int(self.parent.lineEdit_id.text())

		do=0
		for file_index in sorted([item.row() for item in self.listWidget_file_root.selectedIndexes()]):
			
			#取消file data中对concept的标记
			file=self.parent.concept_data[ID]["file"][file_index-do]
			file_name=file["file_name"]
			y=file["y"]
			m=file["m"]
			d=file["d"]
			self.parent.file_data[y][m][d][file_name].remove(ID)

			del self.parent.concept_data[ID]["file"][file_index-do]
			#del之后列表的长度就变了，索引的下标也要多减一
			do+=1

		#更新事物界面
		self.parent.concept_show(ID)
		self.parent.window_title_update()

		for tab in self.parent.custom_tabs_shown:
			tab.tab_update()

		#如果没有选中，返回的是-1，这样下标索引会到倒数第一个
		# if file_index!=-1:
			
			####
				#现在所有的文件都在file manager中，所以concept中文件存在与否就与diary没多大关系了
				#
				# file_link=self.parent.concept_data[ID]["file"][file_index]["file_link"]
				#
				# 判断是否有文本块链接到该文件
				# text_list=[]
				# for year_index in range(1970-1970,2170-1970):
				# 	for month_index in range(0,11):
				# 		for day_index in range(len(self.parent.diary_data[year_index]["date"][month_index])):
				# 			for line_index in range(len(self.parent.diary_data[year_index]["date"][month_index][day_index]["text"])):
				# 				for file_index in range(len(self.parent.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["linked_file"])):
									
				# 					linked_file_link=self.parent.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["linked_file"][file_index]["file_link"]
				# 					line_text=self.parent.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["line_text"]

				# 					if linked_file_link==file_link:
				# 						text_list.append({
				# 							"date":str(year_index+1970)+"."+str(month_index+1)+"."+str(self.parent.diary_data[year_index]["date"][month_index][day_index]["day"]),
				# 							"text":line_text
				# 					})
				# if text_list!=[]:
				# 	message=QMessageBox()
				# 	message.setWindowTitle("Warning")

				# 	#淦QMessageBox的大小不能直接改
				# 	# message.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
				# 	# message.setGeometry(0,0,800,400)

				# 	message.setIcon(QMessageBox.Warning)

				# 	#然而\n
				# 	#\n
				# 	#"这就是最简单(zhizhang)的改大小方法                                                         用空格和回车填充                           简单易用好上手！"
				# 	warning_text=file_link+" 在日志中已存在：\n\n\n                                                                "
				# 	message.setText(warning_text)

				# 	warning_detailed_text=""
				# 	for i in text_list:
				# 		warning_detailed_text+=i["date"]+" : "+i["text"]+"\n"
				# 	message.setDetailedText(warning_detailed_text)

				# 	message.exec_()
				# 	return


	def update_file_list_and_show_parent_concept(self):
		
		self.listWidget_file_root.setEnabled(1)
		self.listWidget_file_leafs.setEnabled(1)
		
		self.update_file_list()
		
		#出去显示concept内容
		self.clicked.emit(self.current_select_ID)

	
	def tab_update(self):
		
		#先检测tree节点的expand属性
		current_root=self.treeWidget.invisibleRootItem()
		self.tree_expand={}
		try:
			self.deep_check_expand(self.tab_selection_depth,current_root)
		except:
			pass
		
		self.treeWidget.clear()

		root_concept=self.parent.concept_data[self.tab_selection_id]
		new_root=QTreeWidgetItem([str(root_concept["id"])+"|"+root_concept["name"]])
		self.treeWidget.addTopLevelItem(new_root)
		self.deep_build_tree(self.tab_selection_depth,root_concept,new_root)
		
		try:
			self.update_file_list()
		except:
			pass

	def deep_check_expand(self,depth,current_root):
		if depth==0:
			return
		depth-=1

		
		for index in range(current_root.childCount()):
			#如果是folder，就记录一下expand属性
			child=current_root.child(index)
			if child.childCount()!=0:
				#key是str类型的id,value是isExpanded
				self.tree_expand[child.text(0).split("|")[0]]=child.isExpanded()
				self.deep_check_expand(depth,child)

		

	def deep_build_tree(self,depth,root_concept,current_root):
		if depth==0 or root_concept["child"]==[]:
			return
		depth-=1

		for concept_id in root_concept["child"]:
			leaf_concept=self.parent.concept_data[concept_id]
			current_leaf=QTreeWidgetItem(current_root,[str(leaf_concept["id"])+"|"+leaf_concept["name"]])
			self.deep_build_tree(depth,leaf_concept,current_leaf)
		
		try:
			current_root.setExpanded(self.tree_expand[str(root_concept["id"])])
		except:
			pass

	def deep_add_leafs_file(self,depth,ID):
		
		if depth==0:
			return
		depth-=1

		item=self.parent.concept_data[ID]
		for file in item["file"]:
			temp=QListWidgetItem()
			temp.setText(file["file_name"])
			temp.setIcon(QIcon(file["file_icon"]))

			file_url=self.parent.file_saving_base+"/"+str(file["y"])+"/"+str(file["m"])+"/"+str(file["d"])+"/"+file["file_name"]
			temp.setToolTip(file_url)
			
			self.listWidget_file_leafs.addItem(temp)
		
		for child_ID in self.parent.concept_data[ID]["child"]:
			
			self.deep_add_leafs_file(depth,child_ID)

	def update_file_list(self):
		try:
			self.current_select_ID=int(self.treeWidget.currentItem().text(0).split("|")[0])
		except:
			pass
		item=self.parent.concept_data[self.current_select_ID]

		#本层的文件
		self.listWidget_file_root.clear()
		for file in item["file"]:
			temp=QListWidgetItem()
			temp.setText(file["file_name"])
			temp.setIcon(QIcon(file["file_icon"]))

			file_url=self.parent.file_saving_base+"/"+str(file["y"])+"/"+str(file["m"])+"/"+str(file["d"])+"/"+file["file_name"]
			temp.setToolTip(file_url)

			self.listWidget_file_root.addItem(temp)

		#计算深入到叶子中的深度
		depth=self.tab_selection_depth+1
		leaf=self.treeWidget.currentItem()
		while leaf!=None:
			leaf=leaf.parent()
			depth-=1
		
		#本层之下的所有child里的文件

		self.listWidget_file_leafs.clear()
		for child_ID in self.parent.concept_data[self.current_select_ID]["child"]:
			self.deep_add_leafs_file(depth,child_ID)


	def root_file_open(self):
		#######################################
		# windows上可以使用os.startfile
		#
		# os.startfile(file)
		# linux上可以使用xdg-open
		# subprocess.call(["xdg-open", file])
		#
		# mac os上可以使用open
		# subprocess.call(["open", file])
		#######################################
		
		clicked_file_link=self.listWidget_file_root.currentItem().toolTip()

		#Alt双击打开文件所在目录
		if self.listWidget_file_root.alt_pressed==True:
			self.listWidget_file_root.alt_pressed=False
			os.startfile(os.path.split(clicked_file_link)[0])
			return
		#########################################################################################
		#########################################################################################
		############################如果按下ctrl双击图片，启动内置的图片浏览器#########################
		clicked_file_name=clicked_file_link.split("/")[-1]
		if which_file_type(clicked_file_name)=="image" and self.listWidget_file_root.ctrl_pressed==True:

			ID=int(self.parent.lineEdit_id.text())

			pic_list=[]

			for file in self.parent.concept_data[ID]["file"]:
				file_link=self.parent.file_saving_base+"/"+str(file["y"])+"/"+str(file["m"])+"/"+str(file["d"])+"/"+file["file_name"]
				file_name=file["file_name"]
				if which_file_type(file_name)=="image":
					pic_list.append(file_link)
		
			clicked_index=pic_list.index(clicked_file_link)

			self.parent.image_viewer=MyImageViewer(pic_list,clicked_index,self.parent.width(),self.parent.height())
			self.parent.image_viewer.show()
			self.listWidget_file_root.ctrl_pressed=False
		############################如果按下ctrl双击图片，启动内置的图片浏览器#########################
		#########################################################################################
		#########################################################################################
		
		else:
			try:
				os.startfile(clicked_file_link)
			except Exception as e :
				e=str(e).split(":",1)
				QMessageBox.critical(self,"Critical Error","%s\n%s\n请手动设置该类型文件的默认启动应用！"%(e[0],e[1]))
		
	def leafs_file_open(self):
		#######################################
		# windows上可以使用os.startfile
		#
		# os.startfile(file)
		# linux上可以使用xdg-open
		# subprocess.call(["xdg-open", file])
		#
		# mac os上可以使用open
		# subprocess.call(["open", file])
		#######################################

		clicked_file_link=self.listWidget_file_leafs.currentItem().toolTip()

		#Alt双击打开文件所在目录
		if self.listWidget_file_leafs.alt_pressed==True:
			self.listWidget_file_leafs.alt_pressed=False
			os.startfile(os.path.split(clicked_file_link)[0])
			return
		#########################################################################################
		#########################################################################################
		############################如果按下ctrl双击图片，启动内置的图片浏览器#########################
		clicked_file_name=clicked_file_link.split("/")[-1]
		if which_file_type(clicked_file_name)=="image" and self.listWidget_file_leafs.ctrl_pressed==True:

			pic_list=[]

			#这里去列表中的所有item找item的tooltip
			for file_index in range(self.listWidget_file_leafs.count()):
				
				file_link=self.listWidget_file_leafs.item(file_index).toolTip()
				file_name=file_link.split("/")[-1]
				if which_file_type(file_name)=="image":
					pic_list.append(file_link)
		
			clicked_index=pic_list.index(clicked_file_link)

			self.parent.image_viewer=MyImageViewer(pic_list,clicked_index,self.parent.width(),self.parent.height())
			self.parent.image_viewer.show()
			self.listWidget_file_leafs.ctrl_pressed=False
		############################如果按下ctrl双击图片，启动内置的图片浏览器#########################
		#########################################################################################
		#########################################################################################
		
		else:
			try:
				os.startfile(clicked_file_link)
			except Exception as e :
				e=str(e).split(":",1)
				QMessageBox.critical(self,"Critical Error","%s\n%s\n请手动设置该类型文件的默认启动应用！"%(e[0],e[1]))


class SettingDialog(QDialog,Ui_setting_dialog):
	def __init__(self,file_saving_base,font,font_size):
		super().__init__()
		self.setupUi(self)
		
		self.pushButtonfile_saving_base.clicked.connect(self.dir_dialog)
		self.pushButton_font.clicked.connect(self.font_dialog)

		self.file_saving_base=file_saving_base
		self.font=font
		self.font_size=font_size

		try:
			self.lineEdit_font.setText(self.font.family()+";"+str(self.font_size))
		except:
			pass

		self.lineEdit_file_saving_base.setText(self.file_saving_base)


	def dir_dialog(self):
		dlg=QFileDialog(self)
		self.file_saving_base=dlg.getExistingDirectory()
		self.lineEdit_file_saving_base.setText(self.file_saving_base)

	def font_dialog(self):
		ok, font = QFontDialog.getFont(QFont(), self)
		if ok:
			self.font=font
			self.font_size=font.pointSize()
			self.lineEdit_font.setText(self.font.family()+";"+str(self.font_size))




class RSS_Feed_Edit_Dialog(QDialog,Ui_rss_feed_edit_dialog):
	#传进来的列表元素是[rss_name,rss_url]
	def __init__(self,parent,rss_url_list):
		super().__init__()
		self.setupUi(self)
		self.parent=parent
		self.rss_url_list=rss_url_list
		
		self.listWidget.itemSelectionChanged.connect(self.save_and_show_feed)
		self.pushButton.clicked.connect(self.mark_all_article)


		#存储修改后的rss信息，这是要传出去修改rss_data的
		self.baked={}
		for rss in rss_url_list:
			rss_name=rss[0]
			rss_url=rss[1]
			self.baked[rss_url]={
				"feed_name":rss_name,
				"frequency":self.parent.rss_data[rss_url]["frequency"],
				"unread":self.parent.rss_data[rss_url]["unread"]
			}

		#初始化rss列表
		self.rss_list_update()
		
		self.current_selection=[0]

		#初始化信息界面，展示第一个条目
		rss_url=self.rss_url_list[0][1]
		self.lineEdit_url.setText(rss_url)
		frefre=""
		for i in self.baked[rss_url]["frequency"]:
			frefre+=str(i)+","
		frefre=frefre[:-1]
		self.lineEdit_frequency.setText(frefre)
		self.lineEdit_name.setText(self.baked[rss_url]["feed_name"])
		self.lineEdit_unread.setText(str(self.baked[rss_url]["unread"]))
	
	def mark_all_article(self):
		if len(self.current_selection)==1:
			index=self.current_selection[0]
			rss_url=self.rss_url_list[index][1]
			self.baked[rss_url]["unread"]=0

			rss_name=self.baked[rss_url]["feed_name"]
			text=rss_url+" "+rss_name
			QMessageBox.information(self,"Information","RSS文章全部标记已读！\n\n%s"%text)
		
		elif len(self.current_selection)>1:
			text=""
			for index in self.current_selection:
				
				rss_url=self.rss_url_list[index][1]
				self.baked[rss_url]["unread"]=0

				rss_name=self.baked[rss_url]["feed_name"]
				text+=rss_url+" "+rss_name+"\n"
			
			QMessageBox.information(self,"Information","RSS文章全部标记已读！\n\n%s"%text)
			
		self.lineEdit_unread.setText("0")
	
	def rss_list_update(self):
		self.listWidget.clear()
		for rss in self.rss_url_list:
			self.listWidget.addItem(rss[0])
	
	def rss_list_item_update(self,index,rss_url):
		self.listWidget.item(index).setText(self.baked[rss_url]["feed_name"])

	def save_and_show_feed(self):
		
		#先到baked中保存信息

		#单条目模式
		if len(self.current_selection)==1:
			index=self.current_selection[0]

			rss_url=self.rss_url_list[index][1]
			name=self.lineEdit_name.text()

			try:
				frequency=list(map(lambda x:int(x),self.lineEdit_frequency.text().split(",")))
			except:
				QMessageBox.warning(self,"Warning","Wrong Format")
				return
			
			#空
			if frequency==[]:
				QMessageBox.warning(self,"Warning","Wrong Format")
				return
			
			checked=[]
			#检查frequency合法性
			for i in frequency:
				#查星期几的范围
				if i not in range(1,8):
					QMessageBox.warning(self,"Warning","Wrong Format")
					return
				#查重
				if i not in checked:
					checked.append(i)
				else:
					QMessageBox.warning(self,"Warning","Wrong Format")
					return
			
			frequency.sort()
			
			self.baked[rss_url]["feed_name"]=name
			self.baked[rss_url]["frequency"]=frequency
			#baked中保存完毕

			#更新rss列表
			self.rss_list_item_update(index,rss_url)
		
		#多条目模式
		elif len(self.current_selection)>1:
			# 这里只保存frequency信息
			
			#如果没有修改，那就不管他了，放他走
			if self.lineEdit_frequency.text()=="":
				pass
			
			#修改了才要保存
			else:
				try:
					frequency=list(map(lambda x:int(x),self.lineEdit_frequency.text().split(",")))
				except:
					QMessageBox.warning(self,"Warning","Wrong Format")
					return

				#空
				if frequency==[]:
					QMessageBox.warning(self,"Warning","Wrong Format")
					return
				
				checked=[]
				#检查frequency合法性
				for i in frequency:
					#查星期几的范围
					if i not in range(1,8):
						QMessageBox.warning(self,"Warning","Wrong Format")
						return
					#查重
					if i not in checked:
						checked.append(i)
					else:
						QMessageBox.warning(self,"Warning","Wrong Format")
						return
				
				frequency.sort()

				for index in self.current_selection:
					
					rss_url=self.rss_url_list[index][1]
					ff=frequency
					self.baked[rss_url]["frequency"]=ff
					#baked中保存完毕
		
		##############################

		#展示新点击的条目
		self.current_selection=sorted([item.row() for item in self.listWidget.selectedIndexes()])

		#单条目模式
		if len(self.current_selection)==1:
			index=self.current_selection[0]

			rss_url=self.rss_url_list[index][1]
			self.lineEdit_url.setText(rss_url)
			
			frefre=""
			for i in self.baked[rss_url]["frequency"]:
				frefre+=str(i)+","
			frefre=frefre[:-1]
			self.lineEdit_frequency.setText(frefre)
			self.lineEdit_name.setText(self.baked[rss_url]["feed_name"])
			self.lineEdit_name.setReadOnly(0)
			self.lineEdit_unread.setText(str(self.baked[rss_url]["unread"]))

		
		#多条目模式
		elif len(self.current_selection)>1:
			name=""
			for index in self.current_selection:
				rss_url=self.rss_url_list[index][1]
				name+=self.baked[rss_url]["feed_name"]+";"
			
			self.lineEdit_frequency.setText("")
			self.lineEdit_name.setText(name)
			self.lineEdit_name.setReadOnly(1)
			self.lineEdit_unread.setText("xxx")



class FileCheckDialog(QDialog,Ui_file_check_dialog):
	"""
		缺失的文件
		missing.append(
			{
				"y":y,
				"m":m,
				"d":d,
				"file_name":file_name,
				"linked_concept":self.file_data[y][m][d][file_name]
			}
		)
		多余的文件
		redundant.append(
			{
				"y":y,
				"m":m,
				"d":d,
				"file_name":file_name
			}
		)
	"""
	def __init__(self,parent,missing,redundant):
		super().__init__()
		self.setupUi(self)
		self.splitter.setStretchFactor(0,10)
		self.splitter.setStretchFactor(1,1)
		self.parent=parent
		self.missing=missing
		self.redundant=redundant


		self.pushButton_quit.clicked.connect(self.close)
		self.pushButton_erase.clicked.connect(self.erase_missing_files)
		self.pushButton_add.clicked.connect(self.add_redundant_files)
		self.pushButton_replace.clicked.connect(self.replace_files)
		self.pushButton_left_clear.clicked.connect(self.listWidget_left.clear)
		self.pushButton_right_clear.clicked.connect(self.listWidget_right.clear)

		self.listWidget_missing_file.itemClicked.connect(self.file_missing_clicked)

		self.file_check_list_update()
	

	def file_missing_clicked(self):
		index=self.listWidget_missing_file.currentRow()

		self.listWidget_missing_file_related_concept.clear()
		for ID in self.missing[index]["linked_concept"]:
			self.listWidget_missing_file_related_concept.addItem(str(ID)+"|"+self.parent.concept_data[ID]["name"])
		
		y=str(self.missing[index]["y"])
		m=str(self.missing[index]["m"])
		d=str(self.missing[index]["d"])
		self.lineEdit_date.setText(y+"."+m+"."+d)

	
	def file_check_list_update(self):
		self.listWidget_missing_file.clear()
		self.listWidget_redundant_file.clear()
		self.listWidget_left.clear()
		self.listWidget_right.clear()
		self.listWidget_missing_file_related_concept.clear()
		self.lineEdit_date.clear()

		for index in range(len(self.missing)):
			file_url=self.parent.file_saving_base+"/"+str(self.missing[index]["y"])+"/"+str(self.missing[index]["m"])+"/"+str(self.missing[index]["d"])+"/"+self.missing[index]["file_name"]
			self.listWidget_missing_file.addItem("L"+"|"+str(index)+"|"+file_url)
		
		for index in range(len(self.redundant)):
			file_url=self.parent.file_saving_base+"/"+str(self.redundant[index]["y"])+"/"+str(self.redundant[index]["m"])+"/"+str(self.redundant[index]["d"])+"/"+self.redundant[index]["file_name"]
			self.listWidget_redundant_file.addItem("R"+"|"+str(index)+"|"+file_url)

	def erase_missing_files(self):
		if len(self.listWidget_missing_file.selectedIndexes())==0:
			QMessageBox.warning(self,"Warning","Empty!")
			return

		self.plainTextEdit.appendPlainText("------------------------")
		self.plainTextEdit.appendPlainText("Erasing Start!\n")
		
		do=0
		for file_index in sorted([item.row() for item in self.listWidget_missing_file.selectedIndexes()]):
			file=self.missing[file_index-do]

			y=file["y"]
			m=file["m"]
			d=file["d"]
			file_name=file["file_name"]

			# (1)清除concept data中的相关数据
			for ID in file["linked_concept"]:
				for ff in self.parent.concept_data[ID]["file"]:
					if ff["y"]==y and ff["m"]==m and ff["d"]==d and ff["file_name"]==file_name:
						self.parent.concept_data[ID]["file"].remove(ff)

						#logging
						self.plainTextEdit.appendPlainText("Erased y:%s m:%s d:%s file_name:%s from concept_data:(id:%s)\n"%(y,m,d,file_name,ID))
						break
					
			# (2)清除diary data中的相关数据
			for year_index in range(1970-1970,2170-1970):
				for month_index in range(0,12):
					for day_index in range(len(self.parent.diary_data[year_index]["date"][month_index])):
						for line_index in range(len(self.parent.diary_data[year_index]["date"][month_index][day_index]["text"])):
							for ff in self.parent.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["linked_file"]:
								if ff["y"]==y and ff["m"]==m and ff["d"]==d and ff["file_name"]==file_name:
									self.parent.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["linked_file"].remove(ff)

									#logging
									self.plainTextEdit.appendPlainText("Erased y:%s m:%s d:%s file_name:%s from diary_data:(y:%s m:%s d:%s line_index:%s)\n"%(y,m,d,file_name,year_index,month_index,day_index,line_index))
									break

			# (3)清除file data中的相关数据
			del self.parent.file_data[y][m][d][file_name]
			#logging
			self.plainTextEdit.appendPlainText("Erased y:%s m:%s d:%s file_name:%s from file_data\n"%(y,m,d,file_name))

			self.missing.pop(file_index-do)
			do+=1
		
		self.plainTextEdit.appendPlainText("\nErasing Done!")
		self.plainTextEdit.appendPlainText("------------------------\n")
		self.file_check_list_update()

	def add_redundant_files(self):
		if len(self.listWidget_redundant_file.selectedIndexes())==0:
			QMessageBox.warning(self,"Warning","Empty!")
			return

		self.plainTextEdit.appendPlainText("------------------------")
		self.plainTextEdit.appendPlainText("Adding Start!\n")
		
		do=0
		for file_index in sorted([item.row() for item in self.listWidget_redundant_file.selectedIndexes()]):
			file=self.redundant[file_index-do]
			y=file["y"]
			m=file["m"]
			d=file["d"]
			file_name=file["file_name"]
			#文件链接concept置空
			self.parent.file_data[y][m][d][file_name]=[]

			#logging
			self.plainTextEdit.appendPlainText("Added y:%s m:%s d:%s file_name:%s into file_data\n"%(y,m,d,file_name))

			self.redundant.pop(file_index-do)
			do+=1
		
		self.plainTextEdit.appendPlainText("\nAdding Done!")
		self.plainTextEdit.appendPlainText("------------------------\n")
		self.file_check_list_update()
	
	def replacing_check(self):
		"replace之前检查合法性"

		left_list=[]
		right_list=[]
		left_total=self.listWidget_left.count()
		right_total=self.listWidget_right.count()

		if left_total!=right_total:
			QMessageBox.warning(self,"Warning","Unmatched!")
			return False
		
		if left_total==0 or right_total==0:
			QMessageBox.warning(self,"Warning","Empty!")
			return False
		for i in range(left_total):
			text=self.listWidget_left.item(i).text()

			#查左右
			if text[0]!="L":
				QMessageBox.warning(self,"Warning","Wrong Side!")
				return False
			
			#查重，应该是一对一，所以不可能会重复的
			if text not in left_list:
				left_list.append(text)
			else:
				QMessageBox.warning(self,"Warning","Duplicated!")
				return False

		for i in range(right_total):
			text=self.listWidget_right.item(i).text()

			#查左右
			if text[0]!="R":
				QMessageBox.warning(self,"Warning","Wrong Side!")
				return False

			#查重，应该是一对一，所以不可能会重复的
			if text not in right_list:
				right_list.append(text)
			else:
				QMessageBox.warning(self,"Warning","Duplicated!")
				return False
		
		return True
	
	def replace_files(self):
		
		if self.replacing_check():
			self.plainTextEdit.appendPlainText("------------------------")
			self.plainTextEdit.appendPlainText("Replacing Start!\n")
			
			#生成old和new的replacing列表
			old_file_list=[]
			need_to_delete=[]
			for index in range(self.listWidget_left.count()):
				file_index=int(self.listWidget_left.item(index).text().split("|")[1])
				file=self.missing[file_index]
				old_file_list.append(file)
				need_to_delete.append(file_index)
			
			do=0
			for index in sorted(need_to_delete):
				self.missing.pop(index-do)
				do+=1
			
			new_file_list=[]
			need_to_delete=[]
			for index in range(self.listWidget_right.count()):
				file_index=int(self.listWidget_right.item(index).text().split("|")[1])
				file=self.redundant[file_index]
				new_file_list.append(file)
				need_to_delete.append(file_index)

			do=0
			for index in sorted(need_to_delete):
				self.redundant.pop(index-do)
				do+=1
			
			del need_to_delete
			del do

			#开始replace
			for index in range(len(old_file_list)):
				
				old_file=old_file_list[index]
				old_y=old_file["y"]
				old_m=old_file["m"]
				old_d=old_file["d"]
				old_file_name=old_file["file_name"]

				new_file=new_file_list[index]
				new_y=new_file["y"]
				new_m=new_file["m"]
				new_d=new_file["d"]
				new_file_name=new_file["file_name"]
				new_file_icon=which_icon(new_file_name)
				# replace concept data中的old data，增加file data中的new data

				self.parent.file_data[new_y][new_m][new_d][new_file_name]=[]
				for ID in old_file["linked_concept"]:
					
					#file data中的linked id顺便改了
					self.parent.file_data[new_y][new_m][new_d][new_file_name].append(ID)

					#replace old file中linked id中的linked file的信息
					for ff_index in range(len(self.parent.concept_data[ID]["file"])):
						
						ff=self.parent.concept_data[ID]["file"][ff_index]
						if ff["y"]==old_y and ff["m"]==old_m and ff["d"]==old_d and ff["file_name"]==old_file_name:
							
							self.parent.concept_data[ID]["file"][ff_index]["y"]=new_y
							self.parent.concept_data[ID]["file"][ff_index]["m"]=new_m
							self.parent.concept_data[ID]["file"][ff_index]["d"]=new_d
							self.parent.concept_data[ID]["file"][ff_index]["file_name"]=new_file_name
							self.parent.concept_data[ID]["file"][ff_index]["file_icon"]=new_file_icon

							#logging
							self.plainTextEdit.appendPlainText("Replaced y:%s m:%s d:%s file_name:%s in concept_data:(id:%s) by y:%s m:%s d:%s file_name:%s\n"%(old_y,old_m,old_d,old_file_name,ID,new_y,new_m,new_d,new_file_name))
							break
					
				
				# 删除file data中的old data
				del self.parent.file_data[old_y][old_m][old_d][old_file_name]
				#logging
				self.plainTextEdit.appendPlainText("Replaced y:%s m:%s d:%s file_name:%s in file_data by y:%s m:%s d:%s file_name:%s\n"%(old_y,old_m,old_d,old_file_name,new_y,new_m,new_d,new_file_name))
				

				# replace diary data中的old data
				for year_index in range(1970-1970,2170-1970):
					for month_index in range(0,12):
						for day_index in range(len(self.parent.diary_data[year_index]["date"][month_index])):
							for line_index in range(len(self.parent.diary_data[year_index]["date"][month_index][day_index]["text"])):
								for ff_index in range(len(self.parent.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["linked_file"])):
									ff=self.parent.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["linked_file"][ff_index]
									if ff["y"]==old_y and ff["m"]==old_m and ff["d"]==old_d and ff["file_name"]==old_file_name:
										
										self.parent.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["linked_file"][ff_index]["y"]=new_y
										self.parent.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["linked_file"][ff_index]["m"]=new_m
										self.parent.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["linked_file"][ff_index]["d"]=new_d
										self.parent.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["linked_file"][ff_index]["file_name"]=new_file_name
										self.parent.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["linked_file"][ff_index]["file_icon"]=new_file_icon

										#logging
										self.plainTextEdit.appendPlainText("Replaced y:%s m:%s d:%s file_name:%s from diary_data:(y:%s m:%s d:%s line_index:%s) by y:%s m:%s d:%s file_name:%s\n"%(old_y,old_m,old_d,old_file_name,year_index,month_index,day_index,line_index,new_y,new_m,new_d,new_file_name))
										break

		self.plainTextEdit.appendPlainText("\nReplacing Done!")
		self.plainTextEdit.appendPlainText("------------------------\n")
		self.file_check_list_update()
		return


class DiarySearchDialog(QDialog,Ui_diary_search_dialog):
	def __init__(self,parent):
		super().__init__()
		self.setupUi(self)
		self.parent=parent

		try:
			font=self.parent.user_settings.value("font")
			font_size=int(self.parent.user_settings.value("font_size"))
		
			self.textEdit.setFont(font)
			font.setPointSize(font_size)
			self.listWidget.setFont(font)
			self.listWidget_concept.setFont(font)
			self.lineEdit.setFont(font)
		except:
			pass

		self.lineEdit.returnPressed.connect(self.list_update)
		self.listWidget.itemClicked.connect(self.show_clicked_item)

	def show_clicked_item(self):
		index=self.listWidget.currentRow()
		
		day_text=""
		clicked_item=self.listing_result[index]
		y=clicked_item["y"]
		m=clicked_item["m"]
		d=clicked_item["d"]
		text=clicked_item["text"]
		d_index=clicked_item["d_index"]

		self.lineEdit_date.setText(str(y)+"."+str(m)+"."+str(d))
		
		self.listWidget_concept.clear()
		for ID in clicked_item["linked_concept"]:
			self.listWidget_concept.addItem(str(ID)+"|"+self.parent.concept_data[ID]["name"])


		day_text=""
		for i in self.parent.diary_data[y-1970]["date"][m-1][d_index]["text"]:
			day_text+=i["line_text"]+"\n\n"
		
		#所在行数，不能保证每次都正确定位，因为markdown中的换行可能是两个可能是一个
		row=day_text[:day_text.find(text)].count("\n\n")+day_text[:day_text.find(text)].replace("\n\n","").count("\n")

		self.textEdit.setFocus()
		self.textEdit.setMarkdown(day_text)
		cursor=QTextCursor(self.textEdit.document().findBlockByLineNumber(row))
		self.textEdit.moveCursor(QTextCursor.End)
		self.textEdit.setTextCursor(cursor)

	def list_update(self):
		# 精确搜索待做 格式："ASD" \c="asd" \c="qwe" \d="2021.3.1"
		self.listWidget.clear()
		self.listWidget.scrollToTop()

		search=self.lineEdit.text()
		self.listing_result=[]
		mode=1
		
		# 普通搜索 格式：asd qwe zxc（然后去text和text linked concept中把所有可能的项目都列出来）
		if mode==1:
			search=search.split()
			for year_index in range(1970-1970,2170-1970):
				for month_index in range(0,12):
					d_index=0
					for day in self.parent.diary_data[year_index]["date"][month_index]:
						for line in day["text"]:
							
							line_text=line["line_text"]
							concept_id_list=line["linked_concept"]

							weight=0
						
							weight_list=[]
							
							ll=line_text.lower()
							for ss in search:
								ss=ss.lower()
								text_weight=ll.count(ss)

								have_concept=False
								for ID in concept_id_list:
									concept=self.parent.concept_data[ID]
									if ss==concept["name"] or ss==concept["az"]:
										concept_weight=2
										have_concept=True
										break
									elif ss in concept["detail"]:
										concept_weight=1.2
										have_concept=True
									
								
								if have_concept==False:
									concept_weight=1
								
								key_weight=text_weight*concept_weight+have_concept*1.5

								weight_list.append(key_weight)
							
							if min(weight_list)==0:
								continue
							weight=sum(weight_list)
							####
								#先统计每个关键词在句子中出现的频度
								# count_list=[]

								# for ss in search:
								# 	ss=ss.lower()
								# 	count_list.append(ll.count(ss))
								
								# #惩罚，如果有关键词不存在，就使劲扣分，用最大的数量去除
								# n=len(count_list)
								# MAX=max(count_list)
								# if MAX!=0:
								# 	for index in range(n):
								# 		if count_list[index]==0:
								# 			for ii in range(n):
								# 				count_list[ii]/=MAX
								# 				count_list[ii]-=1
								# 	weight+=sum(count_list)
								
								# #在句子中关键词全部都没有出现过，考虑到可能另外手动打标了，在concept中有
								# #给他一点机会，只抠掉关键词个数的分数
								# if MAX==0:
								# 	weight-=n
								
								# #如果和concept对应上了，大大地奖赏（这里的1.5分就是很大的分数了，因为上面句子中匹配到一个才加一分）
								# for ID in concept_id_list:
								# 	concept=self.parent.concept_data[ID]
								# 	for ss in search:
								# 		if ss==concept["name"] or ss==concept["az"]:
								# 			weight+=1.5
								# 			#这里如果是2的话就太多了哈哈哈
								# 		elif ss in concept["detail"]:
								# 			weight+=0.2
							
							if weight>0:
								temp={
									"y":day["year"],
									"m":day["month"],
									"d":day["day"],
									"d_index":d_index,
									"text":line_text,
									"linked_concept":line["linked_concept"],
									"weight":weight
								}
								self.listing_result.append(temp)
						d_index+=1
			
		self.listing_result.sort(key=lambda x:x["weight"],reverse=True)
		
		#展示最多前十五条
		self.listing_result=self.listing_result[:15]
		for i in self.listing_result[:15]:
			self.listWidget.addItem(str(i["weight"])+"|"+i["text"])
			# self.listWidget.addItem(i["text"])