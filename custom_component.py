from custom_function import *
from custom_widget import *

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCharts import QtCharts

from mytabwidget_form import Ui_mytabwidget_form
from setting_dialog import Ui_setting_dialog
from file_check_dialog import Ui_file_check_dialog
from rss_feed_edit_dialog import Ui_rss_feed_edit_dialog
from diary_search_dialog import Ui_diary_search_dialog
from diary_analyze_dialog import Ui_diary_analyze_dialog

class RSS_Updator_Threador(QThread):
	"""
	更新文章列表的threador，传入你要更新的rss_url列表，
	每帮你更新完一个就emit一个带有rss_url的progress信号，
	你就要回去拿这里new_article_list去更新rss_data中对应的rss_url的文章，
	注意要正序插入到最前面
	"""

	progress = Signal(str,bool)
	started=Signal(str)
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


		
		#注意要去掉屁股上的后缀信息rss_url.split("||")[0]
		if self.parent.rss_data[rss_url]["type"]=="Standard":
			(Status,feed_name,update_link_list)=self.rss_parser.update_normal_rss(rss_url.split("||")[0])
			
		elif self.parent.rss_data[rss_url]["type"]=="Bilibili Video":
			(Status,feed_name,update_link_list)=self.rss_parser.update_BiliBili_Video(rss_url.split("||")[0])
		
		elif self.parent.rss_data[rss_url]["type"]=="Bandcamp":
			(Status,feed_name,update_link_list)=self.rss_parser.updata_Bandcamp(rss_url.split("||")[0])

		elif self.parent.rss_data[rss_url]["type"]=="Pixiv Illustration":
			cookie=self.parent.user_settings.value("pixiv_cookie")
			if cookie!="" and cookie!=None:
				cookie=decrypt(cookie)
			
			(Status,feed_name,update_link_list)=self.rss_parser.update_Pixiv_Illustration(rss_url.split("||")[0],cookie)
		
		elif self.parent.rss_data[rss_url]["type"]=="Pixiv Manga":
			cookie=self.parent.user_settings.value("pixiv_cookie")
			if cookie!="" and cookie!=None:
				cookie=decrypt(cookie)
			
			(Status,feed_name,update_link_list)=self.rss_parser.update_Pixiv_Manga(rss_url.split("||")[0],cookie)
		
		elif self.parent.rss_data[rss_url]["type"]=="Instagram":
			cookie=self.parent.user_settings.value("instagram_cookie")
			if cookie!="" and cookie!=None:
				cookie=decrypt(cookie)
			
			(Status,feed_name,update_link_list)=self.rss_parser.updata_Instagram(rss_url.split("||")[0],cookie)


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
			
			#update_link_list中新文章在最前面，这里用append，new_article_list中依旧是新文章在最前面
			#出去的时候再倒序遍历new_article_list，insert到rss_data中的最前面
			for article in update_link_list:
				
				if article["link"] not in alreay_have_list:
					# 手动更新和每日自动更新在这里是不会冲突的，因为外面有qlock锁死着呢
					
					self.new_article_list.append([article["title"],article["link"],False,int(time.time())])
					updated=True


			#每做完一个，都要出去更新last_update，另外如果updated==True，外面还要append new_article_list，并且更新tree列表和文章列表
			self.progress.emit(rss_url,updated)

			if updated==True:
				self.tray.hide()
				self.tray.show()
				self.tray.showMessage("Infomation","RSS更新成功:\n%s"%self.parent.rss_data[rss_url]["feed_name"],QIcon(":/icon/holoico.ico"))

			return



	def rss_data_update(self):

		for rss_url in self.updating_url_list:
			#让外面更新windowTitle
			self.started.emit(rss_url)

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

		#比如Pixiv的Illustration和Manga的输入是同样的rss_url，而解析模式不同，自然也应该有不同的标记符
		#所以可以在rss_url的屁股上添加信息
		#在update thread中去掉屁股就可以正常更新解析了
		if self.update_type=="Standard":
			(Status,feed_name,update_link_list)=self.rss_parser.update_normal_rss(rss_url)
			rss_url+="||Standard"
			
		elif self.update_type=="Bilibili Video":
			(Status,feed_name,update_link_list)=self.rss_parser.update_BiliBili_Video(rss_url)
			rss_url+="||Bilibili Video"
		
		elif self.update_type=="Bandcamp":
			(Status,feed_name,update_link_list)=self.rss_parser.updata_Bandcamp(rss_url)
			rss_url+="||Bandcamp"

		elif self.update_type=="Pixiv Illustration":
			cookie=self.parent.user_settings.value("pixiv_cookie")
			if cookie!="" and cookie!=None:
				cookie=decrypt(cookie)
			
			(Status,feed_name,update_link_list)=self.rss_parser.update_Pixiv_Illustration(rss_url,cookie)
			rss_url+="||Pixiv Illustration"

		elif self.update_type=="Pixiv Manga":
			cookie=self.parent.user_settings.value("pixiv_cookie")
			if cookie!="" and cookie!=None:
				cookie=decrypt(cookie)
			
			(Status,feed_name,update_link_list)=self.rss_parser.update_Pixiv_Manga(rss_url,cookie)
			rss_url+="||Pixiv Manga"

		elif self.update_type=="Instagram":
			cookie=self.parent.user_settings.value("instagram_cookie")
			if cookie!="" and cookie!=None:
				cookie=decrypt(cookie)
			
			(Status,feed_name,update_link_list)=self.rss_parser.updata_Instagram(rss_url,cookie)
			rss_url+="||Instagram"

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
			
			#标记最新更新日期
			last_update=str(self.parent.y)+str(self.parent.m)+str(self.parent.d)

			#新建feed容器
			self.successed[rss_url]={
				"type":self.update_type,
				"feed_name":feed_name,
				"unread":0,
				"frequency":[1,2,3,4,5,6,7],
				"last_update":last_update,
				"article_list":[]
			}

			#update_link_list中新文章在最前面，所以添加新feed的时候，可以从前往后直接append在list里面
			for article in update_link_list:
				
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
			
			time.sleep(2)


class MyTabWidget(QWidget,Ui_mytabwidget_form):

	#本来这个是点击tree item后用来传出去show concept用的，现在tab页有自己的concept编辑区了
	# clicked=Signal(int)
	
	def __init__(self,parent,tab_selection_id,tab_selection_depth):
		super().__init__()
		self.setupUi(self)

		self.tab_selection_depth=tab_selection_depth
		self.tab_selection_id=tab_selection_id
		self.parent=parent

		self.current_select_conceptID=None#当前选择的conceptID
		self.current_leaf_conceptID_list=[]#当前选择的conceptID下的所有leaf的ID的列表

		self.begin_date=self.parent.calendarWidget.selectedDate()#当前分析的开始日期，是QDate类型
		self.end_date=self.parent.calendarWidget.selectedDate()#当前分析的结束日期，是QDate类型
		self.MaxY=0#最大的y坐标（一天内最多的concept的数量的最大值
		self.series=None
		self.chartView_spline=MyChartView()
		self.clear_view()

		#貌似没办法在ui文件中定义一个只含有一个widget的splitter，只能先拿一个东西占位，再删掉了
		self.pushButton.deleteLater()
		self.splitter_top.addWidget(self.chartView_spline)
		self.splitter_top.setStretchFactor(0,1)
		self.splitter_top.setStretchFactor(1,1)
		self.splitter_top.setStretchFactor(2,2)
		# print(self.splitter_top.count())

		#编辑结束后自动临时保存
		self.lineEdit_name.editingFinished.connect(self.concept_info_edited_and_save)
		###QPlainTextEdit没有editingFinished信号，就用了自定义的MyPlainTextEdit
		self.plainTextEdit_detail.editingFinished.connect(self.concept_info_edited_and_save)

		#点击更新文件列表并且显示concept内容
		self.treeWidget.itemClicked.connect(self.tree_item_clicked)

		#文件区
		self.listWidget_file_root.itemDoubleClicked.connect(self.root_file_open)
		self.listWidget_file_root.dropped.connect(self.concept_linked_file_add)
		self.listWidget_file_leafs.itemDoubleClicked.connect(self.leafs_file_open)
		
		
		self.tab_update()
	
	def tab_update(self):
		"""
		外面更新了data来调用这个函数，更新tab内所有的内容，
		包括tree，concept的信息，concept的file，concept的diary text，concept-diary text的图线
		"""
		
		###################################################################################
		# Tree

		#先检测tree节点的expand属性
		current_root=self.treeWidget.invisibleRootItem()
		self.tree_expand={}
		try:
			self.tree_deep_check_expand(self.tab_selection_depth,current_root)
		except:
			pass
		
		self.treeWidget.clear()

		root_concept=self.parent.concept_data[self.tab_selection_id]
		new_root=QTreeWidgetItem([str(root_concept["id"])+"|"+root_concept["name"]])
		self.treeWidget.addTopLevelItem(new_root)
		self.tree_deep_duild(self.tab_selection_depth,root_concept,new_root)
		
		###################################################################################
		# Concept
		try:
			self.concept_show()
		except:
			pass

		###################################################################################
		# File
		try:
			self.update_file_list()
		except:
			pass

	def tree_item_clicked(self):
		
		def update_current_leaf_concept_list():
			"更新self.current_leaf_conceptID_list"
			
			def deepin(depth,ID):
				if depth==0:
					return
				depth-=1

				for child_ID in self.parent.concept_data[ID]["child"]:
					self.current_leaf_conceptID_list.append(child_ID)
					deepin(depth,child_ID)
			

			self.current_leaf_conceptID_list=[]
			#计算深入到叶子中的深度
			depth=self.tab_selection_depth+1
			leaf=self.treeWidget.currentItem()
			while leaf!=None:
				leaf=leaf.parent()
				depth-=1

			deepin(depth,self.current_select_conceptID)

		
		#更新self.current_select_conceptID和self.current_leaf_conceptID_list
		self.current_select_conceptID=int(self.treeWidget.currentItem().text(0).split("|")[0])
		update_current_leaf_concept_list()
		
		self.concept_show()

		self.update_file_list()

		self.listWidget_file_root.setEnabled(1)
		self.listWidget_file_leafs.setEnabled(1)
		
		####
			#现在tab页有自己的concept编辑区了
			#出去显示concept内容
			# self.clicked.emit(self.current_select_conceptID)

	def spline_hovered(self,*arg):
		"""
		这里传进来参数有：信号参数hover_point(QPoint)、hover_on_line(True False)

		如果在点上，展示向上的箭头
		否则，展示普通箭头

		有个不完美的地方，这个hovered信号的触发仅限于进入和离开，如果一直在线上移动，是不会触发hovered信号的
		所以如果一直沿着线移动，即使到了点上，也不会展示向上的箭头
		但有谁会无聊到沿着线移鼠标啊？
		
		抖叽~
		"""
		y_range=int(self.chartView_spline.chart().axisY().max())-int(self.chartView_spline.chart().axisY().min())
		y_count=self.chartView_spline.ymax_TickCount
		y_deviation=y_range/(y_count+1)

		hover_point=arg[0]
		hover_x=hover_point.x()
		hover_y=hover_point.y()
		hover_on_line=arg[1]

		if hover_on_line==True:
			# print("in")

			#计算点的位置的附近，是否在存在concept的日期
			for point in self.series.pointsVector():
				x=point.x()
				y=point.y()

				if abs(hover_x-x)<3600000*20 and abs(hover_y-y)<y_deviation:
					# print("found")

					#如果点到了有concept的日期，显示向上的箭头
					self.setCursor(QCursor(Qt.UpArrowCursor))
					break
			else:
				# print("not found")

				#只是在线上的某一点，显示食指
				self.setCursor(QCursor(Qt.PointingHandCursor))

		else:
			# print("out")

			#显示普通箭头
			self.setCursor(QCursor(Qt.ArrowCursor))




	def spline_clicked(self,*arg):
		"""
		这里传进来的参数有：信号参数hover_point(QPoint)
		
		如果点到了有concept的日期，那只显示那一天的diary text，
		"""
		y_range=int(self.chartView_spline.chart().axisY().max())-int(self.chartView_spline.chart().axisY().min())
		y_count=self.chartView_spline.ymax_TickCount
		y_deviation=y_range/(y_count+1)

		clicked_point=arg[0]
		clicked_x=clicked_point.x()
		clicked_y=clicked_point.y()

		
		###################################################################################################
		
		#展示对应concept的diary text

		#计算点的位置的附近，是否在存在concept的日期
		
		for point in self.series.pointsVector():
			x=point.x()
			y=point.y()
			
			if abs(clicked_x-x)<3600000*20 and abs(clicked_y-y)<y_deviation:
				
				datetime=QDateTime().fromMSecsSinceEpoch(int(x))
				date=datetime.date()
				
				y=date.year()
				m=date.month()
				d=date.day()
				
				#如果点到了有concept的日期，那只显示那一天的diary text，
				self.concept_related_text_show(y,m,d)

				break
		else:
			#如果点到不存在concept的日期上，展示该concept所有的diary text
			self.concept_related_text_show()
			pass
	
	def concept_related_text_show(self,y=0,m=0,d=0,plot=False):
		"这里同时操作了series，贴一个防止修改series的狗皮膏药 plot=False"
		
		week_dict=["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
		text_list=[]
		
		#如果点到不存在concept的日期上，展示该concept所有的diary text
		if y==0 and m==0 and d==0:
			
			for year_index in range(1970-1970,2170-1970):
				for month_index in range(0,12):
					for day_index in range(len(self.parent.diary_data[year_index]["date"][month_index])):
						
						y=year_index+1970
						m=month_index+1
						d=self.parent.diary_data[year_index]["date"][month_index][day_index]["day"]
						day_in_week=QDate(y,m,d).dayOfWeek()-1

						nowaday=QDate(y,m,d)
						x=QDateTime(nowaday)

						day_weight=0

						#每天的行
						for line in self.parent.diary_data[year_index]["date"][month_index][day_index]["text"]:
							#每一行
							line_weight=len(line["line_text"])
							
							#self.current_select_conceptID在不在line里面？
							if self.current_select_conceptID in line["linked_concept"]:
								
								text_list.append({
									#老传统用点号和空格分隔
									"date":"%s.%s.%s %s"%(y,m,d,week_dict[day_in_week]),
									"text":line["line_text"]
								})

								day_weight+=line_weight
								continue
							
							#self.current_leaf_conceptID_list的元素在不在line里面？
							for concept_id in self.current_leaf_conceptID_list:
								if concept_id in line["linked_concept"]:
					
									text_list.append({
										#老传统用点号和空格分隔
										"date":"%s.%s.%s %s"%(y,m,d,week_dict[day_in_week]),
										"text":line["line_text"]
									})
									day_weight+=line_weight
									break

						if day_weight!=0 and plot==True:
							
							if self.begin_date==None:
								self.begin_date=nowaday
							
							self.end_date=nowaday
							
							#每天的绘图点
							y=float(day_weight)
							if y>self.MaxY:
								self.MaxY=y
							
							self.series.append(float(x.toMSecsSinceEpoch()),y)
		
		else:

			day_in_week=QDate(y,m,d).dayOfWeek()-1
			
			year_index=y-1970
			month_index=m-1
			day_index=d
			#找该month列表中实际的day_index
			for i in range(len(self.parent.diary_data[year_index]["date"][month_index])):
				if self.parent.diary_data[year_index]["date"][month_index][i]["day"]==day_index:
					day_index=i
					break
			
			#每天的行
			for line in self.parent.diary_data[year_index]["date"][month_index][day_index]["text"]:
				
				#self.current_select_conceptID在不在line里面？
				if self.current_select_conceptID in line["linked_concept"]:
					
					text_list.append({
						#老传统用点号和空格分隔
						"date":"%s.%s.%s %s"%(y,m,d,week_dict[day_in_week]),
						"text":line["line_text"]
					})

					continue
				
				#self.current_leaf_conceptID_list的元素在不在line里面？
				for concept_id in self.current_leaf_conceptID_list:
					if concept_id in line["linked_concept"]:
		
						text_list.append({
							#老传统用点号和空格分隔
							"date":"%s.%s.%s %s"%(y,m,d,week_dict[day_in_week]),
							"text":line["line_text"]
						})
						break

		#如果有的话就列出来
		if text_list!=[]:
			#一日算作一个文本块
			fore_date=text_list[0]["date"]
			construct_text_list=[]
			one_day_text=fore_date+"\n\n"
			for i in text_list:
				if i["date"]==fore_date:
					one_day_text+=i["text"]+"\n\n"
				else:
					construct_text_list.append(one_day_text.strip())
					fore_date=i["date"]
					one_day_text=fore_date+"\n\n"+i["text"]+"\n\n"
			
			construct_text_list.append(one_day_text.strip())
			
			construct_text=""
			for i in construct_text_list:
				construct_text+=i+"\n\n"
			
			self.textEdit_viewer.setMarkdown(construct_text)

	def concept_show(self):
		#ID
		if self.current_select_conceptID!=None:
			self.lineEdit_id.setText(str(self.current_select_conceptID))

		#给宇宙大哥让位
		if self.current_select_conceptID==0:
			self.lineEdit_name.setReadOnly(1)
		else:
			self.lineEdit_name.setReadOnly(0)
		
		#Name
		self.lineEdit_name.setText(self.parent.concept_data[self.current_select_conceptID]["name"])
		#Detail
		self.plainTextEdit_detail.setPlainText(self.parent.concept_data[self.current_select_conceptID]["detail"])
	
		

		self.begin_date=None
		self.MaxY=0#最大的y坐标（一天内最多的concept的数量的最大值
		self.series=QtCharts.QLineSeries()

		color=generate_color()
		self.series.setColor(color)
		
		#改线的宽度还得这样改……
		pen = self.series.pen()
		pen.setWidth(2)
		self.series.setPen(pen)

		#列出self.current_select_conceptID以及它下层所有concept的related text
		self.textEdit_viewer.clear()
		self.concept_related_text_show(plot=True)
		

		#开始绘图
		(chart,xaxis,yaxis)=self.create_spline_chart()

		if self.series.count()==1:
			#只在一天出现过的无法连成线，重置为QScatterSeries点状图类型
			point=self.series.at(0)
			x=point.x()
			y=point.y()
			#新建QLineSeries，并放入字典中
			self.series=QtCharts.QScatterSeries()
			self.series.setColor(color)
			
			self.series.setMarkerSize(10.0)#小点点的大小
			self.series.setBorderColor(QColor(255,255,255))#小点点的边框颜色

			self.series.append(x,y)

		self.series.setPointsVisible(True)
		
		self.series.hovered.connect(self.spline_hovered)
		self.series.clicked.connect(self.spline_clicked)

		chart.addSeries(self.series)
		
		self.series.attachAxis(xaxis)
		self.series.attachAxis(yaxis)

		self.chartView_spline.setChart(chart)
		


	def concept_info_edited_and_save(self):
		if self.current_select_conceptID!=None:
			
			self.parent.concept_data[self.current_select_conceptID]["name"]=self.lineEdit_name.text()
			self.parent.concept_data[self.current_select_conceptID]["az"]=convert_to_az(self.parent.concept_data[self.current_select_conceptID]["name"])
			self.parent.concept_data[self.current_select_conceptID]["detail"]=self.plainTextEdit_detail.toPlainText()

			#直接全部刷新就行了
			self.parent.diary_line_concept_list_update()
			self.parent.concept_search_list_update()
			
			parent_ID=self.parent.lineEdit_id.text()
			if parent_ID!="" and self.current_select_conceptID==int(parent_ID):
				#更新事物界面
				self.parent.concept_show(self.current_select_conceptID)

			for tab in self.parent.custom_tabs_shown:
				tab.tab_update()
			return

	def concept_linked_file_add(self,links):
		"""
		从file library中进来的直接添加到当前日期，（如果带有内部路径，报错！）
		从concept或者tab root或者diary line进来的判断是否为内部文件，
			如果是外部文件那就放到当前日期，
			如果是内部文件，先按照ymd查filedata中有没有，
				如果有就只做链接操作，
				如果没有，那就说明熊孩子在乱搞，明明可以用file check来添加他非得手拖进来，报出警告！
		diary区只允许从内部拖入，只链接文件
		"""
		
		if self.parent.file_saving_base=="":
			QMessageBox.warning(self,"Warning","如果要使用File Library，请先到Setting中设置File Library的基地址。（所有拖进File Library中的文件都会被移动到基地址下）")
			return
		
		self.parent.file_library_check_direcory_exist()
		
		#存不存在当日文件的容器
		try:
			self.parent.file_data[self.parent.y][self.parent.m][self.parent.d]
		except:
			self.parent.file_data[self.parent.y][self.parent.m][self.parent.d]={}

		adding_file=[]

		self.parent.progress=QProgressDialog("Adding File...","Cancel",0,len(links),self)
		self.parent.progress.setWindowTitle("Adding File...")
		self.parent.progress.setWindowModality(Qt.WindowModal)
		# self.parent.progress.setMinimumDuration(0)
		self.parent.progress.setValue(0)
		value=0

		#移动文件到当日路径
		for i in links:
			
			self.parent.progress.setValue(value)
			value+=1
		
			#拥有内部路径吗？
			if self.parent.file_saving_base in i:
				try:
					date_and_name=i.replace(self.parent.file_saving_base,"")[1:].split("/")
					y=int(date_and_name[0])
					m=int(date_and_name[1])
					d=int(date_and_name[2])

					if y in range(1970,2170) and m in range(1,13) and d in range(1,32):
						#如果filedata中已经存在，就只做链接操作
						try:
						
							if "|" in i:
								file_name=i[i.find(">"):]
								file_icon=which_icon(file_name+".url")
							else:
								file_name=date_and_name[3]
								file_icon=which_icon(file_name)
								
							#file_data中是否存在该文件\link
							self.parent.file_data[y][m][d][file_name]

							#如果存在
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
							break
					else:
						QMessageBox.warning(self,"Warning","请不要在file_base下乱建文件夹！")
						break
				except:
					QMessageBox.warning(self,"Warning","请不要在file_base下乱放文件！")
					break
			
			#没有内部路径，说明是新来的，移动到当日的文件库
			else:
				#如果是新来的link
				if i[:4]=="http" or i[:5]=="https":
					i=i.strip().strip("/")

					#link查重
					if not self.parent.link_check_unique(i):
						continue
					
					result=getTitle(i)
					if result[0]==True:
						title=result[1]
					else:
						title="Unkown Page"
						tray=QSystemTrayIcon()
						tray.setContextMenu(self.parent.qmenu)
						tray.setIcon(QIcon(":/icon/holoico.ico"))
						tray.hide()
						tray.show()
						tray.showMessage("Infomation","获取网页Title失败，请查看网络连接是否正常！\n%s"%i)
					
					file_name=">"+title+"|"+i
					self.parent.file_data[self.parent.y][self.parent.m][self.parent.d][file_name]=[]

					file_icon=which_icon(file_name+".url")

				else:
				
					file_name=os.path.basename(i)
					file_dst=self.parent.file_saving_today_dst+"/"+file_name
					
					#文件添加，有可能硬盘被拔掉了
					try:
						shutil.move(i,file_dst)
					except:
						QMessageBox.warning(self,"Warning","路径访问出错！移动失败！")
						break
					
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
		
		self.parent.progress.setValue(len(links))
		self.parent.progress.deleteLater()

		#链接concept与文件的信息

		ID=self.current_select_conceptID

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

		parent_ID=self.parent.lineEdit_id.text()
		if parent_ID!="" and self.current_select_conceptID==int(parent_ID):
			#更新事物界面
			self.parent.concept_show(self.current_select_conceptID)
		
		self.parent.file_library_list_update()

		for tab in self.parent.custom_tabs_shown:
			tab.tab_update()

	def concept_linked_file_remove(self):
		
		ID=self.current_select_conceptID

		dlg = QDialog(self)
		dlg.setWindowTitle("Delete Warning")

		warning_text="确定要删除链接的文件吗？\n这是无法撤销的操作！\n"
		for file_index in sorted([item.row() for item in self.listWidget_file_root.selectedIndexes()]):
			file=self.parent.concept_data[ID]["file"][file_index]
			file_name=file["file_name"]
			warning_text+=file_name+"\n"
		name_label=QLabel(warning_text)
		
		QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
		buttonBox = QDialogButtonBox(QBtn)
		buttonBox.accepted.connect(dlg.accept)
		buttonBox.rejected.connect(dlg.reject)

		layout=QVBoxLayout()
		layout.addWidget(name_label)
		layout.addWidget(buttonBox)
		dlg.setLayout(layout)

		if dlg.exec_():
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


			parent_ID=self.parent.lineEdit_id.text()
			if parent_ID!="" and self.current_select_conceptID==int(parent_ID):
				#更新事物界面
				self.parent.concept_show(self.current_select_conceptID)

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


	def tree_deep_check_expand(self,depth,current_root):
		if depth==0:
			return
		depth-=1

		
		for index in range(current_root.childCount()):
			#如果是folder，就记录一下expand属性
			child=current_root.child(index)
			if child.childCount()!=0:
				#key是str类型的id,value是isExpanded
				self.tree_expand[child.text(0).split("|")[0]]=child.isExpanded()
				self.tree_deep_check_expand(depth,child)

	def tree_deep_duild(self,depth,root_concept,current_root):
		if depth==0 or root_concept["child"]==[]:
			return
		depth-=1

		for concept_id in root_concept["child"]:
			leaf_concept=self.parent.concept_data[concept_id]
			current_leaf=QTreeWidgetItem(current_root,[str(leaf_concept["id"])+"|"+leaf_concept["name"]])
			self.tree_deep_duild(depth,leaf_concept,current_leaf)
		
		try:
			current_root.setExpanded(self.tree_expand[str(root_concept["id"])])
		except:
			pass


	def update_file_list(self):
		
		def generate_file_tree_item_list(concept_id):
			tree_item_list=[]

			item=self.parent.concept_data[concept_id]
			for file in item["file"]:
				y=file["y"]
				m=file["m"]
				d=file["d"]
				file_name=file["file_name"]

				#如果是link
				if "|" in file_name:
					#link的tooltip没有直接设置成url网址
					#考虑到几个file listwidget间的拖动操作需要判断link是否已经在file_data中存在，所以需要附带ymd信息
					#这样损失了直接往浏览器拖动打开网页的功能，但双击、回车打开就行了
					file_url=self.parent.file_saving_base+"/"+str(y)+"/"+str(m)+"/"+str(d)+"/"+file_name
					# ">Google|http://www.google.com"
					file_name=file_name[:file_name.rfind("|")][1:]
				else:
					file_url=self.parent.file_saving_base+"/"+str(y)+"/"+str(m)+"/"+str(d)+"/"+file_name
				
				temp=QListWidgetItem()
				temp.setText(file_name)
				temp.setIcon(QIcon(file["file_icon"]))
				temp.setToolTip(file_url)

				tree_item_list.append(temp)
			
			return tree_item_list


		#本层的文件
		self.listWidget_file_root.clear()
		root_file_tree_item_list=generate_file_tree_item_list(self.current_select_conceptID)
		for tree_item in root_file_tree_item_list:
			self.listWidget_file_root.addItem(tree_item)

		
		
		#本层之下的所有child里的文件
		self.listWidget_file_leafs.clear()
		for concept_id in self.current_leaf_conceptID_list:
			for tree_item in generate_file_tree_item_list(concept_id):
				self.listWidget_file_leafs.addItem(tree_item)


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

		#如果是link
		if "|" in clicked_file_link:
			clicked_file_link=clicked_file_link.split("|")[-1]
			os.system("start explorer \"%s\""%clicked_file_link)
			return
		
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

			ID=self.current_select_conceptID

			pic_list=[]

			for file in self.parent.concept_data[ID]["file"]:
				file_link=self.parent.file_saving_base+"/"+str(file["y"])+"/"+str(file["m"])+"/"+str(file["d"])+"/"+file["file_name"]
				file_name=file["file_name"]
				if which_file_type(file_name)=="image":
					pic_list.append(file_link)
		
			clicked_index=pic_list.index(clicked_file_link)

			self.parent.image_viewer=MyImageViewer(pic_list,clicked_index,self.parent.width(),self.parent.height())
			if self.parent.window_is_stay_on_top()==True:
				self.parent.image_viewer.setWindowFlag(Qt.WindowStaysOnTopHint,True)
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
		
		#如果是link
		if "|" in clicked_file_link:
			clicked_file_link=clicked_file_link.split("|")[-1]
			os.system("start explorer \"%s\""%clicked_file_link)
			return
		
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
			if self.parent.window_is_stay_on_top()==True:
				self.parent.image_viewer.setWindowFlag(Qt.WindowStaysOnTopHint,True)
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


	

	def clear_view(self):
		self.MaxY=0#最大的y坐标（一天内最多的concept的数量的最大值
		self.chartView_spline.setChart(self.create_spline_chart()[0])
	
	def create_spline_chart(self):
		#初始化chart
		chart = QtCharts.QChart()
		# chart.setTitle("Spline chart")
		# chart.legend().setAlignment(Qt.AlignLeft)
		chart.legend().setVisible(False)
		chart.setTheme(QtCharts.QChart.ChartThemeDark)
		
		#填充的时候把边框去掉
		chart.layout().setContentsMargins(0, 0, 0, 0);
		chart.setBackgroundRoundness(0);
		
		# 动画虽然很modern，但拖动的时候有延迟，那就算了吧
		# chart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)
		# chart.setAnimationDuration(100)

		# self.chartView.setRubberBand(MyChartView.HorizontalRubberBand)

		#QDateTimeAxis类型的横坐标
		xaxis=QtCharts.QDateTimeAxis()

		#这里如果是只有一天的话，self.begin_date==self.end_date，设置range会出错，就不显示图像了……
		if self.begin_date==self.end_date:
			xaxis.setRange(QDateTime(self.begin_date).addDays(-1),QDateTime(self.end_date).addDays(1))
		else:
			xaxis.setRange(QDateTime(self.begin_date),QDateTime(self.end_date))
		
		xaxis.setFormat("yyyy.MM.dd")
		xaxis.setLabelsAngle(60)
		try:
			#轴得有个上限，不然缩小了卡死你
			n=self.begin_date.daysTo(self.end_date)
			if n>self.chartView_spline.xmax_TickCount:
				n=self.chartView_spline.xmax_TickCount
			else:
				n+=1
			xaxis.setTickCount(n)
		except:
			pass
		
		
		#QValueAxis类型的纵坐标
		yaxis=QtCharts.QValueAxis()
		yaxis.setRange(0,self.MaxY*1.1)
		yaxis.setLabelFormat("%i")
		try:
			#轴得有个上限，不然缩小了卡死你
			n=int(yaxis.max())-int(yaxis.min())
			if n>self.chartView_spline.ymax_TickCount:
				n=self.chartView_spline.ymax_TickCount
			else:
				n+=1
			yaxis.setTickCount(n)
		except:
			pass

		#放入坐标轴
		chart.addAxis(xaxis,Qt.AlignBottom)
		chart.addAxis(yaxis,Qt.AlignLeft)

		return (chart,xaxis,yaxis)

class SettingDialog(QDialog,Ui_setting_dialog):
	def __init__(self,file_saving_base,font,font_size,pixiv_cookie,instagram_cookie):
		super().__init__()
		self.setupUi(self)
		
		self.pushButtonfile_saving_base.clicked.connect(self.dir_dialog)
		self.pushButton_font.clicked.connect(self.font_dialog)


		self.lineEdit_file_saving_base.setText(file_saving_base)

		self.font=font
		self.font_size=font_size
		try:
			self.lineEdit_font.setText(self.font.family()+";"+str(self.font_size))
		except:
			pass

		try:
			self.lineEdit_pixiv_cookie.setText(pixiv_cookie)
		except:
			pass
		
		try:
			self.lineEdit_instagram_cookie.setText(instagram_cookie)
		except:
			pass

	def dir_dialog(self):
		dlg=QFileDialog(self)
		file_saving_base=dlg.getExistingDirectory()
		self.lineEdit_file_saving_base.setText(file_saving_base)

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
			
			#如果设定为手动更新，那就不能有1-7的日期
			if 0 in frequency and len(frequency)>1:
				QMessageBox.warning(self,"Warning","Wrong Format")
				return
				
			checked=[]
			#检查frequency合法性
			for i in frequency:
				#查星期几的范围
				if i not in range(0,8):
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
				
				#如果设定为手动更新，那就不能有1-7的日期
				if 0 in frequency and len(frequency)>1:
					QMessageBox.warning(self,"Warning","Wrong Format")
					return
				
				checked=[]
				#检查frequency合法性
				for i in frequency:
					#查星期几的范围
					if i not in range(0,8):
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
			url_text=""
			for index in self.current_selection:
				rss_url=self.rss_url_list[index][1]
				name+=self.baked[rss_url]["feed_name"]+";"
				url_text+=rss_url+";"
			
			self.lineEdit_url.setText(url_text)

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
			
			font.setPointSize(int(font_size*0.8))
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
		
		# 普通搜索 “与”模式 格式：asd&qwe&zxc（然后去text和text linked concept中把所有可能的项目都列出来）
		if mode==1:
			search=search.split("&")
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
									if ss in concept["name"].split("|") or ss in concept["az"].split("|"):
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
		
		#展示最多前30条
		self.listing_result=self.listing_result[:30]
		for i in self.listing_result[:30]:
			self.listWidget.addItem(str(i["weight"])+"|"+i["text"])
			# self.listWidget.addItem(i["text"])


class DiaryAnalyzeDialog(QDialog,Ui_diary_analyze_dialog):
	def __init__(self,parent):
		super().__init__()
		self.setupUi(self)
		
		self.parent=parent
		self.begin_date=self.parent.calendarWidget.selectedDate()#当前分析的开始日期，是QDate类型
		self.end_date=self.parent.calendarWidget.selectedDate()#当前分析的结束日期，是QDate类型

		self.MaxY=0#最大的y坐标（一天内最多的concept的数量的最大值
		self.threshold=self.spinBox.value()#过滤的底线

		self.pie_series=None#记录pie series，里面是许多pie slice
		self.all_concept_to_spline_series_dict={}#记录已经纳入图中的id以及它对应的series的指针
		self.all_conceptID_to_times_list=[]#记录这段时期内所有的concept_id，是从大到小排列的
		self.all_conceptID_to_color_dict={}#记录每一个concept的颜色，两边的颜色要保持统一

		try:
			font=self.parent.user_settings.value("font")
			font_size=int(self.parent.user_settings.value("font_size"))
		
			self.textEdit_viewer.setFont(font)
			
			font.setPointSize(int(font_size*0.8))
			self.listWidget_all_concept.setFont(font)
		except:
			pass
		
		self.splitter_chart=QSplitter(self)
		self.splitter_chart.setOrientation(Qt.Horizontal)
		self.splitter_chart.setHandleWidth(10)
		self.verticalLayout.addWidget(self.splitter_chart)
		
		self.chartView_spline=MyChartView()
		self.chartView_pie=QtCharts.QChartView()
		
		self.clear_view()

		self.splitter_chart.addWidget(self.chartView_spline)
		self.splitter_chart.addWidget(self.chartView_pie)
		
		self.splitter_chart.setStretchFactor(0,1)
		self.splitter_chart.setStretchFactor(1,1)

		self.splitter_whole.setStretchFactor(0,1)
		self.splitter_whole.setStretchFactor(1,1)
		self.splitter_whole.setStretchFactor(2,1)
		
		self.splitter_bottom.setStretchFactor(0,1)
		self.splitter_bottom.setStretchFactor(1,5)

		
		self.pushButton_analyze.clicked.connect(self.start_analyze)
		self.pushButton_restore.clicked.connect(self.restore_view)
		self.pushButton_clear.clicked.connect(self.clear_view)
		
		self.dateEdit_begin.setDate(self.begin_date)
		self.dateEdit_end.setDate(self.end_date)

		self.listWidget_all_concept.itemDoubleClicked.connect(self.listitem_clicked)
	
	def clear_view(self):
		"清空图表"
		self.pushButton_restore.setEnabled(0)

		self.begin_date=QDate().currentDate()#当前分析的开始日期，是QDate类型
		self.end_date=QDate().currentDate()#当前分析的结束日期，是QDate类型
		self.MaxY=0#最大的y坐标（一天内最多的concept的数量的最大值
		self.threshold=self.spinBox.value()#过滤的底线

		self.chartView_spline.setChart(self.create_spline_chart()[0])
		self.chartView_pie.setChart(self.create_pie_chart())

	def restore_view(self):
		
		(chart,xaxis,yaxis)=self.create_spline_chart()

		for concept_id in self.all_conceptID_to_times_list:
			
			series=self.all_concept_to_spline_series_dict[concept_id]
			series.setPointsVisible(True)
			chart.addSeries(series)

			series.attachAxis(xaxis)
			series.attachAxis(yaxis)
		
		self.chartView_spline.setChart(chart)
		
		######################################################################

		chart=self.create_pie_chart()

		for pie_slice in self.pie_series.slices():
			pie_slice.setExploded(False)
		
		chart.addSeries(self.pie_series)

		self.chartView_pie.setChart(chart)
	
	def create_spline_chart(self):
		
		#初始化chart
		chart = QtCharts.QChart()
		# chart.setTitle("Spline chart")
		chart.legend().setAlignment(Qt.AlignLeft)
		chart.setTheme(QtCharts.QChart.ChartThemeDark)
		
		#填充的时候把边框去掉
		chart.layout().setContentsMargins(0, 0, 0, 0);
		chart.setBackgroundRoundness(0);
		
		# 动画虽然很modern，但拖动的时候有延迟，那就算了吧
		# chart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)
		# chart.setAnimationDuration(100)

		# self.chartView.setRubberBand(MyChartView.HorizontalRubberBand)

		#QDateTimeAxis类型的横坐标
		xaxis=QtCharts.QDateTimeAxis()
		xaxis.setRange(QDateTime(self.begin_date),QDateTime(self.end_date))
		xaxis.setFormat("yyyy.MM.dd")
		xaxis.setLabelsAngle(60)
		try:
			#轴得有个上限，不然缩小了卡死你
			n=self.begin_date.daysTo(self.end_date)
			if n>self.chartView_spline.xmax_TickCount:
				n=self.chartView_spline.xmax_TickCount
			else:
				n+=1
			xaxis.setTickCount(n)
		except:
			pass
		
		
		#QValueAxis类型的纵坐标
		yaxis=QtCharts.QValueAxis()
		yaxis.setRange(0,self.MaxY*1.1)
		yaxis.setLabelFormat("%i")
		try:
			#轴得有个上限，不然缩小了卡死你
			n=int(yaxis.max())-int(yaxis.min())
			if n>self.chartView_spline.ymax_TickCount:
				n=self.chartView_spline.ymax_TickCount
			else:
				n+=1
			yaxis.setTickCount(n)
		except:
			pass

		#放入坐标轴
		chart.addAxis(xaxis,Qt.AlignBottom)
		chart.addAxis(yaxis,Qt.AlignLeft)

		return (chart,xaxis,yaxis)

	def create_pie_chart(self):
		
		chart = QtCharts.QChart()
		# chart.setTitle("Pie chart")
		chart.legend().setAlignment(Qt.AlignLeft)
		chart.setTheme(QtCharts.QChart.ChartThemeDark)
		
		#填充的时候把边框去掉
		chart.layout().setContentsMargins(0, 0, 0, 0);
		chart.setBackgroundRoundness(0);
		
		chart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)
		chart.setAnimationDuration(300)

		return chart


	def spline_hovered(self,*arg):
		"""
		这里传进来参数有：自定义参数concept_id，和信号参数hover_point(QPoint)、hover_on_line(True False)
		如果在线上，展示食指
		如果在点上，展示向上的箭头
		否则，展示普通箭头

		有个不完美的地方，这个hovered信号的触发仅限于进入和离开，如果一直在线上移动，是不会触发hovered信号的
		所以如果一直沿着线移动，即使到了点上，也不会展示向上的箭头
		但有谁会无聊到沿着线移鼠标啊？
		
		抖叽~
		"""
		y_range=int(self.chartView_spline.chart().axisY().max())-int(self.chartView_spline.chart().axisY().min())
		y_count=self.chartView_spline.ymax_TickCount
		y_deviation=y_range/(y_count+1)

		concept_id=arg[0]
		hover_point=arg[1]
		hover_x=hover_point.x()
		hover_y=hover_point.y()
		hover_on_line=arg[2]
		
		series=self.all_concept_to_spline_series_dict[concept_id]

		if hover_on_line==True:
			# print("in")

			#计算点的位置的附近，是否在存在concept的日期
			for point in series.pointsVector():
				x=point.x()
				y=point.y()

				if abs(hover_x-x)<3600000*20 and abs(hover_y-y)<y_deviation:
					# print("found")

					#如果点到了有concept的日期，显示向上的箭头
					self.setCursor(QCursor(Qt.UpArrowCursor))
					break
			else:
				# print("not found")

				#只是在线上的某一点，显示食指
				self.setCursor(QCursor(Qt.PointingHandCursor))

		else:
			# print("out")

			#显示普通箭头
			self.setCursor(QCursor(Qt.ArrowCursor))
	
	
	def spline_clicked(self,*arg):
		"""
		这里传进来的参数有：自定义参数concept_id，和信号参数hover_point(QPoint)
		
		点击线，展示对应concept的diary text，并且piechart中的那一部分explode
		如果点到了有concept的日期，那只显示那一天的diary text，
		如果点到不存在concept的日期上，展示该concept所有的diary text
		"""
		y_range=int(self.chartView_spline.chart().axisY().max())-int(self.chartView_spline.chart().axisY().min())
		y_count=self.chartView_spline.ymax_TickCount
		y_deviation=y_range/(y_count+1)

		concept_id=arg[0]
		clicked_point=arg[1]
		clicked_x=clicked_point.x()
		clicked_y=clicked_point.y()

		#展示对应concept的diary text
		index=self.all_conceptID_to_times_list.index(concept_id)
		self.listWidget_all_concept.setCurrentRow(index)

		###################################################################################################
		
		#piechart中的那一部分explode
		pie_slice_list=self.pie_series.slices()
		for i in range(len(pie_slice_list)):
			pie_slice=pie_slice_list[i]
			if i==index:
				pie_slice.setExploded(True)
				pie_slice.setExplodeDistanceFactor(0.25)
			else:
				pie_slice.setExploded(False)
		
		###################################################################################################
		
		#展示对应concept的diary text

		#计算点的位置的附近，是否在存在concept的日期
		series=self.all_concept_to_spline_series_dict[concept_id]
		for point in series.pointsVector():
			x=point.x()
			y=point.y()
			if abs(clicked_x-x)<3600000*20 and abs(clicked_y-y)<y_deviation:
				datetime=QDateTime().fromMSecsSinceEpoch(int(x))
				date=datetime.date()
				
				y=date.year()
				m=date.month()
				d=date.day()
				
				#如果点到了有concept的日期，那只显示那一天的diary text，
				self.concept_related_text_show(concept_id,y,m,d)
				break
		else:
			#如果点到不存在concept的日期上，展示该concept所有的diary text
			self.concept_related_text_show(concept_id)
	
	
	def listitem_clicked(self):
		"点击列表中的concept，展示对应concept的diary text，并特写展示对应的线，并且piechart中的那一部分explode"
		index=self.listWidget_all_concept.currentRow()

		#展示对应concept的diary text
		concept_id=self.all_conceptID_to_times_list[index]
		self.concept_related_text_show(concept_id)

		###################################################################################################
		
		#piechart中的那一部分explode
		pie_slice_list=self.pie_series.slices()
		for i in range(len(pie_slice_list)):
			pie_slice=pie_slice_list[i]
			if i==index:
				pie_slice.setExploded(True)
				pie_slice.setExplodeDistanceFactor(0.25)
			else:
				pie_slice.setExploded(False)
		

		###################################################################################################
		
		#特写展示对应的线，这里要建立一个新的chart（貌似不可能实现一个chart包含多个series，但只呈现出一个series）
		(chart,xaxis,yaxis)=self.create_spline_chart()

		series=self.all_concept_to_spline_series_dict[concept_id]
		series.setPointsVisible(True)
		
		chart.addSeries(series)

		series.attachAxis(xaxis)
		series.attachAxis(yaxis)
		
		self.chartView_spline.setChart(chart)


	def concept_related_text_show(self,concept_id,y=0,m=0,d=0):
		
		week_dict=["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
		text_list=[]
		
		#如果点到不存在concept的日期上，展示该concept所有的diary text
		if y==0 and m==0 and d==0:
			#QDate操作真方便！
			nowaday=self.begin_date
			while nowaday<=self.end_date:
				
				#这里出来的是正常的ymd,2021,4,2
				(year_index,month_index,day_index)=QDate_transform(nowaday)
				
				year_index-=1970
				month_index-=1
				#找该month列表中实际的day_index
				for i in range(len(self.parent.diary_data[year_index]["date"][month_index])):
					if self.parent.diary_data[year_index]["date"][month_index][i]["day"]==day_index:
						day_index=i
						break

				try:
					for line in self.parent.diary_data[year_index]["date"][month_index][day_index]["text"]:
						if concept_id in line["linked_concept"]:
							y=year_index+1970
							m=month_index+1
							d=self.parent.diary_data[year_index]["date"][month_index][day_index]["day"]
							day_in_week=QDate(y,m,d).dayOfWeek()-1
							
							text_list.append({
								#老传统用点号和空格分隔
								"date":"%s.%s.%s %s"%(y,m,d,week_dict[day_in_week]),
								"text":line["line_text"]
							})
				except:
					#可能某一天没有日记，就找不到day_index，索引失败
					pass
				
				nowaday=nowaday.addDays(1)
		
		#如果点到了有concept的日期，那只显示那一天的diary text，
		else:
			year_index=y-1970
			month_index=m-1
			day_index=d
			#找该month列表中实际的day_index
			for i in range(len(self.parent.diary_data[year_index]["date"][month_index])):
				if self.parent.diary_data[year_index]["date"][month_index][i]["day"]==day_index:
					day_index=i
					break

			for line in self.parent.diary_data[year_index]["date"][month_index][day_index]["text"]:
				if concept_id in line["linked_concept"]:
					y=year_index+1970
					m=month_index+1
					d=self.parent.diary_data[year_index]["date"][month_index][day_index]["day"]
					day_in_week=QDate(y,m,d).dayOfWeek()-1
					
					text_list.append({
						#老传统用点号和空格分隔
						"date":"%s.%s.%s %s"%(y,m,d,week_dict[day_in_week]),
						"text":line["line_text"]
					})

		#如果有的话就列出来
		if text_list!=[]:
			#一日算作一个文本块
			fore_date=text_list[0]["date"]
			construct_text_list=[]
			one_day_text=fore_date+"\n\n"
			for i in text_list:
				if i["date"]==fore_date:
					one_day_text+=i["text"]+"\n\n"
				else:
					construct_text_list.append(one_day_text.strip())
					fore_date=i["date"]
					one_day_text=fore_date+"\n\n"+i["text"]+"\n\n"
			
			construct_text_list.append(one_day_text.strip())
			
			construct_text=""
			for i in construct_text_list:
				construct_text+=i+"\n\n"
			
			self.textEdit_viewer.setMarkdown(construct_text)


	def start_analyze(self):
		
		def run_statistics(all_conceptID_to_times_dict):

			nowaday=self.begin_date
			#QDate操作真方便！
			while nowaday<=self.end_date:

				#这里出来的是正常的ymd,2021,4,2
				(year_index,month_index,day_index)=QDate_transform(nowaday)
				
				#当日的x坐标
				x=QDateTime()
				x.setDate(nowaday)
				
				year_index-=1970
				month_index-=1
				#找该month列表中实际的day_index
				for i in range(len(self.parent.diary_data[year_index]["date"][month_index])):
					if self.parent.diary_data[year_index]["date"][month_index][i]["day"]==day_index:
						day_index=i
						break

				try:
					day_conceptID_to_times_dict={}#临时记录每日的concept对应的次数，用于绘图
					
					for line in self.parent.diary_data[year_index]["date"][month_index][day_index]["text"]:
						
						#concept对应文本的字数作为权重
						weight=len(line["line_text"])

						for concept_id in line["linked_concept"]:
							
							if all_conceptID_to_times_dict.get(concept_id)==None:
								
								all_conceptID_to_times_dict[concept_id]=weight
								

								#新建QLineSeries，并放入字典中
								series=QtCharts.QLineSeries()
								# series.setUseOpenGL(1)
								series.setName(self.parent.concept_data[concept_id]["name"])
								
								color=generate_color()
								series.setColor(color)
								self.all_conceptID_to_color_dict[concept_id]=color
								
								#改线的宽度还得这样改……
								pen = series.pen()
								pen.setWidth(2)
								series.setPen(pen)

								series.setPointsVisible(True)
								
								# 链接点击线的函数
								# 这里用lambda不知道为什么就是不行，指针都指向了最后一个，换了partial就行了……
								series.hovered.connect(partial(self.spline_hovered,concept_id))
								series.clicked.connect(partial(self.spline_clicked,concept_id))


								#最后放到series字典中
								self.all_concept_to_spline_series_dict[concept_id]=series
								
							else:
								all_conceptID_to_times_dict[concept_id]+=weight
							
							if day_conceptID_to_times_dict.get(concept_id)==None:
								day_conceptID_to_times_dict[concept_id]=weight
							else:
								day_conceptID_to_times_dict[concept_id]+=weight
					
					for concept_id in day_conceptID_to_times_dict.keys():
						series=self.all_concept_to_spline_series_dict[concept_id]

						#每个concept对应的y坐标
						y=float(day_conceptID_to_times_dict[concept_id])
						if y>self.MaxY:
							self.MaxY=y
						series.append(float(x.toMSecsSinceEpoch()),y)
					
					
				except:
					# 可能某一天没有日记，就找不到day_index，索引失败
					pass
				
				nowaday=nowaday.addDays(1)

			return all_conceptID_to_times_dict
		
		def draw_spline_chart():

			#按照all_conceptID_to_times_dict中每个concept_id对应的times，从大到小排序，将concept_id组合成列表
			self.all_conceptID_to_times_list=list(map(lambda x:x[0],sorted(all_conceptID_to_times_dict.items(),key=lambda x:x[1],reverse=True)))
			
			(chart,xaxis,yaxis)=self.create_spline_chart()
			
			#把series放入chart，并关联上坐标轴
			for concept_id in self.all_conceptID_to_times_list:

				series=self.all_concept_to_spline_series_dict[concept_id]

				#过滤掉低于self.threshold的concept
				if series.count()<=self.threshold:
					self.all_concept_to_spline_series_dict.pop(concept_id)
					all_conceptID_to_times_dict.pop(concept_id)
					continue
				
				else:
					#只在一天出现过的无法连成线，重置为QScatterSeries点状图类型
					if series.count()==1:
						
						point=self.all_concept_to_spline_series_dict[concept_id].at(0)
						x=point.x()
						y=point.y()

						#新建QLineSeries，并放入字典中
						series=QtCharts.QScatterSeries()
						# series.setUseOpenGL(1)
						series.setName(self.parent.concept_data[concept_id]["name"])
						
						color=self.all_conceptID_to_color_dict[concept_id]
						series.setColor(color)
						
						series.setMarkerSize(10.0)#小点点的大小
						series.setBorderColor(QColor(255,255,255))#小点点的边框颜色

						series.append(x,y)

						# 链接点击线的函数
						# 这里用lambda不知道为什么就是不行，指针都指向了最后一个，换了partial就行了……
						series.hovered.connect(partial(self.spline_hovered,concept_id))
						series.clicked.connect(partial(self.spline_clicked,concept_id))

						#最后放到series字典中
						self.all_concept_to_spline_series_dict[concept_id]=series
					
					

					chart.addSeries(series)
					
					series.attachAxis(xaxis)
					series.attachAxis(yaxis)

					# concept列表中添加list item
					concept_name=self.parent.concept_data[concept_id]["name"]
					self.listWidget_all_concept.addItem(str(concept_id)+"|"+concept_name)
			

			#pop过滤掉了一些数据，这里重新排序self.all_conceptID_to_times_list
			#按照all_conceptID_to_times_dict中每个concept_id对应的times，从大到小排序，将concept_id组合成列表
			self.all_conceptID_to_times_list=list(map(lambda x:x[0],sorted(all_conceptID_to_times_dict.items(),key=lambda x:x[1],reverse=True)))

			#关联完毕，链接到self.chartView_spline
			self.chartView_spline.setChart(chart)
		
		def draw_pie_chart():
			chart=self.create_pie_chart()

			self.pie_series = QtCharts.QPieSeries(chart)
			
			for concept_id in self.all_conceptID_to_times_list:
				
				series=self.all_concept_to_spline_series_dict[concept_id]

				#过滤掉低于self.threshold的concept
				if series.count()>self.threshold:
					concept_name=self.parent.concept_data[concept_id]["name"]
					concept_times=all_conceptID_to_times_dict[concept_id]

					pie_slice=self.pie_series.append(concept_name,concept_times)
					
					color=self.all_conceptID_to_color_dict[concept_id]
					pie_slice.setColor(color)
					pie_slice.setBorderColor(QColor(1,1,1))#真的奇怪，即使是Qt.black或者QColor(0,0,0)它都会显示白色……
					

					pie_slice.setLabelPosition(QtCharts.QPieSlice.LabelOutside)
					pie_slice.setLabelVisible(True)
			
			chart.addSeries(self.pie_series)

			self.chartView_pie.setChart(chart)

		#清空concept区
		self.listWidget_all_concept.clear()
		#清空
		self.textEdit_viewer.clear()

		self.pushButton_restore.setEnabled(1)

		self.begin_date=self.dateEdit_begin.date()
		self.end_date=self.dateEdit_end.date()
		self.threshold=self.spinBox.value()

		if self.begin_date>self.end_date:
			QMessageBox.warning(self,"Warning","日期设置错误！")
			return
		
		####################################################################################
		# 开始分析
		# 初始化容器
		self.all_concept_to_spline_series_dict={}
		all_conceptID_to_times_dict={}#临时记录每个concept对应的次数，用于最后排序成concept列表，以及绘画PieChart

		
		self.MaxY=0#最大的y坐标（一天内最多的concept的数量的最大值
		
		#开始统计每日的concept
		all_conceptID_to_times_dict=run_statistics(all_conceptID_to_times_dict)
		
		#统计完毕
		#开始绘图
		if all_conceptID_to_times_dict!=[]:
			
			draw_spline_chart()
			draw_pie_chart()

