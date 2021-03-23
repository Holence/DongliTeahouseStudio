# -*- coding: utf-8 -*-

import sys

#### from threading import Thread,Lock

from socket import setdefaulttimeout

from custom_palette import *
from custom_function import *
from custom_widget import *
from custom_component import *

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from PySide2.QtWebEngineWidgets import *

from dongli_teahouse_studio_window import Ui_dongli_teahouse_studio_window



class DongliTeahouseStudio(QMainWindow,Ui_dongli_teahouse_studio_window):

	def initialize_signal(self):
		#所有的删除由当时focus的控件决定操作
		self.actionDelete.triggered.connect(self.center_delete)
		#文本块增加关联concept或文件ctrl+e
		self.actionLine_Link_Concept.triggered.connect(self.diary_line_concept_link)


		#搜索框中输入
		self.lineEdit_search_concept.textEdited.connect(self.concept_search_list_update)
		#双击进入搜索的选项
		self.listWidget_search_concept.itemDoubleClicked.connect(lambda:self.concept_show(self.listWidget_search_concept.currentItem().text().split("|")[0]))
		#拖动重排
		#model()是什么玩意，这就变成了QAbstractItemModel ？
		self.listWidget_search_concept.model().rowsMoved.connect(self.concept_search_list_drag_update)

		#双击关联列表
		self.listWidget_parent.itemDoubleClicked.connect(lambda:self.concept_show(self.listWidget_parent.currentItem().text().split("|")[0]))
		self.listWidget_child.itemDoubleClicked.connect(lambda:self.concept_show(self.listWidget_child.currentItem().text().split("|")[0]))
		self.listWidget_relative.itemDoubleClicked.connect(lambda:self.concept_show(self.listWidget_relative.currentItem().text().split("|")[0]))

		#编辑结束后自动临时保存
		self.lineEdit_name.editingFinished.connect(self.concept_info_edited_and_save)
		###QPlainTextEdit没有editingFinished信号，就用了自定义的MyPlainTextEdit
		self.plainTextEdit_detail.editingFinished.connect(self.concept_info_edited_and_save)
		###QPlainTextEdit没有editingFinished信号，就用了自定义的MyPlainTextEdit
		self.plainTextEdit_single_line.editingFinished.connect(self.diary_line_edited_and_save)


		#新建事物ctrl+n
		self.actionCreate_Concept.triggered.connect(self.concept_creat)
		
		#保存到外存ctrl+s
		self.actionSave_Diary_Data.triggered.connect(self.diary_data_save_out)

		#关联列表操作ctrl+123
		self.actionAdd_Concept_To_Parent.triggered.connect(lambda:self.concept_relationship_add("parent"))
		self.actionAdd_Concept_To_Child.triggered.connect(lambda:self.concept_relationship_add("child"))
		self.actionAdd_Concept_To_Relative.triggered.connect(lambda:self.concept_relationship_add("relative"))

		#新增一行ctrl+d
		self.actionAdd_New_Line.triggered.connect(self.diary_line_add)


		#
		self.calendarWidget.clicked.connect(lambda :self.diary_show(self.QDate_transform(self.calendarWidget.selectedDate())))
		
		#点击关联事物列表
		self.listWidget_text_related_concept.itemDoubleClicked.connect(lambda:self.concept_show(self.listWidget_text_related_concept.currentItem().text().split("|")[0]))

		#点击行显示文本
		self.listWidget_lines.itemClicked.connect(self.diary_line_show)
		#拖动行重排
		self.listWidget_lines.model().rowsMoved.connect(self.diary_line_list_drag_update)

		#concept链接文件
		#自定义了MyFileDragAndDropList，实现外部文件的dropin
		self.listWidget_concept_linked_file.dropped.connect(self.concept_linked_file_add)
		self.listWidget_concept_linked_file.itemDoubleClicked.connect(self.concept_linked_file_open)
		#一开始没有展示item了，就禁用file列表
		self.listWidget_concept_linked_file.setEnabled(0)

		####
			# 现在要拖到外面了，就不限制了
			####icon展示模式会排列混乱，不想让它在内部drag了，设置setDragEnabled(0)，它就不让从外部drop了，真是难伺候
			####侦测在外部还是在内部，改变dragEnable
			#### self.listWidget_concept_linked_file.focusouted.connect(lambda:self.listWidget_concept_linked_file.setDragEnabled(1))
			#### self.listWidget_concept_linked_file.focusined.connect(lambda:self.listWidget_concept_linked_file.setDragEnabled(0))
		
		#file manager文件
		self.listWidget_search_file.dropped.connect(self.file_library_file_add)
		self.listWidget_search_file.itemDoubleClicked.connect(self.file_library_file_open)
		self.listWidget_search_file.enter_pressed.connect(self.file_library_file_open)
		#点击展示信息
		self.listWidget_search_file.itemClicked.connect(self.file_library_file_info_show)
		#file manager指针上下移动，即刻展示信息
		self.listWidget_search_file.currentItemChanged.connect(self.file_library_file_info_show)

		#文件搜索
		self.lineEdit_search_file.textEdited.connect(self.file_library_list_update)
		self.lineEdit_search_file.returnPressed.connect(self.file_library_list_focus)
		#文件链接concept的列表
		self.listWidget_file_related_concept.itemDoubleClicked.connect(lambda:self.concept_show(self.listWidget_file_related_concept.currentItem().text().split("|")[0]))

		#text链接文件
		self.listWidget_text_linked_file.dropped.connect(self.diary_line_file_link)
		self.listWidget_text_linked_file.itemDoubleClicked.connect(self.diary_line_file_open)



		#筛选concept对应的diary text
		self.listWidget_concept_related_text.itemDoubleClicked.connect(self.concept_related_text_review)


		#添加view设置
		action=self.dockWidget_concept.toggleViewAction()
		action.setIcon(QIcon(":/icon/database.svg"))
		action.setShortcut(QKeySequence(Qt.Key_F5))
		self.menuView.addAction(action)

		action=self.dockWidget_diary.toggleViewAction()
		action.setShortcut(QKeySequence(Qt.Key_F6))
		action.setIcon(QIcon(":/icon/feather.svg"))
		self.menuView.addAction(action)

		action=self.dockWidget_library.toggleViewAction()
		action.setShortcut(QKeySequence(Qt.Key_F7))
		action.setIcon(QIcon(":/icon/hard-drive.svg"))
		self.menuView.addAction(action)

		action=self.dockWidget_sticker.toggleViewAction()
		action.setShortcut(QKeySequence(Qt.Key_F8))
		action.setIcon(QIcon(":/icon/coffee.svg"))
		self.menuView.addAction(action)

		#f11全屏
		self.actionToggle_Fullscreen.triggered.connect(self.window_toggle_fullscreen)
		
		#ctrl+w关闭
		self.actionExit.triggered.connect(self.close)

		#about界面
		self.actionAbout.triggered.connect(self.about)

		#ctrl+q自动锁定搜索框
		self.actionSearch_Concept.triggered.connect(self.concept_search_focus)

	

		#搜索框按enter自动展示第一个concept
		self.lineEdit_search_concept.returnPressed.connect(lambda: self.concept_show(self.listWidget_search_concept.item(0).text().split("|")[0]) if self.listWidget_search_concept.item(0)!=None else 0)

		####
			#导入文件树
			# self.actionImport_File_Tree_to_Concept.triggered.connect(self.concept_import_file_tree)


		self.actionCreate_New_Tab.triggered.connect(self.tab_custom_create)
		self.actionHide_Current_Tab.triggered.connect(self.tab_custom_hide)
		self.actionDelete_Current_Tab.triggered.connect(self.tab_custom_delete)


		self.actionCreate_RSS_Folder.triggered.connect(self.rss_feed_folder_create)
		self.actionAdd_RSS_Feed.triggered.connect(self.rss_feed_add)
		self.actionOpen_WebPage_In_Browser.triggered.connect(self.rss_open_webpage)
		
		#点击treeitem，show文章列表
		self.treeWidget_rss.itemClicked.connect(self.rss_feed_show)
		#每次拖动排阶级后，就检查，RSS不能作为folder
		self.treeWidget_rss.dropped.connect(self.rss_tree_drop_update)
		#点击文章
		self.listWidget_rss.itemClicked.connect(self.rss_feed_article_show)

		#导出
		self.actionExport_Concept_Data_to_Json.triggered.connect(lambda:self.center_export("Concept"))
		self.actionExport_Diary_Data_to_Json.triggered.connect(lambda:self.center_export("Diary"))
		self.actionExport_File_Data_to_Json.triggered.connect(lambda:self.center_export("File"))
		self.actionExport_RSS_Data_to_Json.triggered.connect(lambda:self.center_export("RSS"))

		#Setting
		self.actionSetting.triggered.connect(self.setting_menu)

		#运行File Ckeck
		self.actionFile_Check.triggered.connect(self.file_check)
		
		#F2编辑文件信息或者RSS信息
		self.actionEdit.triggered.connect(self.center_edit)

		#手动更新RSS
		self.actionRSS_Update_Manually.triggered.connect(self.rss_feed_manually_update)
		
		#Diary text search
		self.actionSearch_Diary_Text.triggered.connect(self.diary_text_search)

		#ctrl+q搜索文件
		self.actionSearch_File_Library.triggered.connect(self.file_library_search_focus)

		self.actionLocate_File_in_File_Library.triggered.connect(self.center_locate_file_in_library)

	def initialize_window(self):
		#恢复界面设置
		try:
			
			self.restoreGeometry(self.user_settings.value("geometry"))
			self.restoreState(self.user_settings.value("windowState"))
			self.resize(self.user_settings.value("size"))
			self.move(self.user_settings.value("pos"))

			self.splitter_rss.restoreState(self.user_settings.value("splitter_rss"))
			
			font=self.user_settings.value("font")
			font_size=self.user_settings.value("font_size")
			self.font_set(font,font_size)

			sticker_text=decrypt(self.user_settings.value("sticker"))
			self.plainTextEdit_sticker.setPlainText(sticker_text)
			
			
			
			
			
			# settings_list=self.user_settings.allKeys()
			# print(settings_list)
		except:
			pass


	def initialize_custom_tab(self):

		#恢复custom_tab配置
		try:#不是第一次进来
			self.custom_tab_data=decrypt(self.user_settings.value("custom_tab_data"))
			
			# print(self.custom_tab_data)

			index=0
			for custom_tab in self.custom_tab_data:
				#把要展示出来的tab生成在tabwidget中
				if custom_tab[3]==True:
					#新建一个tab，调用自定义的MyTabWidget
					tab=MyTabWidget(self,custom_tab[1],custom_tab[2])

					#这里的tab应该算是一个指针，可以在这里链上一些槽
					#点击内部的leaf，回传到这里，去显示concept
					tab.clicked.connect(lambda ID:self.concept_show(ID))
					
					#一开始不让操作
					tab.listWidget_file_root.setEnabled(0)
					tab.listWidget_file_leafs.setEnabled(0)

					self.tabWidget.addTab(tab,QIcon(":/icon/trello.svg"),custom_tab[0])
					

					#正在界面上展示的tabs，这些是用来实时与concept data同步更新的
					self.custom_tabs_shown.append(tab)
				
				#把隐藏了的tab，放在tab menu的action里面
				else:
					
					ii=index
					action=QAction(custom_tab[0],self)
					action.setIcon(QIcon(":/icon/trello.svg"))
					#貌似这里如果直接用了index，好像调进去的就是指向index的地址的数字了，就是那个循环结束后的index了
					#所以用另一个ii先指向了index，如果index变化了，ii还能保存之前的那个数
					action.triggered.connect(lambda:self.tab_custom_resurrection(ii,action))
					self.menuTab.addAction(action)
					
				index+=1
		
		except:#第一次进来，初始化custom_tab_data

			self.custom_tab_data=[]


	def closeEvent(self,event):
		super(DongliTeahouseStudio,self).closeEvent(event)

		
		#Kill RSS的线程
		try:
			self.daily_update_thread.need_to_quit=True

			if not self.daily_update_thread.wait(1.0):
				self.daily_update_thread.terminate()
				self.daily_update_thread.wait()
			
			del self.daily_update_thread
		except:
			pass
		
		try:
			self.adding_feed_thread.need_to_quit=True
			
			if not self.adding_feed_thread.wait(1.0):
				self.adding_feed_thread.terminate()
				self.adding_feed_thread.wait()
			
			del self.adding_feed_thread
		except:
			pass
		
		#保存未保存的内容
		if self.windowTitle()=="Dongli Teahouse Studio *Unsaved Change*":
			dlg = QMessageBox(self)
			dlg.setWindowTitle("Unsaved Change")
			dlg.setText("Diary的内容未保存，需要保存吗？")
			dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No |QMessageBox.Cancel)
			dlg.setIcon(QMessageBox.Warning)
			button = dlg.exec_()

			if button == QMessageBox.Yes:
				event.accept()
				self.diary_data_save_out()
			elif button == QMessageBox.Cancel:
				event.ignore()
			elif button == QMessageBox.No:
				event.accept()

		#
		self.user_settings.setValue("geometry",self.saveGeometry())
		self.user_settings.setValue("windowState",self.saveState())
		self.user_settings.setValue("size",self.size())
		self.user_settings.setValue("pos",self.pos())

		self.user_settings.setValue("splitter_rss",self.splitter_rss.saveState())

		#自动保存tab data
		self.user_settings.setValue("custom_tab_data",encrypt(self.custom_tab_data))

		sticker_text=self.plainTextEdit_sticker.toPlainText()
		self.user_settings.setValue("sticker",encrypt(sticker_text))

		#自动保存concept data
		encrypt_save(self.concept_data,"Concept_Data.dlcw")

		#自动保存file data
		encrypt_save(self.file_data,"File_Data.dlcw")

		#自动保存RSS data
		encrypt_save(self.rss_data,"RSS_Data.dlcw")
		self.user_settings.setValue("rss_tree_data",encrypt(self.rss_tree_data))

	# def mousePressEvent(self, event):
	# 	if event.button() == Qt.LeftButton:
	# 		self.__press_pos = event.pos()  

	# def mouseReleaseEvent(self, event):
	# 	if event.button() == Qt.LeftButton:
	# 		self.__press_pos = QPoint()

	# def mouseMoveEvent(self, event):
	# 	if not self.__press_pos.isNull():  
	# 		self.move(self.pos() + (event.pos() - self.__press_pos))
		
	def __init__(self):
		super().__init__()
		self.setupUi(self)

		# self.__press_pos = QPoint()
		# self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.CustomizeWindowHint)
		# self.setWindowOpacity(0.95)


		#初始化信号
		self.initialize_signal()

		self.user_settings=QSettings("user_settings.ini",QSettings.IniFormat)

		# QCoreApplication.setApplicationName("Teahouse Studio")
		# QCoreApplication.setOrganizationName("Dongli Teahouse")


		#初始化变量
		self.qmenu=QMenu(self)

		self.current_year_index=0
		self.current_month_index=0
		self.current_day_index=0
		self.current_day=0#记录这个，用来找那些不存在当前日的，重排序后的index
		self.is_new_diary=0#标记新日记，增添容器、新建新日记时要用
		self.is_first_arrived=0#增添、删除、列出链接物的时候要用
		self.new_diary={}#临时存储还没重排序找到day索引值的新日记
		self.current_line_index=0

		self.easter_egg_deleting_universe=0

		self.qlock=QMutex(QMutex.NonRecursive)

		#初始化diary、concept、file、rss的data
		if self.data_validity_check()==1:
			
			self.data_load()

			self.concept_search_list_update()

			self.diary_show(self.QDate_transform(self.calendarWidget.selectedDate()))

			ymd=time.localtime(time.time())
			self.y=ymd[0]
			self.m=ymd[1]
			self.d=ymd[2]
			#当日存文件的地方
			self.file_saving_today_dst=self.file_saving_base+"/"+str(self.y)+"/"+str(self.m)+"/"+str(self.d)
			self.searching_file=[]
			self.file_library_list_update()

			self.current_rss_showing=None#如果点开的是rss，那么放的是rss_url；如果点开的是folder，那么存所有文章结构体的列表，
			self.browser=QWebEngineView()
			self.splitter_rss.addWidget(self.browser)
			self.splitter_rss.setStretchFactor(0,1)
			self.splitter_rss.setStretchFactor(1,1)
			self.splitter_rss.setStretchFactor(2,1)
			self.rss_tree_build()

			self.rss_feed_daily_update()
			self.manually_updateing=False
		else:
			exit()
		

		# 初始化窗体
		self.initialize_window()

		#初始化tab
		#custom_tabs_shown存储正在界面上展示的tabs，这些是用来实时与concept data同步更新的
		self.custom_tabs_shown=[]
		self.initialize_custom_tab()
		self.tabWidget.setCurrentIndex(0)


		# self.setWindowFlag(Qt.WindowStaysOnTopHint)
		# self.dockWidget_concept.setWindowFlag(Qt.WindowStaysOnTopHint )



	def diary_text_search(self):
		dlg=DiarySearchDialog(self)
		dlg.exec_()

	def file_check(self):
		if self.file_saving_base=="":
			QMessageBox.warning(self,"Warning","如果要使用File Library，请先到Setting中设置File Library的基地址。（所有拖进File Library中的文件都会被移动到基地址下）")
			return

		redundant=[]
		missing=[]
		dont_exist=[]
		
		base=self.file_saving_base
		for y_dir in os.listdir(base):
			
			y=y_dir
			y_dir=os.path.join(base,y_dir)
			if os.path.isdir(y_dir) and str.isdigit(y) and int(y) in range(1970,2170):
				y=int(y)
				
				for m_dir in os.listdir(y_dir):
					
					m=m_dir
					m_dir=os.path.join(y_dir,m_dir)
					if os.path.isdir(m_dir) and str.isdigit(m) and int(m) in range(1,13):
						m=int(m)

						for d_dir in os.listdir(m_dir):
							
							d=d_dir
							d_dir=os.path.join(m_dir,d_dir)
							if os.path.isdir(d_dir) and str.isdigit(d) and int(d) in range(1,32):
								d=int(d)

								file_heap_have=os.listdir(d_dir)

								try:
									file_data_have=self.file_data[y][m][d].keys()
								except:
									#如果没有当日的容器那就新建好了
									self.file_data[y][m][d]={}
									file_data_have=self.file_data[y][m][d].keys()
								
								#文件堆中多出来的光头
								for file_name in file_heap_have:
									# file路径中是/，不是\
									# file_dir=os.path.join(d_dir,file_name).replace("\\","/")
									if file_name not in file_data_have:
										redundant.append(
											{
												"y":y,
												"m":m,
												"d":d,
												"file_name":file_name
											}
										)

								#文件堆缺失的
								for file_name in file_data_have:
									# #file路径中是/，不是\
									# file_dir=os.path.join(d_dir,file_name).replace("\\","/")
									if "|" not in file_name and file_name not in file_heap_have:
										missing.append(
											{
												"y":y,
												"m":m,
												"d":d,
												"file_name":file_name,
												"linked_concept":self.file_data[y][m][d][file_name]
											}
										)
								
		#判断每日的文件夹存不存在
		for y in range(1970,2170):
			for m in range(1,13):
				for d in self.file_data[y][m].keys():
					
					#如果整个文件夹都消失了
					if not os.path.exists(self.file_saving_base+"/"+str(y)+"/"+str(m)+"/"+str(d)):
						#missing添加全部的file
						for file_name in self.file_data[y][m][d].keys():
							missing.append(
								{
									"y":y,
									"m":m,
									"d":d,
									"file_name":file_name,
									"linked_concept":self.file_data[y][m][d][file_name]
								}
							)
		
		file_checker=FileCheckDialog(self,missing,redundant)
		file_checker.exec_()

		#保存所有相关的数据
		self.diary_data_save_out()
		encrypt_save(self.concept_data,"Concept_Data.dlcw")
		encrypt_save(self.file_data,"File_Data.dlcw")
		self.window_title_update()

		

		#更新所有相关的界面
		try:
			ID=self.lineEdit_id.text()
			self.concept_show(ID)
		except:
			pass
		self.diary_show(self.QDate_transform(self.calendarWidget.selectedDate()))
		self.file_library_list_update()

	def file_library_search_focus(self):
		self.lineEdit_search_file.setFocus()
		self.lineEdit_search_file.selectAll()


	def file_library_add_a_file_to_search_list(self,y,m,d,file_name):
		"传进来int类型的ymd，以及file_name，在listWidget_search_file中添加一个item，并在self.searching_file中append信息"
		self.searching_file.append(
			{
				"y":y,
				"m":m,
				"d":d,
				"file_name":file_name,
				"linked_concept":self.file_data[y][m][d][file_name]
			}
		)
		
		#如果是link
		if "|" in file_name:
			#link的tooltip没有直接设置成url网址
			#考虑到几个file listwidget间的拖动操作需要判断link是否已经在file_data中存在，所以需要附带ymd信息
			#这样损失了直接往浏览器拖动打开网页的功能，但双击、回车打开就行了
			file_url=self.file_saving_base+"/"+str(y)+"/"+str(m)+"/"+str(d)+"/"+file_name
			# ">Google|http://www.google.com"
			file_name=file_name[:file_name.rfind("|")][1:]
		else:
			file_url=self.file_saving_base+"/"+str(y)+"/"+str(m)+"/"+str(d)+"/"+file_name
			
		temp=QListWidgetItem()
		temp.setText(file_name)
		temp.setToolTip(file_url)

		
		self.listWidget_search_file.addItem(temp)

	def file_library_list_update(self):
		"file_data[y][m][d]字典里key的顺序是乱的，也就这里列出来看的时候要按文件名sort一下"


		def list_file_in_today():
			try:
				y=self.y
				m=self.m
				d=self.d
				self.dockWidget_library.setWindowTitle("Library : Searching: Date: %s.%s.%s"%(y,m,d))

				for file_name in sorted(self.file_data[y][m][d].keys()):
					self.file_library_add_a_file_to_search_list(y,m,d,file_name)
					
			except:
				#可能self.file_data[y][m][d]的容器还没创建出来
				pass
		
		def list_file_in_date(search):
			try:
				date=search[3:].split(".")
				y=int(date[0])
				m=int(date[1])
				d=int(date[2])

				for file_name in sorted(self.file_data[y][m][d].keys()):
					self.file_library_add_a_file_to_search_list(y,m,d,file_name)
				
				self.dockWidget_library.setWindowTitle("Library : Searching: Date: %s.%s.%s"%(y,m,d))
			except:
				self.dockWidget_library.setWindowTitle("Library : Searching: Date: ")
				pass
		
		def list_file_without_concept():
			self.dockWidget_library.setWindowTitle("Library : Searching: No Linked Concept: ")
			for y in range(1970,2170):
				for m in range(1,13):
					for d in self.file_data[y][m].keys():
						
						for file_name in sorted(self.file_data[y][m][d].keys()):
							if self.file_data[y][m][d][file_name]==[]:
								self.file_library_add_a_file_to_search_list(y,m,d,file_name)

		def list_file_with_and_concept(search):
			#“与”模式
			searched_concepts=search[3:].split("&")

			#记录文件数量
			result={}
			
			for concept in self.concept_data:
				for searched_concept_name in searched_concepts:
					
					if searched_concept_name in concept["name"].split("|") or searched_concept_name in concept["az"].split("|"):
						for file in concept["file"]:
							y=file["y"]
							m=file["m"]
							d=file["d"]
							file_name=file["file_name"]
							file_str=str(y)+"|"+str(m)+"|"+str(d)+"|"+file_name
							try:
								result[file_str]
							except:
								result[file_str]=0
							result[file_str]+=1
						
			
			search_mun=len(searched_concepts)

			for file_str in result:
				#只有数量大于等于concept数的才算配对成功（小于就说明匹配到的concept太少了）
				if result[file_str]>=search_mun:
					file=file_str.split("|")
					y=int(file[0])
					m=int(file[1])
					d=int(file[2])
					file_name=file[3]

					self.file_library_add_a_file_to_search_list(y,m,d,file_name)

			if searched_concepts!=[]:
				title="Library : Searching: Concept Name: "
				for searched_concept_name in searched_concepts:
					title+=searched_concept_name+" & "
				title=title[:-3]
				self.dockWidget_library.setWindowTitle(title)
			else:
				self.dockWidget_library.setWindowTitle("Library : Searching: Concept Name: ")
		
		def list_file_in_filename(search):
			for y in range(1970,2170):
				for m in range(1,13):
					for d in self.file_data[y][m].keys():
						
						for file_name in sorted(self.file_data[y][m][d].keys()):
							if search in file_name or search in convert_to_az(file_name):
								self.file_library_add_a_file_to_search_list(y,m,d,file_name)
			
			self.dockWidget_library.setWindowTitle("Library : Searching: File Name: %s"%search)


		########################################################################################
		########################################################################################
		########################################################################################
		
		if self.file_saving_base=="":
			QMessageBox.warning(self,"Warning","如果要使用File Library，请先到Setting中设置File Library的基地址。（所有拖进File Library中的文件都会被移动到基地址下）")
			return
		
		search=self.lineEdit_search_file.text()
		
		# 更新待选列表
		self.listWidget_search_file.clear()
		self.lineEdit_date.clear()
		self.listWidget_file_related_concept.clear()
		self.searching_file=[]

		# "输入为空，列出当日的文件"
		if search=="":
			list_file_in_today()
			return
		
		else:
			#特殊搜索模式
			if search[0]=="\\":
				self.dockWidget_library.setWindowTitle("Library : Searching: Special Mode: ")

				# "日期搜索模式:\d 2021.3.12"
				if search[:3]=="\\d " or search[:3]=="\\D ":
					list_file_in_date(search)
					return
				
				#"没有concept归属搜索模式：\^c"
				elif search[:3]=="\\^c" or search[:3]=="\\^C":
					list_file_without_concept()
					return

				# "concept name“与”搜索模式:\c 宇宙 地球"
				elif search[:3]=="\\c " or search[:3]=="\\C ":
					list_file_with_and_concept(search)
					return

			# 文件名搜索模式
			else:
				list_file_in_filename(search)
				return



	def file_library_list_focus(self):
		self.listWidget_search_file.setFocus()
		self.listWidget_search_file.setCurrentRow(0)


	def file_library_file_info_show(self):
		"""
		searching_file列表的信息
		self.searching_file.append(
			{
				"y":y,
				"m":m,
				"d":d,
				"file_name":file_name,
				"linked_concept":self.file_data[y][m][d][file_name]
			}
		)
		"""
		

		index=self.listWidget_search_file.currentRow()

		y=self.searching_file[index]["y"]
		m=self.searching_file[index]["m"]
		d=self.searching_file[index]["d"]
		file_name=self.searching_file[index]["file_name"]
		self.lineEdit_date.setText(self.file_saving_base+"/"+str(y)+"/"+str(m)+"/"+str(d)+"/"+file_name)
		
		self.listWidget_file_related_concept.clear()
		for ID in self.searching_file[index]["linked_concept"]:
			self.listWidget_file_related_concept.addItem(str(ID)+"|"+self.concept_data[ID]["name"])

	def link_check_unique(self,link):
		"查一查file_data中link是否已存在，存在的话返回False，不存在的话返回True"
		for y in range(1970,2170):
			for m in range(1,13):
				for d in self.file_data[y][m].keys():
					for file_name in self.file_data[y][m][d].keys():
						if ">" in file_name:
							have_link=file_name.split("|")[1]
							if have_link==link:
								tray=QSystemTrayIcon()
								tray.setContextMenu(self.qmenu)
								tray.setIcon(QIcon(":/icon/holoico.ico"))
								tray.hide()
								tray.show()
								tray.showMessage("Infomation","该链接已存在！\n%s"%link)
								return False
		return True

	def file_library_file_add(self,links):
		"""
		从file library中进来的直接添加到当前日期，（如果带有内部路径，报错！）
		从concept或者tab root或者diary line进来的判断是否为内部文件，
			如果是外部文件那就放到当前日期，
			如果是内部文件，先按照ymd查filedata中有没有，
				如果有就只做链接操作，
				如果没有，那就说明熊孩子在乱搞，明明可以用file check来添加他非得手拖进来，报出警告！
		
		"""
		"这里进来的要么是文件路径D:/，要么是网址http(s)"
		
		if self.file_saving_base=="":
			QMessageBox.warning(self,"Warning","如果要使用File Library，请先到Setting中设置File Library的基地址。（所有拖进File Library中的文件都会被移动到基地址下）")
			return
		
		#当日路径在不在
		if not os.path.exists(self.file_saving_today_dst):
			os.makedirs(self.file_saving_today_dst)
		else:
			pass
		
		#存不存在当日文件的容器
		try:
			self.file_data[self.y][self.m][self.d]
		except:
			self.file_data[self.y][self.m][self.d]={}
		
		self.progress=QProgressDialog("Adding File...","Cancel",0,len(links),self)
		self.progress.setWindowTitle("Adding File...")
		self.progress.setWindowModality(Qt.WindowModal)
		# self.progress.setMinimumDuration(0)
		self.progress.setValue(0)
		value=0

		#移动文件到当日路径
		for i in links:
			
			self.progress.setValue(value)
			value+=1

			#内部的link不要拖到file区了！
			if ">" in i:
				QMessageBox.warning(self,"Warning","禁止内部拖动Link到File区！")
				return
			
			#如果是网址的，不生成文件
			#file_name拥有特殊标记>和|符号（这个符号是不能存在在文件名中的），>为link的开头，|前为网页title，|后为url
			if i[:4]=="http" or i[:5]=="https":
				i=i.strip().strip("/")

				#link查重
				if not self.link_check_unique(i):
					continue
				
				result=getTitle(i)
				if result[0]==True:
					title=result[1]
				else:
					title="Unkown Page"
					tray=QSystemTrayIcon()
					tray.setContextMenu(self.qmenu)
					tray.setIcon(QIcon(":/icon/holoico.ico"))
					tray.hide()
					tray.show()
					tray.showMessage("Infomation","获取网页Title失败，请查看网络连接是否正常！\n%s"%i)
				
				file_name=">"+title+"|"+i
				self.file_data[self.y][self.m][self.d][file_name]=[]

				####
					# 制造url文件，已废弃！
					# 网页收藏是分散在各地的url文件不够便携！
					# url_file_result=creat_net_url_file(i)
					# if url_file_result[0]==False:
					# 	QMessageBox.critical(self,"Error","获取网页Title失败:\n%s\n%s\n\n网络连接正常吗？\n网页编码标准吗？\n网页标题有没有文件名不允许出现的字符？\n\n请及时更改url文件名，否则第二次会被覆盖掉"%(url_file_result[2],i))
					
					# i=url_file_result[1]
			
			#如果是文件
			else:
				#是不是来自内部路径的文件
				try:
					#检查file
					#如果拥有内部路径
					if self.file_saving_base in i:
						date_and_name=i.replace(self.file_saving_base,"")[1:].split("/")
						y=int(date_and_name[0])
						m=int(date_and_name[1])
						d=int(date_and_name[2])
						if y in range(1970,2170) and m in range(1,13) and d in range(1,32):
							QMessageBox.warning(self,"Warning","禁止内部拖动文件到File区！同时禁止从内部路径导入文件（可以用File Chack功能添加abundant文件）")
							return
				except:
					pass
				
				file_name=os.path.basename(i)
				file_dst=self.file_saving_today_dst+"/"+file_name
				shutil.move(i,file_dst)
				#文件链接concept置空
				self.file_data[self.y][self.m][self.d][file_name]=[]
			
		self.progress.setValue(value)
		self.progress.deleteLater()
		
		self.file_library_list_update()


	def file_library_file_open(self):
		"""
		searching_file列表的信息
		self.searching_file.append(
			{
				"y":y,
				"m":m,
				"d":d,
				"file_name":file_name,
				"linked_concept":self.file_data[y][m][d][file_name]
			}
		)
		"""

		clicked_file_link=self.listWidget_search_file.currentItem().toolTip()
		
		#如果是link
		if "|" in clicked_file_link:
			clicked_file_link=clicked_file_link.split("|")[-1]
			os.system("start explorer \"%s\""%clicked_file_link)
			return
		
		#Alt双击打开文件所在目录
		if self.listWidget_search_file.alt_pressed==True:
			self.listWidget_search_file.alt_pressed=False
			os.startfile(os.path.split(clicked_file_link)[0])
			return
		#########################################################################################
		#########################################################################################
		############################如果按下ctrl双击图片，启动内置的图片浏览器#########################
		clicked_file_name=clicked_file_link.split("/")[-1]
		if which_file_type(clicked_file_name)=="image" and self.listWidget_search_file.ctrl_pressed==True:
			
			pic_list=[]

			for index in range(self.listWidget_search_file.count()):
				file_link=self.listWidget_search_file.item(index).toolTip()
				file_name=file_link.split("/")[-1]
				
				if which_file_type(file_name)=="image":
					pic_list.append(file_link)
		
			clicked_index=pic_list.index(clicked_file_link)

			self.image_viewer=MyImageViewer(pic_list,clicked_index,self.width(),self.height())
			self.image_viewer.show()
			self.listWidget_search_file.ctrl_pressed=False
		############################如果按下ctrl双击图片，启动内置的图片浏览器#########################
		#########################################################################################
		#########################################################################################
		else:
			try:
				os.startfile(clicked_file_link)
			except Exception as e :
				e=str(e).split(":",1)
				QMessageBox.critical(self,"Critical Error","%s\n%s\n请手动设置该类型文件的默认启动应用！"%(e[0],e[1]))


	def file_library_file_delete(self):
		"""
		searching列表的信息
		self.searching_file.append(
			{
				"y":y,
				"m":m,
				"d":d,
				"file_name":file_name,
				"linked_concept":self.file_data[y][m][d][file_name]
			}
		)
		"""


		#先打印出来确认一下
		warning_text="确认要从库中删除文件吗（文件将会移动到回收站，Link将会彻底删除无法撤回），\n同时与该文件相关的concept、diary text链接信息也会被抹去）\n这是无法撤销的操作！\n"
		for file_index in sorted([item.row() for item in self.listWidget_search_file.selectedIndexes()]):
			file=self.searching_file[file_index]
			y=file["y"]
			m=file["m"]
			d=file["d"]
			file_name=file["file_name"]
			warning_text+="\n"+self.file_saving_base+"/"+str(y)+"/"+str(m)+"/"+str(d)+"/"+file_name
		
		

		dlg = QDialog(self)
		dlg.setWindowTitle("Delete Warning")

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
			
			#这里就不用记录do去更新索引下标了，因为不用删除searching_file的元素，在最后file_library_list_update()的时候自动全部就更新了
			for file_index in sorted([item.row() for item in self.listWidget_search_file.selectedIndexes()]):
				file=self.searching_file[file_index]

				y=file["y"]
				m=file["m"]
				d=file["d"]
				file_name=file["file_name"]

				#如果不是link，那么移动文件到回收站
				if "|" not in file_name:
					file_url=self.file_saving_base+"/"+str(y)+"/"+str(m)+"/"+str(d)+"/"+file_name
					if delete_to_recyclebin(file_url)==False:
						QMessageBox.critical(self,"Critical Error","删除文件发生错误，当：\n%s"%file_url)
					

				# (1)清除concept data中的相关数据
				for ID in file["linked_concept"]:
					for ff in self.concept_data[ID]["file"]:
						if ff["y"]==y and ff["m"]==m and ff["d"]==d and ff["file_name"]==file_name:
							self.concept_data[ID]["file"].remove(ff)

							break
						
				# (2)清除diary data中的相关数据
				for year_index in range(1970-1970,2170-1970):
					for month_index in range(0,12):
						for day_index in range(len(self.diary_data[year_index]["date"][month_index])):
							for line_index in range(len(self.diary_data[year_index]["date"][month_index][day_index]["text"])):
								for ff in self.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["linked_file"]:
									if ff["y"]==y and ff["m"]==m and ff["d"]==d and ff["file_name"]==file_name:
										self.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["linked_file"].remove(ff)

										break
				self.diary_data_save_out()

				# (3)清除file data中的相关数据
				del self.file_data[y][m][d][file_name]
		
		
		self.file_library_list_update()
		try:
			self.concept_show(int(self.lineEdit_id.text()))
		except:
			pass
		self.diary_line_file_show()

		for tab in self.custom_tabs_shown:
			tab.tab_update()


	def file_library_file_rename(self):
		def check_validity(new_name_enter,buttonBox):
			if should_not_change!="":
				# ">Google|http://www.google.com"
				new_file_name=new_name_enter.text()
				#没有>了
				if new_file_name[0]!=">":
					buttonBox.setEnabled(0)
					return
				else:
					buttonBox.setEnabled(1)
				
				#没有|http://www.google.com了
				tail="|"+new_file_name.split("|")[-1]
				if should_not_change!=tail:
					buttonBox.button(QDialogButtonBox.Ok).setEnabled(0)
				else:
					buttonBox.button(QDialogButtonBox.Ok).setEnabled(1)
		
		for file_index in sorted([item.row() for item in self.listWidget_search_file.selectedIndexes()]):
			
			old_file=self.searching_file[file_index]
			
			old_y=old_file["y"]
			old_m=old_file["m"]
			old_d=old_file["d"]
			old_file_name=old_file["file_name"]


			dlg = QDialog(self)
			dlg.setMinimumSize(400,200)
			dlg.setWindowTitle("Rename")

			old_name_label=QLabel("Old Name:")
			old_name_enter=QLineEdit()
			old_name_enter.setText(old_file_name)
			old_name_enter.setReadOnly(1)

			new_name_label=QLabel("New Name:")
			new_name_enter=QLineEdit()
			new_name_enter.setText(old_file_name)
			
			QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
			buttonBox = QDialogButtonBox(QBtn)
			buttonBox.accepted.connect(dlg.accept)
			buttonBox.rejected.connect(dlg.reject)

			layout=QVBoxLayout()
			layout.addWidget(old_name_label)
			layout.addWidget(old_name_enter)
			layout.addWidget(new_name_label)
			layout.addWidget(new_name_enter)
			layout.addWidget(buttonBox)
			dlg.setLayout(layout)

			new_name_enter.textEdited.connect(lambda:check_validity(new_name_enter,buttonBox))
			#输入框自动定位
			new_name_enter.setFocus()

			#should_not_change用来防止乱修改网址link
			if "|" in old_file_name:
				# ">Google|http://www.google.com"
				should_not_change="|"+old_file_name.split("|")[-1]
				old_file_extension=old_file_name.split("|")[-1]
				new_name_enter.setSelection(1,len(old_file_name)-len(old_file_extension)-2)
			else:
				should_not_change=""
				old_file_extension=old_file_name.split(".")[-1]
				new_name_enter.setSelection(0,len(old_file_name)-len(old_file_extension)-1)

			if dlg.exec_():
				new_file_name=new_name_enter.text()
				
				if new_file_name==old_file_name:
					continue


				old_file_url=self.file_saving_base+"/"+str(old_y)+"/"+str(old_m)+"/"+str(old_d)+"/"+old_file_name
				new_file_url=self.file_saving_base+"/"+str(old_y)+"/"+str(old_m)+"/"+str(old_d)+"/"+new_file_name
				
				if should_not_change=="":
					try:
						os.rename(old_file_url,new_file_url)
					except Exception as e:
						# dont_allow=["?","*","/","\\","<",">",":","\"","|"]
						#出错，继续下一个文件
						QMessageBox.critical(self,"Error","重命名%s出错：\n\n%s"%(old_file_url,e))
						continue

				if should_not_change=="":
					new_file_icon=which_icon(new_file_name)
				else:
					new_file_icon=which_icon(new_file_name+".url")

				# replace concept data中的old data，增加file data中的new data
				self.file_data[old_y][old_m][old_d][new_file_name]=[]
				for ID in old_file["linked_concept"]:

					#file data中的linked id顺便改了
					self.file_data[old_y][old_m][old_d][new_file_name].append(ID)

					#replace old file中linked id中的linked file的信息
					for ff_index in range(len(self.concept_data[ID]["file"])):
						
						ff=self.concept_data[ID]["file"][ff_index]
						if ff["y"]==old_y and ff["m"]==old_m and ff["d"]==old_d and ff["file_name"]==old_file_name:
							self.concept_data[ID]["file"][ff_index]["file_name"]=new_file_name
							self.concept_data[ID]["file"][ff_index]["file_icon"]=new_file_icon

							break
					
				
				# 删除file data中的old data
				del self.file_data[old_y][old_m][old_d][old_file_name]

				# replace diary data中的old data
				for year_index in range(1970-1970,2170-1970):
					for month_index in range(0,12):
						for day_index in range(len(self.diary_data[year_index]["date"][month_index])):
							for line_index in range(len(self.diary_data[year_index]["date"][month_index][day_index]["text"])):
								for ff_index in range(len(self.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["linked_file"])):
									ff=self.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["linked_file"][ff_index]
									if ff["y"]==old_y and ff["m"]==old_m and ff["d"]==old_d and ff["file_name"]==old_file_name:
										
										self.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["linked_file"][ff_index]["file_name"]=new_file_name
										self.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["linked_file"][ff_index]["file_icon"]=new_file_icon

										break
				self.diary_data_save_out()
				
			else:
				#一个文件取消重命名，进行下一个
				continue
		
		self.file_library_list_update()
		try:
			self.concept_show(int(self.lineEdit_id.text()))
		except:
			pass
		self.diary_line_file_show()

		for tab in self.custom_tabs_shown:
			tab.tab_update()






	def setting_menu(self):

		try:
			font=self.user_settings.value("font")
			font_size=self.user_settings.value("font_size")
		except:
			font=None
			font_size=""
			pass
		
		try:
			pixiv_cookie=decrypt(self.user_settings.value("pixiv_cookie"))
		except:
			pixiv_cookie=""
			pass
		
		dlg=SettingDialog(self.file_saving_base,font,font_size,pixiv_cookie)
		

		if dlg.exec_():

			if dlg.font!=None:
				font=dlg.font
				font_size=dlg.font_size

				self.user_settings.setValue("font",font)
				self.user_settings.setValue("font_size",font_size)
				self.font_set(font,font_size)
			
			
			self.file_saving_base=dlg.lineEdit_file_saving_base.text()
			self.user_settings.setValue("file_saving_base",encrypt(self.file_saving_base))
			self.file_saving_today_dst=self.file_saving_base+"/"+str(self.y)+"/"+str(self.m)+"/"+str(self.d)
			self.file_library_list_update()
			

			pixiv_cookie=dlg.lineEdit_pixiv_cookie.text()
			self.user_settings.setValue("pixiv_cookie",encrypt(pixiv_cookie))
			
		else:
			pass



	def center_export(self,which):
		if which=="Concept":
			save_to_json(self.concept_data,"Concept_Data.json")
		elif which=="Diary":
			save_to_json(self.diary_data,"Diary_Data.json")
		elif which=="File":
			save_to_json(self.file_data,"File_Data.json")
		elif which=="RSS":
			save_to_json(self.rss_data,"RSS_Data.json")



	def rss_feed_daily_update(self):
		#淦！为了搞界面展示后的自动后台更新，搞了将近四个小时……
		#先是搞不好QSystemTrayIcon
		#然后不知道python的thread库和QT的QThread的区别，捣腾了半天python的thread，最终卡界面……
		#网上各种进界面后自动运行还不影响界面操作的方法，什么修改window的showEvent啊，
		#什么qApp.processEvents()啊，还是侦测第一次点进窗体啊，但是无论哪种都会卡界面……
		#
		#为了不卡界面还是得用QT的QThread……
		#然后尝试QThread的class又不允许用__init__传参……
		#咋就没想到传参函数呢？
		def partial_work_done(rss_url,updated):
		
			self.qlock.lock()
			
			#标记最新更新日期
			last_update=str(self.y)+str(self.m)+str(self.d)
			self.rss_data[rss_url]["last_update"]=last_update
			
			#如果有新文章，那就append，并且更新tree列表和文章列表
			if updated==True:
				#正序遍历，每个都放在第一个，所以最新的就在最前面了
				for article in self.daily_update_thread.new_article_list:
					
					self.rss_data[rss_url]["article_list"].insert(0,article)
					self.rss_data[rss_url]["unread"]+=1
			
				self.rss_feed_show()
				self.rss_tree_build()
			
			self.qlock.unlock()
			
		
		def fuckyou():
			self.treeWidget_rss.setDragEnabled(1)
			self.treeWidget_rss.setDragDropMode(QAbstractItemView.InternalMove)
			

		# 在每日更新的时候有qlock请求，
		# 如果这时拖动了树会调用rss_tree_data_update去更新tree_data
		# 就会请求qlock，就会和每日更新的qlock争抢，导致界面假死
		# 所以禁止拖动树
		self.treeWidget_rss.setDragEnabled(0)
		self.treeWidget_rss.setDragDropMode(QAbstractItemView.NoDragDrop)


		#制定今天更新的列表
		today=what_day_is_today()#today的范围是0-7，所以如果frequency为0，那么不会自动更新，只能手动更新
		last_update=str(self.y)+str(self.m)+str(self.d)
		
		updating_url_list=[]
		for rss_url in self.rss_data.keys():
			
			#选出今天应该更新，并且今天没有更新过的feed
			if today in self.rss_data[rss_url]["frequency"] and last_update!=self.rss_data[rss_url]["last_update"]:
				updating_url_list.append(rss_url)
				

		# print("Today is",today)

		#传入要更新的列表
		self.daily_update_thread = RSS_Updator_Threador()
		self.daily_update_thread.setdata(self,updating_url_list)

		self.daily_update_thread.progress.connect(partial_work_done)
		self.daily_update_thread.finished.connect(fuckyou)
		self.daily_update_thread.start()


	def rss_feed_manually_update(self):
		
		def partial_work_done(rss_url):
			
			self.qlock.lock()
			
			#正序遍历，每个都放在第一个，所以最新的就在最前面了
			for article in self.manually_update_thread.new_article_list:
				
				self.rss_data[rss_url]["article_list"].insert(0,article)
				self.rss_data[rss_url]["unread"]+=1
			
			self.qlock.unlock()
			
			self.rss_feed_show()
			self.rss_tree_build()
		
		def fuckyou():
			self.treeWidget_rss.setDragEnabled(1)
			self.treeWidget_rss.setDragDropMode(QAbstractItemView.InternalMove)
			self.manually_updateing=False
		
		# 只允许一个手动更新存在
		if self.manually_updateing==True:
			QMessageBox.warning(self,"Warning","上一个手动更新还未结束！")
			return
		
		selected_item=[item for item in self.treeWidget_rss.selectedItems()]

		#先检查，选中的全部都是RSS吗
		is_all_rss=True
		for item in selected_item:
			if item.text(1)!="RSS":
				is_all_rss=False
				break
		
		#全部都是rss
		if is_all_rss==True:
			updating_url_list=[]
			for item in selected_item:
				rss_url=item.text(2)
				updating_url_list.append(rss_url)

			#传入要更新的列表
			self.manually_update_thread = RSS_Updator_Threador()
			self.manually_update_thread.setdata(self,updating_url_list)

			self.manually_update_thread.progress.connect(partial_work_done)
			self.manually_update_thread.finished.connect(fuckyou)

			self.manually_updateing=True
			self.manually_update_thread.start()

			return
			
		#不全部都是RSS
		else:
			###############################################################################
			###################################Folder######################################
			###############################################################################
			#如果只选中了一个folder
			if len(selected_item)==1 and selected_item[0].text(1)=="Folder":
				folder=selected_item[0]
				

				updating_url_list=[]

				folder_name=re.findall("(?<=\d\]\|).*",folder.text(0))[0]
				#找文件夹中所有的RSS
				for item in self.rss_tree_data:
					if type(item)==dict and item["folder_name"]==folder_name:
						for rss_url in [feed[2] for feed in item["RSS"]]:
							updating_url_list.append(rss_url)
						break
				
				#传入要更新的列表
				self.manually_update_thread = RSS_Updator_Threador()
				self.manually_update_thread.setdata(self,updating_url_list)

				self.manually_update_thread.progress.connect(partial_work_done)
				self.manually_update_thread.finished.connect(fuckyou)

				self.manually_updateing=True
				self.manually_update_thread.start()
				
				return
				
			#如果选中了乱七八糟
			else:
				QMessageBox.warning(self,"Warning","要更新RSS Feed就好好选！")

	def rss_feed_add(self):
		"批量导入Standar RSS feed或者Custom RSS feed"
		def all_work_done(progress_max):

			self.qlock.lock()

			for i in self.adding_feed_thread.successed.keys():
				self.rss_data[i]=self.adding_feed_thread.successed[i]
			
			for temp in self.adding_feed_thread.temp_tree_item_list:
				self.treeWidget_rss.addTopLevelItem(temp)
			
			self.qlock.unlock()
			
			self.rss_tree_data_update()

			if self.adding_feed_thread.failed==[]:
				QMessageBox.information(self,"Information","全部导入成功！")
			else:
				warning_text="未导入以下链接：\n"
				for i in self.adding_feed_thread.failed:
					warning_text+=i+"\n"
				QMessageBox.warning(self,"Warning",warning_text)

			self.progress.setValue(progress_max)
			self.progress.deleteLater()

			
		def fuckyou(i):
			self.progress.setValue(i)
			

		dlg = QDialog(self)
		dlg.setWindowTitle("Add New RSS Feed")
		text="""Rss Url:（支持多行导入，一行一个，不用空行）
已经内置Bilibili Video RSS（在上方选择Bilibili Video模式，添加https://space.bilibili.com/ID）
已经内置Bandcamp RSS（在上方选择Bandcamp模式，添加https://BANDNAME.bandcamp.com）
已经内置Pixiv Illustration RSS（在上方选择Pixiv Illustration模式，添加https://www.pixiv.net/users/ID）
已经内置Pixiv Manga RSS（在上方选择Pixiv Manga模式，添加https://www.pixiv.net/users/ID）

其他自制RSS源站点：
https://rsshub.app/
https://feedx.net/
https://feedx.top/

豆瓣动态: https://rsshub.app/douban/people/ID/status
知乎: https://rss.lilydjwg.me/zhihu/用户ID
Youtube: https://www.youtube.com/feeds/videos.xml?channel_id=频道ID
Reddit: https://www.reddit.com/r/SUBREDDIT.rss
"""
		rss_url_label=QTextBrowser(self)
		rss_url_label.setText(text)
		rss_url_label.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Maximum)
		
		rss_url_enter=QPlainTextEdit()

		combobox=QComboBox(self)
		combobox.addItem("Standard")
		combobox.addItem("Bilibili Video")
		combobox.addItem("Bandcamp")
		combobox.addItem("Pixiv Illustration")
		combobox.addItem("Pixiv Manga")
		
		QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
		buttonBox = QDialogButtonBox(QBtn)
		buttonBox.accepted.connect(dlg.accept)
		buttonBox.rejected.connect(dlg.reject)

		layout=QVBoxLayout()
		layout.addWidget(combobox)
		layout.addWidget(rss_url_label)
		layout.addWidget(rss_url_enter)
		layout.addWidget(buttonBox)
		dlg.setLayout(layout)
		dlg.setMinimumSize(600,600)

		if dlg.exec_():
			
			TYPE=combobox.currentText()
			
			#支持多行导入，一行一个，不用空行
			rss_url_list=rss_url_enter.toPlainText().split("\n")
			
			#看看有哪些需要导入的
			alredy_have=self.rss_data.keys()

			need_to_add=[]
			dont_need_to_add=[]
			warning_need_to_add_text=""
			warning_dont_need_to_add_text=""

			for i in rss_url_list:
				i=i.strip().strip("/")

				#alredy_have里的rss_url是已经加了||TYPE信息的东西了，这里比较的时候也要加上去
				if i+"||"+TYPE in alredy_have:
					dont_need_to_add.append(i)
					warning_dont_need_to_add_text+=i+"\n"
				else:
					#可能有糊涂蛋一次导入了多个一模一样的家伙
					#这里自动去重
					#这里need_to_add中是要传到parser中的，所以先不要加||TYPE信息
					if i not in need_to_add:
						need_to_add.append(i)
						warning_need_to_add_text+=i+"\n"
			
			if dont_need_to_add!=[]:
				warning_text="已存在如下链接：\n"+warning_dont_need_to_add_text+"\n"+"即将导入如下链接：\n"+warning_need_to_add_text
				QMessageBox.warning(self,"Warning",warning_text)
			

			#开始导入！
			if need_to_add!=[]:
				progress_max=len(need_to_add)+1

				self.progress=QProgressDialog("Adding RSS Feed...","Cancel",0,progress_max,self)
				self.progress.setWindowTitle("Adding RSS Feed...")
				self.progress.setWindowModality(Qt.WindowModal)
				self.progress.setMinimumDuration(0)
				self.progress.setValue(1)
				
				
				self.adding_feed_thread = RSS_Adding_Getor_Threador()

				TYPE=combobox.currentText()
				self.adding_feed_thread.setdata(self,need_to_add,TYPE)

				
				self.adding_feed_thread.progress.connect(fuckyou)
				self.adding_feed_thread.finished.connect(lambda:all_work_done(progress_max))
				
				
				self.adding_feed_thread.start()

		else:
			pass


	def rss_feed_folder_create(self):
		dlg = QDialog(self)
		dlg.setWindowTitle("Create New RSS Folder")

		name_label=QLabel("Folder Name:")
		name_enter=QLineEdit()
		
		QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
		buttonBox = QDialogButtonBox(QBtn)
		buttonBox.accepted.connect(dlg.accept)
		buttonBox.rejected.connect(dlg.reject)

		layout=QVBoxLayout()
		layout.addWidget(name_label)
		layout.addWidget(name_enter)
		layout.addWidget(buttonBox)
		dlg.setLayout(layout)

		if dlg.exec_():
			folder_name=name_enter.text()
			
			#文件夹不能重名
			alreay_have=[]
			for i in self.rss_tree_data:
				if type(i)==dict:
					alreay_have.append(i["folder_name"])
			
			if folder_name not in alreay_have:

				#哈哈哈哈，隐藏了header后，它只显示第一个column，这样就可以在后面添加附属信息了！
				#这样就可以不用每时每刻记录RSS data，每时每刻修改RSS data
				#只用在最后遍历整棵树，存储RSS树就行了！
				temp=QTreeWidgetItem(["[0]|"+folder_name,"Folder",""])
				temp.setIcon(0,QIcon(":/icon/folder.svg"))

				self.treeWidget_rss.addTopLevelItem(temp)

				self.rss_tree_data_update()
			else:
				QMessageBox.warning(self,"Warning","RSS文件夹不能重名！")
				return
		else:
			return


	def rss_feed_delete(self):
		def deepin_del_feed_in_tree(root,pointer,delete_feed_url):
			for index in range(root.childCount()):
				
				#如果是RSS
				if root.child(index).text(2)!="":
					#找到了！
					if root.child(index).text(2)==delete_feed_url:
						ii=0
						for i in pointer:
							try:
								if i[2]==delete_feed_url:
									break
							except:
								pass
							ii+=1
						#删除这个feed
						pointer.pop(ii)
						return

					#没找到
					else:
						continue
				
				#如果是Folder
				else:
					
					#传入这个folder中的rss列表的pointer
					deepin_del_feed_in_tree(root.child(index),pointer[index]["RSS"],delete_feed_url)
		
		delete_list=[item for item in self.treeWidget_rss.selectedItems()]

		dlg = QDialog(self)
		dlg.setWindowTitle("Delete Warning")

		warning_text="确认要删除这些RSS Feed吗？注意，删除文件夹将会删除文件夹下的所有Feed！\n这是无法撤销的操作！\n"
		for item in delete_list:
			if item.text(2)!="":
				warning_text+="RSS: "+item.text(0)+": "+item.text(2)+"\n"
			else:
				warning_text+="Folder: "+item.text(0)+"\n"
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
			
			#先删feed
			for item in delete_list:
				#如果是Feed
				if item.text(2)!="":

					#去rss_tree_data中删除那个元组
					root=self.treeWidget_rss.invisibleRootItem()
					deepin_del_feed_in_tree(root,self.rss_tree_data,item.text(2))


					self.qlock.lock()

					del self.rss_data[item.text(2)]
					
					self.qlock.unlock()
			
			#再删Folder
			for item in delete_list:
				#如果是Folder
				if item.text(2)=="":
					folder_name=re.findall("(?<=\d\]\|).*",item.text(0))[0]

					self.qlock.lock()

					for i in range(len(self.rss_tree_data)):
						if type(self.rss_tree_data[i])==dict:
							
							if self.rss_tree_data[i]["folder_name"]==folder_name:
								
								for j in self.rss_tree_data[i]["RSS"]:
									feed_url=j[2]
									del self.rss_data[feed_url]
									
								del self.rss_tree_data[i]
								break

					self.qlock.unlock()


			self.rss_tree_build()
			self.listWidget_rss.clear()


	def rss_edit(self):
		def mark_all_article_in_folder(folder_name):
			
			#先列出文件夹中所有的feed
			feed_list=[]
			for item in self.rss_tree_data:
				if type(item)==dict and item["folder_name"]==folder_name:
					for rss_url in [feed[2] for feed in item["RSS"]]:
						feed_list.append(rss_url)
					break

			self.qlock.lock()

			for rss_url in feed_list:
				article_list=self.rss_data[rss_url]["article_list"]
				for article in article_list:
					if article[2]==False:
						article[2]=True
						self.rss_data[rss_url]["unread"]-=1


			self.qlock.unlock()

			self.rss_feed_show()
			self.rss_tree_build()
			QMessageBox.information(self,"Information","Folder内的文章全部标记已读！")



		selected_item=[item for item in self.treeWidget_rss.selectedItems()]
		
		if selected_item==[]:
			return
		
		#先检查，选中的全部都是RSS吗
		is_all_rss=True
		for item in selected_item:
			if item.text(1)!="RSS":
				is_all_rss=False
				break
		
		###############################################################################
		###################################RSS们#######################################
		###############################################################################
		#全部都是rss，编辑feed更新频率，feed内全部已读
		if is_all_rss==True:
			rss_url_list=[]
			for item in selected_item:
				#每个元素是[rss_name,rss_url]
				rss_name=re.findall("(?<=\d\]\|).*",item.text(0))[0]
				rss_url=item.text(2)
				rss_url_list.append([rss_name,rss_url])
			
			#传进去一个元素是[rss_name,rss_url]的rss列表
			dlg = RSS_Feed_Edit_Dialog(self,rss_url_list)

			if dlg.exec_():
				#这个保存的操作是通过改变选取触发的，如果最后没改变选取，那这里再保存一下
				dlg.save_and_show_feed()
				
				result=dlg.baked
				
				"""帮你bake好了，是个字典
				# self.baked[rss_url]={
				# 	"feed_name":rss_name,
				# 	"frequency":self.parent.rss_data[rss_url]["frequency"],
				# 	"unread":self.parent.rss_data[rss_url]["unread"]
				# }
				
				"""
				
				self.qlock.lock()
	

				for rss_url in result.keys():
					
					self.rss_data[rss_url]["frequency"]=result[rss_url]["frequency"]
					
					#已读了吗
					if result[rss_url]["unread"]==0:
						self.rss_data[rss_url]["unread"]=0
						for article in self.rss_data[rss_url]["article_list"]:
							article[2]=True
					
					#改名字了吗
					if self.rss_data[rss_url]["feed_name"]!=result[rss_url]["feed_name"]:
						
						self.rss_data[rss_url]["feed_name"]=result[rss_url]["feed_name"]
						
						#去rss_tree_data中修改rss的名字
						for i in range(len(self.rss_tree_data)):
							#folder
							if type(self.rss_tree_data[i])==dict:
								for j in range(len(self.rss_tree_data[i]["RSS"])):
									if self.rss_tree_data[i]["RSS"][j][2]==rss_url:
										#淦，竟然弄成了元组类型，这里没法直接改，那就重新制定吧
										self.rss_tree_data[i]["RSS"][j]=(result[rss_url]["feed_name"],"RSS",rss_url)
							#顶层的RSS
							if type(self.rss_tree_data[i])==tuple:
								if self.rss_tree_data[i][2]==rss_url:
									self.rss_tree_data[i]=(result[rss_url]["feed_name"],"RSS",rss_url)
					

				self.qlock.unlock()

				self.rss_feed_show()
				self.rss_tree_build()

			else:
				pass


		#不全部都是RSS
		else:
			###############################################################################
			###################################Folder#######################################
			###############################################################################
			#如果只选中了一个folder
			#编辑Folder名字，folder内全部已读
			if len(selected_item)==1 and selected_item[0].text(1)=="Folder":
				folder=selected_item[0]

				dlg = QDialog(self)
				dlg.setMinimumSize(400,100)
				dlg.setWindowTitle("Edit RSS Folder")
				
				btn=QPushButton("Mark All Articles in This Folder")
				label=QLabel("Folder Name")
				enter=QLineEdit()
				
				old_folder_name=re.findall("(?<=\d\]\|).*",folder.text(0))[0]
				btn.clicked.connect(lambda:mark_all_article_in_folder(old_folder_name))
				enter.setText(old_folder_name)

				QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
				buttonBox = QDialogButtonBox(QBtn)
				buttonBox.accepted.connect(dlg.accept)
				buttonBox.rejected.connect(dlg.reject)

				layout=QVBoxLayout()
				layout.addWidget(btn)
				layout.addWidget(label)
				layout.addWidget(enter)
				layout.addWidget(buttonBox)
				dlg.setLayout(layout)

				if dlg.exec_():

					self.qlock.lock()

					new_folder_name=enter.text()
					for item in self.rss_tree_data:
						if type(item)==dict and item["folder_name"]==old_folder_name:
							item["folder_name"]=new_folder_name
					
					self.qlock.unlock()
					
					self.rss_feed_show()
					self.rss_tree_build()
				else:
					pass

			#如果选中了乱七八糟
			else:
				QMessageBox.warning(self,"Warning","要编辑RSS Feed信息就好好选！")

	def rss_tree_drop_update(self):
		
			
			# 每次拖动排阶级后，就检查，RSS不能作为folder
			
			root=self.treeWidget_rss.invisibleRootItem()
			for index in range(root.childCount()):
				top_level=root.child(index)

				#如果是根级的rss，那么它的下面不能有东西
				if top_level.text(2)!="":
					if top_level.childCount()!=0:
						QMessageBox.warning(self,"Warning","RSS源不能作为Folder！")
						self.rss_tree_build()
						return
				
				#如果是根级的folder，那么它的下面不能有folder，只能有rss，且rss底下不能有东西
				else:
					for index2 in range(top_level.childCount()):
						second_level=top_level.child(index2)

						#是folder
						if second_level.text(2)=="":
							QMessageBox.warning(self,"Warning","Folder只能有一层！")
							self.rss_tree_build()
							return
						#是rss
						else:
							if second_level.childCount()!=0:
								QMessageBox.warning(self,"Warning","RSS源不能作为Folder！")
								self.rss_tree_build()
								return
			
			self.rss_tree_data_update()
			self.rss_tree_build()
		


	def rss_tree_data_update(self):
		# 根据树的结构，重塑rss_tree_data
		def deepin(root,pointer):
			for index in range(root.childCount()):
				
				#如果是RSS
				if root.child(index).text(2)!="":
					if root.child(index).text(1)=="RSS":
						rss_name=re.findall("(?<=\d\]\|).*",root.child(index).text(0))[0]
						rss_url=root.child(index).text(2)
						
						#树的信息中不区分RSS是Standard还是Custom，只区分Folder和RSS！这东西只是用于建树以及判断rss树的合法性的
						pointer.append((rss_name,"RSS",rss_url))
						continue
				
				#如果是Folder
				else:
					folder_name=re.findall("(?<=\d\]\|).*",root.child(index).text(0))[0]
					folder={
						"folder_name":folder_name,
						"RSS":[]
					}
					pointer.append(folder)
					
					#传入这个folder中的rss列表的pointer
					deepin(root.child(index),folder["RSS"])
		
		self.qlock.lock()

		self.rss_tree_data=[]
		root=self.treeWidget_rss.invisibleRootItem()
		deepin(root,self.rss_tree_data)

		self.qlock.unlock()


	def rss_tree_build(self):
		# 根据rss_tree_data的层级结构，建树
		tree_expand={}
		root=self.treeWidget_rss.invisibleRootItem()
		for index in range(root.childCount()):
			#如果是folder，就记录一下expand属性
			if root.child(index).text(2)=="":
				folder_name=re.findall("(?<=\d\]\|).*",root.child(index).text(0))[0]
				tree_expand[folder_name]=root.child(index).isExpanded()
		

		self.treeWidget_rss.clear()
		for top_level in self.rss_tree_data:
			#top_level放了folder
			if type(top_level)==dict:
				folder_name=top_level["folder_name"]
				folder_unread=0
				
				#这里folder_name先这样写，下面还会计算未读数量，重新写folder_name的
				temp_root=QTreeWidgetItem([folder_name,"Folder",""])
				temp_root.setIcon(0,QIcon(":/icon/folder.svg"))
				self.treeWidget_rss.addTopLevelItem(temp_root)

				for rss in top_level["RSS"]:
					
					rss_name=rss[0]
					rss_url=rss[2]
					feed_unread=self.rss_data[rss_url]["unread"]
					folder_unread+=feed_unread

					temp=QTreeWidgetItem(temp_root,["[%s]|"%feed_unread+rss_name,"RSS",rss_url])
					temp.setIcon(0,QIcon(":/icon/rss.svg"))
				
				#重新写folder_name
				temp_root.setText(0,"[%s]|"%folder_unread+folder_name)

				try:
					temp_root.setExpanded(tree_expand[folder_name])
				except:
					pass
			
			#top_level放了rss
			elif type(top_level)==tuple:
				rss=top_level
				
				rss_name=rss[0]
				rss_url=rss[2]
				feed_unread=self.rss_data[rss_url]["unread"]

				temp=QTreeWidgetItem(["[%s]|"%feed_unread+rss_name,"RSS",rss_url])
				temp.setIcon(0,QIcon(":/icon/rss.svg"))

				self.treeWidget_rss.addTopLevelItem(temp)


	def rss_feed_show(self):
		"""
		因为自动更新rss时会同时刷新tree和刷新文章列表，所以会捕获不到treeWidget_rss.currentItem()，
		这样就分了四种情况。这里还“巧妙”地用了戳不到屁股的列表死角嘿嘿嘿
		"""

		self.listWidget_rss.clear()
		
		try:
			#第一次点进来
			rss_url=self.treeWidget_rss.currentItem().text(2)

			#点的不是folder，而是rss
			if rss_url!="":
				self.current_rss_showing=rss_url
				article_list=self.rss_data[rss_url]["article_list"]
				for article in article_list:
					#这里可以直接按顺序列出，因为放入的时候我已经把新的放在最前面了
					article_name=article[0]
					if article[2]==False:
						self.listWidget_rss.addItem("[NEW]|"+article_name)
					else:
						self.listWidget_rss.addItem("[√]|"+article_name)
			
			#点的是folder，展示下层的所有文章
			elif rss_url=="":
				folder_name=re.findall("(?<=\d\]\|).*",self.treeWidget_rss.currentItem().text(0))[0]

				#先列出文件夹中所有的feed
				feed_list=[]
				for item in self.rss_tree_data:
					if type(item)==dict and item["folder_name"]==folder_name:
						for rss_url in [feed[2] for feed in item["RSS"]]:
							feed_list.append(rss_url)					
						break

				# self.current_rss_showing存所有文章结构体的列表，
				# 每个文章结构体的结构：[article_name,article_url,article_read,article_time,rss_url,article_index]
				self.current_rss_showing=[]
				for rss_url in feed_list:
					article_list=self.rss_data[rss_url]["article_list"]

					index=0
					for article in article_list:
						article_name=article[0]
						article_url=article[1]
						article_read=article[2]
						article_time=article[3]
						article_index=index#文章在feed中所属的index，记录这个方便点文章时，回去标记已读过
						self.current_rss_showing.append([article_name,article_url,article_read,article_time,rss_url,article_index])
						index+=1

				#按时间排序
				self.current_rss_showing.sort(key=lambda x:x[3],reverse=True)
				
				for i in self.current_rss_showing:
					article_name=i[0]
					if i[2]==False:
						self.listWidget_rss.addItem("[NEW]|"+article_name)
					else:
						self.listWidget_rss.addItem("[√]|"+article_name)
				
				"把正在看的folder的name藏在最后，重新进这个函数的时候有用（就是下面的那种情况），反正那边点击文章的也不会戳到屁股上的"
				self.current_rss_showing.append(folder_name)
		except:
			#tree刷新了，也要更新article list
			#但是刷新后，rss_url=tree.currentItem()没有东西啊
			#rss_url不能用了
			#那就展示和self.current_rss_showing一样的东西好了
			#点的不是folder，而是rss
			if type(self.current_rss_showing)==str:
				rss_url=self.current_rss_showing
				article_list=self.rss_data[rss_url]["article_list"]
				for article in article_list:
					#这里可以直接按顺序列出，因为放入的时候我已经把新的放在最前面了
					article_name=article[0]
					if article[2]==False:
						self.listWidget_rss.addItem("[NEW]|"+article_name)
					else:
						self.listWidget_rss.addItem("[√]|"+article_name)
			
			#点的是folder，展示下层的所有文章
			elif type(self.current_rss_showing)==list:
				"把正在看的folder的name藏在了最后，重新进这个函数的时候有用（就是下面的那种情况），反正那边点击文章的也不会戳到屁股上的"
				folder_name=self.current_rss_showing[-1]

				#先列出文件夹中所有的feed
				feed_list=[]
				for item in self.rss_tree_data:
					if type(item)==dict and item["folder_name"]==folder_name:
						for rss_url in [feed[2] for feed in item["RSS"]]:
							feed_list.append(rss_url)
						break

				# self.current_rss_showing存所有文章结构体的列表，
				# 每个文章结构体的结构：[article_name,article_url,article_read,article_time,rss_url,article_index]
				self.current_rss_showing=[]
				for rss_url in feed_list:
					article_list=self.rss_data[rss_url]["article_list"]

					index=0
					for article in article_list:
						article_name=article[0]
						article_url=article[1]
						article_read=article[2]
						article_time=article[3]
						article_index=index#文章在feed中所属的index，记录这个方便点文章时，回去标记已读过
						self.current_rss_showing.append([article_name,article_url,article_read,article_time,rss_url,article_index])
						index+=1

				#按时间排序
				self.current_rss_showing.sort(key=lambda x:x[3],reverse=True)
				
				for i in self.current_rss_showing:
					article_name=i[0]
					if i[2]==False:
						self.listWidget_rss.addItem("[NEW]|"+article_name)
					else:
						self.listWidget_rss.addItem("[√]|"+article_name)
				
				"把正在看的folder的name藏在最后，重新进这个函数的时候有用（就是现在这种情况），反正那边点击文章的也不会戳到屁股上的"
				self.current_rss_showing.append(folder_name)




	def rss_feed_article_show(self):
		"""
		两种情况，文章列表来源于单个rss，或者文章列表来源于folder
		点击文章是戳不到self.current_rss_showing的屁股上的
		"""

		

		index=self.listWidget_rss.currentRow()

		#文章列表来源于单个rss
		if type(self.current_rss_showing)==str:
			article=self.rss_data[self.current_rss_showing]["article_list"][index]
			article_name=article[0]
			article_url=article[1]
			
			if article[2]==False:
				
				self.qlock.lock()

				article[2]=True
				self.rss_data[self.current_rss_showing]["unread"]-=1

				self.qlock.unlock()

				#更新文章列表的前缀
				self.listWidget_rss.item(index).setText("[√]|"+article_name)
				#更新tree列表中的前缀
				self.rss_tree_build()
			
		#文章列表来源于folder
		# self.current_rss_showing存所有文章结构体的列表，
		# 每个文章结构体的结构：[article_name,article_url,article_read,article_time,rss_url,article_index]
		elif type(self.current_rss_showing)==list:
			article=self.current_rss_showing[index]
			article_name=article[0]
			article_url=article[1]
			rss_url=article[4]
			article_index=article[5]

			if article[2]==False:
				
				self.qlock.lock()

				self.rss_data[rss_url]["article_list"][article_index][2]=True
				self.rss_data[rss_url]["unread"]-=1

				self.qlock.unlock()

				#更新文章列表的前缀
				self.listWidget_rss.item(index).setText("[√]|"+article_name)
				#更新tree列表中的前缀
				self.rss_tree_build()
		
		
		article_url=QUrl.fromUserInput(article_url)
		if article_url.isValid():
			self.browser.load(article_url)


	def rss_open_webpage(self):
		curren_url=self.browser.page().url().toString()
		if curren_url!="":
			os.system("start explorer \"%s\""%curren_url)






	def tab_custom_create(self):
		dlg = QDialog(self)
		dlg.setWindowTitle("Create New Tab")

		tab_name_label=QLabel("Tab Name:")
		tab_name_enter=QLineEdit()
		tab_selection_id_label=QLabel("Root ID:")
		tab_selection_id_enter=QLineEdit()
		tab_selection_depth_label=QLabel("Max Tree Depth:")
		tab_selection_depth_enter=QLineEdit()
		
		QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
		buttonBox = QDialogButtonBox(QBtn)
		buttonBox.accepted.connect(dlg.accept)
		buttonBox.rejected.connect(dlg.reject)

		layout=QVBoxLayout()
		layout.addWidget(tab_name_label)
		layout.addWidget(tab_name_enter)
		layout.addWidget(tab_selection_id_label)
		layout.addWidget(tab_selection_id_enter)
		layout.addWidget(tab_selection_depth_label)
		layout.addWidget(tab_selection_depth_enter)
		layout.addWidget(buttonBox)
		dlg.setLayout(layout)

		if dlg.exec_():
			tab_name=tab_name_enter.text()

			#查重
			already_have=[x[0] for x in self.custom_tab_data]
			if tab_name in already_have:
				QMessageBox.warning(self,"Warning","Tab页不能重名！")
				return
			
			else:
				try:
					tab_selection_id=int(tab_selection_id_enter.text())
					self.concept_data[tab_selection_id]
				except:
					QMessageBox.warning(self,"Error","请输入合法的Concept ID！")
					return
				try:
					tab_selection_depth=int(tab_selection_depth_enter.text())
				except:
					QMessageBox.warning(self,"Error","请输入合法的Tree Depth！")
					return

				#新建一个tab，调用自定义的MyTabWidget
				tab=MyTabWidget(self,tab_selection_id,tab_selection_depth)

				#这里的tab应该算是一个指针，可以在这里链上一些槽
				#点击内部的leaf，回传到这里，去显示concept
				tab.clicked.connect(lambda ID:self.concept_show(ID))

				#一开始不让操作
				tab.listWidget_file_root.setEnabled(0)
				tab.listWidget_file_leafs.setEnabled(0)
				
				self.tabWidget.addTab(tab,QIcon(":/icon/trello.svg"),tab_name)
				self.tabWidget.setCurrentIndex(self.tabWidget.indexOf(tab))

				#更新custom_tab_data的数据
				self.custom_tab_data.append([tab_name,tab_selection_id,tab_selection_depth,True])

				#custom_tabs_shown存储正在界面上展示的tabs，这些是用来实时与concept data同步更新的
				self.custom_tabs_shown.append(tab)

		else:
			return

	def tab_custom_hide(self):
		
		tab_index=self.tabWidget.currentIndex()
		tab_name=self.tabWidget.tabText(tab_index)
		
		if tab_name not in ["Home","Diary","RSS"]:
			
			index=0
			for i in range(len(self.custom_tab_data)):
				if self.custom_tab_data[i][0]==tab_name:
					self.custom_tab_data[i][3]=False
					break
				index+=1
			
			#custom_tabs_shown存储正在界面上展示的tabs，这些是用来实时与concept data同步更新的
			tab=self.tabWidget.currentWidget()
			self.custom_tabs_shown.remove(tab)
			
			#tab窗删除这个tab
			self.tabWidget.removeTab(tab_index)

			#新增一个指向“能恢复tab并且销毁自身”的action
			action=QAction(tab_name,self)
			action.setIcon(QIcon(":/icon/trello.svg"))
			action.triggered.connect(lambda:self.tab_custom_resurrection(index,action))
			self.menuTab.addAction(action)
			

	def tab_custom_resurrection(self,index,action):
		#更新custom_tab_data的数据
		self.custom_tab_data[index][3]=True

		#新建一个tab，调用自定义的MyTabWidget
		tab=MyTabWidget(self,self.custom_tab_data[index][1],self.custom_tab_data[index][2])

		#这里的tab应该算是一个指针，可以在这里链上一些槽
		#点击内部的leaf，回传到这里，去显示concept
		tab.clicked.connect(lambda ID:self.concept_show(ID))

		self.tabWidget.addTab(tab,QIcon(":/icon/trello.svg"),self.custom_tab_data[index][0])
		self.tabWidget.setCurrentIndex(self.tabWidget.indexOf(tab))
		
		#custom_tabs_shown存储正在界面上展示的tabs，这些是用来实时与concept data同步更新的
		self.custom_tabs_shown.append(tab)

		#销毁action
		self.menuTab.removeAction(action)
		
	def tab_custom_delete(self):
		tab_index=self.tabWidget.currentIndex()
		tab_name=self.tabWidget.tabText(tab_index)
		
		if tab_name not in ["Home","Diary","RSS"]:
			
			dlg = QDialog(self)
			dlg.setWindowTitle("Delete Warning")

			name_label=QLabel("确认要删除Tab:%s吗？"%tab_name)
			
			QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
			buttonBox = QDialogButtonBox(QBtn)
			buttonBox.accepted.connect(dlg.accept)
			buttonBox.rejected.connect(dlg.reject)

			layout=QVBoxLayout()
			layout.addWidget(name_label)
			layout.addWidget(buttonBox)
			dlg.setLayout(layout)

			if dlg.exec_():
				index=0
				for i in range(len(self.custom_tab_data)):
					if self.custom_tab_data[i][0]==tab_name:
						break
					index+=1
				
				self.custom_tab_data.pop(index)

				#custom_tabs_shown存储正在界面上展示的tabs，这些是用来实时与concept data同步更新的
				tab=self.tabWidget.currentWidget()
				self.custom_tabs_shown.remove(tab)
				
				#tab窗删除这个tab
				self.tabWidget.removeTab(tab_index)



	############################################################################
	# 要摒弃树就彻底一点，这个就别用了哈~
	# 这东西也没法用了哈哈，现在是固定格式、固定位置的File Library了
	# 是不能允许在外面逍遥自在的文件树的存在的
	# 这东西还是留着吧，当时自己敲这个一遍通过，还挺高兴的呢
	# 想看这东西的效果的话，去旧版本看吧。
	# 现在在这里数据结构不匹配，存进去了file也打不开。
	# def concept_import_file_tree(self):
		
	# 	def deepin(current_dir,parent_ID):

	# 		current_dir=current_dir.replace("\\","/")
	# 		ID=len(self.concept_data)
	# 		name=current_dir.split("/")[-1]
	# 		self.concept_data.append({
	# 			"id": ID,
	# 			"name": name,
	# 			"detail": "",
	# 			"parent": [],
	# 			"child": [],
	# 			"relative": [],
	# 			"az": convert_to_az(name),
	# 			"file": []
	# 		})
	# 		if parent_ID!=-1:
	# 			#和上一级建立父子关系
	# 			self.concept_data[parent_ID]["child"].append(ID)
	# 			self.concept_data[ID]["parent"].append(parent_ID)

	# 		dir_list=os.listdir(current_dir)
	# 		dir_list.sort()
	# 		for i in dir_list:
				
	# 			next_dir=os.path.join(current_dir,i)
	# 			#是file
	# 			if not os.path.isdir(next_dir):
	# 				next_dir=next_dir.replace("\\","/")
	# 				file_name=next_dir.split("/")[-1]
	# 				file_icon=which_icon(file_name)
	# 				self.concept_data[ID]["file"].append({
	# 					"file_name":file_name,
	# 					"file_link":next_dir,
	# 					"file_icon":file_icon
	# 				})
				
	# 			#是dir
	# 			else:
	# 				if self.progress.wasCanceled():
	# 					return
	# 				self.cnt+=1
	# 				self.progress.setValue(self.cnt)

	# 				deepin(next_dir,ID)
			
	# 		self.concept_data[ID]["parent"].sort()
	# 		self.concept_data[ID]["child"].sort()
	# 		self.concept_data[ID]["file"].sort(key=lambda x:x["file_name"])
	# 		return
		

	# 	QMessageBox.warning(self,"Warning","这个功能将会导入文件树，其中的文件夹算作concept，\n文件夹中的文件算作concept linked file，这并不是\n很符合软件的理念，但也许有人会用得上吧。")
		
	# 	dlg=QFileDialog(self)
	# 	directory=dlg.getExistingDirectory()

	# 	self.progress=QProgressDialog("Importing Concept From File Tree...","Cancel",0,20000,self)
	# 	################################################################
	# 	#################他奶奶的凭什么加上这句话就不会假死?!!!!##############
	# 	########################我他妈折腾这东西花了快两个小时？！！##########
	# 	####################又是用多线程又是用延迟，！######################
	# 	####################结果你就告诉我用这个?！#########################
	# 	self.progress.setWindowModality(Qt.WindowModal)
	# 	#####他妈的学校这破网还连不上VPN，##################################
	# 	#############################没有GOOGLE怎么活啊？！！##############
	# 	################################################################
	# 	self.progress.setMinimumDuration(1)
	# 	self.cnt=0

	# 	deepin(directory,-1)
		
	# 	self.progress.setValue(20000)

	# 	del self.progress
	# 	del self.cnt


	# 	self.concept_search_list_update()
	# 	self.window_title_update()

	# 	for tab in self.custom_tabs_shown:
	# 		tab.tab_update()
	############################################################################

	def about(self):
		QMessageBox.about(self,"About","Dongli Teahouse Studio\nVersion: 0.1.9.0\nAuthor: 鍵山狐\nContact: Holence08@gmail.com")





	def font_set(self,font,font_size):
		font_size=int(font_size)

		#正常字体大小
		self.plainTextEdit_single_line.setFont(font)
		self.plainTextEdit_sticker.setFont(font)
		self.listWidget_lines.setFont(font)
		self.listWidget_concept_related_text.setFont(font)
		self.treeWidget_rss.setFont(font)
		self.listWidget_rss.setFont(font)

		#偏小
		font.setPointSize(int(font_size*0.8))
		self.lineEdit_search_concept.setFont(font)
		self.listWidget_search_concept.setFont(font)
		self.lineEdit_id.setFont(font)
		self.lineEdit_name.setFont(font)
		self.plainTextEdit_detail.setFont(font)
		
		self.listWidget_parent.setFont(font)
		self.listWidget_child.setFont(font)
		self.listWidget_relative.setFont(font)

		self.listWidget_text_related_concept.setFont(font)
		
		self.listWidget_concept_linked_file.setFont(font)
		self.listWidget_text_linked_file.setFont(font)
		
		#展示区偏大
		font.setPointSize(int(font_size*1.4))
		self.textEdit_viewer.setFont(font)

		#头文字偏小
		font.setPointSize(int(font_size*0.8))
		# QApplication.setFont(font)
		self.menubar.setFont(font)
		self.tabWidget.setFont(font)
		self.dockWidget_diary.setFont(font)
		self.toolBox_text.setFont(font)
		self.dockWidget_concept.setFont(font)
		self.toolBox_concept.setFont(font)

		font.setPointSize(10)
		self.calendarWidget.setFont(font)

		#文件列表的icon与间距大小
		font_size=font_size*2
		self.listWidget_text_linked_file.setIconSize(QSize(font_size,font_size))
		self.listWidget_text_linked_file.setGridSize(QSize(font_size*3,font_size*3))
		self.listWidget_text_linked_file.setSpacing(font_size)
		self.listWidget_text_linked_file.setWordWrap(1)
		self.listWidget_concept_linked_file.setIconSize(QSize(font_size,font_size))
		self.listWidget_concept_linked_file.setGridSize(QSize(font_size*3,font_size*3))
		self.listWidget_concept_linked_file.setSpacing(font_size)
		self.listWidget_concept_linked_file.setWordWrap(1)
		
	def center_locate_file_in_library(self):
		def locating(listwidget):
			if len(listwidget.selectedIndexes())>1:
				QMessageBox.warning(self,"Warning","一次只能Locate一个文件！")
				return
			else:
				
				file_str=listwidget.currentItem().toolTip()
				
				#replace出来的东西：
				#/2021/3/23/>John Legend|https://www.youtube.com/aadasdasd
				#/2021/3/23/24.jpg
				date_and_name=file_str.replace(self.file_saving_base,"")[1:].split("/")
				y=int(date_and_name[0])
				m=int(date_and_name[1])
				d=int(date_and_name[2])

				if "|" in file_str:
					file_name=file_str[file_str.find(">"):]
				else:
					file_name=date_and_name[3]

				self.listWidget_search_file.clear()
				self.lineEdit_date.clear()
				self.listWidget_file_related_concept.clear()
				self.searching_file=[]
				
				self.file_library_add_a_file_to_search_list(y,m,d,file_name)
				
				self.dockWidget_library.activateWindow()
				self.listWidget_search_file.setFocus()
				self.listWidget_search_file.setCurrentRow(0)


		#concept删除链接文件
		if self.listWidget_concept_linked_file.hasFocus():
			locating(self.listWidget_concept_linked_file)

		
		#文本块删除链接文件
		elif self.listWidget_text_linked_file.hasFocus():
			locating(self.listWidget_text_linked_file)
		
		#tab删除root file
		else:
			for tab in self.custom_tabs_shown:
				if tab.listWidget_file_root.hasFocus():
					locating(tab.listWidget_file_root)
					break

	def center_delete(self):
		
		
		#文本块删除
		if self.listWidget_lines.hasFocus():
			self.diary_line_delete()
		
		#文本块删除链接concept
		elif self.listWidget_text_related_concept.hasFocus():
			self.diary_line_concept_remove()

		#concept删除
		elif self.lineEdit_id.hasFocus():
			self.concept_delete()
		
		#concept删除relationship
		elif self.listWidget_parent.hasFocus() or self.listWidget_child.hasFocus() or self.listWidget_relative.hasFocus():
			self.concept_realationship_remove()
		
		#rss删除feed or folder
		elif self.treeWidget_rss.hasFocus():
			self.rss_feed_delete()
		
		#file manager处删除库的文件
		elif self.listWidget_search_file.hasFocus():
			self.file_library_file_delete()
		
		#concept删除链接文件
		elif self.listWidget_concept_linked_file.hasFocus():
			self.concept_linked_file_remove()
		
		#文本块删除链接文件
		elif self.listWidget_text_linked_file.hasFocus():
			self.diary_line_file_remove()
		
		#tab删除root file
		else:
			for tab in self.custom_tabs_shown:
				if tab.listWidget_file_root.hasFocus():
					tab.concept_linked_file_remove()
					break

	
	def center_edit(self):
		
		#文件重命名
		if self.listWidget_search_file.hasFocus():
			self.file_library_file_rename()
		

		elif self.treeWidget_rss.hasFocus():
			self.rss_edit()


	def window_toggle_fullscreen(self):
		
		if self.isFullScreen():
			
			self.showNormal()
		else:
			self.showFullScreen()


	def data_validity_check(self):
		"检查diary concept file rss的data"

		##########################################################################################################
		#################################################Diary####################################################
		##########################################################################################################
		#为了能直接索引到年月日，所以固定存储格式
		l=range(1970,2170)
		if "Diary_Data.dlcw" in os.listdir("."):
			#如果有Diary_Data.dlcw文件
			try:
				data=decrypt_load("Diary_Data.dlcw")
				#不是从1970到2169年都有的，或者一年不是十二个月的，报错
				for i in range(len(l)):
					if data[i]["year"]!=l[i] or len(data[i]["date"])!=12:
						QMessageBox.critical(self,"Error","Diary_Data.dlcw文件Diary结构出错，请联系相关开发人员！")
						return 0
						
			except:
				QMessageBox.critical(self,"Error","Diary_Data.dlcw文件出错，请联系相关开发人员！")
				return 0

		else:
			#如果没有Diary_Data.dlcw文件
			data=[]
			for i in l:
				temp_year={
					"year":i,
					"date":[
						[],[],[],[],
						[],[],[],[],
						[],[],[],[]
					]
				}
				data.append(temp_year)
			
			encrypt_save(data,"Diary_Data.dlcw")
				
		##########################################################################################################
		#################################################Concept##################################################
		##########################################################################################################
		if "Concept_Data.dlcw" in os.listdir("."):
			#如果有Concept_Data.dlcw文件
			try:
				data=decrypt_load("Concept_Data.dlcw")
			except:
				QMessageBox.critical(self,"Error","Concept_Data.dlcw文件出错，请联系相关开发人员！")
				return 0

			try:
				if "Universe" not in data[0]["name"] or data[0]["parent"]!=-1:
					QMessageBox.critical(self,"Error","Concept_Data.dlcw文件头部结构出错，请联系相关开发人员！")
					return 0
			except:
				QMessageBox.critical(self,"Error","Concept_Data.dlcw文件数据结构出错，请联系相关开发人员！")
				return 0

			try:
				for i in data[1:]:
					if isinstance(i["id"],int) and isinstance(i["name"],str) and isinstance(i["detail"],str) and isinstance(i["parent"],list) and isinstance(i["child"],list) and isinstance(i["relative"],list) and isinstance(i["az"],str) and isinstance(i["file"],list):
						continue
					else:
						QMessageBox.critical(self,"Error","Concept_Data.dlcw文件Concept结构出错，请联系相关开发人员！")
						return 0
						
			except:
				QMessageBox.critical(self,"Error","Concept_Data.dlcw文件数据结构出错，请联系相关开发人员！")
				return 0
			
			
		else:
			#如果没有Concept_Data.dlcw文件
			data=[{
				"id": 0,
				"name": "宇宙|Universe",
				"detail": "",
				"parent": -1,
				"child": [],
				"relative": [],
				"az": "yz|universe",
				"file": []
			}]
			encrypt_save(data,"Concept_Data.dlcw")
		

		##########################################################################################################
		#################################################File#####################################################
		##########################################################################################################
		#为了能直接索引到年月日，所以固定存储格式
		l=range(1970,2170)
		if "File_Data.dlcw" in os.listdir("."):
			#如果有File_Data文件
			try:
				data=decrypt_load("File_Data.dlcw")
			except:
				QMessageBox.critical(self,"Error","File_Data.dlcw文件出错，请联系相关开发人员！")
				return 0

			try:
				self.file_saving_base=decrypt(self.user_settings.value("file_saving_base"))
			except:
				QMessageBox.critical(self,"Error","file_saving_base出错，请联系相关开发人员！")
				return 0
		else:
			data={}
			for i in l:
				data[i]={
					1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{},11:{},12:{}
				}
			encrypt_save(data,"File_Data.dlcw")
			#默认路径
			self.file_saving_base=""
		
		##########################################################################################################
		#################################################RSS######################################################
		##########################################################################################################
		if "RSS_Data.dlcw" in os.listdir("."):
			#不是第一次进来
			try:
				#检查rss_tree_data和rss_data中的url是否有出入
				rss_tree_data=decrypt(self.user_settings.value("rss_tree_data"))
				l0=[]
				for top_level in rss_tree_data:
					#top_level放了folder
					if type(top_level)==dict:
						for rss in top_level["RSS"]:

							rss_url=rss[2]
							l0.append(rss_url)

					#top_level放了rss
					elif type(top_level)==tuple:
						rss=top_level
						
						rss_url=rss[2]
						l0.append(rss_url)

				rss_data=decrypt_load("RSS_Data.dlcw")
				l1=list(rss_data.keys())

				if list_difference(l0,l1)==[]:
					pass
				else:
					QMessageBox.critical(self,"Error","RSS信息不匹配，请联系相关开发人员！")
					return 0
			except:
				QMessageBox.critical(self,"Error","RSS文件出错，请联系相关开发人员！")
				return 0
		
		#第一次进来
		else:
			rss_tree_data=[]
			rss_data={}
			#因为是多线程，所以最好实时保存到外存
			self.user_settings.setValue("rss_tree_data",encrypt(rss_tree_data))
			encrypt_save(rss_data,"RSS_Data.dlcw")
		
		##########################################################################################################
		#################################################Done#####################################################
		##########################################################################################################
		

		return 1


	def data_load(self):
		"load file、concept、file、rss的data"

		self.diary_data=decrypt_load("Diary_Data.dlcw")
		self.origin_diary_data=decrypt_load("Diary_Data.dlcw")

		self.concept_data=decrypt_load("Concept_Data.dlcw")

		self.file_data=decrypt_load("File_Data.dlcw")

		self.rss_data=decrypt_load("RSS_Data.dlcw")
	
		self.rss_tree_data=decrypt(self.user_settings.value("rss_tree_data"))
		
		# print(self.rss_tree_data)

		# for rss_url in self.rss_data.keys():
		# 	try:
		# 		self.rss_data[rss_url]["article_list"].pop()
		# 		self.rss_data[rss_url]["article_list"].pop()
		# 		self.rss_data[rss_url]["article_list"].pop()
		# 	except :
		# 		pass
		#
		# for i in self.rss_data.keys():
		# 	print(self.rss_data[i]["type"],self.rss_data[i]["feed_name"],self.rss_data[i]["unread"])

		

		##################################################
		#如果之后更新了az转换规则，启用下面的操作，更新所有事物的az属性：
		# for i in self.concept_data:
		# 	i["az"]=convert_to_az(i["name"])
		##################################################

		####弃用
			######################################################################
			#QT自带的搜索提示，没啥用，用自己的列表匹配还能用拼音呢
			# self.dictionary=[]
			# for i in self.concept_data:
			# 	self.dictionary.append(i["name"])
			#
			# self.completer=QCompleter(self.dictionary)
			# self.lineEdit_search_concept.setCompleter(self.completer)
			# self.completer.activated.connect(self.concept_search_list_update)#点击搜索提示
			######################################################################

	def concept_info_edited_and_save(self):
		try:
			ID=int(self.lineEdit_id.text())
			self.concept_data[ID]["name"]=self.lineEdit_name.text()
			self.concept_data[ID]["az"]=convert_to_az(self.concept_data[ID]["name"])
			self.concept_data[ID]["detail"]=self.plainTextEdit_detail.toPlainText()

			#如果当前的文本块或者当日的text中链接的concept中有正在编辑的，那就更新一下
			#所以不用费劲判断current行或者每一行有没有修改中的ID
			#直接全部刷新就行了
			self.diary_line_concept_list_update()
			self.concept_search_list_update()

			for tab in self.custom_tabs_shown:
				tab.tab_update()
			return
		except:
			pass
	
	def diary_line_fix_index(self):
		#添加删除行之后，会出现重复或间隔的index，在此修复
		for i in range(len(self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"])):
			self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][i]["index"]=i
	
	def diary_line_edited_and_save(self):
		
		#每编辑完一行就保存一下文本
		try:
			#如果不存在该日，是新来的日记，
			if self.is_new_diary==1:
				
				self.new_diary["text"][self.current_line_index]["line_text"]=self.plainTextEdit_single_line.toPlainText()

				#把临时存储的新馆复制进去
				self.diary_data[self.current_year_index]["date"][self.current_month_index].append(self.new_diary)
				#再按日重排序
				self.diary_data[self.current_year_index]["date"][self.current_month_index].sort(key=lambda x:x["day"])
				
				#重新定位current_day_index
				self.current_day_index=0
				for day in self.diary_data[self.current_year_index]["date"][self.current_month_index]:
					if day["day"]!=self.current_day:
						self.current_day_index+=1
					else:
						break
				#这样就有了重排序后正确的index
				
				self.is_new_diary=0
			
			#如果已经存在该日
			else:
				if self.current_line_index!=-1:
					self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][self.current_line_index]["line_text"]=self.plainTextEdit_single_line.toPlainText()

			self.window_title_update()
			self.diary_line_fix_index()
			self.diary_text_update()
			self.diary_line_concept_list_update()
			self.diary_line_file_show()
		except:
			pass
		
		#万一页面中显示的concept正好就与编辑的文本块有关，那就要更新concept related text
		try:
			item_id=int(self.lineEdit_id.text())
			#要更新一下concept related text，就用这个好了
			self.concept_show(item_id)
		except:
			pass

	def diary_data_save_out(self):
		#保存到外存
		encrypt_save(self.diary_data,"Diary_Data.dlcw")
		self.origin_diary_data=decrypt_load("Diary_Data.dlcw")

		self.window_title_update()

	
	def window_title_update(self):
		
		if self.origin_diary_data!=self.diary_data:
			self.setWindowTitle("Dongli Teahouse Studio *Unsaved Change*")
		else:
			self.setWindowTitle("Dongli Teahouse Studio")

	def concept_search_focus(self):
		self.lineEdit_search_concept.setFocus()
		self.lineEdit_search_concept.selectAll()
	
	def concept_search_list_update(self):
		
		search=self.lineEdit_search_concept.text()
		
		#只有展示全部事物的时候才能拖动排序
		#因为新的id由列表从上到下的位号决定
		if search!="":
			self.listWidget_search_concept.setDragEnabled(0)
		else:
			self.listWidget_search_concept.setDragEnabled(1)
		
		#更新待选列表
		self.listWidget_search_concept.clear()

		#####################################################
		#
		# 这里还可以添加很多种搜索模式
		# p[A&B&C] ABC的p的交集
		# p[A|B|C] ABC的p的并集
		# p[A|B|C] "asd" ABC的p的并集之中名字叫asd的
		# p[A|B] & c[C] （AB的p的并集）与（C的c）的交集
		#
		#####################################################
		
		#没有parent
		if search[:4]=="\^p " and search[4:7]!="\^c":
			
			#无附加信息
			if len(search)==4:
				for i in self.concept_data:
					if i["parent"]==[]:
						self.listWidget_search_concept.addItem(str(i["id"])+"|"+i["name"])
				self.dockWidget_concept.setWindowTitle("Concept Searching: No Parent")
			#附加name信息
			else:
				search_name=search[4:]
				for i in self.concept_data:
					if i["parent"]==[]:
						if search_name==str(i["id"]) or search_name in i["name"] or search_name in i["az"] or search_name in i["detail"]:
							self.listWidget_search_concept.addItem(str(i["id"])+"|"+i["name"])
				self.dockWidget_concept.setWindowTitle("Concept Searching: No Parent %s"%search_name)

		#没有child
		elif search[:4]=="\^c " and search[4:7]!="\^p":
			#无附加信息
			if len(search)==4:
				for i in self.concept_data:
					if i["child"]==[]:
						self.listWidget_search_concept.addItem(str(i["id"])+"|"+i["name"])
				self.dockWidget_concept.setWindowTitle("Concept Searching: No Child")
			#附加name信息
			else:
				search_name=search[4:]
				for i in self.concept_data:
					if i["child"]==[]:
						if search_name==str(i["id"]) or search_name in i["name"] or search_name in i["az"] or search_name in i["detail"]:
							self.listWidget_search_concept.addItem(str(i["id"])+"|"+i["name"])
				self.dockWidget_concept.setWindowTitle("Concept Searching: No Child %s"%search_name)

		#没有parent也没有child
		elif search[:8]=="\^p \^c " or search[:8]=="\^c \^p ":
			#无附加信息
			if len(search)==8:
				for i in self.concept_data:
					if i["parent"]==[] and i["child"]==[]:
						self.listWidget_search_concept.addItem(str(i["id"])+"|"+i["name"])
				self.dockWidget_concept.setWindowTitle("Concept Searching: No Parent & No Child")
			#附加name信息
			else:
				search_name=search[8:]
				for i in self.concept_data:
					if i["parent"]==[] and i["child"]==[]:
						if search_name==str(i["id"]) or search_name in i["name"] or search_name in i["az"] or search_name in i["detail"]:
							self.listWidget_search_concept.addItem(str(i["id"])+"|"+i["name"])
				self.dockWidget_concept.setWindowTitle("Concept Searching: No Parent & No Child %s"%search_name)

		#正常模式搜名字
		else:
			for i in self.concept_data:
				#搜索id或name或az name或detail
				if search==str(i["id"]) or search in i["name"] or search in i["az"] or search in i["detail"]:
					self.listWidget_search_concept.addItem(str(i["id"])+"|"+i["name"])
			self.dockWidget_concept.setWindowTitle("Concept Searching: %s"%search)

	
	def concept_search_list_drag_update(self):
		# 因为file data中也有concept id的信息，若要修改


		if self.listWidget_search_concept.item(0).text()[0]!="0":
			self.concept_search_list_update()
			QMessageBox.warning(self,"Error","哦我的上帝，你最好不要拖动宇宙！")
			return
		
		#清空展示区
		self.lineEdit_id.clear()
		self.lineEdit_name.clear()
		self.plainTextEdit_detail.clear()
		self.listWidget_parent.clear()
		self.listWidget_child.clear()
		self.listWidget_relative.clear()

		changed_id_dict={}
		#找出id改变的序偶
		for i in range(self.listWidget_search_concept.count()):
			old_id=int(self.listWidget_search_concept.item(i).text().split("|")[0])
			new_id=i
			if new_id!=old_id:
				changed_id_dict[old_id]=new_id
		
		changed_id_dict_keys=list(changed_id_dict.keys())
		#修改id、parent、child、relative中有改变的id
		for item in self.concept_data:
			if item["id"] in changed_id_dict_keys:
				item["id"]=changed_id_dict[item["id"]]
			
			if item["parent"]!=-1:
				for i in range(len(item["parent"])):
					if item["parent"][i] in changed_id_dict_keys:
						item["parent"][i]=changed_id_dict[item["parent"][i]]
			
			for i in range(len(item["child"])):
					if item["child"][i] in changed_id_dict_keys:
						item["child"][i]=changed_id_dict[item["child"][i]]
			
			for i in range(len(item["relative"])):
					if item["relative"][i] in changed_id_dict_keys:
						item["relative"][i]=changed_id_dict[item["relative"][i]]
		#排序
		self.concept_data.sort(key=lambda x:x["id"])

		#修改diary_data中有改变的id
		for year_index in range(1970-1970,2170-1970):
			for month_index in range(0,12):
				for day_index in range(len(self.diary_data[year_index]["date"][month_index])):
					for line_index in range(len(self.diary_data[year_index]["date"][month_index][day_index]["text"])):
						for linked_item_index in range(len(self.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["linked_concept"])):
							old_id=self.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["linked_concept"][linked_item_index]
							if old_id in changed_id_dict_keys:
								self.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["linked_concept"][linked_item_index]=changed_id_dict[old_id]
		self.diary_data_save_out()

		#修改file_data中有改变的id
		#这里的数据都是是字典……索引和diary的方式不一样的……
		for year_index in range(1970,2170):
			for month_index in range(1,13):
				for day in self.file_data[year_index][month_index].keys():
					for file in self.file_data[year_index][month_index][day].keys():
						for item_old_id in self.file_data[year_index][month_index][day][file]:
							if item_old_id in changed_id_dict_keys:
								self.file_data[year_index][month_index][day][file].remove(item_old_id)
								self.file_data[year_index][month_index][day][file].append(changed_id_dict[item_old_id])
		

		self.diary_line_concept_list_update()
		self.concept_search_list_update()

		for tab in self.custom_tabs_shown:
			tab.tab_update()


	def diary_markdown_view_update(self):
		full_text=""
		for i in self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"]:
			full_text+=i["line_text"]+"\n\n"
		self.textEdit_viewer.setMarkdown(full_text)
	
	def diary_text_update(self):
		self.listWidget_lines.clear()
		for single_line in self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"]:
			#列出所有行
			self.listWidget_lines.addItem(single_line["line_text"])
		self.diary_markdown_view_update()


	def concept_show(self,ID):
		#点开一个item才允许用file列表
		self.listWidget_concept_linked_file.setEnabled(1)

		item=self.concept_data[int(ID)]#当前展示的事物

		self.lineEdit_id.setText(str(item["id"]))

		#给宇宙大哥让位
		if item["id"]==0:
			self.lineEdit_name.setReadOnly(1)
		else:
			self.lineEdit_name.setReadOnly(0)
		
		self.lineEdit_name.setText(item["name"])
		self.plainTextEdit_detail.setPlainText(item["detail"])

		#关联item列表
		self.listWidget_parent.clear()
		self.listWidget_child.clear()
		self.listWidget_relative.clear()
		if item["parent"]!=-1:
			for related_ID in item["parent"]:
				related_item=self.concept_data[related_ID]
				name=str(related_item["id"])+"|"+related_item["name"]
				self.listWidget_parent.addItem(name)
		for related_ID in item["child"]:
			related_item=self.concept_data[related_ID]
			name=str(related_item["id"])+"|"+related_item["name"]
			self.listWidget_child.addItem(name)
		for related_ID in item["relative"]:
			related_item=self.concept_data[related_ID]
			name=str(related_item["id"])+"|"+related_item["name"]
			self.listWidget_relative.addItem(name)
		
		#file链接列表
		self.listWidget_concept_linked_file.clear()
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
				file_url=self.file_saving_base+"/"+str(y)+"/"+str(m)+"/"+str(d)+"/"+file_name
				# ">Google|http://www.google.com"
				file_name=file_name[:file_name.rfind("|")][1:]
			else:
				file_url=self.file_saving_base+"/"+str(y)+"/"+str(m)+"/"+str(d)+"/"+file_name
				
			temp=QListWidgetItem()
			temp.setText(file_name)
			temp.setIcon(QIcon(file["file_icon"]))
			temp.setToolTip(file_url)
			
			self.listWidget_concept_linked_file.addItem(temp)
		

		#找一找Concept related text
		self.listWidget_concept_related_text.clear()
		text_list=[]
		for year_index in range(1970-1970,2170-1970):
			for month_index in range(0,12):
				for day_index in range(len(self.diary_data[year_index]["date"][month_index])):
					for line_index in range(len(self.diary_data[year_index]["date"][month_index][day_index]["text"])):
						for linked_item_index in range(len(self.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["linked_concept"])):
							item_id=self.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["linked_concept"][linked_item_index]
							if item_id==item["id"]:
								text_list.append({
									#老传统用点号分隔
									"date":str(year_index+1970)+"."+str(month_index+1)+"."+str(self.diary_data[year_index]["date"][month_index][day_index]["day"]),
									"text":self.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["line_text"]
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

			for i in construct_text_list:
				self.listWidget_concept_related_text.addItem(i)
		self.listWidget_concept_related_text.scrollToBottom()



		####弃用
			#######################################################################
			#本来还想在QGridLayout中自动生成QPushButton，每一个按钮对应一个链接物的
			#结果大概是在生成按钮时内存覆盖了，放弃改用列表……
			#
			#手动设置处世空的GridLayout的拉伸系数，这样在里面添加组件的时候才能保持想要的宽度
			# for i in range(5):#
			# 	self.gridLayout_parent.setColumnStretch(i,1)
			# 	self.gridLayout_child.setColumnStretch(i,1)
			# 	self.gridLayout_relative.setColumnStretch(i,1)
			#
			# def clear_button():
			# 	#清空GridLayout中的所有组件
			# 	for i in reversed(range(self.gridLayout_parent.count())):
			# 		self.gridLayout_parent.itemAt(i).widget().deleteLater()
			#
			# def list_button(item):
			# 	row=0
			# 	column=0
			# 	for related_ID in item["parent"]:
			# 		if related_ID==-1:
			# 			break
			# 		#手动换行，貌似清空组件后直接用addWidget（不加位置信息）塞进去位置有问题
			# 		if column==5:
			# 			column=0
			# 			row+=1
			# 		related_item=self.concept_data[related_ID]
			# 		btn_name=str(related_item["id"])+"|"+related_item["name"]
			# 		btn=QPushButton(btn_name)
			# 		btn.clicked.connect(lambda:self.concept_show(btn_name))
			# 		self.gridLayout_parent.addWidget(btn,row,column)
			# 		column+=1
			#######################################################################
	
	def concept_creat(self):
		#防止宇宙大哥的余波
		self.lineEdit_name.setReadOnly(0)

		self.lineEdit_name.setFocus()

		ID=len(self.concept_data)
		self.lineEdit_id.setText(str(ID))
		self.lineEdit_name.clear()
		self.plainTextEdit_detail.clear()

		self.concept_data.append({
		"id":ID,
		"name":"",
		"detail":"",
		"parent":[],
		"child":[],
		"relative":[],
		"az":"",
		"file":[]
		})

		
		self.concept_search_list_update()
		self.concept_show(ID)

		for tab in self.custom_tabs_shown:
			tab.tab_update()

	def concept_delete(self):
		try:
			ID=int(self.lineEdit_id.text())

			dlg = QDialog(self)
			dlg.setWindowTitle("Delete Warning")

			name_label=QLabel("确定要删除 ID = %s 吗？\n这是无法撤销的操作！\n"%ID)
			
			QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
			buttonBox = QDialogButtonBox(QBtn)
			buttonBox.accepted.connect(dlg.accept)
			buttonBox.rejected.connect(dlg.reject)

			layout=QVBoxLayout()
			layout.addWidget(name_label)
			layout.addWidget(buttonBox)
			dlg.setLayout(layout)

			if dlg.exec_():

				#删除宇宙的后果
				if ID==0:
					if self.easter_egg_deleting_universe==0:
						QMessageBox.warning(self,"Warning","哦我的上帝，你不可以删除宇宙，你真的，不可以。")
						self.easter_egg_deleting_universe+=1
						return
					if self.easter_egg_deleting_universe==1:
						QMessageBox.warning(self,"Error","哦上帝，为什么你不听我的话，伙计，西姆叔叔不喜欢倔脾气小孩的。")
						self.easter_egg_deleting_universe+=1
						return
					if self.easter_egg_deleting_universe==2:
						QMessageBox.warning(self,"Error","我亲爱的上朋友！看看你在干些什么？真见鬼！我已经说过了，你不可以删除宇宙。我发誓，如果你要是再尝试删除宇宙，我就要立刻告诉詹妮弗牧师去！")
						self.easter_egg_deleting_universe+=1
						return
					if self.easter_egg_deleting_universe==3:
						QMessageBox.warning(self,"Error","真是见鬼！看在上帝的份上，请不要再删除宇宙了。我敢发誓你的老屁股要和我祖父的老靴子马上会来个亲密接触了。伙计，别担心，如果你愿意支付给我150马克的话，也许我会在我祖父面前为你求求请。")
						self.easter_egg_deleting_universe+=1
						return
					if self.easter_egg_deleting_universe==4:
						QMessageBox.warning(self,"Error","该死，这已经够糟糕了。如果你再不收手，我就去狠狠的踢隔壁欧德毛猫的屁股，我发誓！")
						self.easter_egg_deleting_universe+=1
						return
					if self.easter_egg_deleting_universe==5:
						QMessageBox.critical(self,"Critical Error","程序崩溃！\n\n请联系开发人员，并提供您的错误信息，以及更好玩的翻译腔生成器。\n\n邮箱地址：Holence08@gmail.com")
						QCoreApplication.exit()
						return


				#判断diary中是否已链接了这个item
				#把已链接了这个item的文本打印出来看
				text_list=[]
				for year_index in range(1970-1970,2170-1970):
					for month_index in range(0,12):
						for day_index in range(len(self.diary_data[year_index]["date"][month_index])):
							for line_index in range(len(self.diary_data[year_index]["date"][month_index][day_index]["text"])):
								for linked_item_index in range(len(self.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["linked_concept"])):
									item_id=self.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["linked_concept"][linked_item_index]
									if item_id==ID:
										text_list.append({
											"date":str(year_index+1970)+"."+str(month_index+1)+"."+str(self.diary_data[year_index]["date"][month_index][day_index]["day"]),
											"text":self.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["line_text"]
										})
				if text_list!=[]:
					message=QMessageBox()
					message.setWindowTitle("Warning")

					#淦QMessageBox的大小不能直接改
					# message.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
					# message.setGeometry(0,0,800,400)

					message.setIcon(QMessageBox.Warning)

					#然而\n
					#\n
					#"这就是最简单(zhizhang)的改大小方法                                                         用空格和回车填充                           简单易用好上手！"
					warning_text=str(ID)+"|"+"%s"%self.concept_data[ID]["name"]+" 在日志中已存在：\n\n\n                                                                "
					message.setText(warning_text)

					warning_detailed_text=""
					for i in text_list:
						warning_detailed_text+=i["date"]+" : "+i["text"]+"\n"
					message.setDetailedText(warning_detailed_text)

					message.exec_()
					return
				

				#把关联物的关联信息删掉
				if self.concept_data[ID]["parent"]!=-1:
					for i in self.concept_data[ID]["parent"]:
						self.concept_data[i]["child"].remove(ID)
				
				for i in self.concept_data[ID]["child"]:
					self.concept_data[i]["parent"].remove(ID)
				
				for i in self.concept_data[ID]["relative"]:
					self.concept_data[i]["relative"].remove(ID)

				#把关联file的链接ID信息删掉
				for file in self.concept_data[ID]["file"]:
					file_name=file["file_name"]
					y=file["y"]
					m=file["m"]
					d=file["d"]
					self.file_data[y][m][d][file_name].remove(ID)

				#清空展示区
				self.lineEdit_id.clear()
				self.lineEdit_name.clear()
				self.plainTextEdit_detail.clear()
				self.listWidget_parent.clear()
				self.listWidget_child.clear()
				self.listWidget_relative.clear()
				self.listWidget_concept_linked_file.clear()

				#当前没有展示item了，就禁用file列表
				self.listWidget_concept_linked_file.setEnabled(0)


				del self.concept_data[ID]

				changed_id_dict={}
				#找出id改变的序偶
				for i in range(len(self.concept_data)):
					if i!=self.concept_data[i]["id"]:
						self.concept_data[i]["id"]-=1
						changed_id_dict[i]=i-1
				#因为之前删除了一个元素，所以range里漏掉了最后一个元素
				#这里手动添加
				previouse_len=len(self.concept_data)+1
				previouse_last_id=previouse_len-1
				changed_id_dict[previouse_last_id]=previouse_last_id-1

				changed_id_dict_keys=list(changed_id_dict.keys())
				#修改id、parent、child、relative中有改变的id
				for item in self.concept_data:
					if item["parent"]!=-1:
						for i in range(len(item["parent"])):
							if item["parent"][i] in changed_id_dict_keys:
								item["parent"][i]=changed_id_dict[item["parent"][i]]
					
					for i in range(len(item["child"])):
							if item["child"][i] in changed_id_dict_keys:
								item["child"][i]=changed_id_dict[item["child"][i]]
					
					for i in range(len(item["relative"])):
							if item["relative"][i] in changed_id_dict_keys:
								item["relative"][i]=changed_id_dict[item["relative"][i]]
				
				#修改diary_data中有改变的id
				for year_index in range(1970-1970,2170-1970):
					for month_index in range(0,12):
						for day_index in range(len(self.diary_data[year_index]["date"][month_index])):
							for line_index in range(len(self.diary_data[year_index]["date"][month_index][day_index]["text"])):
								for linked_item_index in range(len(self.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["linked_concept"])):
									item_old_id=self.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["linked_concept"][linked_item_index]
									if item_old_id in changed_id_dict_keys:
										self.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["linked_concept"][linked_item_index]=changed_id_dict[item_old_id]
				self.diary_data_save_out()
				
				#修改file_data中有改变的id
				#这里的数据都是是字典……索引和diary的方式不一样的……
				for year_index in range(1970,2170):
					for month_index in range(1,13):
						for day in self.file_data[year_index][month_index].keys():
							for file in self.file_data[year_index][month_index][day].keys():
								for item_old_id in self.file_data[year_index][month_index][day][file]:
									if item_old_id in changed_id_dict_keys:
										self.file_data[year_index][month_index][day][file].remove(item_old_id)
										self.file_data[year_index][month_index][day][file].append(changed_id_dict[item_old_id])
				

				self.diary_line_concept_list_update()
				self.concept_search_list_update()

				for tab in self.custom_tabs_shown:
					tab.tab_update()


		
		except:
			pass


	def concept_relationship_add(self,mode):
		try:
			item_ID=int(self.lineEdit_id.text())
			link_ID=int(self.listWidget_search_concept.currentItem().text().split("|")[0])
			item_name=self.concept_data[item_ID]["name"]
			link_name=self.concept_data[link_ID]["name"]

			if mode=="parent":
				if link_ID==item_ID:
					QMessageBox.warning(self,"Error","哦我的上帝，你不能链接自身")
					return
				if item_ID==0:
					QMessageBox.warning(self,"Error","哦我的上帝，就让宇宙先生当DAI王吧")
					return
				elif self.concept_data[item_ID]["parent"]!=-1 and link_ID in self.concept_data[item_ID]["parent"] :
					QMessageBox.warning(self,"Error","哦我的上帝，%s 已经是 %s 的父辈了"%(link_name,item_name))
					return
				elif link_ID in self.concept_data[item_ID]["child"]:
					QMessageBox.warning(self,"Error","哦我的上帝，%s 已经是 %s 的子辈了"%(link_name,item_name))
					return
				else:
					self.concept_data[item_ID]["parent"].append(link_ID)
					self.concept_data[item_ID]["parent"].sort()
					self.concept_data[link_ID]["child"].append(item_ID)
					self.concept_data[link_ID]["child"].sort()
			
			if mode=="child":
				if link_ID==item_ID:
					QMessageBox.warning(self,"Error","哦我的上帝，你不能链接自身")
					return
				if link_ID==0:
					QMessageBox.warning(self,"Error","哦我的上帝，就让宇宙先生当DAI王吧")
					return
				elif self.concept_data[item_ID]["parent"]!=-1 and link_ID in self.concept_data[item_ID]["parent"]:
					QMessageBox.warning(self,"Error","哦我的上帝，%s 已经是 %s 的父辈了"%(link_name,item_name))
					return
				elif link_ID in self.concept_data[item_ID]["child"]:
					QMessageBox.warning(self,"Error","哦我的上帝，%s 已经是 %s 的子辈了"%(link_name,item_name))
					return
				else:
					self.concept_data[item_ID]["child"].append(link_ID)
					self.concept_data[item_ID]["child"].sort()
					self.concept_data[link_ID]["parent"].append(item_ID)
					self.concept_data[link_ID]["parent"].sort()
				
			if mode=="relative":
				if link_ID==item_ID:
					QMessageBox.warning(self,"Error","哦我的上帝，你不能链接自身")
					return
				elif link_ID in self.concept_data[item_ID]["relative"]:
					QMessageBox.warning(self,"Error","哦我的上帝，%s 已经是 %s 的亲属了"%(link_name,item_name))
					return
				else:
					self.concept_data[item_ID]["relative"].append(link_ID)
					self.concept_data[item_ID]["relative"].sort()
					self.concept_data[link_ID]["relative"].append(item_ID)
					self.concept_data[link_ID]["relative"].sort()
			
			#更新事物界面
			self.concept_show(item_ID)

			for tab in self.custom_tabs_shown:
				tab.tab_update()
		except:
			pass

	def concept_realationship_remove(self):
		try:
			item_ID=int(self.lineEdit_id.text())

			if self.listWidget_parent.hasFocus():
				
				link_ID=int(self.listWidget_parent.currentItem().text().split("|")[0])

				dlg = QDialog(self)
				dlg.setWindowTitle("Delete Warning")

				name_label=QLabel("确定要删除 Linked ID = %s 吗？\n这是无法撤销的操作！\n"%link_ID)
				
				QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
				buttonBox = QDialogButtonBox(QBtn)
				buttonBox.accepted.connect(dlg.accept)
				buttonBox.rejected.connect(dlg.reject)

				layout=QVBoxLayout()
				layout.addWidget(name_label)
				layout.addWidget(buttonBox)
				dlg.setLayout(layout)

				if dlg.exec_():
					self.concept_data[item_ID]["parent"].remove(link_ID)
					self.concept_data[link_ID]["child"].remove(item_ID)
				else:
					return
			
			elif self.listWidget_child.hasFocus():

				link_ID=int(self.listWidget_child.currentItem().text().split("|")[0])
				
				dlg = QDialog(self)
				dlg.setWindowTitle("Delete Warning")

				name_label=QLabel("确定要删除Linked ID=%s吗？"%link_ID)
				
				QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
				buttonBox = QDialogButtonBox(QBtn)
				buttonBox.accepted.connect(dlg.accept)
				buttonBox.rejected.connect(dlg.reject)

				layout=QVBoxLayout()
				layout.addWidget(name_label)
				layout.addWidget(buttonBox)
				dlg.setLayout(layout)

				if dlg.exec_():
					self.concept_data[item_ID]["child"].remove(link_ID)
					self.concept_data[link_ID]["parent"].remove(item_ID)
				else:
					return
				
			elif self.listWidget_relative.hasFocus():
				
				link_ID=int(self.listWidget_relative.currentItem().text().split("|")[0])
				
				dlg = QDialog(self)
				dlg.setWindowTitle("Delete Warning")

				name_label=QLabel("确定要删除Linked ID=%s吗？"%link_ID)
				
				QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
				buttonBox = QDialogButtonBox(QBtn)
				buttonBox.accepted.connect(dlg.accept)
				buttonBox.rejected.connect(dlg.reject)

				layout=QVBoxLayout()
				layout.addWidget(name_label)
				layout.addWidget(buttonBox)
				dlg.setLayout(layout)

				if dlg.exec_():
					self.concept_data[item_ID]["relative"].remove(link_ID)
					self.concept_data[link_ID]["relative"].remove(item_ID)
				else:
					return
			
			#更新事物界面
			self.concept_show(item_ID)

			for tab in self.custom_tabs_shown:
				tab.tab_update()
		except:
			pass


	def QDate_transform(self,Date):
		return (QDate.year(Date),QDate.month(Date),QDate.day(Date))
		

	def diary_show(self,date):
		y=int(date[0])
		m=int(date[1])
		d=int(date[2])
		self.dockWidget_diary.setWindowTitle("Diary %s.%s.%s"%(y,m,d))
		
		self.plainTextEdit_single_line.clear()
		self.plainTextEdit_single_line.setEnabled(0)
		self.listWidget_text_linked_file.setEnabled(0)

		self.listWidget_lines.clear()
		self.listWidget_text_related_concept.clear()
		self.listWidget_text_linked_file.clear()
		self.textEdit_viewer.clear()

		#存储当前年月坐标
		
		self.current_year_index=y-1970
		self.current_month_index=m-1
		self.current_day=d#记录这个，用来找那些不存在当前日的，重排序后的index

		#找一找当前的日坐标，并看一看是不是全新的：is_new_diary
		find=0
		self.is_new_diary=0
		self.current_day_index=0
		for day in self.diary_data[self.current_year_index]["date"][self.current_month_index]:
			if day["day"]==self.current_day:
				find=1
				break
				#如果找到了，就刚好是那个月中的日的下标
			self.current_day_index+=1
		#如果没找到，暂且放在最后一个，打个标，存储的时候就知道需要日期重排序了
		if find==0:
			self.is_new_diary=1
		
		#标记，初来乍到
		self.is_first_arrived=1

		if self.is_new_diary==0:
			#如果是已经有内容的日期，就正常操作

			#初始行号设为最后一行，这样直接新增的话就在最后一行了
			self.current_line_index=len(self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"])-1

			#列出行和关联事物
			listed_item=[]
			for single_line in self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"]:
				#列出所有行
				self.listWidget_lines.addItem(single_line["line_text"])
				#列出所有行的关联事物
				self.diary_line_concept_list_update()
				#列出所有行的关联文件
				self.diary_line_file_show()

			
			#最后展示md
			self.diary_markdown_view_update()

		else:
			#如果是点到了没有内容的日期，建立临时容器
			self.new_diary={
				"year":self.current_year_index+1970,
				"month":self.current_month_index+1,
				"day":self.current_day,
				"text":[]
			}

			#初始行号设置为-1，这样新增的话就在第一行了
			self.current_line_index=-1
		
		

	def diary_line_show(self):
		
		#标记，已经是自家人了
		self.is_first_arrived=0
		
		self.listWidget_text_linked_file.setEnabled(1)

		#存储当前行号
		self.current_line_index=self.listWidget_lines.currentRow()
		

		#列出当前行
		current_line=self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][self.current_line_index]
		self.plainTextEdit_single_line.setPlainText(current_line["line_text"])
		self.plainTextEdit_single_line.setEnabled(1)

		#列出当前行的关联事物、关联文件
		self.diary_line_concept_list_update()
		self.diary_line_file_show()

	def diary_line_add(self):
		
		self.plainTextEdit_single_line.setEnabled(1)
		self.plainTextEdit_single_line.setFocus()
		
		if self.is_new_diary==0:
			if self.is_first_arrived==0:
				#不是初来乍到的，就先保存上一行的内容
				self.diary_line_edited_and_save()
			else:
				#刚点开一篇日记，就要新增的话，就不用保存之前的一行
				self.is_first_arrived=0
			#清空文本框
			self.plainTextEdit_single_line.clear()
			#行号+1
			self.current_line_index+=1
			#新增文本容器
			self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"].insert(self.current_line_index,
				{
					"index":self.current_line_index,
					"line_text":"",
					"linked_concept":[],
					"linked_file":[]
				}
			)
			#把新的容器添加到
			self.diary_line_edited_and_save()
		else:
			#新日记如果要新增内容，就说明临时容器中应该加上文本信息了，并且要增加到diary_data中
			self.current_line_index+=1
			self.new_diary["text"].append(
				{
					"index":self.current_line_index,
					"line_text":"",
					"linked_concept":[],
					"linked_file":[]
				}
			)
			#这里就去把新日期更新到diary_data中，以及日的重排序的操作
			self.diary_line_edited_and_save()
			#下一次再diary_line_add时，is_new_diary就已经是0了

			#标记，已经是自家人了，下一次再diary_line_add时，就要保存上一行内容了
			self.is_first_arrived=0

	def diary_line_delete(self):
		#初来乍到的，连选中行都没选，不能删除
		if self.is_first_arrived==1:
			return
		
		#支持多行删除
		if [item.row() for item in self.listWidget_lines.selectedIndexes()]!=[]:
			
			dlg = QDialog(self)
			dlg.setWindowTitle("Delete Warning")

			warning_text="确定要删除Lines吗？\n这是无法撤销的操作！\n"
			for line_index in sorted([item.row() for item in self.listWidget_lines.selectedIndexes()]):
				poped_item_line=self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][line_index]
				warning_text+=poped_item_line["line_text"]+"\n"
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
				
				self.plainTextEdit_single_line.clear()

				do=0
				#记录一下删掉的concept的index，万一页面中显示的concept正好就与编辑的文本块有关，那就要更新concept related text
				poped_item_index_list=[]
				for line_index in sorted([item.row() for item in self.listWidget_lines.selectedIndexes()]):
					#selectedIndexes的顺序由点击顺序决定，所以重排序以便从前往后删除
					poped_item_line=self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"].pop(line_index-do)

					for poped_item_index in poped_item_line["linked_concept"]:
						if poped_item_index not in poped_item_index_list:
							poped_item_index_list.append(poped_item_index)
					#每删掉一个，索引时候的下标要往多前减少一个
					do+=1
				
				try:
					#万一页面中显示的concept正好就与编辑的文本块有关，那就要更新concept related text
					item_id=int(self.lineEdit_id.text())
					if item_id in poped_item_index_list:
						#要更新一下concept related text，就用这个好了
						self.concept_show(item_id)
				except:
					pass

				self.diary_line_fix_index()

				self.current_line_index=-1
				

				#这里不用下面的更新法，因为current_line_index不知道会指向哪个，所以只清空就行了
				# self.diary_line_concept_list_update()
				# self.diary_line_file_show()
				self.listWidget_text_related_concept.clear()
				self.listWidget_text_linked_file.clear()

				self.window_title_update()
				self.diary_text_update()
	
	def diary_line_concept_link(self):
		
		if self.is_first_arrived==1:
			QMessageBox.warning(self,"Warning","请选中行后再进行链接！")
			return
		try:
			item_id=int(self.lineEdit_id.text())
			#支持多行同时添加链接物
			#支持过滤已有链接物
			for line_index in [item.row() for item in self.listWidget_lines.selectedIndexes()]:
				if item_id in self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][line_index]["linked_concept"]:
					continue
				else:
					self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][line_index]["linked_concept"].append(item_id)
			#最后呈现出来的还是之前点击进入的行的链接物

			#万一页面中显示的concept正好就与编辑的文本块有关，那就要更新concept related text
			#要更新一下concept related text，就用这个好了
			self.concept_show(item_id)

			#列出当前行的关联事物
			self.diary_line_concept_list_update()
			self.window_title_update()
		except:
			pass
	
	def diary_line_concept_remove(self):
		#初来乍到的，连选中行都没选，删除什么行链接物啊
		if self.is_first_arrived==1:
			QMessageBox.warning(self,"Warning","请选中行后再进行删除！")
			return
		
		dlg = QDialog(self)
		dlg.setWindowTitle("Delete Warning")

		warning_text="确定要删除Line Linked ID吗？\n这是无法撤销的操作！\n"
		for linked_item_index in sorted([item.row() for item in self.listWidget_text_related_concept.selectedIndexes()]):
			poped_item_index=self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][self.current_line_index]["linked_concept"][linked_item_index]
			warning_text+=str(poped_item_index)+"|"+self.concept_data[poped_item_index]["name"]+"\n"
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
			#记录一下删掉的concept的index，万一页面中显示的concept正好就与编辑的文本块有关，那就要更新concept related text
			poped_item_index_list=[]
			for linked_item_index in sorted([item.row() for item in self.listWidget_text_related_concept.selectedIndexes()]):
				poped_item_index=self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][self.current_line_index]["linked_concept"].pop(linked_item_index-do)
				poped_item_index_list.append(poped_item_index)
				#每删掉一个，索引时候的下标要往多前减少一个
				do+=1

			try:
				#记录一下删掉的concept的index，万一页面中显示的concept正好就与编辑的文本块有关，那就要更新concept related text
				item_id=int(self.lineEdit_id.text())
				if item_id in poped_item_index_list:
					#要更新一下concept related text，就用这个好了
					self.concept_show(item_id)
			except:
				pass

			#列出当前行的关联事物
			self.diary_line_concept_list_update()
			self.window_title_update()
		

		
		

	def diary_line_list_drag_update(self):
		#drag and drop是一个一个放入的，而rowsMoved这个信号，如果移动了多行，就在第一个放入的时候触发了，导致只有第一个放入的行被正确重排了
		#所以干脆在多选的时候禁止drag and drop，功能不完善总比有bug好一些

		#下面这个重排还是专门为多行重排设计的，无奈没用了……
		showing_text=self.plainTextEdit_single_line.toPlainText()
		#但还是有缺陷，如果有多个文本内容相同，但链接物不同，移动之后那个位置的文本行的链接物就可能是另一个相同文本的链接物，就有一点乱掉了
		#这种情况在单行移动时也是会发生的！
		#不过，真会有人会无聊到写两行一模一样的东西还添加了不同链接物吗？
		#那只能向作者反馈并多请作者吃好吃的了
		old_text_pool=[]
		new_text_pool=[]

		total=len(self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"])
		for i in range(total):
			old_text_pool.append([i,self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][i]["line_text"]])
			new_text_pool.append([i,self.listWidget_lines.item(i).text()])
		
		while old_text_pool!=[]:
			# if len(old_text_pool)!=len(new_text_pool):
			# 	QMessageBox.critical(self,"Critical Error","程序崩溃！\n重排行1出错！")
			# 	QCoreApplication.exit()

			old_text_index=old_text_pool[0][0]
			old_text=old_text_pool[0][1]


			for i in range((len(new_text_pool))):
				new_text_index=new_text_pool[i][0]
				new_text=new_text_pool[i][1]

				#重定位self.current_line_index
				if showing_text==new_text:
					self.current_line_index=new_text_index
				#重定位每段的index
				if old_text==new_text:
					self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][old_text_index]["index"]=new_text_index
					old_text_pool.pop(0)
					new_text_pool.pop(i)
					break

		# if old_text_pool!=[] or new_text_pool!=[]:
		# 	QMessageBox.critical(self,"Critical Error","程序崩溃！\n重排行2出错！")
		# 	QCoreApplication.exit()

		self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"].sort(key=lambda x:x["index"])

		try:
			#万一页面中显示的concept正好就与编辑的文本块有关，那就要更新concept related text
			#这里就不判断了，每种情况有每种情况的判断，丫的烦死我了
			item_id=int(self.lineEdit_id.text())
			self.concept_show(item_id)
		except:
			pass

		self.diary_text_update()
		self.window_title_update()

	def diary_line_concept_list_update(self):
		if self.is_first_arrived==1 and self.current_line_index==-1:
			#初来乍到一个没有记录的日期，那就走人吧
			return
		if self.is_first_arrived==1 and self.current_line_index!=-1:
			#初来乍到一个已有的日期，列出所有行的关联事物
			self.listWidget_text_related_concept.clear()
			have_shown=[]
			for single_line in self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"]:
				for item_id in single_line["linked_concept"]:
					if item_id not in have_shown:
						have_shown.append(item_id)
						self.listWidget_text_related_concept.addItem(str(item_id)+"|"+self.concept_data[item_id]["name"])
			return
		if self.is_first_arrived==0:
			#已经是老伙计了，只需要列出单行就行了
			self.listWidget_text_related_concept.clear()
			for item_id in self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][self.current_line_index]["linked_concept"]:
				self.listWidget_text_related_concept.addItem(str(item_id)+"|"+self.concept_data[item_id]["name"])

	

	def concept_linked_file_add(self,links):
		"""
		从file library中进来的直接添加到当前日期，（如果带有内部路径，报错！）
		从concept或者tab root或者diary line进来的判断是否为内部文件，
			如果是外部文件那就放到当前日期，
			如果是内部文件，先按照ymd查filedata中有没有，
				如果有就只做链接操作，
				如果没有，那就说明熊孩子在乱搞，明明可以用file check来添加他非得手拖进来，报出警告！
		
		"""
		
		if self.file_saving_base=="":
			QMessageBox.warning(self,"Warning","如果要使用File Library，请先到Setting中设置File Library的基地址。（所有拖进File Library中的文件都会被移动到基地址下）")
			return
		
		#当日路径在不在
		if not os.path.exists(self.file_saving_today_dst):
			os.makedirs(self.file_saving_today_dst)
		else:
			pass
		
		#存不存在当日文件的容器
		try:
			self.file_data[self.y][self.m][self.d]
		except:
			self.file_data[self.y][self.m][self.d]={}

		adding_file=[]

		self.progress=QProgressDialog("Adding File...","Cancel",0,len(links),self)
		self.progress.setWindowTitle("Adding File...")
		self.progress.setWindowModality(Qt.WindowModal)
		# self.progress.setMinimumDuration(0)
		self.progress.setValue(0)
		value=0

		#移动文件到当日路径
		for i in links:
			
			self.progress.setValue(value)
			value+=1
			
			#拥有内部路径吗？
			if self.file_saving_base in i:
				date_and_name=i.replace(self.file_saving_base,"")[1:].split("/")
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
						self.file_data[y][m][d][file_name]

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
						return
				else:
					QMessageBox.warning(self,"Warning","请不要在file_base下乱建文件夹！")
					return

			#没有内部路径，说明是新来的，移动到当日的文件库
			else:
				#如果是新来的link
				if i[:4]=="http" or i[:5]=="https":
					i=i.strip().strip("/")

					#link查重
					if not self.link_check_unique(i):
						continue
					
					result=getTitle(i)
					if result[0]==True:
						title=result[1]
					else:
						title="Unkown Page"
						tray=QSystemTrayIcon()
						tray.setContextMenu(self.qmenu)
						tray.setIcon(QIcon(":/icon/holoico.ico"))
						tray.hide()
						tray.show()
						tray.showMessage("Infomation","获取网页Title失败，请查看网络连接是否正常！\n%s"%i)
					
					file_name=">"+title+"|"+i
					self.file_data[self.y][self.m][self.d][file_name]=[]

					file_icon=which_icon(file_name+".url")

				else:
				
					file_name=os.path.basename(i)
					file_dst=self.file_saving_today_dst+"/"+file_name
					shutil.move(i,file_dst)
					#文件链接concept置空
					self.file_data[self.y][self.m][self.d][file_name]=[]

					file_icon=which_icon(file_name)
				
				adding_file.append(
					{
						"y":self.y,
						"m":self.m,
						"d":self.d,
						"file_name":file_name,
						"file_icon":file_icon
					}
				)
		
		self.progress.setValue(value)
		self.progress.deleteLater()

		#链接concept与文件的信息

		ID=int(self.lineEdit_id.text())

		already_have=self.concept_data[ID]["file"]

		for file in adding_file:
			file_name=file["file_name"]
			y=file["y"]
			m=file["m"]
			d=file["d"]
			if file not in already_have:
				self.concept_data[ID]["file"].append(file)
			if ID not in self.file_data[y][m][d][file_name]:
				self.file_data[y][m][d][file_name].append(ID)
		
		#按照文件名排序
		self.concept_data[ID]["file"].sort(key=lambda x:x["file_name"])

		#更新事物界面
		self.concept_show(ID)
		self.file_library_list_update()

		for tab in self.custom_tabs_shown:
			tab.tab_update()


	def concept_linked_file_open(self):
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
		
		clicked_file_link=self.listWidget_concept_linked_file.currentItem().toolTip()
		
		#如果是link
		if "|" in clicked_file_link:
			clicked_file_link=clicked_file_link.split("|")[-1]
			os.system("start explorer \"%s\""%clicked_file_link)
			return
		
		#Alt双击打开文件所在目录
		if self.listWidget_concept_linked_file.alt_pressed==True:
			self.listWidget_concept_linked_file.alt_pressed=False
			os.startfile(os.path.split(clicked_file_link)[0])
			return
		#########################################################################################
		#########################################################################################
		############################如果按下ctrl双击图片，启动内置的图片浏览器#########################
		clicked_file_name=clicked_file_link.split("/")[-1]
		if which_file_type(clicked_file_name)=="image" and self.listWidget_concept_linked_file.ctrl_pressed==True:
			
			ID=int(self.lineEdit_id.text())

			pic_list=[]

			for file in self.concept_data[ID]["file"]:
				file_link=self.file_saving_base+"/"+str(file["y"])+"/"+str(file["m"])+"/"+str(file["d"])+"/"+file["file_name"]
				file_name=file["file_name"]
				if which_file_type(file_name)=="image":
					pic_list.append(file_link)
		
			clicked_index=pic_list.index(clicked_file_link)

			self.image_viewer=MyImageViewer(pic_list,clicked_index,self.width(),self.height())
			self.image_viewer.show()
			self.listWidget_concept_linked_file.ctrl_pressed=False
		############################如果按下ctrl双击图片，启动内置的图片浏览器#########################
		#########################################################################################
		#########################################################################################
		
		#其他文件启动外部浏览器
		else:
			try:
				os.startfile(clicked_file_link)
			except Exception as e :
				e=str(e).split(":",1)
				QMessageBox.critical(self,"Critical Error","%s\n%s\n请手动设置该类型文件的默认启动应用！"%(e[0],e[1]))


	def concept_linked_file_remove(self):
		
		ID=int(self.lineEdit_id.text())

		dlg = QDialog(self)
		dlg.setWindowTitle("Delete Warning")

		warning_text="确定要删除链接的文件吗？\n这是无法撤销的操作！\n"
		for file_index in sorted([item.row() for item in self.listWidget_concept_linked_file.selectedIndexes()]):
			file=self.concept_data[ID]["file"][file_index]
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
			for file_index in sorted([item.row() for item in self.listWidget_concept_linked_file.selectedIndexes()]):
				#取消file data中对concept的标记
				#del之后列表的长度就变了，索引的下标也要多减一
				file=self.concept_data[ID]["file"][file_index-do]
				file_name=file["file_name"]
				y=file["y"]
				m=file["m"]
				d=file["d"]
				self.file_data[y][m][d][file_name].remove(ID)

				del self.concept_data[ID]["file"][file_index-do]
				do+=1

			#更新事物界面
			self.concept_show(ID)

			for tab in self.custom_tabs_shown:
				tab.tab_update()
			
			#如果没有选中，返回的是-1，这样下标索引会到倒数第一个
			# if file_index!=-1:
				
				####
					#现在所有的文件都在file manager中，所以concept中文件存在与否就与diary没多大关系了
					#
					# file_link=self.concept_data[ID]["file"][file_index]["file_link"]
					#
					# 判断是否有文本块链接到该文件
					# text_list=[]
					# for year_index in range(1970-1970,2170-1970):
					# 	for month_index in range(0,11):
					# 		for day_index in range(len(self.diary_data[year_index]["date"][month_index])):
					# 			for line_index in range(len(self.diary_data[year_index]["date"][month_index][day_index]["text"])):
					# 				for file_index in range(len(self.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["linked_file"])):
										
					# 					linked_file_link=self.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["linked_file"][file_index]["file_link"]
					# 					line_text=self.diary_data[year_index]["date"][month_index][day_index]["text"][line_index]["line_text"]

					# 					if linked_file_link==file_link:
					# 						text_list.append({
					# 							"date":str(year_index+1970)+"."+str(month_index+1)+"."+str(self.diary_data[year_index]["date"][month_index][day_index]["day"]),
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

			


	def concept_related_text_review(self):
		ID=int(self.lineEdit_id.text())
		review=self.listWidget_concept_related_text.currentItem().text().split()
		review_date=review[0].split(".")
		y=int(review_date[0])
		m=int(review_date[1])
		d=int(review_date[2])
		
		self.calendarWidget.setSelectedDate(QDate(y,m,d))
		self.diary_show((y,m,d))

		review_text=review[1]#只取一日内的第一个出来，去最后定位，因为我没法定位多个

		review_text_id=0
		for i in self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"]:
			if review_text in i["line_text"]:
				review_linked_concept_id=i["linked_concept"].index(ID)
				break
			review_text_id+=1
		
		self.listWidget_lines.scrollToItem(self.listWidget_lines.item(review_text_id))
		self.listWidget_lines.item(review_text_id).setSelected(1)


		self.listWidget_text_related_concept.scrollToItem(self.listWidget_text_related_concept.item(review_linked_concept_id))
		self.listWidget_text_related_concept.item(review_linked_concept_id).setSelected(1)

	def diary_line_file_show(self):
		self.listWidget_text_linked_file.clear()
		#刚进来，展示所有的文本块的文件
		if self.is_new_diary==0:
			
			if self.is_first_arrived==1:	
				for line_index in range(len(self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"])):
					for file in self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][line_index]["linked_file"]:
						y=file["y"]
						m=file["m"]
						d=file["d"]
						file_name=file["file_name"]

						#如果是link
						if "|" in file_name:
							#link的tooltip没有直接设置成url网址
							#考虑到几个file listwidget间的拖动操作需要判断link是否已经在file_data中存在，所以需要附带ymd信息
							#这样损失了直接往浏览器拖动打开网页的功能，但双击、回车打开就行了
							file_url=self.file_saving_base+"/"+str(y)+"/"+str(m)+"/"+str(d)+"/"+file_name
							# ">Google|http://www.google.com"
							file_name=file_name[:file_name.rfind("|")][1:]
						else:
							file_url=self.file_saving_base+"/"+str(y)+"/"+str(m)+"/"+str(d)+"/"+file_name
							
						temp=QListWidgetItem()
						temp.setText(file_name)
						temp.setIcon(QIcon(file["file_icon"]))
						temp.setToolTip(file_url)

						self.listWidget_text_linked_file.addItem(temp)
			#只要一行的
			else:
				for file in self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][self.current_line_index]["linked_file"]:
					y=file["y"]
					m=file["m"]
					d=file["d"]
					file_name=file["file_name"]

					#如果是link
					if "|" in file_name:
						#link的tooltip没有直接设置成url网址
						#考虑到几个file listwidget间的拖动操作需要判断link是否已经在file_data中存在，所以需要附带ymd信息
						#这样损失了直接往浏览器拖动打开网页的功能，但双击、回车打开就行了
						file_url=self.file_saving_base+"/"+str(y)+"/"+str(m)+"/"+str(d)+"/"+file_name
						# ">Google|http://www.google.com"
						file_name=file_name[:file_name.rfind("|")][1:]
					else:
						file_url=self.file_saving_base+"/"+str(y)+"/"+str(m)+"/"+str(d)+"/"+file_name
						
					temp=QListWidgetItem()
					temp.setText(file_name)
					temp.setIcon(QIcon(file["file_icon"]))
					temp.setToolTip(file_url)
					
					self.listWidget_text_linked_file.addItem(temp)


	def diary_line_file_link(self,links):
		"""
		从file library中进来的直接添加到当前日期，（如果带有内部路径，报错！）
		从concept或者tab root或者diary line进来的判断是否为内部文件，
			如果是外部文件那就放到当前日期，
			如果是内部文件，先按照ymd查filedata中有没有，
				如果有就只做链接操作，
				如果没有，那就说明熊孩子在乱搞，明明可以用file check来添加他非得手拖进来，报出警告！
		
		"""

		if self.file_saving_base=="":
			QMessageBox.warning(self,"Warning","如果要使用File Library，请先到Setting中设置File Library的基地址。（所有拖进File Library中的文件都会被移动到基地址下）")
			return
		
		#当日路径在不在
		if not os.path.exists(self.file_saving_today_dst):
			os.makedirs(self.file_saving_today_dst)
		else:
			pass
		
		#存不存在当日文件的容器
		try:
			self.file_data[self.y][self.m][self.d]
		except:
			self.file_data[self.y][self.m][self.d]={}

		adding_file=[]

		self.progress=QProgressDialog("Adding File...","Cancel",0,len(links),self)
		self.progress.setWindowTitle("Adding File...")
		self.progress.setWindowModality(Qt.WindowModal)
		# self.progress.setMinimumDuration(0)
		self.progress.setValue(0)
		value=0

		#移动文件到当日路径
		for i in links:

			self.progress.setValue(value)
			value+=1

			#拥有内部路径吗？
			if self.file_saving_base in i:
				date_and_name=i.replace(self.file_saving_base,"")[1:].split("/")
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
						self.file_data[y][m][d][file_name]

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
						return
				else:
					QMessageBox.warning(self,"Warning","请不要在file_base下乱建文件夹！")
					return

			#没有内部路径，说明是新来的，移动到当日的文件库
			else:
				#如果是新来的link
				if i[:4]=="http" or i[:5]=="https":
					i=i.strip().strip("/")

					#link查重
					if not self.link_check_unique(i):
						continue
					
					
					result=getTitle(i)
					if result[0]==True:
						title=result[1]
					else:
						title="Unkown Page"
						tray=QSystemTrayIcon()
						tray.setContextMenu(self.qmenu)
						tray.setIcon(QIcon(":/icon/holoico.ico"))
						tray.hide()
						tray.show()
						tray.showMessage("Infomation","获取网页Title失败，请查看网络连接是否正常！\n%s"%i)
					
					file_name=">"+title+"|"+i
					self.file_data[self.y][self.m][self.d][file_name]=[]

					file_icon=which_icon(file_name+".url")

				else:
				
					file_name=os.path.basename(i)
					file_dst=self.file_saving_today_dst+"/"+file_name
					shutil.move(i,file_dst)
					#文件链接concept置空
					self.file_data[self.y][self.m][self.d][file_name]=[]

					file_icon=which_icon(file_name)
				
				adding_file.append(
					{
						"y":self.y,
						"m":self.m,
						"d":self.d,
						"file_name":file_name,
						"file_icon":file_icon
					}
				)
		
		self.progress.setValue(value)
		self.progress.deleteLater()

		already_have=self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][self.current_line_index]["linked_file"]
		
		#支持多选链接
		for file in adding_file:
			if file not in already_have:
				self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][self.current_line_index]["linked_file"].append(file)

		self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][self.current_line_index]["linked_file"].sort(key=lambda x:x["file_name"])

		self.diary_line_file_show()
		self.window_title_update()
		self.file_library_list_update()

		####
			# for i in links:
			# 	if i[:4]=="http" or i[:5]=="https":
			# 		QMessageBox.warning(self,"Warning","禁止向Diary区导入外部的Link！")
			# 		return
			# 	try:
			# 		#获取file的date信息
			# 		date=list(map(lambda x:int(x),i.split("/")[-4:-1]))
			# 		y=date[0]
			# 		m=date[1]
			# 		d=date[2]
			# 		#检查file
			# 		#如果拥有内部路径
			# 		if self.file_saving_base in i:
			# 			if y in range(1970,2170) or m in range(1,13) or d in range(1,32):
							
			# 				#如果filedata中已经存在，就只做链接操作
			# 				try:
			# 					file_name=os.path.basename(i)
			# 					self.file_data[y][m][d][file_name]

			# 					file_icon=which_icon(file_name)
			# 					adding_file.append(
			# 						{
			# 							"y":y,
			# 							"m":m,
			# 							"d":d,
			# 							"file_name":file_name,
			# 							"file_icon":file_icon
			# 						}
			# 					)
			# 				#如果不存在，那就说明熊孩子在乱搞，从内部路径拖了一个不在filedata中的文件到diary区
			# 				except:
			# 					QMessageBox.warning(self,"Warning","禁止向Diary区导入新文件！")
			# 					return
			# 	except:
			# 		#它连三个/都没有
			# 		QMessageBox.warning(self,"Warning","若要从外部导入文件，请拖到File区！")
			# 		return


	def diary_line_file_open(self):
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
		
		clicked_file_link=self.listWidget_text_linked_file.currentItem().toolTip()

		#如果是link
		if "|" in clicked_file_link:
			clicked_file_link=clicked_file_link.split("|")[-1]
			os.system("start explorer \"%s\""%clicked_file_link)
			return
		
		#Alt双击打开文件所在目录
		if self.listWidget_text_linked_file.alt_pressed==True:
			self.listWidget_text_linked_file.alt_pressed=False
			os.startfile(os.path.split(clicked_file_link)[0])
			return

		#########################################################################################
		#########################################################################################
		############################如果按下ctrl双击图片，启动内置的图片浏览器#########################
		clicked_file_name=clicked_file_link.split("/")[-1]
		if which_file_type(clicked_file_name)=="image" and self.listWidget_text_linked_file.ctrl_pressed==True:

			pic_list=[]

			for file in self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][self.current_line_index]["linked_file"]:
				file_link=self.file_saving_base+"/"+str(file["y"])+"/"+str(file["m"])+"/"+str(file["d"])+"/"+file["file_name"]
				file_name=file["file_name"]
				if which_file_type(file_name)=="image":
					pic_list.append(file_link)
		
			clicked_index=pic_list.index(clicked_file_link)

			self.image_viewer=MyImageViewer(pic_list,clicked_index,self.width(),self.height())
			self.image_viewer.show()
			self.listWidget_text_linked_file.ctrl_pressed=False
		############################如果按下ctrl双击图片，启动内置的图片浏览器#########################
		#########################################################################################
		#########################################################################################
		else:
			try:
				os.startfile(clicked_file_link)
			except Exception as e :
				e=str(e).split(":",1)
				QMessageBox.critical(self,"Critical Error","%s\n%s\n请手动设置该类型文件的默认启动应用！"%(e[0],e[1]))

	def diary_line_file_remove(self):
		if self.is_first_arrived==0:
			dlg = QDialog(self)
			dlg.setWindowTitle("Delete Warning")

			warning_text="确定要删除链接的文件吗？\n这是无法撤销的操作！\n"
			for file_index in sorted([item.row() for item in self.listWidget_text_linked_file.selectedIndexes()]):
				file=self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][self.current_line_index]["linked_file"][file_index]
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
				for file_index in sorted([item.row() for item in self.listWidget_text_linked_file.selectedIndexes()]):
					
					del self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][self.current_line_index]["linked_file"][file_index-do]
					do+=1
					
				self.diary_line_file_show()
				self.window_title_update()	

	

"无框窗口！！！self.setWindowFlags(Qt.CustomizeWindowHint|Qt.FramelessWindowHint)"











if __name__ == "__main__":
	
	setdefaulttimeout(3.0)
	
	# QApplication.setAttribute(Qt.AA_UseOpenGLES)
	# QApplication.setAttribute(Qt.AA_UseSoftwareOpenGL)
	# QApplication.setAttribute(Qt.AA_UseDesktopOpenGL)
	# QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

	# QDesktopServices.openUrl(QUrl("https://doc.qt.io/qt-5/qdesktopservices.html", QUrl.TolerantMode));
	app = QApplication([])
	
	app.setStyle("Fusion")
	app.setPalette(MyDarkPalette())
	window=DongliTeahouseStudio()
	

	
	window.show()
	sys.exit(app.exec_())
