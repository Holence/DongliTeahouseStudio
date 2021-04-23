# -*- coding: utf-8 -*-
from socket import setdefaulttimeout

from custom_function import *
from custom_widget import *
from custom_component import *

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtNetwork import *
from PySide2.QtWebEngineWidgets import *

from dongli_teahouse_studio_window import Ui_dongli_teahouse_studio_window

class DongliTeahouseStudio(QMainWindow,Ui_dongli_teahouse_studio_window):

	def __init__(self,password):
		super().__init__()
		self.setupUi(self)
		self.password=password
		self.user_settings=QSettings("user_settings.ini",QSettings.IniFormat)
		self.qlock=QMutex(QMutex.NonRecursive)
		setdefaulttimeout(3.0)

		#开始跑炫酷的splash screen
		splash_screen=SplashScreen(7,speed=10)
		splash_screen.label_stastus.setText("loading...")

		#1
		#初始化concept、diary、file、rss、zen的数据
		splash_screen.label_description.setText("<strong>Retrieving</strong> Data")
		self.initialize_data()
		splash_screen.progress()

		#2
		#初始化tab
		splash_screen.label_description.setText("<strong>Rendering</strong> Tabs")
		self.initialize_custom_tab()
		splash_screen.progress()

		#3
		#初始化信号
		splash_screen.label_description.setText("<strong>Connecting</strong> Signal")
		self.initialize_signal()
		splash_screen.progress()

		#4
		#初始化system tray
		splash_screen.label_description.setText("<strong>Creating</strong> System Tray Icon")
		self.initialize_tray()
		splash_screen.progress()

		#5
		#初始化自定义menu
		splash_screen.label_description.setText("<strong>Initializing</strong> Context Menu")
		self.initialize_menu()
		splash_screen.progress()

		#6
		#初始化窗体
		splash_screen.label_description.setText("<strong>Buiding</strong> Window")
		#这个一定得放在initialize_window之前，貌似对dock的设置会被其中某个步骤重置掉
		self.initialize_dockwidget()
		#这个得放在initialize_data之前，因为initialize_data中可能弹出file_base的警告窗口，如果不先initialize_window，窗口的风格会是系统原生风格
		self.initialize_window()
		splash_screen.progress()

		#7
		splash_screen.label_description.setText("<strong>Welcome</strong>")
		splash_screen.label_stastus.setText("Done")
		splash_screen.progress()
		splash_screen.progressBar.setValue(splash_screen.progressBar.maximum())

		delay_msecs(800)
		splash_screen.close()

		self.show()

	def initialize_signal(self):
		
		self.btn_stack_home.clicked.connect(lambda:self.stackedWidget.setCurrentIndex(0))
		self.btn_stack_rss.clicked.connect(lambda:self.stackedWidget.setCurrentIndex(1))
		self.btn_stack_diary.clicked.connect(lambda:self.stackedWidget.setCurrentIndex(2))
		self.btn_stack_zen.clicked.connect(lambda:self.stackedWidget.setCurrentIndex(3))
		self.btn_stack_tab.clicked.connect(lambda:self.stackedWidget.setCurrentIndex(4))

		self.label_hello.clicked.connect(self.initialize_random_text)

		#########################################################################################################
		#File
		#导出
		self.actionExport_Concept_Data_to_Json.triggered.connect(lambda:self.center_export("Concept"))
		self.actionExport_Diary_Data_to_Json.triggered.connect(lambda:self.center_export("Diary"))
		self.actionExport_File_Data_to_Json.triggered.connect(lambda:self.center_export("File"))
		self.actionExport_RSS_Data_to_Json.triggered.connect(lambda:self.center_export("RSS"))
		self.actionExport_RSS_Tree_Data_to_Json.triggered.connect(lambda:self.center_export("RSS Tree"))
		self.actionExport_Zen_Data_to_Json.triggered.connect(lambda:self.center_export("Zen"))
		self.actionExport_Zen_Tree_Data_to_Json.triggered.connect(lambda:self.center_export("Zen Tree"))

		#Setting
		self.actionSetting.triggered.connect(self.setting_menu)
		#保存所有数据到外存ctrl+s
		self.actionSave_Data.triggered.connect(self.data_save)
		self.actionData_Security_Check.triggered.connect(self.data_security_check)
		#ctrl+w关闭
		self.actionExit.triggered.connect(self.close)

		#########################################################################################################
		#Tool
		#所有的删除由当时focus的控件决定操作
		self.actionDelete.triggered.connect(self.center_delete)
		#F2编辑文件信息或者RSS信息或Concept related texxt
		self.actionEdit.triggered.connect(self.center_edit)

		#########################################################################################################
		#Concept
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
		#新建事物ctrl+n
		self.actionCreate_Concept.triggered.connect(self.concept_creat)
		#关联列表操作ctrl+123
		self.actionAdd_Concept_To_Parent.triggered.connect(lambda:self.concept_relationship_add("parent"))
		self.actionAdd_Concept_To_Child.triggered.connect(lambda:self.concept_relationship_add("child"))
		self.actionAdd_Concept_To_Relative.triggered.connect(lambda:self.concept_relationship_add("relative"))
		#concept链接文件
		#自定义了MyFileDragAndDropList，实现外部文件的dropin
		self.listWidget_concept_linked_file.dropped.connect(self.concept_linked_file_add)
		self.listWidget_concept_linked_file.itemDoubleClicked.connect(self.concept_linked_file_open)
		#一开始没有展示item了，就禁用file列表
		self.listWidget_concept_linked_file.setEnabled(0)
		#筛选concept对应的diary text
		self.listWidget_concept_related_text.itemDoubleClicked.connect(self.concept_related_text_review)

		#ctrl+q自动锁定搜索框
		self.actionSearch_Concept.triggered.connect(self.concept_search_focus)
		#搜索框按enter自动展示第一个concept
		self.lineEdit_search_concept.returnPressed.connect(lambda: self.concept_show(self.listWidget_search_concept.item(0).text().split("|")[0]) if self.listWidget_search_concept.item(0)!=None else 0)

		####
			#导入文件树
			# self.actionImport_File_Tree_to_Concept.triggered.connect(self.concept_import_file_tree)

		####
			# 现在要拖到外面了，就不限制了
			####icon展示模式会排列混乱，不想让它在内部drag了，设置setDragEnabled(0)，它就不让从外部drop了，真是难伺候
			####侦测在外部还是在内部，改变dragEnable
			#### self.listWidget_concept_linked_file.focusouted.connect(lambda:self.listWidget_concept_linked_file.setDragEnabled(1))
			#### self.listWidget_concept_linked_file.focusined.connect(lambda:self.listWidget_concept_linked_file.setDragEnabled(0))


		#########################################################################################################
		#Diary
		self.calendarWidget.clicked.connect(lambda :self.diary_show(QDate_transform(self.calendarWidget.selectedDate())))
		#新增一行ctrl+d
		self.actionAdd_New_Line.triggered.connect(self.diary_line_add)
		###QPlainTextEdit没有editingFinished信号，就用了自定义的MyPlainTextEdit
		self.plainTextEdit_single_line.editingFinished.connect(self.diary_line_edited_and_save)
		#文本块增加关联concept或文件ctrl+e
		self.actionLink_Concept_to_Line.triggered.connect(self.diary_line_concept_link)
		#点击关联事物列表
		self.listWidget_text_related_concept.itemDoubleClicked.connect(lambda:self.concept_show(self.listWidget_text_related_concept.currentItem().text().split("|")[0]))
		#点击行显示文本
		self.listWidget_lines.itemClicked.connect(self.diary_line_show)
		#拖动行重排
		self.listWidget_lines.model().rowsMoved.connect(self.diary_line_list_drag_update)
		#text链接文件
		self.listWidget_text_linked_file.dropped.connect(self.diary_line_file_link)
		self.listWidget_text_linked_file.itemDoubleClicked.connect(self.diary_line_file_open)
		#Diary text search
		self.actionSearch_Diary_Text.triggered.connect(self.diary_text_search)
		#Diary分析
		self.actionAnalyze_Diary_with_Concept.triggered.connect(self.diary_analyze)
		#I'm Feeling Lucky
		self.actionI_m_Feeling_Lucky.triggered.connect(self.diary_random_date)

		# self.listWidget_lines.右键点击

		#########################################################################################################
		#File Library
		#file manager文件
		self.listWidget_search_file.dropped.connect(self.file_library_file_add)
		self.listWidget_search_file.itemDoubleClicked.connect(self.file_library_file_open)
		self.listWidget_search_file.enter_pressed.connect(self.file_library_file_open)
		#点击展示信息
		self.listWidget_search_file.itemClicked.connect(self.file_library_file_info_show)
		#file manager指针上下移动，即刻展示信息
		self.listWidget_search_file.currentItemChanged.connect(self.file_library_file_info_show)

		#文件搜索
		# self.lineEdit_search_file.textEdited.connect(self.file_library_list_update)
		self.lineEdit_search_file.returnPressed.connect(self.file_library_list_update)
		self.lineEdit_search_file.returnPressed.connect(self.file_library_list_focus)
		#文件链接concept的列表
		self.listWidget_file_related_concept.itemDoubleClicked.connect(lambda:self.concept_show(self.listWidget_file_related_concept.currentItem().text().split("|")[0]))
		#运行File Ckeck
		self.actionFile_Check.triggered.connect(self.file_check)
		#ctrl+q搜索文件
		self.actionSearch_File_Library.triggered.connect(self.file_library_search_focus)
		#在Library中定位选中的文件
		self.actionLocate.triggered.connect(self.center_locate)

		#########################################################################################################
		#RSS
		self.actionCreate_RSS_Folder.triggered.connect(self.rss_feed_folder_create)
		self.actionAdd_RSS_Feed.triggered.connect(self.rss_feed_add)
		self.actionOpen_WebPage_In_Browser.triggered.connect(self.rss_open_webpage)
		#点击treeitem，show文章列表
		self.treeWidget_rss.itemClicked.connect(self.rss_feed_article_list_show)
		#每次拖动排阶级后，就检查，RSS不能作为folder
		self.treeWidget_rss.dropped.connect(self.rss_tree_drop_update)
		#点击文章
		self.listWidget_rss.itemClicked.connect(self.rss_feed_article_show)
		#手动更新RSS
		self.actionUpdate_Feed_Manually.triggered.connect(self.rss_feed_manually_update)
		#rss搜索
		self.lineEdit_rss_search.returnPressed.connect(self.rss_tree_build)
		#手动每日更新
		self.actionStart_Daily_Update_Manually.triggered.connect(lambda:self.rss_feed_daily_update(manually=True))
		#地址栏回车键
		self.lineEdit_browser.returnPressed.connect(self.rss_browser_goto_url)

		#########################################################################################################
		#Zen
		self.actionCreate_Zen_Folder.triggered.connect(self.zen_folder_create)
		self.actionAdd_Zen_Segment.triggered.connect(self.zen_segment_add)
		self.actionSwitch_between_View_Edit.triggered.connect(self.zen_switch_mode)
		
		#zen搜索
		self.lineEdit_zen_search.textEdited.connect(self.zen_tree_build)
		
		#每次拖动排阶级后，就检查，
		self.treeWidget_zen.dropped.connect(self.zen_tree_drop_update)

		self.treeWidget_zen.itemDoubleClicked.connect(self.zen_segment_show)

		self.plainTextEdit_zen.editingFinished.connect(self.zen_segment_save)

		self.pushButton_sublime.clicked.connect(self.zen_open_sublime)
		self.pushButton_typora.clicked.connect(self.zen_open_typora)
		
		#QPlainTextEdit没有textEdited，自制的MyPlainTextEdit侦测keypress放出edited信号
		self.plainTextEdit_zen.edited.connect(self.zen_text_search_or_count)
		self.lineEdit_zen_text_search.textEdited.connect(self.zen_text_search_or_count)
		self.lineEdit_zen_text_search.returnPressed.connect(self.zen_text_search_or_count)

		#########################################################################################################
		#Tab
		self.actionCreate_New_Tab.triggered.connect(self.tab_custom_create)
		self.actionHide_Current_Tab.triggered.connect(self.tab_custom_hide)
		self.actionDelete_Current_Tab.triggered.connect(self.tab_custom_delete)

		#其他地方改变了并不是实时更新所有的tab，只有当正在tab页时去更新正在显示的那个tab，所以每次点进来时候就要更新正在显示的那个
		self.tabWidget.currentChanged.connect(self.tab_refresh_current_tab)
		self.btn_stack_tab.clicked.connect(self.tab_refresh_current_tab)


		#########################################################################################################
		#View
		#f11全屏
		self.actionToggle_Fullscreen.triggered.connect(self.window_toggle_fullscreen)
		#置顶Action
		self.actionStay_on_Top.triggered.connect(self.window_toggle_stay_on_top)

		self.actionRestore_Main_Window.triggered.connect(self.showNormal)
		self.actionHide_Main_Window.triggered.connect(self.hide)
		self.actionRestore_to_Normal_Size.triggered.connect(self.window_restore_normal_size)
		#牛逼疯了！我要的就是这个！
		#如果是点窗口右上角的的最小化，调用的是self.showMinimized
		#这会把所有归属于mainwindow的窗口都最小化，我的漂浮dockwidget就没了
		#
		#而如果用的是hide，那只会把mainwindow隐藏掉，我的漂浮dockwidget就一直在那里！

		#添加view设置
		self.actionToggleConcept=self.dockWidget_concept.toggleViewAction()
		self.actionToggleConcept.setIcon(QIcon(":/icon/database.svg"))
		self.actionToggleConcept.setShortcut(QKeySequence(Qt.Key_F5))
		self.menuView.addAction(self.actionToggleConcept)

		self.actionToggleDiary=self.dockWidget_diary.toggleViewAction()
		self.actionToggleDiary.setShortcut(QKeySequence(Qt.Key_F6))
		self.actionToggleDiary.setIcon(QIcon(":/icon/feather.svg"))
		self.menuView.addAction(self.actionToggleDiary)

		self.actionToggleLibrary=self.dockWidget_library.toggleViewAction()
		self.actionToggleLibrary.setShortcut(QKeySequence(Qt.Key_F7))
		self.actionToggleLibrary.setIcon(QIcon(":/icon/hard-drive.svg"))
		self.menuView.addAction(self.actionToggleLibrary)

		self.actionToggleSticker=self.dockWidget_sticker.toggleViewAction()
		self.actionToggleSticker.setShortcut(QKeySequence(Qt.Key_F8))
		self.actionToggleSticker.setIcon(QIcon(":/icon/coffee.svg"))
		self.menuView.addAction(self.actionToggleSticker)

		#########################################################################################################
		#Help
		#about界面
		self.actionAbout.triggered.connect(self.about)

	def initialize_dockwidget(self):
		def dock_change_location(dockWidget):
			if dockWidget==self.dockWidget_concept:
				if self.dockWidget_concept.isFloating():
					self.frame_sizegrip_concept.show()
					self.pushButton_concept_close.show()
				else:
					self.frame_sizegrip_concept.hide()
					self.pushButton_concept_close.hide()
			if dockWidget==self.dockWidget_diary:
				if self.dockWidget_diary.isFloating():
					self.frame_sizegrip_diary.show()
					self.pushButton_diary_close.show()
				else:
					self.frame_sizegrip_diary.hide()
					self.pushButton_diary_close.hide()
			if dockWidget==self.dockWidget_library:
				if self.dockWidget_library.isFloating():
					self.frame_sizegrip_library.show()
					self.pushButton_library_close.show()
				else:
					self.frame_sizegrip_library.hide()
					self.pushButton_library_close.hide()
			if dockWidget==self.dockWidget_sticker:
				if self.dockWidget_sticker.isFloating():
					self.frame_sizegrip_sticker.show()
					self.pushButton_sticker_close.show()
				else:
					self.frame_sizegrip_sticker.hide()
					self.pushButton_sticker_close.hide()
		

		self.dockWidget_concept.setTitleBarWidget(self.verticalWidget_titlebar_concept)
		self.pushButton_concept_close.clicked.connect(lambda:self.dockWidget_concept.hide())
		QSizeGrip(self.frame_sizegrip_concept)
		
		self.dockWidget_concept.dockLocationChanged.connect(lambda:dock_change_location(self.dockWidget_concept))
		if self.dockWidget_concept.isFloating():
			self.frame_sizegrip_concept.show()
		else:
			self.frame_sizegrip_concept.hide()


		self.dockWidget_diary.setTitleBarWidget(self.verticalWidget_titlebar_diary)
		self.pushButton_diary_close.clicked.connect(lambda:self.dockWidget_diary.hide())
		QSizeGrip(self.frame_sizegrip_diary)

		self.dockWidget_diary.dockLocationChanged.connect(lambda:dock_change_location(self.dockWidget_diary))
		if self.dockWidget_diary.isFloating():
			self.frame_sizegrip_diary.show()
		else:
			self.frame_sizegrip_diary.hide()
		
		self.dockWidget_library.setTitleBarWidget(self.verticalWidget_titlebar_library)
		self.pushButton_library_close.clicked.connect(lambda:self.dockWidget_library.hide())
		QSizeGrip(self.frame_sizegrip_library)

		self.dockWidget_library.dockLocationChanged.connect(lambda:dock_change_location(self.dockWidget_library))
		if self.dockWidget_library.isFloating():
			self.frame_sizegrip_library.show()
		else:
			self.frame_sizegrip_library.hide()

		self.dockWidget_sticker.setTitleBarWidget(self.verticalWidget_titlebar_sticker)
		self.pushButton_sticker_close.clicked.connect(lambda:self.dockWidget_sticker.hide())
		QSizeGrip(self.frame_sizegrip_sticker)

		self.dockWidget_sticker.dockLocationChanged.connect(lambda:dock_change_location(self.dockWidget_sticker))
		if self.dockWidget_sticker.isFloating():
			self.frame_sizegrip_sticker.show()
		else:
			self.frame_sizegrip_sticker.hide()

	def initialize_window(self):

		#设置拖动坐标和控件
		self.label_title_bar_top.set_drag_papa(self)

		#无边框
		self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.CustomizeWindowHint)
		
		#右上角的三个按钮
		self.btn_minimize.clicked.connect(self.showMinimized)
		self.btn_maximize.clicked.connect(self.window_toggle_maximun)
		self.btn_close.clicked.connect(self.close)

		if self.isFullScreen():
			self.btn_maximize.hide()
			self.btn_minimize.hide()
		
		self.browser=QWebEngineView()
		self.browser.settings().setAttribute(QWebEngineSettings.PluginsEnabled,True)
		self.browser.settings().setAttribute(QWebEngineSettings.JavascriptEnabled,True)
		self.browser.settings().setAttribute(QWebEngineSettings.AllowWindowActivationFromJavaScript,True)
		self.browser.settings().setAttribute(QWebEngineSettings.WebGLEnabled,True)
		self.browser.settings().setAttribute(QWebEngineSettings.ScrollAnimatorEnabled,True)
		self.browser.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled,True)
		self.browser.settings().setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled,True)
		self.browser.settings().setAttribute(QWebEngineSettings.AllowRunningInsecureContent,True)
		self.verticalLayout_browser.addWidget(self.browser)

		#恢复界面设置
		try:
			self.restoreGeometry(self.user_settings.value("geometry"))
			self.restoreState(self.user_settings.value("windowState"))
			self.resize(self.user_settings.value("size"))
			self.move(self.user_settings.value("pos"))
			self.splitter_rss.restoreState(self.user_settings.value("splitter_rss"))
			self.splitter_zen.restoreState(self.user_settings.value("splitter_zen"))
		except:
			pass
		
		try:
			font=self.user_settings.value("font")
			font_size=self.user_settings.value("font_size")
			self.font_set(font,font_size)
		except:
			pass
		
		try:
			sticker_text=decrypt(self.user_settings.value("sticker"))
			self.plainTextEdit_sticker.setPlainText(sticker_text)
		except:
			pass
		
		self.initialize_random_text()

		# settings_list=self.user_settings.allKeys()
		# print(settings_list)
		
		# self.setWindowOpacity(0.95)
		# self.shadow = QGraphicsDropShadowEffect(self)
		# self.shadow.setBlurRadius(17)
		# self.shadow.setXOffset(0)
		# self.shadow.setYOffset(0)
		# self.shadow.setColor(QColor(0, 0, 0, 150))
		# self.dockWidget_concept.setGraphicsEffect(self.shadow)

		# QCoreApplication.setApplicationName("Teahouse Studio")
		# QCoreApplication.setOrganizationName("Dongli Teahouse")
	
	def initialize_random_text(self):
		try:
			self.label_hello.setMaximumWidth(int(self.stackedWidget.width())*0.75)
			random_text_directory=decrypt(self.user_settings.value("random_text_directory"))
			
			with open(random_text_directory,"r",encoding="utf-8") as f:
				text=f.read()
			
			text_list=text.split("\n\n")
			# name=random_text_directory.split("/")[-1]
			# name="《"+name[:name.rfind(".")]+"》"

			random_text=text_list[randint(0,len(text_list))].replace("\n","\n\n")
			self.label_hello.setText(random_text)

			#如果成功的话再改字体，否则保持原来的Segoe UI
			font=self.user_settings.value("font")
			self.label_hello.setFont(font)
		except:
			pass
	
	def initialize_data(self):
		#初始化diary、concept、file、rss的data
		if self.data_validity_check()==1:
			self.data_load()
			
			#####################################################################################################################
			self.easter_egg_deleting_universe=0
			
			self.concept_search_list_update()

			#####################################################################################################################
			self.current_year_index=0
			self.current_month_index=0
			self.current_day_index=0
			self.current_day=0#记录这个，用来找那些不存在当前日的，重排序后的index
			self.is_new_diary=0#标记新日记，增添容器、新建新日记时要用
			self.is_first_arrived=0#增添、删除、列出链接物的时候要用
			self.new_diary={}#临时存储还没重排序找到day索引值的新日记
			self.current_line_index=0

			self.diary_show(QDate_transform(self.calendarWidget.selectedDate()))

			#####################################################################################################################

			ymd=time.localtime(time.time())
			self.y=ymd[0]
			self.m=ymd[1]
			self.d=ymd[2]
			#当日存文件的地方
			self.file_saving_today_dst=self.file_saving_base+"/"+str(self.y)+"/"+str(self.m)+"/"+str(self.d)
			self.searching_file=[]
			self.file_saving_today_dst_exist=False
			
			# 这个不着急，在shutil.move之前做检查就行了
			# self.file_saving_today_dst_exist_check()
			if not os.path.exists("./cache"):
				os.makedirs("./cache")

			self.file_library_list_update(starting=True)

			#####################################################################################################################

			self.current_rss_showing=None#如果点开的是rss，那么放的是rss_url；如果点开的是folder，那么存所有文章结构体的列表，
			self.manually_updateing=False

			self.rss_tree_build()
			self.rss_feed_daily_update()

			#####################################################################################################################
			
			self.zen_tree_build()
			
			#####################################################################################################################
		else:
			self.close()

	def initialize_custom_tab(self):
		#custom_tabs_shown存储正在界面上展示的tabs，这些是用来实时与concept data同步更新的
		self.custom_tabs_shown=[]

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

					####
						#tab页有自己的concept编辑区啦
						#这里的tab应该算是一个指针，可以在这里链上一些槽
						#点击内部的leaf，回传到这里，去显示concept
						# tab.clicked.connect(lambda ID:self.concept_show(ID))
					
					#一开始不让操作
					tab.listWidget_file_root.setEnabled(0)
					tab.listWidget_file_leafs.setEnabled(0)

					#正在界面上展示的tabs，这些是用来实时与concept data同步更新的
					self.custom_tabs_shown.append(tab)

					self.tabWidget.addTab(tab,QIcon(":/icon/trello.svg"),custom_tab[0])
				
				#把隐藏了的tab，放在tab menu的action里面
				else:
					
					action=QAction(custom_tab[0],self)
					action.setIcon(QIcon(":/icon/trello.svg"))
					action.triggered.connect(partial(self.tab_custom_resurrection,index,action))
					self.menuTab.addAction(action)
					
				index+=1
		
		except:#第一次进来，初始化custom_tab_data
			self.custom_tab_data=[]
		
		#Home页
		self.tabWidget.setCurrentIndex(0)

	def initialize_tray(self):
		self.trayIconMenu=QMenu(self)

		self.trayIcon=QSystemTrayIcon(self)
		self.trayIcon.setIcon(QIcon(":/icon/holoico_trans.ico"))
		
		#################################################################

		self.trayIconMenu.addAction(self.actionSetting)
		self.trayIconMenu.addSeparator()
		self.trayIconMenu.addAction(self.actionToggleConcept)
		self.trayIconMenu.addAction(self.actionToggleDiary)
		self.trayIconMenu.addAction(self.actionToggleLibrary)
		self.trayIconMenu.addAction(self.actionToggleSticker)
		self.trayIconMenu.addSeparator()
		self.trayIconMenu.addAction(self.actionToggle_Fullscreen)
		self.trayIconMenu.addAction(self.actionHide_Main_Window)
		self.trayIconMenu.addAction(self.actionRestore_Main_Window)
		self.trayIconMenu.addAction(self.actionRestore_to_Normal_Size)
		self.trayIconMenu.addAction(self.actionStay_on_Top)
		self.trayIconMenu.addSeparator()
		self.trayIconMenu.addAction(self.actionExit)

		self.trayIcon.setContextMenu(self.trayIconMenu)
		self.trayIcon.show()

	def initialize_menu(self):
		
		def show_context_menu_beneath(menu,btn):
			btn_pos=btn.pos()
			icon_height=btn.width()
			btn_pos+=QPoint(0,icon_height)
			true_pos=btn.parentWidget().mapToGlobal(btn_pos)
			menu.exec_(true_pos)
		
		def show_context_menu_right(menu,btn):
			btn_pos=btn.pos()
			icon_height=btn.width()
			btn_pos+=QPoint(icon_height,0)
			true_pos=btn.parentWidget().mapToGlobal(btn_pos)
			menu.exec_(true_pos)
		
		def generate_WholeMenu():
			"生成全总Menu，并且给Mainwindow添加所有的快捷键（ self.addAction(action)"
			WholeMenu=QMenu(self)

			self.menuFile.addMenu(self.menuExport)
			
			#五个分tool menu放到总tool menu中
			for menu in [self.menuConcept,self.menuDiary,self.menuLibrary,self.menuRSS,self.menuZen,self.menuTab]:
				self.menuTool.insertMenu(self.actionEdit,menu)
				for action in menu.actions():
					self.addAction(action)
			
			menu_list=[self.menuFile,self.menuTool,self.menuView,self.menuHelp]
			for menu in menu_list:
				WholeMenu.addMenu(menu)
				for action in menu.actions():
					self.addAction(action)
			
			for action in self.menuOther.actions():
				WholeMenu.addAction(action)
				self.addAction(action)
			
			return WholeMenu
		
		def generate_ConceptMenu():
			ConceptMenu=QMenu(self)
			for action in self.menuConcept.actions():
					ConceptMenu.addAction(action)
			return ConceptMenu
		
		def generate_DiaryMenu():
			DiaryMenu=QMenu(self)
			for action in self.menuDiary.actions():
					DiaryMenu.addAction(action)
			return DiaryMenu
		
		def generate_LibraryMenu():
			LibraryMenu=QMenu(self)
			for action in self.menuLibrary.actions():
					LibraryMenu.addAction(action)
			return LibraryMenu
		
		def generate_RSSMenu():
			RSSMenu=QMenu(self)
			for action in self.menuRSS.actions():
					RSSMenu.addAction(action)
			return RSSMenu
		
		def generate_ZenMenu():
			ZenMenu=QMenu(self)
			for action in self.menuZen.actions():
					ZenMenu.addAction(action)
			return ZenMenu
		
		def generate_TabMenu():
			TabMenu=QMenu(self)
			for action in self.menuTab.actions():
					TabMenu.addAction(action)
			return TabMenu

		#自带的隐藏掉
		self.menubar.setVisible(False)

		
		#点击title icon和下面的三个点展示WholeMenu
		WholeMenu=generate_WholeMenu()
		ConceptMenu=generate_ConceptMenu()
		DiaryMenu=generate_DiaryMenu()
		LibraryMenu=generate_LibraryMenu()
		RSSMenu=generate_RSSMenu()
		ZenMenu=generate_ZenMenu()
		#这个得是全局变量，因为Tab的恢复和建立是动态的，所以也会在其他地方被动态修改
		self.TabMenu=generate_TabMenu()

		self.btn_menu.clicked.connect(lambda:show_context_menu_beneath(WholeMenu,self.btn_menu))

		#
		self.btn_stack_rss.rightclicked.connect(lambda:show_context_menu_right(RSSMenu,self.btn_stack_rss))
		self.btn_stack_diary.rightclicked.connect(lambda:show_context_menu_right(DiaryMenu,self.btn_stack_diary))
		self.btn_stack_zen.rightclicked.connect(lambda:show_context_menu_right(ZenMenu,self.btn_stack_zen))
		self.btn_stack_tab.rightclicked.connect(lambda:show_context_menu_right(self.TabMenu,self.btn_stack_tab))
		self.btn_stack_menu.clicked.connect(lambda:show_context_menu_right(WholeMenu,self.btn_stack_menu))

		#
		self.label_concept_icon.clicked.connect(lambda:show_context_menu_right(ConceptMenu,self.label_concept_icon))
		self.label_diary_icon.clicked.connect(lambda:show_context_menu_right(DiaryMenu,self.label_diary_icon))
		self.label_library_icon.clicked.connect(lambda:show_context_menu_right(LibraryMenu,self.label_library_icon))

	def closeEvent(self,event):
		super(DongliTeahouseStudio,self).closeEvent(event)
		
		self.hide()
		
		#开始跑炫酷的splash screen
		splash_screen=SplashScreen(4,speed=5)
		splash_screen.label_stastus.setText("closing...")

		#1
		#Kill RSS的线程
		splash_screen.label_description.setText("<strong>Killing</strong> RSS Thread")
		try:
			self.daily_update_thread.need_to_quit=True

			if not self.daily_update_thread.wait(1.0):
				self.daily_update_thread.terminate()
				self.daily_update_thread.wait()
			
			del self.daily_update_thread
		except:
			pass
		
		try:
			self.manually_update_thread.need_to_quit=True

			if not self.manually_update_thread.wait(1.0):
				self.manually_update_thread.terminate()
				self.manually_update_thread.wait()
			
			del self.manually_update_thread
		except:
			pass
		
		try:
			self.adding_feed_thread.need_to_quit=True
			
			if not self.adding_feed_thread.wait(1.0):
				self.adding_feed_thread.terminate()
				self.adding_feed_thread.wait(1.0)
			
			del self.adding_feed_thread
		except:
			pass
		splash_screen.progress()

		#2
		#保存所有数据
		splash_screen.label_description.setText("<strong>Saving</strong> Data")
		self.data_save()
		splash_screen.progress()

		#3
		#保存界面设置
		splash_screen.label_description.setText("<strong>Saving</strong> Window Data")
		self.user_settings.setValue("geometry",self.saveGeometry())
		self.user_settings.setValue("windowState",self.saveState())
		self.user_settings.setValue("size",self.size())
		self.user_settings.setValue("pos",self.pos())
		self.user_settings.setValue("splitter_rss",self.splitter_rss.saveState())
		self.user_settings.setValue("splitter_zen",self.splitter_zen.saveState())
		self.user_settings.setValue("custom_tab_data",encrypt(self.custom_tab_data))
		splash_screen.progress()

		#4
		splash_screen.label_description.setText("<strong>Have a Nice Day~</strong>")
		splash_screen.label_stastus.setText("Done")
		splash_screen.progress()
		splash_screen.progressBar.setValue(splash_screen.progressBar.maximum())


		delay_msecs(800)
		splash_screen.close()


		####
			#全部自动保存
			#保存未保存的内容
			# if self.windowTitle()=="Dongli Teahouse Studio *Unsaved Change*":
			# 	dlg = QMessageBox(self)
			# 	dlg.setWindowTitle("Unsaved Change")
			# 	dlg.setText("Diary的内容未保存，需要保存吗？")
			# 	dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No |QMessageBox.Cancel)
			# 	dlg.setIcon(QMessageBox.Warning)
			# 	button = dlg.exec_()

			# 	if button == QMessageBox.Yes:
			# 		event.accept()
			# 		self.diary_data_save_out()
			# 	elif button == QMessageBox.Cancel:
			# 		event.ignore()
			# 	elif button == QMessageBox.No:
			# 		event.accept()

	def zen_folder_create(self):
		if self.lineEdit_zen_search.text()!="":
			QMessageBox.warning(self,"Warning","请清空Zen搜索条件！")
			return
		
		dlg = QDialog(self)
		dlg.setWindowTitle("Create New Zen Folder")

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
			for i in self.zen_tree_data:
				if type(i)==dict:
					alreay_have.append(i["folder_name"])
			
			if folder_name not in alreay_have:

				#哈哈哈哈，隐藏了header后，它只显示第一个column，这样就可以在后面添加附属信息了！
				#这样就可以不用每时每刻记录Zen data，每时每刻修改Zen data
				#只用在最后遍历整棵树，存储Zen树就行了！
				temp=QTreeWidgetItem([folder_name,"Folder"])
				temp.setIcon(0,QIcon(":/icon/folder.svg"))

				self.treeWidget_zen.addTopLevelItem(temp)

				self.zen_tree_data_update()
			else:
				QMessageBox.warning(self,"Warning","Zen文件夹不能重名！")
				return
		else:
			return
	
	def zen_segment_add(self):
		if self.lineEdit_zen_search.text()!="":
			QMessageBox.warning(self,"Warning","请清空Zen搜索条件！")
			return
		
		dlg = QDialog(self)
		dlg.setWindowTitle("Create New Zen Segment")

		name_label=QLabel("Segment Name:")
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
			segment_name=name_enter.text()
			
			#segment不能重名
			alreay_have=self.zen_data.keys()
			
			if segment_name not in alreay_have:

				#哈哈哈哈，隐藏了header后，它只显示第一个column，这样就可以在后面添加附属信息了！
				#这样就可以不用每时每刻记录Zen data，每时每刻修改Zen data
				#只用在最后遍历整棵树，存储Zen树就行了！
				temp=QTreeWidgetItem([segment_name,"Segment"])
				temp.setIcon(0,QIcon(":/icon/feather.svg"))

				self.treeWidget_zen.addTopLevelItem(temp)
				self.zen_data[segment_name]=""

				self.zen_tree_data_update()
			else:
				QMessageBox.warning(self,"Warning","Segment不能重名！")
				return
		else:
			return
	
	def zen_tree_build(self):
		# 根据zen_tree_data的层级结构，建树
		tree_expand={}
		root=self.treeWidget_zen.invisibleRootItem()
		for index in range(root.childCount()):
			#如果是folder，就记录一下expand属性
			if root.child(index).text(2)=="":
				folder_name=root.child(index).text(0)
				tree_expand[folder_name]=root.child(index).isExpanded()
		
		self.treeWidget_zen.clear()
		
		zen_searching=self.lineEdit_zen_search.text()

		#默认搜Feed name
		if zen_searching!="":
			
			#反正在搜索模式下拖动排序也是没用的
			#（因为搜索模式下的zen_tree_data_update要先清空搜索，再zen_tree_build出完整的tree，侦测tree中的从属关系，最后在恢复原有搜索）
			#所以这里干脆禁止拖动
			self.treeWidget_zen.setDragEnabled(0)
			self.treeWidget_zen.setDragDropMode(QAbstractItemView.NoDragDrop)

			#搜文件夹
			if zen_searching[:3]=="f: " or zen_searching[:3]=="F: ":
				search_name=zen_searching[3:].lower()
				for top_level in self.zen_tree_data:
					if type(top_level)==dict and ( search_name in top_level["folder_name"] or search_name in convert_to_az(top_level["folder_name"]) ):
						
						folder_name=top_level["folder_name"]

						temp_root=QTreeWidgetItem([folder_name,"Folder"])
						temp_root.setIcon(0,QIcon(":/icon/folder.svg"))
						temp_root.setText(0,folder_name)
						self.treeWidget_zen.addTopLevelItem(temp_root)

						for segment_name in top_level["Segment"]:
							
							temp=QTreeWidgetItem(temp_root,[segment_name,"Segment"])
							temp.setIcon(0,QIcon(":/icon/feather.svg"))

						try:
							temp_root.setExpanded(tree_expand[folder_name])
						except:
							pass

			#搜text 内容
			elif zen_searching[:3]=="t: " or zen_searching[:3]=="T: ":
				search_name=zen_searching[3:]
				for top_level in self.zen_tree_data:
					#top_level放了folder
					if type(top_level)==dict:
						
						folder_name=top_level["folder_name"]

						temp_root=QTreeWidgetItem([folder_name,"Folder",""])
						temp_root.setIcon(0,QIcon(":/icon/folder.svg"))
						temp_root.setText(0,folder_name)

						has=False
						
						for segment_name in top_level["Segment"]:

							if search_name in self.zen_data[segment_name] or search_name in convert_to_az(self.zen_data[segment_name]):
								has=True
								
								temp=QTreeWidgetItem(temp_root,[segment_name,"Segment"])
								temp.setIcon(0,QIcon(":/icon/feather.svg"))
						
						if has==True:
							self.treeWidget_zen.addTopLevelItem(temp_root)

							try:
								temp_root.setExpanded(tree_expand[folder_name])
							except:
								pass
					
					#top_level放了segment
					else:
						segment_name=top_level

						if search_name in self.zen_data[segment_name] or search_name in convert_to_az(self.zen_data[segment_name]):
							
							temp=QTreeWidgetItem([segment_name,"Segment"])
							temp.setIcon(0,QIcon(":/icon/feather.svg"))

							self.treeWidget_zen.addTopLevelItem(temp)

			#默认搜feed name
			else:
				search_name=zen_searching.lower()
				for top_level in self.zen_tree_data:
					#top_level放了folder
					if type(top_level)==dict:
						
						folder_name=top_level["folder_name"]

						temp_root=QTreeWidgetItem([folder_name,"Folder",""])
						temp_root.setIcon(0,QIcon(":/icon/folder.svg"))
						temp_root.setText(0,folder_name)

						has=False
						
						for segment_name in top_level["Segment"]:

							if search_name in segment_name or search_name in convert_to_az(segment_name):
								has=True
								
								temp=QTreeWidgetItem(temp_root,[segment_name,"Segment"])
								temp.setIcon(0,QIcon(":/icon/feather.svg"))
						
						if has==True:
							self.treeWidget_zen.addTopLevelItem(temp_root)

							try:
								temp_root.setExpanded(tree_expand[folder_name])
							except:
								pass
					
					#top_level放了segment
					else:
						segment_name=top_level

						if search_name in segment_name or search_name in convert_to_az(segment_name):

							temp=QTreeWidgetItem([segment_name,"Segment"])
							temp.setIcon(0,QIcon(":/icon/feather.svg"))

							self.treeWidget_zen.addTopLevelItem(temp)
		
		#搜索为空，展示全部
		else:

			self.treeWidget_zen.setDragEnabled(1)
			self.treeWidget_zen.setDragDropMode(QAbstractItemView.InternalMove)

			for top_level in self.zen_tree_data:
				#top_level放了folder
				if type(top_level)==dict:
					folder_name=top_level["folder_name"]
					
					temp_root=QTreeWidgetItem([folder_name,"Folder",""])
					temp_root.setIcon(0,QIcon(":/icon/folder.svg"))
					temp_root.setText(0,folder_name)
					self.treeWidget_zen.addTopLevelItem(temp_root)

					for segment_name in top_level["Segment"]:
						
						temp=QTreeWidgetItem(temp_root,[segment_name,"Segment"])
						temp.setIcon(0,QIcon(":/icon/feather.svg"))

					try:
						temp_root.setExpanded(tree_expand[folder_name])
					except:
						pass
				
				#top_level放了segment
				else:
					segment_name=top_level

					temp=QTreeWidgetItem([segment_name,"Segment"])
					temp.setIcon(0,QIcon(":/icon/feather.svg"))

					self.treeWidget_zen.addTopLevelItem(temp)
	
	def zen_tree_data_update(self):
		# 根据树的结构，重塑zen_tree_data
		def deepin(root,pointer):
			for index in range(root.childCount()):
				
				#如果是segment
				if root.child(index).text(1)=="Segment":
					segment_name=root.child(index).text(0)
					
					pointer.append(segment_name)
					continue
				
				#如果是Folder
				else:
					folder_name=root.child(index).text(0)
					folder={
						"folder_name":folder_name,
						"Segment":[]
					}
					pointer.append(folder)
					
					#传入这个folder中的zen列表的pointer
					deepin(root.child(index),folder["Segment"])
		

		#这里更新zen_tree_data用的是遍历树侦测结构的方法，所以如果在搜索模式中，要先清除搜索，还原树
		zen_searching=self.lineEdit_zen_search.text()
		if zen_searching!="":
			self.lineEdit_zen_search.setText("")
			self.zen_tree_build()


		self.zen_tree_data=[]
		root=self.treeWidget_zen.invisibleRootItem()
		deepin(root,self.zen_tree_data)


		if zen_searching!="":
			self.lineEdit_zen_search.setText(zen_searching)

	def zen_tree_drop_update(self):
		# 每次拖动排阶级后，就检查，zen不能作为folder
		
		root=self.treeWidget_zen.invisibleRootItem()
		for index in range(root.childCount()):
			top_level=root.child(index)

			#如果是根级的Segment，那么它的下面不能有东西
			if top_level.text(1)=="Segment":
				if top_level.childCount()!=0:
					QMessageBox.warning(self,"Warning","Segment不能作为Folder！")
					self.zen_tree_build()
					return
			
			#如果是根级的folder，那么它的下面不能有folder，只能有Segment，且Segment底下不能有东西
			else:
				for index2 in range(top_level.childCount()):
					second_level=top_level.child(index2)

					#是folder
					if second_level.text(1)=="Folder":
						QMessageBox.warning(self,"Warning","Folder只能有一层！")
						self.zen_tree_build()
						return
					#是Segment
					else:
						if second_level.childCount()!=0:
							QMessageBox.warning(self,"Warning","Segment不能作为Folder！")
							self.zen_tree_build()
							return
		
		self.zen_tree_data_update()
		self.zen_tree_build()

	def zen_segment_show(self):
		TYPE=self.treeWidget_zen.currentItem().text(1)
		if TYPE=="Folder":
			return
		
		segment_name=self.treeWidget_zen.currentItem().text(0)
		
		# self.stackedWidget_zen.setCurrentIndex(0)
		text=self.zen_data[segment_name]

		self.textEdit_viewer_zen.setMarkdown(text)
		self.plainTextEdit_zen.setPlainText(text)
		
		self.zen_text_search_or_count()

		# 奶奶的 《老 子》 不干了
		# zen_searching=self.lineEdit_zen_search.text()
		# if zen_searching[:3]=="t: " or zen_searching[:3]=="T: ":
		# 	searching_text=zen_searching[3:]
		# 	#所在行数，不能保证每次都正确定位，因为markdown中的换行可能是两个可能是一个
		# 	row=text[:text.find(searching_text)].count("\n\n")+text[:text.find(searching_text)].replace("\n\n","").count("\n")
		# 	self.plainTextEdit_zen.row=row
			
		# 	self.textEdit_viewer_zen.setFocus()
		# 	cursor=QTextCursor(self.textEdit_viewer_zen.document().findBlockByLineNumber(row))
		# 	self.textEdit_viewer_zen.moveCursor(QTextCursor.End)
		# 	self.textEdit_viewer_zen.setTextCursor(cursor)
	
	def zen_segment_save(self):
		try:
			segment_name=self.treeWidget_zen.currentItem().text(0)
			self.zen_data[segment_name]=self.plainTextEdit_zen.toPlainText()
		except:
			pass
	
	def zen_switch_mode(self):
		# self.stackedWidget_zen的第0个是textEdit_viewer_zen
		# self.stackedWidget_zen的第1个是plainTextEdit_zen

		

		if self.stackedWidget_zen.currentIndex()==0:
			#切换到编辑模式
			self.stackedWidget_zen.setCurrentIndex(1)

			####
				#根本不用这么麻烦，切换回去就完事了……
				# text=self.textEdit_viewer_zen.toMarkdown()
				# text=re.sub("(?<=[^\n])\n(?=[^\n])","",text)
				# self.plainTextEdit_zen.setPlainText(text)

				# #恢复cursor位置
				# cursor=self.plainTextEdit_zen.restore_cursor_pos()
				# self.plainTextEdit_zen.moveCursor(QTextCursor.End)
				# self.plainTextEdit_zen.setTextCursor(cursor)
			
		elif self.stackedWidget_zen.currentIndex()==1:
			#切换到预览模式
			self.stackedWidget_zen.setCurrentIndex(0)
			text=self.plainTextEdit_zen.toPlainText()
			self.textEdit_viewer_zen.setMarkdown(text)
		
		self.zen_text_search_or_count()
		
			####
				#更新cursor位置
				# self.plainTextEdit_zen.update_cursor_pos()

	def zen_edit(self):
		selected_item=[item for item in self.treeWidget_zen.selectedItems()]
		
		if len(selected_item)>1:
			QMessageBox.warning(self,"Warning","一个一个编辑吧")
			return
		
		item=selected_item[0]

		old_name=item.text(0)
		#改文件夹的名字
		
		dlg = QDialog(self)
		dlg.setMinimumSize(400,200)
		dlg.setWindowTitle("Rename")

		old_name_label=QLabel("Old Name:")
		old_name_enter=QLineEdit()
		old_name_enter.setText(old_name)
		old_name_enter.setReadOnly(1)

		new_name_label=QLabel("New Name:")
		new_name_enter=QLineEdit()
		new_name_enter.setText(old_name)
		
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

		#输入框自动定位
		new_name_enter.setFocus()
		new_name_enter.setSelection(0,len(old_name))

		if dlg.exec_():
			new_name=new_name_enter.text()
			
			if item.text(1)=="Folder":
				for top_level in self.zen_tree_data:
					#top_level放了folder
					if type(top_level)==dict and top_level["folder_name"]==old_name:
						top_level["folder_name"]=new_name
						break
				
			elif item.text(1)=="Segment":
				index=0
				for top_level in self.zen_tree_data:
					#top_level放了folder
					if type(top_level)==dict:
						index1=0
						find=False
						for segment_name in top_level["Segment"]:
							if segment_name==old_name:
								top_level["Segment"][index1]=new_name

								old_text=self.zen_data[old_name]
								self.zen_data.pop(old_name)
								self.zen_data[new_name]=old_text

								find=True
								break
							index1+=1
						
						if find==True:
							break
					else:
						segment_name=top_level
						if segment_name==old_name:
							self.zen_tree_data[index]=new_name
							
							old_text=self.zen_data[old_name]
							self.zen_data.pop(old_name)
							self.zen_data[new_name]=old_text
							
							break
					index+=1
			self.zen_tree_build()
		pass

	def diary_text_search(self):
		dlg=DiarySearchDialog(self)
		if self.window_is_stay_on_top()==True:
			dlg.setWindowFlag(Qt.WindowStaysOnTopHint,True)
		dlg.exec_()

	def diary_analyze(self):
		dlg=DiaryAnalyzeDialog(self)
		if self.window_is_stay_on_top()==True:
			dlg.setWindowFlag(Qt.WindowStaysOnTopHint,True)
		dlg.exec_()

	def file_check(self):
		if self.file_saving_base=="":
			QMessageBox.warning(self,"Warning","如果要使用File Library，请先到Setting中设置File Library的基地址。（所有拖进File Library中的文件都会被移动到基地址下）")
			return

		redundant=[]
		missing=[]
		
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
								if file_heap_have!=[]:
									file_heap_exist=True
								else:
									file_heap_exist=False

								try:
									file_data_have=self.file_data[y][m][d].keys()
									file_data_exist=True
								except:
									#如果没有当日的容器那就新建好了
									self.file_data[y][m][d]={}
									file_data_have=self.file_data[y][m][d].keys()
									file_data_exist=False
								
								if file_heap_exist or file_data_exist:
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
							#可以没有文件夹但存在网页链接，所以这里missing的只是那些文件，不包含网页链接
							if "|" not in file_name:
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

		if self.window_is_stay_on_top()==True:
			file_checker.setWindowFlag(Qt.WindowStaysOnTopHint,True)

		file_checker.exec_()

		#保存所有相关的数据
		self.diary_data_save_out()
		Fernet_Encrypt_Save(self.password,self.concept_data,"Concept_Data.dlcw")
		Fernet_Encrypt_Save(self.password,self.file_data,"File_Data.dlcw")		

		#更新所有相关的界面
		try:
			self.concept_show(int(self.lineEdit_id.text()))
		except:
			pass
		self.diary_show(QDate_transform(self.calendarWidget.selectedDate()))
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
		
		temp=QListWidgetItem()
		
		file_url=self.file_saving_base+"/"+str(y)+"/"+str(m)+"/"+str(d)+"/"+file_name
		temp.setIcon(self.listWidget_search_file.which_icon(file_url))

		#如果是link
		if "|" in file_name:
			#link的tooltip没有直接设置成url网址
			#考虑到几个file listwidget间的拖动操作需要判断link是否已经在file_data中存在，所以需要附带ymd信息
			#这样损失了直接往浏览器拖动打开网页的功能，但双击、回车打开就行了
			# ">Google|http://www.google.com"
			file_name=file_name[:file_name.rfind("|")][1:]
		
		temp.setText(file_name)
		temp.setToolTip(file_url)
		
		self.listWidget_search_file.addItem(temp)

	def file_library_list_update(self,starting=False):
		"file_data[y][m][d]字典里key的顺序是乱的，也就这里列出来看的时候要按文件名sort一下"


		def list_file_in_today():
			try:
				y=self.y
				m=self.m
				d=self.d
				self.label_titlebar_library.setText("Library : Searching: Date: %s.%s.%s"%(y,m,d))

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
				
				self.label_titlebar_library.setText("Library : Searching: Date: %s.%s.%s"%(y,m,d))
			except:
				self.label_titlebar_library.setText("Library : Searching: Date: ")
				pass
		
		def list_file_without_concept():
			self.label_titlebar_library.setText("Library : Searching: No Linked Concept: ")
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
					
					#因为网页链接的命名是不受限制的，这里不管用什么作分隔符都可能会冲突
					#所以用|的话只要解决好找名字就行了
					#因为这里如果是网页链接的话，文件名本身就带有|，所以得这样处理
					file_name=""
					for i in file[3:]:
						file_name+=i+"|"
					file_name=file_name[:-1]

					self.file_library_add_a_file_to_search_list(y,m,d,file_name)

			if searched_concepts!=[]:
				title="Library : Searching: Concept Name: "
				for searched_concept_name in searched_concepts:
					title+=searched_concept_name+" & "
				title=title[:-3]
				self.label_titlebar_library.setText(title)
			else:
				self.label_titlebar_library.setText("Library : Searching: Concept Name: ")
		
		def list_file_in_filename(search):
			"搜索文件名只有“与”模式，关键词用空格分隔，列出文件名同时包含所有关键词的文件"
			search=list(map(lambda x: x.lower(),search.split()))
			for y in range(1970,2170):
				for m in range(1,13):
					for d in self.file_data[y][m].keys():
						
						for file_name in sorted(self.file_data[y][m][d].keys()):
							for i in search:
								if i not in file_name and i not in convert_to_az(file_name):
									break
							else:
								self.file_library_add_a_file_to_search_list(y,m,d,file_name)
			
			self.label_titlebar_library.setText("Library : Searching: File Name: %s"%search)


		########################################################################################
		########################################################################################
		########################################################################################
		#为了不让启动的时候跳出警告窗口，只能这样勉强一下了
		if starting==False:
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
		
		else:
			#特殊搜索模式
			if search[0]=="\\":
				self.label_titlebar_library.setText("Library : Searching: Special Mode: ")

				# "日期搜索模式:\d 2021.3.12"
				if search[:3]=="\\d " or search[:3]=="\\D ":
					list_file_in_date(search)
				
				#"没有concept归属搜索模式：\^c"
				elif search[:3]=="\\^c" or search[:3]=="\\^C":
					list_file_without_concept()

				# "concept name“与”搜索模式:\c 宇宙 地球"
				elif search[:3]=="\\c " or search[:3]=="\\C ":
					list_file_with_and_concept(search)

			# 文件名搜索模式
			else:
				list_file_in_filename(search)

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
								self.trayIcon.showMessage("Infomation","该链接已存在！\n%s"%link)
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
		"这里进来的要么是文件路径D:/，要么是网址http(s)"
		
		另外如果从内部拖到Library区，可以执行copy操作。
		"""

		def file_dir_dialog(lineedit):
			dlg=QFileDialog(self)
			file_saving_base=dlg.getExistingDirectory()
			lineedit.setText(file_saving_base)
		



		if self.file_saving_base=="":
			QMessageBox.warning(self,"Warning","如果要使用File Library，请先到Setting中设置File Library的基地址。（所有拖进File Library中的文件都会被移动到基地址下）")
			return
		
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
		
		coping_file=[]

		#移动文件到当日路径
		for i in links:
			
			self.progress.setValue(value)
			value+=1

			#内部的link不要拖到file区了！
			if ">" in i:
				continue
			
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
					title="Unknown Page"
					self.trayIcon.showMessage("Infomation","获取网页Title失败，请查看网络连接是否正常！\n%s"%i)
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

						if "|" not in i and len(date_and_name)>4:
							QMessageBox.warning(self,"Warning","禁止从内部路径之下导入文件，先拖出到内部路径之外处。")
							break
						
						#考虑把这些文件复制出去
						y=int(date_and_name[0])
						m=int(date_and_name[1])
						d=int(date_and_name[2])

						if "|" in i:
							#网页链接就算了
							continue
						else:
							file_name=date_and_name[3]
						
						try:
							#file_data中是否存在该文件
							self.file_data[y][m][d][file_name]
						except:
							#如果都不存在，说明是在尝试导入基地址下的，但不在file_data中的文件
							QMessageBox.warning(self,"Warning","禁止从内部路径导入文件（可以用File Chack功能添加abundant文件）")
							break
						#如果存在

						#那就添加到复制列表中
						coping_file.append(i)
						#继续下一个
						continue

				except:
					QMessageBox.warning(self,"Warning","请不要在file_base下乱放文件！")
					break
				
				file_name=os.path.basename(i)
				file_dst=self.file_saving_today_dst+"/"+file_name
				
				self.file_saving_today_dst_exist_check()

				#文件添加，有可能硬盘被拔掉了
				try:
					shutil.move(i,file_dst)
				except:
					QMessageBox.warning(self,"Warning","路径访问出错！移动失败！")
					break
					
				#文件链接concept置空
				self.file_data[self.y][self.m][self.d][file_name]=[]
		
		self.progress.setValue(len(links))
		self.progress.deleteLater()
		
		if coping_file!=[]:
			
			warning_text="确认要将这些文件复制到出去吗？\n\n"
			for i in coping_file:
				warning_text+=i+"\n"
			
			dlg = QDialog(self)
			dlg.setWindowTitle("Copy Warning")

			warning_text_edit=QPlainTextEdit()
			warning_text_edit.setPlainText(warning_text)
			warning_text_edit.setReadOnly(True)
			warning_text_edit.setFixedSize(400,300)

			lineedit_dst=QLineEdit(dlg)
			lineedit_dst.setReadOnly(1)

			button=QPushButton("Open",dlg)
			button.clicked.connect(lambda:file_dir_dialog(lineedit_dst))
			
			QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
			buttonBox = QDialogButtonBox(QBtn)
			buttonBox.accepted.connect(dlg.accept)
			buttonBox.rejected.connect(dlg.reject)

			layout=QVBoxLayout()
			layout.addWidget(warning_text_edit)
			layout.addWidget(lineedit_dst)
			layout.addWidget(button)
			layout.addWidget(buttonBox)
			dlg.setLayout(layout)

			if dlg.exec_():
				dst=lineedit_dst.text()
				
				if dst!="":
					self.progress=QProgressDialog("Coping File...","Cancel",0,len(coping_file),self)
					self.progress.setWindowTitle("Coping File...")
					#禁止cancel和close
					btn=QPushButton("Cancel")
					btn.setDisabled(True)
					self.progress.setCancelButton(btn)
					self.progress.setWindowFlag(Qt.WindowCloseButtonHint,False)
					self.progress.setWindowModality(Qt.WindowModal)
					self.progress.setMinimumDuration(0)
					
					ii=1
					self.progress.setValue(ii)
					try:
						for i in coping_file:
							self.progress.setValue(ii)
							
							file_name=os.path.basename(i)
							file_dst=os.path.join(dst,file_name)
							if os.path.isdir(i):
								shutil.copytree(i,file_dst)
							else:
								shutil.copyfile(i,file_dst)
							ii+=1
					except Exception as e:
						QMessageBox.warning(self,"Warning","复制出错！\n%s"%e)
						self.progress.setValue(len(coping_file))

				else:
					QMessageBox.warning(self,"Warning","请设置目标地址！")

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
		try:
			clicked_file_link=self.listWidget_search_file.currentItem().toolTip()
		except:
			pass
		
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
		if which_file_type(clicked_file_link)=="image" and self.listWidget_search_file.ctrl_pressed==True:
			
			pic_list=[]

			for index in range(self.listWidget_search_file.count()):
				file_link=self.listWidget_search_file.item(index).toolTip()
				file_name=file_link.split("/")[-1]
				
				if which_file_type(file_name)=="image":
					pic_list.append(file_link)
		
			clicked_index=pic_list.index(clicked_file_link)

			self.image_viewer=MyImageViewer(pic_list,clicked_index,self.width(),self.height())
			if self.window_is_stay_on_top()==True:
				self.image_viewer.setWindowFlag(Qt.WindowStaysOnTopHint,True)
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

			self.tab_refresh_current_tab()

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

		self.tab_refresh_current_tab()

	def concept_linked_file_rename(self):
		"直接复制粘贴file_library_file_rename的了，懒得抽象了"
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
		
		for file_index in sorted([item.row() for item in self.listWidget_concept_linked_file.selectedIndexes()]):
			
			file_str=self.listWidget_concept_linked_file.item(file_index).toolTip()
			old_file=file_str.replace(self.file_saving_base,"")[1:].split("/")
			
			
			old_y=int(old_file[0])
			old_m=int(old_file[1])
			old_d=int(old_file[2])

			if "|" in file_str:
				old_file_name=file_str[file_str.find(">"):]
			else:
				old_file_name=old_file[3]

			old_file_linked_concept=self.file_data[old_y][old_m][old_d][old_file_name]

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

				# replace concept data中的old data，增加file data中的new data
				self.file_data[old_y][old_m][old_d][new_file_name]=[]
				for ID in old_file_linked_concept:

					#file data中的linked id顺便改了
					self.file_data[old_y][old_m][old_d][new_file_name].append(ID)

					#replace old file中linked id中的linked file的信息
					for ff_index in range(len(self.concept_data[ID]["file"])):
						
						ff=self.concept_data[ID]["file"][ff_index]
						if ff["y"]==old_y and ff["m"]==old_m and ff["d"]==old_d and ff["file_name"]==old_file_name:
							self.concept_data[ID]["file"][ff_index]["file_name"]=new_file_name

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

		self.tab_refresh_current_tab()

	def diary_line_file_rename(self):
		"直接复制粘贴file_library_file_rename的了，懒得抽象了"
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
		
		for file_index in sorted([item.row() for item in self.listWidget_text_linked_file.selectedIndexes()]):
			
			file_str=self.listWidget_text_linked_file.item(file_index).toolTip()
			old_file=file_str.replace(self.file_saving_base,"")[1:].split("/")
			
			
			old_y=int(old_file[0])
			old_m=int(old_file[1])
			old_d=int(old_file[2])

			if "|" in file_str:
				old_file_name=file_str[file_str.find(">"):]
			else:
				old_file_name=old_file[3]

			old_file_linked_concept=self.file_data[old_y][old_m][old_d][old_file_name]

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

				# replace concept data中的old data，增加file data中的new data
				self.file_data[old_y][old_m][old_d][new_file_name]=[]
				for ID in old_file_linked_concept:

					#file data中的linked id顺便改了
					self.file_data[old_y][old_m][old_d][new_file_name].append(ID)

					#replace old file中linked id中的linked file的信息
					for ff_index in range(len(self.concept_data[ID]["file"])):
						
						ff=self.concept_data[ID]["file"][ff_index]
						if ff["y"]==old_y and ff["m"]==old_m and ff["d"]==old_d and ff["file_name"]==old_file_name:
							self.concept_data[ID]["file"][ff_index]["file_name"]=new_file_name
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

		self.tab_refresh_current_tab()

	def file_saving_today_dst_exist_check(self):
		#这个判断是为了不要每次都去侦测硬盘路径，如果打开程序后侦测过一次后，就不要侦测第二次了
		#如果只是添加网页link的话没必要侦测硬盘，机械硬盘从休眠到启动很慢的
		#在shutil.move之前做检查就行了
		if self.file_saving_today_dst_exist==False:
			
			#当日路径在不在，这里不作过多限制，如果硬盘拔掉了，创建不了路径也没关系，因为要允许添加网页链接
			if not os.path.exists(self.file_saving_today_dst) and self.file_saving_base!="":
				try:
					os.makedirs(self.file_saving_today_dst)
					self.file_saving_today_dst_exist=True
				except:
					#创建不了就算了，那就只能添加网页link了，想添加文件的话会报错的
					pass

	def setting_menu(self):
		
		def settings_retrieve():
			self.file_saving_base=dlg.lineEdit_file_saving_base.text()
			self.user_settings.setValue("file_saving_base",encrypt(self.file_saving_base))
			self.file_saving_today_dst=self.file_saving_base+"/"+str(self.y)+"/"+str(self.m)+"/"+str(self.d)
			self.file_library_list_update(starting=True)

			if dlg.font!=None:
				font=dlg.font
				font_size=dlg.font_size

				self.user_settings.setValue("font",font)
				self.user_settings.setValue("font_size",font_size)
				self.font_set(font,font_size)

			typora_directory=dlg.lineEdit_typora.text()
			self.user_settings.setValue("typora_directory",encrypt(typora_directory))

			sublime_directory=dlg.lineEdit_sublime.text()
			self.user_settings.setValue("sublime_directory",encrypt(sublime_directory))
			
			random_text_directory=dlg.lineEdit_random_text.text()
			self.user_settings.setValue("random_text_directory",encrypt(random_text_directory))


			######################################################################################
			pixiv_cookie=dlg.lineEdit_pixiv_cookie.text()
			self.user_settings.setValue("pixiv_cookie",encrypt(pixiv_cookie))
			
			instagram_cookie=dlg.lineEdit_instagram_cookie.text()
			self.user_settings.setValue("instagram_cookie",encrypt(instagram_cookie))
			
			rss_auto_update=dlg.checkBox_rss_auto_update.isChecked()
			self.user_settings.setValue("rss_auto_update",rss_auto_update)
		

		dlg=SettingDialog(self)

		if self.window_is_stay_on_top()==True:
			dlg.setWindowFlag(Qt.WindowStaysOnTopHint,True)
		
		if dlg.exec_():
			settings_retrieve()
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
		elif which=="RSS Tree":
			save_to_json(self.rss_tree_data,"RSS_Tree_Data.json")
		elif which=="Zen":
			save_to_json(self.zen_data,"Zen_Data.json")
		elif which=="Zen Tree":
			save_to_json(self.zen_tree_data,"Zen_Tree_Data.json")

	def rss_feed_daily_update(self,manually=False):
		#淦！为了搞界面展示后的自动后台更新，搞了将近四个小时……
		#先是搞不好QSystemTrayIcon
		#然后不知道python的thread库和QT的QThread的区别，捣腾了半天python的thread，最终卡界面……
		#网上各种进界面后自动运行还不影响界面操作的方法，什么修改window的showEvent啊，
		#什么qApp.processEvents()啊，还是侦测第一次点进窗体啊，但是无论哪种都会卡界面……
		#
		#为了不卡界面还是得用QT的QThread……
		#然后尝试QThread的class又不允许用__init__传参……
		#咋就没想到传参函数呢？
		def update_window_title(rss_url):
			"实时显示正在更新的RSS名称"
			self.statusBar.showMessage("Updating RSS Feed: "+self.rss_data[rss_url]["feed_name"])

		def partial_work_done(rss_url,updated):

			self.qlock.lock()
			
			#标记最新更新日期
			last_update=str(self.y)+str(self.m)+str(self.d)
			self.rss_data[rss_url]["last_update"]=last_update
			
			#如果有新文章，那就append，并且更新tree列表和文章列表
			if updated==True:
				#new_article_list中最新的在最前面，这里倒序遍历，每个都放在第一个，这样最新的就在最前面了
				for article in self.daily_update_thread.new_article_list[::-1]:
					
					self.rss_data[rss_url]["article_list"].insert(0,article)
					self.rss_data[rss_url]["unread"]+=1
			
				self.rss_feed_article_list_show()
				self.rss_tree_build()
			
			self.qlock.unlock()
			
		
		def fuckyou():
			self.treeWidget_rss.setDragEnabled(1)
			self.treeWidget_rss.setDragDropMode(QAbstractItemView.InternalMove)
			
			self.statusBar.clearMessage()
		
		
		if manually==False:
			rss_auto_update=self.user_settings.value("rss_auto_update")
			if rss_auto_update!="true" and rss_auto_update!="True":
				return

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
				
		# print(updating_url_list)
		# print("Today is",today)

		#传入要更新的列表
		self.daily_update_thread = RSS_Updator_Threador()
		self.daily_update_thread.setdata(self,updating_url_list)

		self.daily_update_thread.progress.connect(partial_work_done)
		self.daily_update_thread.finished.connect(fuckyou)
		self.daily_update_thread.started.connect(update_window_title)
		self.daily_update_thread.start()

	def rss_feed_manually_update(self):
		
		def update_window_title(rss_url):
			"实时显示正在更新的RSS名称"
			self.statusBar.showMessage("Updating RSS Feed: "+self.rss_data[rss_url]["feed_name"])
		
		def partial_work_done(rss_url,updated):
			
			self.qlock.lock()

			#标记最新更新日期
			last_update=str(self.y)+str(self.m)+str(self.d)
			self.rss_data[rss_url]["last_update"]=last_update
			
			#如果有新文章，那就append，并且更新tree列表和文章列表
			if updated==True:
				#new_article_list中最新的在最前面，这里倒序遍历，每个都放在第一个，这样最新的就在最前面了
				for article in self.manually_update_thread.new_article_list[::-1]:
					
					self.rss_data[rss_url]["article_list"].insert(0,article)
					self.rss_data[rss_url]["unread"]+=1
				
			self.qlock.unlock()
			
			self.rss_feed_article_list_show()
			self.rss_tree_build()
		
		def fuckyou():
			self.treeWidget_rss.setDragEnabled(1)
			self.treeWidget_rss.setDragDropMode(QAbstractItemView.InternalMove)
			self.manually_updateing=False

			self.statusBar.clearMessage()
		
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
			self.manually_update_thread.started.connect(update_window_title)

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

				folder_name=re.findall("(?<=\]\|).*",folder.text(0))[0]
				#找文件夹中所有的RSS
				for item in self.rss_tree_data:
					if type(item)==dict and item["folder_name"]==folder_name:
						for rss_url in [feed[1] for feed in item["RSS"]]:
							updating_url_list.append(rss_url)
						break
				
				#传入要更新的列表
				self.manually_update_thread = RSS_Updator_Threador()
				self.manually_update_thread.setdata(self,updating_url_list)

				self.manually_update_thread.progress.connect(partial_work_done)
				self.manually_update_thread.finished.connect(fuckyou)
				self.manually_update_thread.started.connect(update_window_title)

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
			

		if self.rss_searching!="":
			QMessageBox.warning(self,"Warning","请清空RSS搜索条件！")
			return

		dlg = QDialog(self)
		dlg.setWindowTitle("Add New RSS Feed")
		text="""Rss Url:（支持多行导入，一行一个，不用空行）
已经内置Bilibili Video RSS（在上方选择Bilibili Video模式，添加https://space.bilibili.com/ID）
已经内置Bandcamp RSS（在上方选择Bandcamp模式，添加https://BANDNAME.bandcamp.com）
已经内置Pixiv Illustration RSS（在上方选择Pixiv Illustration模式，添加https://www.pixiv.net/users/ID）
已经内置Pixiv Manga RSS（在上方选择Pixiv Manga模式，添加https://www.pixiv.net/users/ID）
已经内置Instagram RSS（在上方选择Instagram模式，添加https://www.instagram.com/ID）

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
		combobox.addItem("Instagram")
		
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
				#禁止cancel和close
				btn=QPushButton("Cancel")
				btn.setDisabled(True)
				self.progress.setCancelButton(btn)
				self.progress.setWindowFlag(Qt.WindowCloseButtonHint,False)
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
		if self.rss_searching!="":
			QMessageBox.warning(self,"Warning","请清空RSS搜索条件！")
			return
		
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
				temp=QTreeWidgetItem(["[🗸]|"+folder_name,"Folder",""])
				temp.setIcon(0,QIcon(":/icon/folder.svg"))

				self.treeWidget_rss.addTopLevelItem(temp)

				self.rss_tree_data_update()
			else:
				QMessageBox.warning(self,"Warning","RSS文件夹不能重名！")
				return
		else:
			return

	def rss_feed_delete(self):
		
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

					self.qlock.lock()

					# # 根本没必要递归嘛
					# # root=self.treeWidget_rss.invisibleRootItem()
					# # deepin_del_feed_in_tree(root,self.rss_tree_data,item.text(2))

					rss_url=item.text(2)

					#去rss_tree_data中删除那个元组
					for i in range(len(self.rss_tree_data)):
						#folder
						if type(self.rss_tree_data[i])==dict:
							for j in range(len(self.rss_tree_data[i]["RSS"])):
								if self.rss_tree_data[i]["RSS"][j][1]==rss_url:
									self.rss_tree_data[i]["RSS"].pop(j)
									break
						#顶层的RSS
						if type(self.rss_tree_data[i])==list:
							if self.rss_tree_data[i][1]==rss_url:
								self.rss_tree_data.pop(i)
								break

					del self.rss_data[rss_url]
					
					self.qlock.unlock()
			
			#再删Folder
			for item in delete_list:
				#如果是Folder
				if item.text(2)=="":
					folder_name=re.findall("(?<=\]\|).*",item.text(0))[0]

					self.qlock.lock()

					for i in range(len(self.rss_tree_data)):
						#folder
						if type(self.rss_tree_data[i])==dict:
							if self.rss_tree_data[i]["folder_name"]==folder_name:
								
								for j in self.rss_tree_data[i]["RSS"]:
									feed_url=j[1]
									del self.rss_data[feed_url]
									
								del self.rss_tree_data[i]
								break

					self.qlock.unlock()


			self.rss_tree_build()
			self.listWidget_rss.clear()
	
		####
			# 根本没必要递归嘛
			# def deepin_del_feed_in_tree(root,pointer,delete_feed_url):
			# 	for index in range(root.childCount()):
					
			# 		#如果是RSS
			# 		if root.child(index).text(2)!="":
			# 			#找到了！
			# 			if root.child(index).text(2)==delete_feed_url:
			# 				ii=0
			# 				for i in pointer:
			# 					try:
			# 						if i[2]==delete_feed_url:
			# 							break
			# 					except:
			# 						pass
			# 					ii+=1
			# 				#删除这个feed
			# 				pointer.pop(ii)
			# 				return

			# 			#没找到
			# 			else:
			# 				continue
					
			# 		#如果是Folder
			# 		else:
						
			# 			#传入这个folder中的rss列表的pointer
			# 			deepin_del_feed_in_tree(root.child(index),pointer[index]["RSS"],delete_feed_url)

	def rss_edit(self):
		def mark_all_article_in_folder(folder_name):
			
			#先列出文件夹中所有的feed
			feed_list=[]
			for item in self.rss_tree_data:
				if type(item)==dict and item["folder_name"]==folder_name:
					for rss_url in [feed[1] for feed in item["RSS"]]:
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

			self.rss_feed_article_list_show()
			self.rss_tree_build()
			QMessageBox.information(self,"Information","Folder内的文章全部标记已读！")

		def delete_all_read_in_folder(folder_name):
			
			#先列出文件夹中所有的feed
			feed_list=[]
			for item in self.rss_tree_data:
				if type(item)==dict and item["folder_name"]==folder_name:
					for rss_url in [feed[1] for feed in item["RSS"]]:
						feed_list.append(rss_url)
					break

			self.qlock.lock()

			for rss_url in feed_list:
				#要删除article吗？
				article_index=0
				while True:
					if article_index==len(self.rss_data[rss_url]["article_list"]):
						break

					if self.rss_data[rss_url]["article_list"][article_index][2]==True:
						self.rss_data[rss_url]["article_list"].pop(article_index)
						continue
					else:
						article_index+=1

			self.qlock.unlock()

			self.rss_feed_article_list_show()
			self.rss_tree_build()
			QMessageBox.information(self,"Information","Folder内的全部已读文章已删除！")

		#################################################################################

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
				rss_name=re.findall("(?<=\]\|).*",item.text(0))[0]
				rss_url=item.text(2)
				rss_url_list.append([rss_name,rss_url])
			
			#传进去一个元素是[rss_name,rss_url]的rss列表
			dlg = RSSFeedEditDialog(self,rss_url_list)

			if self.window_is_stay_on_top()==True:
				dlg.setWindowFlag(Qt.WindowStaysOnTopHint,True)

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
					
					#要删除article吗？
					if result[rss_url]["delete"]==True:
						
						article_index=0
						while True:
							if article_index==len(self.rss_data[rss_url]["article_list"]):
								break

							if self.rss_data[rss_url]["article_list"][article_index][2]==True:
								self.rss_data[rss_url]["article_list"].pop(article_index)
								continue
							else:
								article_index+=1

					#改名字了吗
					if self.rss_data[rss_url]["feed_name"]!=result[rss_url]["feed_name"]:
						
						self.rss_data[rss_url]["feed_name"]=result[rss_url]["feed_name"]
						
						#去rss_tree_data中修改rss的名字
						for i in range(len(self.rss_tree_data)):
							#folder
							if type(self.rss_tree_data[i])==dict:
								for j in range(len(self.rss_tree_data[i]["RSS"])):
									if self.rss_tree_data[i]["RSS"][j][1]==rss_url:
										#淦，竟然弄成了元组类型，这里没法直接改，那就重新制定吧
										self.rss_tree_data[i]["RSS"][j]=(result[rss_url]["feed_name"],rss_url)
							#顶层的RSS
							if type(self.rss_tree_data[i])==list:
								if self.rss_tree_data[i][1]==rss_url:
									self.rss_tree_data[i]=(result[rss_url]["feed_name"],rss_url)
					

				self.qlock.unlock()

				self.rss_feed_article_list_show()
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
				btn2=QPushButton("Delete Articles which Have Been Read")
				label=QLabel("Folder Name")
				enter=QLineEdit()
				
				old_folder_name=re.findall("(?<=\]\|).*",folder.text(0))[0]
				btn.clicked.connect(lambda:mark_all_article_in_folder(old_folder_name))
				btn2.clicked.connect(lambda:delete_all_read_in_folder(old_folder_name))
				enter.setText(old_folder_name)

				QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
				buttonBox = QDialogButtonBox(QBtn)
				buttonBox.accepted.connect(dlg.accept)
				buttonBox.rejected.connect(dlg.reject)

				layout=QVBoxLayout()
				layout.addWidget(btn)
				layout.addWidget(btn2)
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
					
					self.rss_feed_article_list_show()
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
		#这里需要重新计算文件夹包含的未读数，所以还得去更新一下
		self.rss_tree_build()

	def rss_tree_data_update(self):
		# 根据树的结构，重塑rss_tree_data
		def deepin(root,pointer):
			for index in range(root.childCount()):
				
				#如果是RSS
				if root.child(index).text(2)!="":
					if root.child(index).text(1)=="RSS":
						rss_name=re.findall("(?<=\]\|).*",root.child(index).text(0))[0]
						rss_url=root.child(index).text(2)
						
						#树的信息中不区分RSS是Standard还是Custom，只区分Folder和RSS！这东西只是用于建树以及判断rss树的合法性的
						pointer.append([rss_name,rss_url])
						continue
				
				#如果是Folder
				else:
					folder_name=re.findall("(?<=\]\|).*",root.child(index).text(0))[0]
					folder={
						"folder_name":folder_name,
						"RSS":[]
					}
					pointer.append(folder)
					
					#传入这个folder中的rss列表的pointer
					deepin(root.child(index),folder["RSS"])
		

		#这里更新rss_tree_data用的是遍历树侦测结构的方法，所以如果在搜索模式中，要先清除搜索，还原树
		self.rss_searching=self.lineEdit_rss_search.text()
		if self.rss_searching!="":
			self.lineEdit_rss_search.setText("")
			self.rss_tree_build()

		self.qlock.lock()

		self.rss_tree_data=[]
		root=self.treeWidget_rss.invisibleRootItem()
		deepin(root,self.rss_tree_data)

		self.qlock.unlock()

		if self.rss_searching!="":
			self.lineEdit_rss_search.setText(self.rss_searching)

	def rss_tree_build(self):
		# 根据rss_tree_data的层级结构，建树
		tree_expand={}
		root=self.treeWidget_rss.invisibleRootItem()
		for index in range(root.childCount()):
			#如果是folder，就记录一下expand属性
			if root.child(index).text(2)=="":
				folder_name=re.findall("(?<=\]\|).*",root.child(index).text(0))[0]
				tree_expand[folder_name]=root.child(index).isExpanded()
		
		self.treeWidget_rss.clear()
		
		self.rss_searching=self.lineEdit_rss_search.text()

		#默认搜Feed name
		if self.rss_searching!="":
			
			#反正在搜索模式下拖动排序也是没用的
			#（因为搜索模式下的rss_tree_data_update要先清空搜索，再rss_tree_build出完整的tree，侦测tree中的从属关系，最后在恢复原有搜索）
			#所以这里干脆禁止拖动
			self.treeWidget_rss.setDragEnabled(0)
			self.treeWidget_rss.setDragDropMode(QAbstractItemView.NoDragDrop)

			#搜文件夹
			if self.rss_searching[:3]=="f: " or self.rss_searching[:3]=="F: ":
				search_name=self.rss_searching[3:].lower()
				for top_level in self.rss_tree_data:
					if type(top_level)==dict and ( search_name in top_level["folder_name"] or search_name in convert_to_az(top_level["folder_name"]) ):
						
						folder_name=top_level["folder_name"]
						folder_unread=0

						#这里folder_name先这样写，下面还会计算未读数量，重新写folder_name的
						temp_root=QTreeWidgetItem([folder_name,"Folder",""])
						temp_root.setIcon(0,QIcon(":/icon/folder.svg"))
						self.treeWidget_rss.addTopLevelItem(temp_root)

						for rss in top_level["RSS"]:
							
							rss_name=rss[0]
							rss_url=rss[1]
							feed_unread=self.rss_data[rss_url]["unread"]
							folder_unread+=feed_unread

							if feed_unread==0:
								temp=QTreeWidgetItem(temp_root,["[🗸]|"+rss_name,"RSS",rss_url])
							else:
								temp=QTreeWidgetItem(temp_root,["[%s]|"%feed_unread+rss_name,"RSS",rss_url])
							
							temp.setIcon(0,QIcon(":/icon/rss.svg"))
						
						#重新写folder_name
						if folder_unread==0:
							temp_root.setText(0,"[🗸]|"+folder_name)
						else:
							temp_root.setText(0,"[%s]|"%folder_unread+folder_name)

						try:
							temp_root.setExpanded(tree_expand[folder_name])
						except:
							pass

			#搜Feed url
			elif self.rss_searching[:3]=="u: " or self.rss_searching[:3]=="U: ":
				search_name=self.rss_searching[3:]
				for top_level in self.rss_tree_data:
					#top_level放了folder
					if type(top_level)==dict:
						
						folder_name=top_level["folder_name"]
						folder_unread=0

						#这里folder_name先这样写，下面还会计算未读数量，重新写folder_name的
						temp_root=QTreeWidgetItem([folder_name,"Folder",""])
						temp_root.setIcon(0,QIcon(":/icon/folder.svg"))

						has=False
						
						for rss in top_level["RSS"]:
							rss_name=rss[0]
							rss_url=rss[1]
							feed_unread=self.rss_data[rss_url]["unread"]
							folder_unread+=feed_unread

							if search_name in rss_url or search_name in convert_to_az(rss_url):
								has=True
								
								if feed_unread==0:
									temp=QTreeWidgetItem(temp_root,["[🗸]|"+rss_name,"RSS",rss_url])
								else:
									temp=QTreeWidgetItem(temp_root,["[%s]|"%feed_unread+rss_name,"RSS",rss_url])

								temp.setIcon(0,QIcon(":/icon/rss.svg"))
						
						if has==True:
							self.treeWidget_rss.addTopLevelItem(temp_root)
							
							#重新写folder_name
							if folder_unread==0:
								temp_root.setText(0,"[🗸]|"+folder_name)
							else:
								temp_root.setText(0,"[%s]|"%folder_unread+folder_name)

							try:
								temp_root.setExpanded(tree_expand[folder_name])
							except:
								pass
					
					#top_level放了rss
					elif type(top_level)==list:
						rss=top_level
						
						rss_name=rss[0]
						rss_url=rss[1]

						if search_name in rss_url or search_name in convert_to_az(rss_url):
							feed_unread=self.rss_data[rss_url]["unread"]

							if feed_unread==0:
								temp=QTreeWidgetItem(["[🗸]|"+rss_name,"RSS",rss_url])
							else:
								temp=QTreeWidgetItem(["[%s]|"%feed_unread+rss_name,"RSS",rss_url])
							
							temp.setIcon(0,QIcon(":/icon/rss.svg"))

							self.treeWidget_rss.addTopLevelItem(temp)

			#默认搜feed name
			else:
				search_name=self.rss_searching.lower()
				for top_level in self.rss_tree_data:
					#top_level放了folder
					if type(top_level)==dict:
						
						folder_name=top_level["folder_name"]
						folder_unread=0

						#这里folder_name先这样写，下面还会计算未读数量，重新写folder_name的
						temp_root=QTreeWidgetItem([folder_name,"Folder",""])
						temp_root.setIcon(0,QIcon(":/icon/folder.svg"))

						has=False
						
						for rss in top_level["RSS"]:
							rss_name=rss[0]
							rss_url=rss[1]
							feed_unread=self.rss_data[rss_url]["unread"]
							folder_unread+=feed_unread

							if search_name in rss_name or search_name in convert_to_az(rss_name):
								has=True
								
								if feed_unread==0:
									temp=QTreeWidgetItem(temp_root,["[🗸]|"+rss_name,"RSS",rss_url])
								else:
									temp=QTreeWidgetItem(temp_root,["[%s]|"%feed_unread+rss_name,"RSS",rss_url])

								temp.setIcon(0,QIcon(":/icon/rss.svg"))
						
						if has==True:
							self.treeWidget_rss.addTopLevelItem(temp_root)
							
							#重新写folder_name
							if folder_unread==0:
								temp_root.setText(0,"[🗸]|"+folder_name)
							else:
								temp_root.setText(0,"[%s]|"%folder_unread+folder_name)

							try:
								temp_root.setExpanded(tree_expand[folder_name])
							except:
								pass
					
					#top_level放了rss
					elif type(top_level)==list:
						rss=top_level
						
						rss_name=rss[0]
						rss_url=rss[1]

						if search_name in rss_name or search_name in convert_to_az(rss_name):
							feed_unread=self.rss_data[rss_url]["unread"]

							if feed_unread==0:
								temp=QTreeWidgetItem(["[🗸]|"+rss_name,"RSS",rss_url])
							else:
								temp=QTreeWidgetItem(["[%s]|"%feed_unread+rss_name,"RSS",rss_url])
							
							temp.setIcon(0,QIcon(":/icon/rss.svg"))

							self.treeWidget_rss.addTopLevelItem(temp)
		
		#搜索为空，展示全部
		else:

			self.treeWidget_rss.setDragEnabled(1)
			self.treeWidget_rss.setDragDropMode(QAbstractItemView.InternalMove)

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
						rss_url=rss[1]
						feed_unread=self.rss_data[rss_url]["unread"]
						folder_unread+=feed_unread

						if feed_unread==0:
							temp=QTreeWidgetItem(temp_root,["[🗸]|"+rss_name,"RSS",rss_url])
						else:
							temp=QTreeWidgetItem(temp_root,["[%s]|"%feed_unread+rss_name,"RSS",rss_url])
						
						temp.setIcon(0,QIcon(":/icon/rss.svg"))
					
					#重新写folder_name
					if folder_unread==0:
						temp_root.setText(0,"[🗸]|"+folder_name)
					else:
						temp_root.setText(0,"[%s]|"%folder_unread+folder_name)

					try:
						temp_root.setExpanded(tree_expand[folder_name])
					except:
						pass
				
				#top_level放了rss
				elif type(top_level)==list:
					rss=top_level
					
					rss_name=rss[0]
					rss_url=rss[1]
					feed_unread=self.rss_data[rss_url]["unread"]

					if feed_unread==0:
						temp=QTreeWidgetItem(["[🗸]|"+rss_name,"RSS",rss_url])
					else:
						temp=QTreeWidgetItem(["[%s]|"%feed_unread+rss_name,"RSS",rss_url])
					
					temp.setIcon(0,QIcon(":/icon/rss.svg"))

					self.treeWidget_rss.addTopLevelItem(temp)

		# 为什么只有rss_tree_drop_update来的会导致scrollbar移到最顶上，其他情况就好好的？
		# 你大爷的我不鸟你了，鸡儿卡就卡着吧
		# self.treeWidget_rss.verticalScrollBar().setValue(24)
		# self.treeWidget_rss.verticalScrollBar().value()

	def rss_feed_article_list_show(self):
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
						self.listWidget_rss.addItem("✨|"+article_name)
					else:
						self.listWidget_rss.addItem("🗸|"+article_name)
			
			#点的是folder，展示下层的所有文章
			elif rss_url=="":
				folder_name=re.findall("(?<=\]\|).*",self.treeWidget_rss.currentItem().text(0))[0]

				#先列出文件夹中所有的feed
				feed_list=[]
				for item in self.rss_tree_data:
					if type(item)==dict and item["folder_name"]==folder_name:
						for rss_url in [feed[1] for feed in item["RSS"]]:
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
						self.listWidget_rss.addItem("✨|"+article_name)
					else:
						self.listWidget_rss.addItem("🗸|"+article_name)
				
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
						self.listWidget_rss.addItem("✨|"+article_name)
					else:
						self.listWidget_rss.addItem("🗸|"+article_name)
			
			#点的是folder，展示下层的所有文章
			elif type(self.current_rss_showing)==list:
				"把正在看的folder的name藏在了最后，重新进这个函数的时候有用（就是下面的那种情况），反正那边点击文章的也不会戳到屁股上的"
				folder_name=self.current_rss_showing[-1]

				#先列出文件夹中所有的feed
				feed_list=[]
				for item in self.rss_tree_data:
					if type(item)==dict and item["folder_name"]==folder_name:
						for rss_url in [feed[1] for feed in item["RSS"]]:
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
						self.listWidget_rss.addItem("✨|"+article_name)
					else:
						self.listWidget_rss.addItem("🗸|"+article_name)
				
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
				self.listWidget_rss.item(index).setText("🗸|"+article_name)
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
				self.listWidget_rss.item(index).setText("🗸|"+article_name)
				#更新tree列表中的前缀
				self.rss_tree_build()
		
		
		self.lineEdit_browser.setText(article_url)
		article_url=QUrl.fromUserInput(article_url)
		if article_url.isValid():
			self.browser.load(article_url)

	def rss_browser_goto_url(self):
		"Bilibili登录按钮点不了，那就自己输网址去登录吧"
		url=self.lineEdit_browser.text()
		self.browser.load(url)

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

				####
					#tab页有自己的concept编辑区啦
					#这里的tab应该算是一个指针，可以在这里链上一些槽
					#点击内部的leaf，回传到这里，去显示concept
					# tab.clicked.connect(lambda ID:self.concept_show(ID))

				#一开始不让操作
				tab.listWidget_file_root.setEnabled(0)
				tab.listWidget_file_leafs.setEnabled(0)
				
				#更新custom_tab_data的数据
				self.custom_tab_data.append([tab_name,tab_selection_id,tab_selection_depth,True])

				#custom_tabs_shown存储正在界面上展示的tabs，这些是用来实时与concept data同步更新的
				self.custom_tabs_shown.append(tab)

				self.tabWidget.addTab(tab,QIcon(":/icon/trello.svg"),tab_name)
				self.tabWidget.setCurrentIndex(self.tabWidget.indexOf(tab))

				self.tab_set_font(tab)

		else:
			return

	def tab_custom_hide(self):
		tab_index=self.tabWidget.currentIndex()
		
		if tab_index==-1:
			return

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
			action.triggered.connect(partial(self.tab_custom_resurrection,index,action))
			self.menuTab.addAction(action)
			self.TabMenu.addAction(action)

	def tab_custom_resurrection(self,index,action):
		#更新custom_tab_data的数据
		self.custom_tab_data[index][3]=True

		#新建一个tab，调用自定义的MyTabWidget
		tab=MyTabWidget(self,self.custom_tab_data[index][1],self.custom_tab_data[index][2])

		####
			#tab页有自己的concept编辑区啦
			#这里的tab应该算是一个指针，可以在这里链上一些槽
			#点击内部的leaf，回传到这里，去显示concept
			# tab.clicked.connect(lambda ID:self.concept_show(ID))

		#custom_tabs_shown存储正在界面上展示的tabs，这些是用来实时与concept data同步更新的
		self.custom_tabs_shown.append(tab)

		self.tabWidget.addTab(tab,QIcon(":/icon/trello.svg"),self.custom_tab_data[index][0])
		self.tabWidget.setCurrentIndex(self.tabWidget.indexOf(tab))
		
		self.tab_set_font(tab)

		#销毁action
		self.menuTab.removeAction(action)
		self.TabMenu.removeAction(action)

	def tab_custom_delete(self):
		tab_index=self.tabWidget.currentIndex()
		if tab_index==-1:
			return
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

	def tab_refresh_current_tab(self):
		if self.stackedWidget.currentIndex()==4:
			if self.tabWidget.currentIndex()!=-1:
				tab=self.custom_tabs_shown[self.tabWidget.currentIndex()]
				tab.tab_update()

	def tab_set_font(self,tab):
		"因为Tab是动态生成的，所以creat和resurrection时要再来设置一下字体"
		font=self.user_settings.value("font")
		font_size=int(self.user_settings.value("font_size"))

		font.setPointSize(int(font_size*0.8))
		tab.lineEdit_id.setFont(font)
		tab.lineEdit_name.setFont(font)
		tab.plainTextEdit_detail.setFont(font)
		tab.listWidget_relative.setFont(font)
		tab.listWidget_file_root.setFont(font)
		tab.listWidget_file_leafs.setFont(font)
		tab.treeWidget.setFont(font)
		tab.tabWidget.setFont(font)
		
		font.setPointSize(font_size)
		tab.textEdit_viewer.setFont(font)

		tab.listWidget_file_root.setIconSize(QSize(font_size*2,font_size*2))
		tab.listWidget_file_root.setGridSize(QSize(font_size*6,font_size*6))
		tab.listWidget_file_root.setSpacing(font_size*2)
		tab.listWidget_file_root.setWordWrap(1)
		
		tab.listWidget_file_leafs.setIconSize(QSize(font_size*2,font_size*2))
		tab.listWidget_file_leafs.setGridSize(QSize(font_size*6,font_size*6))
		tab.listWidget_file_leafs.setSpacing(font_size*2)
		tab.listWidget_file_leafs.setWordWrap(1)

	####
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

		# 	self.tab_refresh_current_tab()
		############################################################################

	def about(self):
		QMessageBox.about(self,"About","Dongli Teahouse Studio\nVersion: 1.0.0.1\nAuthor: Holence\nContact: Holence08@gmail.com")

	def font_set(self,font,font_size):
		font_size=int(font_size)

		#设置icon size
		icon_size_big=(font_size//2)*2
		if icon_size_big<36:
			icon_size_big=36
		self.btn_menu.setFixedSize(QSize(icon_size_big,icon_size_big))
		self.btn_menu.setIconSize(QSize(icon_size_big,icon_size_big))

		self.btn_stack_home.setFixedSize(QSize(icon_size_big,icon_size_big))
		self.btn_stack_home.setIconSize(QSize(icon_size_big,icon_size_big))
		self.btn_stack_rss.setFixedSize(QSize(icon_size_big,icon_size_big))
		self.btn_stack_rss.setIconSize(QSize(icon_size_big,icon_size_big))
		self.btn_stack_diary.setFixedSize(QSize(icon_size_big,icon_size_big))
		self.btn_stack_diary.setIconSize(QSize(icon_size_big,icon_size_big))
		self.btn_stack_zen.setFixedSize(QSize(icon_size_big,icon_size_big))
		self.btn_stack_zen.setIconSize(QSize(icon_size_big,icon_size_big))
		self.btn_stack_tab.setFixedSize(QSize(icon_size_big,icon_size_big))
		self.btn_stack_tab.setIconSize(QSize(icon_size_big,icon_size_big))
		self.btn_stack_menu.setFixedSize(QSize(icon_size_big,icon_size_big))
		self.btn_stack_menu.setIconSize(QSize(icon_size_big,icon_size_big))
		
		#title的字体是固定的Segoe UI，不能与其他混为一谈
		title_font=self.label_title_bar_top.font()
		title_font.setPointSize(int(icon_size_big*0.5))
		self.label_title_bar_top.setFont(title_font)
		
		icon_size_small=int(icon_size_big*0.66)
		if icon_size_small<24:
			icon_size_small=24
		self.btn_close.setFixedSize(QSize(icon_size_big,icon_size_big))
		self.btn_close.setIconSize(QSize(icon_size_small,icon_size_small))
		self.btn_maximize.setFixedSize(QSize(icon_size_big,icon_size_big))
		self.btn_maximize.setIconSize(QSize(icon_size_small,icon_size_small))
		self.btn_minimize.setFixedSize(QSize(icon_size_big,icon_size_big))
		self.btn_minimize.setIconSize(QSize(icon_size_small,icon_size_small))

		#hide dock的小叉叉
		self.pushButton_concept_close.setFixedSize(QSize(icon_size_small,icon_size_small))
		self.pushButton_concept_close.setIconSize(QSize(icon_size_small,icon_size_small))
		self.pushButton_diary_close.setFixedSize(QSize(icon_size_small,icon_size_small))
		self.pushButton_diary_close.setIconSize(QSize(icon_size_small,icon_size_small))
		self.pushButton_library_close.setFixedSize(QSize(icon_size_small,icon_size_small))
		self.pushButton_library_close.setIconSize(QSize(icon_size_small,icon_size_small))
		self.pushButton_sticker_close.setFixedSize(QSize(icon_size_small,icon_size_small))
		self.pushButton_sticker_close.setIconSize(QSize(icon_size_small,icon_size_small))
		

		#正常字体大小
		self.plainTextEdit_single_line.setFont(font)
		self.plainTextEdit_sticker.setFont(font)
		self.listWidget_lines.setFont(font)
		self.listWidget_concept_related_text.setFont(font)

		#偏小
		font.setPointSize(int(font_size*0.8))
		self.treeWidget_zen.setFont(font)
		self.listWidget_rss.setFont(font)
		self.treeWidget_rss.setFont(font)
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
		font.setPointSize(int(font_size*1.2))
		self.textEdit_viewer.setFont(font)
		self.textEdit_viewer_zen.setFont(font)
		self.plainTextEdit_zen.setFont(font)

		#头文字以及头icon偏小
		#其他的icon要和旁边的文字差不多大，就得比0.8大，1倍刚好
		font.setPointSize(int(font_size*0.8))
		# QApplication.setFont(font)
		# self.menubar.setFont(font)
		self.tabWidget.setFont(font)
		self.tabWidget.setIconSize(QSize(font_size,font_size))
		
		#toolbox竟然没有iconsize选项，那我就不管啦
		self.label_titlebar_concept.setFont(font)
		self.toolBox_concept.setFont(font)
		self.label_concept_icon.setFixedSize(QSize(font_size,font_size))

		self.label_titlebar_diary.setFont(font)
		self.toolBox_text.setFont(font)
		self.label_diary_icon.setFixedSize(QSize(font_size,font_size))

		self.label_titlebar_library.setFont(font)
		self.label_library_icon.setFixedSize(QSize(font_size,font_size))

		self.label_titlebar_sticker.setFont(font)
		self.label_sticker_icon.setFixedSize(QSize(font_size,font_size))

		#日历区不变
		font.setPointSize(10)
		self.calendarWidget.setFont(font)

		#文件列表的icon与间距大小
		self.listWidget_text_linked_file.setIconSize(QSize(font_size*2,font_size*2))
		self.listWidget_text_linked_file.setGridSize(QSize(font_size*6,font_size*6))
		self.listWidget_text_linked_file.setSpacing(font_size*2)
		self.listWidget_text_linked_file.setWordWrap(1)

		self.listWidget_concept_linked_file.setIconSize(QSize(font_size*2,font_size*2))
		self.listWidget_concept_linked_file.setGridSize(QSize(font_size*6,font_size*6))
		self.listWidget_concept_linked_file.setSpacing(font_size*2)
		self.listWidget_concept_linked_file.setWordWrap(1)

		for tab in self.custom_tabs_shown:
			font.setPointSize(int(font_size*0.8))
			tab.lineEdit_id.setFont(font)
			tab.lineEdit_name.setFont(font)
			tab.plainTextEdit_detail.setFont(font)
			tab.listWidget_relative.setFont(font)
			tab.listWidget_file_root.setFont(font)
			tab.listWidget_file_leafs.setFont(font)
			tab.treeWidget.setFont(font)
			tab.tabWidget.setFont(font)
			
			font.setPointSize(font_size)
			tab.textEdit_viewer.setFont(font)

			tab.listWidget_file_root.setIconSize(QSize(font_size*2,font_size*2))
			tab.listWidget_file_root.setGridSize(QSize(font_size*6,font_size*6))
			tab.listWidget_file_root.setSpacing(font_size*2)
			tab.listWidget_file_root.setWordWrap(1)
			
			tab.listWidget_file_leafs.setIconSize(QSize(font_size*2,font_size*2))
			tab.listWidget_file_leafs.setGridSize(QSize(font_size*6,font_size*6))
			tab.listWidget_file_leafs.setSpacing(font_size*2)
			tab.listWidget_file_leafs.setWordWrap(1)
	
	def file_library_locate_from_other_place(self,listwidget):
		
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

	def concept_locate_from_tab(self,treeWidget):
		ID=treeWidget.currentItem().text(0).split("|")[0]
		self.concept_show(ID)

	def center_locate(self):
		#concept 链接文件 定位
		if self.listWidget_concept_linked_file.hasFocus():
			self.file_library_locate_from_other_place(self.listWidget_concept_linked_file)
		#文本块 链接文件 定位
		elif self.listWidget_text_linked_file.hasFocus():
			self.file_library_locate_from_other_place(self.listWidget_text_linked_file)
		#tab定位
		else:
			for tab in self.custom_tabs_shown:
				#tab root file 定位
				if tab.listWidget_file_root.hasFocus():
					self.file_library_locate_from_other_place(tab.listWidget_file_root)
					break
				#tab root file 定位
				if tab.listWidget_file_leafs.hasFocus():
					self.file_library_locate_from_other_place(tab.listWidget_file_leafs)
					break
				#tab tree concept 定位
				elif tab.treeWidget.hasFocus():
					self.concept_locate_from_tab(tab.treeWidget)
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
		
		#rss编辑
		if self.treeWidget_rss.hasFocus():
			self.rss_edit()
		
		#rss编辑
		elif self.treeWidget_zen.hasFocus():
			self.zen_edit()

		#Concept related text编辑
		elif self.listWidget_concept_related_text.hasFocus():
			self.concept_related_text_edit()
		
		#文件重命名
		elif self.listWidget_search_file.hasFocus():
			self.file_library_file_rename()
		elif self.listWidget_concept_linked_file.hasFocus():
			self.concept_linked_file_rename()
		elif self.listWidget_text_linked_file.hasFocus():
			self.diary_line_file_rename()		
		#tab删除root file
		else:
			for tab in self.custom_tabs_shown:
				if tab.listWidget_file_root.hasFocus():
					tab.concept_linked_file_rename()
					break

	def window_toggle_maximun(self):
		if self.isMaximized():
			self.showNormal()
			self.btn_maximize.setIcon(QIcon(":/icon/cil-window-maximize.png"))
		else:
			self.showMaximized()
			self.btn_maximize.setIcon(QIcon(":/icon/cil-window-restore.png"))

	def window_toggle_fullscreen(self):
		
		if self.isFullScreen():
			self.showNormal()
			self.btn_maximize.show()
			self.btn_minimize.show()
		else:
			self.showFullScreen()
			self.btn_maximize.hide()
			self.btn_minimize.hide()

	def window_is_stay_on_top(self):
		"Mainwindow是否正在置顶"
		return bool(self.windowFlags() & Qt.WindowStaysOnTopHint)

	def window_toggle_stay_on_top(self):
		
		#正在置顶，取消置顶
		if self.window_is_stay_on_top()==True:
			self.setWindowFlag(Qt.WindowStaysOnTopHint,False)
			self.dockWidget_concept.setWindowFlag(Qt.WindowStaysOnTopHint,False)
			self.dockWidget_diary.setWindowFlag(Qt.WindowStaysOnTopHint,False)
			self.dockWidget_library.setWindowFlag(Qt.WindowStaysOnTopHint,False)
			self.dockWidget_sticker.setWindowFlag(Qt.WindowStaysOnTopHint,False)

		#没有置顶，设置置顶
		else:
			self.setWindowFlag(Qt.WindowStaysOnTopHint,True)
			self.dockWidget_concept.setWindowFlag(Qt.WindowStaysOnTopHint,True)
			self.dockWidget_diary.setWindowFlag(Qt.WindowStaysOnTopHint,True)
			self.dockWidget_library.setWindowFlag(Qt.WindowStaysOnTopHint,True)
			self.dockWidget_sticker.setWindowFlag(Qt.WindowStaysOnTopHint,True)
		
		# #很奇怪，设置WindowStaysOnTopHint后，所有漂浮的窗口都会被最小化
		# #所以还得一个一个恢复显示状态
		if self.isFullScreen():
			self.showFullScreen()
		else:
			self.showNormal()
		
		if not self.dockWidget_diary.isHidden():
			self.dockWidget_diary.showNormal()
		if not self.dockWidget_concept.isHidden():
			self.dockWidget_concept.showNormal()
		if not self.dockWidget_library.isHidden():
			self.dockWidget_library.showNormal()
		if not self.dockWidget_sticker.isHidden():
			self.dockWidget_sticker.showNormal()

	def window_restore_normal_size(self):
		pos=self.pos()
		x=pos.x()
		y=pos.y()
		mini_size=self.minimumSize()
		w=mini_size.width()
		h=mini_size.height()
		self.setGeometry(x,y,w,h)

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
				data=Fernet_Decrypt_Load(self.password,"Diary_Data.dlcw")
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
			
			Fernet_Encrypt_Save(self.password,data,"Diary_Data.dlcw")
				
		##########################################################################################################
		#################################################Concept##################################################
		##########################################################################################################
		if "Concept_Data.dlcw" in os.listdir("."):
			#如果有Concept_Data.dlcw文件
			try:
				data=Fernet_Decrypt_Load(self.password,"Concept_Data.dlcw")
			except:
				QMessageBox.critical(self,"Error","Concept_Data.dlcw文件出错，请联系相关开发人员！")
				return 0

			try:
				if "Universe" not in data[0]["name"] or data[0]["parent"]!=[]:
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
				"parent": [],
				"child": [],
				"relative": [],
				"az": "yz|universe",
				"file": []
			}]
			Fernet_Encrypt_Save(self.password,data,"Concept_Data.dlcw")
		

		##########################################################################################################
		#################################################File#####################################################
		##########################################################################################################
		#为了能直接索引到年月日，所以固定存储格式
		l=range(1970,2170)
		if "File_Data.dlcw" in os.listdir("."):
			#如果有File_Data文件
			try:
				data=Fernet_Decrypt_Load(self.password,"File_Data.dlcw")
			except:
				QMessageBox.critical(self,"Error","File_Data.dlcw文件出错，请联系相关开发人员！")
				return 0

			try:
				self.file_saving_base=decrypt(self.user_settings.value("file_saving_base"))
			except:
				# QMessageBox.critical(self,"Error","file_saving_base为空！")
				self.file_saving_base=""
		else:
			data={}
			for i in l:
				data[i]={
					1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{},11:{},12:{}
				}
			Fernet_Encrypt_Save(self.password,data,"File_Data.dlcw")
			#默认路径
			self.file_saving_base=""
		
		##########################################################################################################
		#################################################RSS######################################################
		##########################################################################################################
		if "RSS_Data.dlcw" in os.listdir("."):
			#不是第一次进来
			try:
				#检查rss_tree_data和rss_data中的url是否有出入
				
				rss_tree_data=Fernet_Decrypt_Load(self.password,"RSS_Tree_Data.dlcw")
				l0=[]
				for top_level in rss_tree_data:
					#top_level放了folder
					if type(top_level)==dict:
						for rss in top_level["RSS"]:

							rss_url=rss[1]
							l0.append(rss_url)

					#top_level放了rss
					elif type(top_level)==list:
						rss=top_level
						
						rss_url=rss[1]
						l0.append(rss_url)

				rss_data=Fernet_Decrypt_Load(self.password,"RSS_Data.dlcw")
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
			
			Fernet_Encrypt_Save(self.password,rss_tree_data,"RSS_Tree_Data.dlcw")
			Fernet_Encrypt_Save(self.password,rss_data,"RSS_Data.dlcw")
		
		##########################################################################################################
		#################################################ZEN######################################################
		##########################################################################################################

		if "Zen_Data.dlcw" in os.listdir("."):
			#不是第一次进来
			try:
				#检查zen_tree_data和zen_data中的segment_name是否有出入
				
				zen_tree_data=Fernet_Decrypt_Load(self.password,"Zen_Tree_Data.dlcw")
				l0=[]
				for top_level in zen_tree_data:
					#top_level放了folder
					if type(top_level)==dict:
						for segment_name in top_level["Segment"]:
							l0.append(segment_name)

					#top_level放了segment
					else:
						segment_name=top_level
						l0.append(segment_name)

				zen_data=Fernet_Decrypt_Load(self.password,"Zen_Data.dlcw")
				l1=list(zen_data.keys())

				if list_difference(l0,l1)==[]:
					pass
				else:
					QMessageBox.critical(self,"Error","Zen信息不匹配，请联系相关开发人员！")
					return 0
			except:
				QMessageBox.critical(self,"Error","Zen文件出错，请联系相关开发人员！")
				return 0
		
		#第一次进来
		else:
			zen_tree_data=[]
			zen_data={}
			
			Fernet_Encrypt_Save(self.password,zen_tree_data,"Zen_Tree_Data.dlcw")
			Fernet_Encrypt_Save(self.password,zen_data,"Zen_Data.dlcw")


		##########################################################################################################
		#################################################Done#####################################################
		##########################################################################################################
		

		return 1

	def data_load(self):
		"load file、concept、file、rss的data"

		self.diary_data=Fernet_Decrypt_Load(self.password,"Diary_Data.dlcw")
		self.origin_diary_data=Fernet_Decrypt_Load(self.password,"Diary_Data.dlcw")

		self.concept_data=Fernet_Decrypt_Load(self.password,"Concept_Data.dlcw")

		self.file_data=Fernet_Decrypt_Load(self.password,"File_Data.dlcw")

		self.rss_data=Fernet_Decrypt_Load(self.password,"RSS_Data.dlcw")
		self.rss_tree_data=Fernet_Decrypt_Load(self.password,"RSS_Tree_Data.dlcw")
		
		self.zen_data=Fernet_Decrypt_Load(self.password,"Zen_Data.dlcw")
		self.zen_tree_data=Fernet_Decrypt_Load(self.password,"Zen_Tree_Data.dlcw")
		
		# print(self.rss_tree_data)

		# for rss_url in self.rss_data.keys():
		# 	try:
		# 		self.rss_data[rss_url]["article_list"].pop(0)
		# 		self.rss_data[rss_url]["article_list"].pop(0)
		# 		self.rss_data[rss_url]["article_list"].pop(0)
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

	def data_save(self):
		
		#Diary data
		self.diary_data_save_out()

		#concept data
		Fernet_Encrypt_Save(self.password,self.concept_data,"Concept_Data.dlcw")

		#file data
		Fernet_Encrypt_Save(self.password,self.file_data,"File_Data.dlcw")

		#RSS data
		Fernet_Encrypt_Save(self.password,self.rss_data,"RSS_Data.dlcw")
		Fernet_Encrypt_Save(self.password,self.rss_tree_data,"RSS_Tree_Data.dlcw")

		#Zen data
		Fernet_Encrypt_Save(self.password,self.zen_data,"Zen_Data.dlcw")
		Fernet_Encrypt_Save(self.password,self.zen_tree_data,"Zen_Tree_Data.dlcw")

		#sticker
		sticker_text=self.plainTextEdit_sticker.toPlainText()
		self.user_settings.setValue("sticker",encrypt(sticker_text))
	
	def data_security_check(self):
		
		#1.Concept中的链接文件是否在File_data中存在？
		warning_text=""
		for concept in self.concept_data:
			for file in concept["file"]:
				y=file["y"]
				m=file["m"]
				d=file["d"]
				file_name=file["file_name"]
				try:
					self.file_data[y][m][d][file_name]
				except:
					warning_text+="%s/%s/%s/%s\n"%(y,m,d,file_name)
		
		if warning_text!="":
			warning_text="Concept中的链接文件在File_Data中缺失：\n"+warning_text
			QMessageBox.warning(self,"Warning",warning_text)
		
		#2.Diary中的链接文件是否在File_data中存在？
		warning_text=""
		for year_index in range(1970-1970,2170-1970):
			for month_index in range(0,12):
				for day_index in range(len(self.diary_data[year_index]["date"][month_index])):
					for line in self.diary_data[year_index]["date"][month_index][day_index]["text"]:
						for file in line["linked_file"]:
							y=file["y"]
							m=file["m"]
							d=file["d"]
							file_name=file["file_name"]
							try:
								self.file_data[y][m][d][file_name]
							except:
								warning_text+="%s/%s/%s/%s\n"%(y,m,d,file_name)
		if warning_text!="":
			warning_text="Diary中的链接文件在File_Data中缺失：\n"+warning_text
			QMessageBox.warning(self,"Warning",warning_text)

		QMessageBox.information(self,"Infomation","检查完毕！")
		
	def diary_data_save_out(self):
		#保存到外存
		Fernet_Encrypt_Save(self.password,self.diary_data,"Diary_Data.dlcw")
		self.origin_diary_data=Fernet_Decrypt_Load(self.password,"Diary_Data.dlcw")

		self.window_title_update()

	def concept_info_edited_and_save(self):
		try:
			ID=int(self.lineEdit_id.text())
			self.concept_data[ID]["name"]=self.lineEdit_name.text()
			self.concept_data[ID]["az"]=convert_to_az(self.concept_data[ID]["name"])
			self.concept_data[ID]["detail"]=self.plainTextEdit_detail.toPlainText()

			#直接全部刷新就行了
			self.diary_line_concept_list_update()
			self.concept_search_list_update()

			self.tab_refresh_current_tab()
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

	def window_title_update(self):
		
		if self.origin_diary_data!=self.diary_data:
			self.label_title_bar_top.setText("Dongli Teahouse Studio *Unsaved Change*")
		else:
			self.label_title_bar_top.setText("Dongli Teahouse Studio")

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
				self.label_titlebar_concept.setText("Concept Searching: No Parent")
			#附加name信息
			else:
				search_name=search[4:]
				for i in self.concept_data:
					if i["parent"]==[]:
						if search_name==str(i["id"]) or search_name in i["name"] or search_name in i["az"] or search_name in i["detail"] or search_name in convert_to_az(i["detail"]):
							self.listWidget_search_concept.addItem(str(i["id"])+"|"+i["name"])
				self.label_titlebar_concept.setText("Concept Searching: No Parent %s"%search_name)

		#没有child
		elif search[:4]=="\^c " and search[4:7]!="\^p":
			#无附加信息
			if len(search)==4:
				for i in self.concept_data:
					if i["child"]==[]:
						self.listWidget_search_concept.addItem(str(i["id"])+"|"+i["name"])
				self.label_titlebar_concept.setText("Concept Searching: No Child")
			#附加name信息
			else:
				search_name=search[4:]
				for i in self.concept_data:
					if i["child"]==[]:
						if search_name==str(i["id"]) or search_name in i["name"] or search_name in i["az"] or search_name in i["detail"] or search_name in convert_to_az(i["detail"]):
							self.listWidget_search_concept.addItem(str(i["id"])+"|"+i["name"])
				self.label_titlebar_concept.setText("Concept Searching: No Child %s"%search_name)

		#没有parent也没有child
		elif search[:8]=="\^p \^c " or search[:8]=="\^c \^p ":
			#无附加信息
			if len(search)==8:
				for i in self.concept_data:
					if i["parent"]==[] and i["child"]==[]:
						self.listWidget_search_concept.addItem(str(i["id"])+"|"+i["name"])
				self.label_titlebar_concept.setText("Concept Searching: No Parent & No Child")
			#附加name信息
			else:
				search_name=search[8:]
				for i in self.concept_data:
					if i["parent"]==[] and i["child"]==[]:
						if search_name==str(i["id"]) or search_name in i["name"] or search_name in i["az"] or search_name in i["detail"] or search_name in convert_to_az(i["detail"]):
							self.listWidget_search_concept.addItem(str(i["id"])+"|"+i["name"])
				self.label_titlebar_concept.setText("Concept Searching: No Parent & No Child %s"%search_name)

		#正常模式搜名字
		else:
			for i in self.concept_data:
				#搜索id或name或az name或detail
				if search==str(i["id"]) or search in i["name"] or search in i["az"] or search in i["detail"] or search in convert_to_az(i["detail"]):
					self.listWidget_search_concept.addItem(str(i["id"])+"|"+i["name"])
			self.label_titlebar_concept.setText("Concept Searching: %s"%search)

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
			
			if item["id"]!=0:
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
						for linked_item_index in range(len(self.file_data[year_index][month_index][day][file])):
							old_id=self.file_data[year_index][month_index][day][file][linked_item_index]
							if old_id in changed_id_dict_keys:
								self.file_data[year_index][month_index][day][file][linked_item_index]=changed_id_dict[old_id]
		

		self.diary_line_concept_list_update()
		self.concept_search_list_update()

		self.tab_refresh_current_tab()

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
		if len(item["file"])>0:
			self.toolBox_concept.setItemText(1,"Concept Linked File: %s"%len(item["file"]))
		else:
			self.toolBox_concept.setItemText(1,"Concept Linked File")
		
		for file in item["file"]:
			y=file["y"]
			m=file["m"]
			d=file["d"]
			file_name=file["file_name"]

			temp=QListWidgetItem()

			file_url=self.file_saving_base+"/"+str(y)+"/"+str(m)+"/"+str(d)+"/"+file_name
			temp.setIcon(self.listWidget_concept_linked_file.which_icon(file_url))
			
			#如果是link
			if "|" in file_name:
				#link的tooltip没有直接设置成url网址
				#考虑到几个file listwidget间的拖动操作需要判断link是否已经在file_data中存在，所以需要附带ymd信息
				#这样损失了直接往浏览器拖动打开网页的功能，但双击、回车打开就行了
				# ">Google|http://www.google.com"
				file_name=file_name[:file_name.rfind("|")][1:]
			
			temp.setText(file_name)
			temp.setToolTip(file_url)
			
			self.listWidget_concept_linked_file.addItem(temp)
		

		#找一找Concept related text
		week_dict=["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
		self.listWidget_concept_related_text.clear()
		text_list=[]
		for year_index in range(1970-1970,2170-1970):
			for month_index in range(0,12):
				for day_index in range(len(self.diary_data[year_index]["date"][month_index])):
					for line in self.diary_data[year_index]["date"][month_index][day_index]["text"]:
						if item["id"] in line["linked_concept"]:
							y=year_index+1970
							m=month_index+1
							d=self.diary_data[year_index]["date"][month_index][day_index]["day"]
							weeknum=QDate(y,m,d).dayOfWeek()-1
							
							text_list.append({
								#老传统用点号和空格分隔
								"date":"%s.%s.%s %s"%(y,m,d,week_dict[weeknum]),
								"text":line["line_text"]
							})
							
	
		#如果有的话就列出来
		if text_list!=[]:
			
			self.toolBox_concept.setItemText(0,"Concept Related Text: %s"%len(text_list))
			
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
		else:
			self.toolBox_concept.setItemText(0,"Concept Related Text")
		
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

		self.tab_refresh_current_tab()

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
						self.close()
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
					if item["id"]!=0:
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
								for linked_item_index in range(len(self.file_data[year_index][month_index][day][file])):
									old_id=self.file_data[year_index][month_index][day][file][linked_item_index]
									if old_id in changed_id_dict_keys:
										self.file_data[year_index][month_index][day][file][linked_item_index]=changed_id_dict[old_id]
				

				self.diary_line_concept_list_update()
				self.concept_search_list_update()

				self.tab_refresh_current_tab()


		
		except:
			pass

	def concept_relationship_add(self,mode):
		try:
			item_ID=int(self.lineEdit_id.text())
			
			if self.listWidget_search_concept.hasFocus():
				link_ID=int(self.listWidget_search_concept.currentItem().text().split("|")[0])
			else:
				for tab in self.custom_tabs_shown:
					if tab.treeWidget.hasFocus():
						link_ID=int(tab.treeWidget.currentItem().text(0).split("|")[0])
						break
			
			item_name=self.concept_data[item_ID]["name"]
			link_name=self.concept_data[link_ID]["name"]

			if mode=="parent":
				if link_ID==item_ID:
					QMessageBox.warning(self,"Error","哦我的上帝，你不能链接自身")
					return
				if item_ID==0:
					QMessageBox.warning(self,"Error","哦我的上帝，就让宇宙先生当DAI王吧")
					return
				elif item_ID!=0 and link_ID in self.concept_data[item_ID]["parent"] :
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
				elif item_ID!=0 and link_ID in self.concept_data[item_ID]["parent"]:
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

			self.tab_refresh_current_tab()
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

			self.tab_refresh_current_tab()
		except:
			pass

	def diary_show(self,date):
		y=int(date[0])
		m=int(date[1])
		d=int(date[2])
		self.label_titlebar_diary.setText("Diary %s.%s.%s"%(y,m,d))
		
		self.plainTextEdit_single_line.clear()
		self.plainTextEdit_single_line.setEnabled(0)
		self.listWidget_text_linked_file.setEnabled(0)

		self.listWidget_lines.clear()
		self.listWidget_text_related_concept.clear()
		self.listWidget_text_linked_file.clear()
		self.textEdit_viewer.clear()

		self.toolBox_text.setItemText(0,"Text Related Concept")
		self.toolBox_text.setItemText(1,"Text Linked File")

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
		
		# if self.is_first_arrived==1:
		# 	QMessageBox.warning(self,"Warning","请选中行后再进行链接！")
		# 	return
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
			# 	self.close()

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
		# 	self.close()

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
			
			if len(have_shown)>0:
				self.toolBox_text.setItemText(0,"Text Related Concept: %s"%len(have_shown))
			else:
				self.toolBox_text.setItemText(0,"Text Related Concept")
			
			return
		if self.is_first_arrived==0:
			#已经是老伙计了，只需要列出单行就行了
			self.listWidget_text_related_concept.clear()

			count=0
			for item_id in self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][self.current_line_index]["linked_concept"]:
				self.listWidget_text_related_concept.addItem(str(item_id)+"|"+self.concept_data[item_id]["name"])
				count+=1

			if count>0:
				self.toolBox_text.setItemText(0,"Text Related Concept: %s"%count)
			else:
				self.toolBox_text.setItemText(0,"Text Related Concept")

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
				try:
					date_and_name=i.replace(self.file_saving_base,"")[1:].split("/")
					
					if "|" not in i and len(date_and_name)>4:
						QMessageBox.warning(self,"Warning","禁止从内部路径之下导入文件，先拖出到内部路径之外处。")
						break
					
					y=int(date_and_name[0])
					m=int(date_and_name[1])
					d=int(date_and_name[2])

					if y in range(1970,2170) and m in range(1,13) and d in range(1,32):
						#如果filedata中已经存在，就只做链接操作
						try:
							if "|" in i:
								file_name=i[i.find(">"):]
							else:
								file_name=date_and_name[3]
							
							#file_data中是否存在该文件\link
							self.file_data[y][m][d][file_name]

							#如果存在
							adding_file.append(
								{
									"y":y,
									"m":m,
									"d":d,
									"file_name":file_name
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
					if not self.link_check_unique(i):
						continue
					
					result=getTitle(i)
					if result[0]==True:
						title=result[1]
					else:
						title="Unknown Page"
						self.trayIcon.showMessage("Infomation","获取网页Title失败，请查看网络连接是否正常！\n%s"%i)
					
					file_name=">"+title+"|"+i
					self.file_data[self.y][self.m][self.d][file_name]=[]

				else:
				
					file_name=os.path.basename(i)
					file_dst=self.file_saving_today_dst+"/"+file_name
					
					self.file_saving_today_dst_exist_check()

					#文件添加，有可能硬盘被拔掉了
					try:
						shutil.move(i,file_dst)
					except:
						QMessageBox.warning(self,"Warning","路径访问出错！移动失败！")
						break

					#文件链接concept置空
					self.file_data[self.y][self.m][self.d][file_name]=[]
				
				adding_file.append(
					{
						"y":self.y,
						"m":self.m,
						"d":self.d,
						"file_name":file_name
					}
				)
		
		self.progress.setValue(len(links))
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
		
		#按照文件名排序，并且把文件夹放在最前面
		self.concept_data[ID]["file"].sort(key=lambda x:x["file_name"])
		for index in range(len(self.concept_data[ID]["file"])):
			file_name=self.concept_data[ID]["file"][index]["file_name"]
			if which_file_type(file_name)=="folder":
				folder=self.concept_data[ID]["file"].pop(index)
				self.concept_data[ID]["file"].insert(0,folder)
			
		#更新事物界面
		self.concept_show(ID)
		self.file_library_list_update()


		self.tab_refresh_current_tab()

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
		if which_file_type(clicked_file_link)=="image" and self.listWidget_concept_linked_file.ctrl_pressed==True:
			
			ID=int(self.lineEdit_id.text())

			pic_list=[]

			for file in self.concept_data[ID]["file"]:
				file_link=self.file_saving_base+"/"+str(file["y"])+"/"+str(file["m"])+"/"+str(file["d"])+"/"+file["file_name"]
				file_name=file["file_name"]
				if which_file_type(file_name)=="image":
					pic_list.append(file_link)
		
			clicked_index=pic_list.index(clicked_file_link)

			self.image_viewer=MyImageViewer(pic_list,clicked_index,self.width(),self.height())
			if self.window_is_stay_on_top()==True:
				self.image_viewer.setWindowFlag(Qt.WindowStaysOnTopHint,True)
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

			self.tab_refresh_current_tab()
			
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

	def concept_related_text_edit(self):
		source_id=int(self.lineEdit_id.text())
		dlg=ConceptRelatedTextEditDialog(self,source_id)
		dlg.exec_()
		try:
			self.concept_show(int(self.lineEdit_id.text()))
		except:
			pass
		self.diary_line_concept_list_update()

	def concept_related_text_review(self):
		ID=int(self.lineEdit_id.text())
		review=self.listWidget_concept_related_text.currentItem().text().split("\n\n")
		#2021.4.2 星期几，空格之前的是date
		review_date=review[0].split()[0].split(".")
		y=int(review_date[0])
		m=int(review_date[1])
		d=int(review_date[2])
		
		self.calendarWidget.setSelectedDate(QDate(y,m,d))
		self.diary_show((y,m,d))

		try:
			review_text=review[1]#只取一日内的第一个出来，去最后定位，因为我没法定位多个

			review_text_id=0
			for i in self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"]:
				if review_text in i["line_text"]:
					
					review_linked_concept_id=i["linked_concept"].index(ID)
					break
				review_text_id+=1

			self.listWidget_lines.scrollToItem(self.listWidget_lines.item(review_text_id))
			self.listWidget_lines.item(review_text_id).setSelected(1)
		except:
			pass

	def diary_line_file_show(self):

		self.listWidget_text_linked_file.clear()
		
		#不是新的一篇
		if self.is_new_diary==0:
			
			#刚进来，展示所有的文本块的文件
			if self.is_first_arrived==1:	
				count=0

				for line_index in range(len(self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"])):
					for file in self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][line_index]["linked_file"]:
						y=file["y"]
						m=file["m"]
						d=file["d"]
						file_name=file["file_name"]

						temp=QListWidgetItem()
						
						file_url=self.file_saving_base+"/"+str(y)+"/"+str(m)+"/"+str(d)+"/"+file_name
						temp.setIcon(self.listWidget_text_linked_file.which_icon(file_url))
						
						#如果是link
						if "|" in file_name:
							#link的tooltip没有直接设置成url网址
							#考虑到几个file listwidget间的拖动操作需要判断link是否已经在file_data中存在，所以需要附带ymd信息
							#这样损失了直接往浏览器拖动打开网页的功能，但双击、回车打开就行了
							# ">Google|http://www.google.com"
							file_name=file_name[:file_name.rfind("|")][1:]

						temp.setText(file_name)
						temp.setToolTip(file_url)

						self.listWidget_text_linked_file.addItem(temp)
						count+=1
					
				if count>0:
					self.toolBox_text.setItemText(1,"Text Linked File: %s"%count)
				else:
					self.toolBox_text.setItemText(1,"Text Linked File")
			#只要一行的
			else:
				count=0
				for file in self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][self.current_line_index]["linked_file"]:
					y=file["y"]
					m=file["m"]
					d=file["d"]
					file_name=file["file_name"]

					temp=QListWidgetItem()
					
					file_url=self.file_saving_base+"/"+str(y)+"/"+str(m)+"/"+str(d)+"/"+file_name
					temp.setIcon(self.listWidget_text_linked_file.which_icon(file_url))

					#如果是link
					if "|" in file_name:
						#link的tooltip没有直接设置成url网址
						#考虑到几个file listwidget间的拖动操作需要判断link是否已经在file_data中存在，所以需要附带ymd信息
						#这样损失了直接往浏览器拖动打开网页的功能，但双击、回车打开就行了
						# ">Google|http://www.google.com"
						file_name=file_name[:file_name.rfind("|")][1:]
					
					temp.setText(file_name)
					temp.setToolTip(file_url)
					
					self.listWidget_text_linked_file.addItem(temp)
					count+=1

				if count>0:
					self.toolBox_text.setItemText(1,"Text Linked File: %s"%count)
				else:
					self.toolBox_text.setItemText(1,"Text Linked File")

	
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
				try:
					date_and_name=i.replace(self.file_saving_base,"")[1:].split("/")

					if "|" not in i and len(date_and_name)>4:
						QMessageBox.warning(self,"Warning","禁止从内部路径之下导入文件，先拖出到内部路径之外处。")
						break
					
					y=int(date_and_name[0])
					m=int(date_and_name[1])
					d=int(date_and_name[2])

					if y in range(1970,2170) and m in range(1,13) and d in range(1,32):
						#如果filedata中已经存在，就只做链接操作
						try:
							
							if "|" in i:
								file_name=i[i.find(">"):]
							else:
								file_name=date_and_name[3]
								
							#file_data中是否存在该文件\link
							self.file_data[y][m][d][file_name]

							#如果存在
							adding_file.append(
								{
									"y":y,
									"m":m,
									"d":d,
									"file_name":file_name
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
					if not self.link_check_unique(i):
						continue
					
					
					result=getTitle(i)
					if result[0]==True:
						title=result[1]
					else:
						title="Unknown Page"
						self.trayIcon.showMessage("Infomation","获取网页Title失败，请查看网络连接是否正常！\n%s"%i)
					
					file_name=">"+title+"|"+i
					self.file_data[self.y][self.m][self.d][file_name]=[]

				else:
				
					file_name=os.path.basename(i)
					file_dst=self.file_saving_today_dst+"/"+file_name
					
					self.file_saving_today_dst_exist_check()

					#文件添加，有可能硬盘被拔掉了
					try:
						shutil.move(i,file_dst)
					except:
						QMessageBox.warning(self,"Warning","路径访问出错！移动失败！")
						break
					
					#文件链接concept置空
					self.file_data[self.y][self.m][self.d][file_name]=[]
				
				adding_file.append(
					{
						"y":self.y,
						"m":self.m,
						"d":self.d,
						"file_name":file_name
					}
				)
		
		self.progress.setValue(len(links))
		self.progress.deleteLater()

		already_have=self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][self.current_line_index]["linked_file"]
		
		#支持多选链接
		for file in adding_file:
			if file not in already_have:
				self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][self.current_line_index]["linked_file"].append(file)

		self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][self.current_line_index]["linked_file"].sort(key=lambda x:x["file_name"])
		for index in range(len(self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][self.current_line_index]["linked_file"])):
			file_name=self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][self.current_line_index]["linked_file"][index]["file_name"]
			if which_file_type(file_name)=="folder":
				folder=self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][self.current_line_index]["linked_file"].pop(index)
				self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][self.current_line_index]["linked_file"].insert(0,folder)

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
		if which_file_type(clicked_file_link)=="image" and self.listWidget_text_linked_file.ctrl_pressed==True:

			pic_list=[]

			for file in self.diary_data[self.current_year_index]["date"][self.current_month_index][self.current_day_index]["text"][self.current_line_index]["linked_file"]:
				file_link=self.file_saving_base+"/"+str(file["y"])+"/"+str(file["m"])+"/"+str(file["d"])+"/"+file["file_name"]
				file_name=file["file_name"]
				if which_file_type(file_name)=="image":
					pic_list.append(file_link)
		
			clicked_index=pic_list.index(clicked_file_link)

			self.image_viewer=MyImageViewer(pic_list,clicked_index,self.width(),self.height())
			if self.window_is_stay_on_top()==True:
				self.image_viewer.setWindowFlag(Qt.WindowStaysOnTopHint,True)
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

	def zen_open_typora(self):
		try:
			typora_directory=decrypt(self.user_settings.value("typora_directory"))
		except:
			QMessageBox.warning(self,"Warning","请先设置Typora启动路径！")
			return

		if typora_directory!="":
			try:
				Popen(typora_directory)
			except Exception as e:
				QMessageBox.warning(self,"Warning","%s"%e)
		else:
			QMessageBox.warning(self,"Warning","请先设置Typora启动路径！")
			return

	def zen_open_sublime(self):
		
		try:
			sublime_directory=decrypt(self.user_settings.value("sublime_directory"))
		except:
			QMessageBox.warning(self,"Warning","请先设置Sublime启动路径！")
			return

		if sublime_directory!="":
			try:
				Popen(sublime_directory)
			except Exception as e:
				QMessageBox.warning(self,"Warning","%s"%e)
		else:
			QMessageBox.warning(self,"Warning","请先设置Sublime启动路径！")
			return

	def zen_text_search_or_count(self):
		
		def zen_count():
			count=len(text)
			self.label_zen_text_search.setText(str(count))
		
		def text_fmt_clear():
			"恢复初始着色"
			cursor.setPosition(0, QTextCursor.MoveAnchor)
			cursor.setPosition(len(text), QTextCursor.KeepAnchor)
			cursor.setCharFormat(fmt)
		
		def text_search():
			#上色
			fmt.setBackground(QColor(107,114,74))
			
			#正则搜索
			try:
				l=re.finditer(searching,text)
			except:
				return
			l=[m.span() for m in l]
			#出来的是形如[(0, 1), (2, 4), (5, 6)]的下表列表，(起始位置,终止位置的后一位)
			for i in l:
				begin=i[0]
				end=i[1]
				cursor.setPosition(begin, QTextCursor.MoveAnchor)
				cursor.setPosition(end, QTextCursor.KeepAnchor)
				cursor.setCharFormat(fmt)

			count=len(l)
			self.label_zen_text_search.setText(str(count))


		searching=self.lineEdit_zen_text_search.text()
		
		fmt=QTextCharFormat()

		#显示总字数的以plainTextEdit_zen为准
		text=self.plainTextEdit_zen.toPlainText()

		if self.stackedWidget_zen.currentIndex()==1:
			#Edit模式
			cursor=QTextCursor(self.plainTextEdit_zen.document())
			text_fmt_clear()
			if searching=="":
				zen_count()
			else:
				text_search()

		if self.stackedWidget_zen.currentIndex()==0:
			#View模式
			if searching=="":
				zen_count()
			else:
				pass
		
		# 发现markdown的标记格式会被fmt抹掉，那view模式下的搜索高亮还是削了吧……
		# 	text=self.textEdit_viewer_zen.toPlainText()
		# 	cursor=QTextCursor(self.textEdit_viewer_zen.document())

	def diary_random_date(self):
		pool=[]
		# replace diary data中的old data
		for year_index in range(1970-1970,2170-1970):
			for month_index in range(0,12):
				for day_index in range(len(self.diary_data[year_index]["date"][month_index])):
					y=self.diary_data[year_index]["date"][month_index][day_index]["year"]
					m=self.diary_data[year_index]["date"][month_index][day_index]["month"]
					d=self.diary_data[year_index]["date"][month_index][day_index]["day"]
					pool.append((y,m,d))
		if len(pool)>=1:
			lucky=pool[randint(0,len(pool)-1)]
			self.calendarWidget.setSelectedDate(QDate(lucky[0],lucky[1],lucky[2]))
			self.diary_show(lucky)


from password_check_window import Ui_password_check_window

class PasswordCheckWindow(QMainWindow,Ui_password_check_window):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		#设置拖动坐标和控件
		self.label_title_bar_top.set_drag_papa(self)
		#无边框
		self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.CustomizeWindowHint)

		#Signal
		self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.ok_clicked)
		self.lineEdit.returnPressed.connect(self.ok_clicked)
		self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.close)
		self.btn_close.clicked.connect(self.close)

		#初始化加密状态信息
		self.user_settings=QSettings("user_settings.ini",QSettings.IniFormat)
		self.cheker=self.user_settings.value("password_checker")
		
		if self.cheker!=None:
			#老用户了
			self.lineEdit.setPlaceholderText("Password")
			self.new_comer=False
		else:
			#新用户
			self.lineEdit.setPlaceholderText("Set a new password here.")
			self.new_comer=True
		
		#尝试的次数
		self.left_times=5
		
		self.lineEdit.setFocus()
		self.show()

	def ok_clicked(self):
		self.password=self.lineEdit.text()
		if self.new_comer==True:
			
			#密码至少六位
			if len(self.lineEdit.text())<6:
				self.label.setText("Password should be at least six characters long.")
				return
			
			new_cheker=Fernet_Encrypt(self.password,"Dongli Teahouse")
			self.user_settings.setValue("password_checker",new_cheker)
			self.close()
			DongliTeahouseStudio(self.password)
		else:
			if Fernet_Decrypt(self.password,self.cheker)=="Dongli Teahouse":
				self.close()
				DongliTeahouseStudio(self.password)
			else:
				self.left_times-=1
				self.label.setText("Wrong Password! Remaining Times: %s"%self.left_times)
				if self.left_times==0:
					self.close()