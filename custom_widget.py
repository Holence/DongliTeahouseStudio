# -*- coding: utf-8 -*-
from custom_function import *

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCharts import QtCharts
import resource_rc

class MyChartView(QtCharts.QChartView):
	def __init__(self):
		super(MyChartView, self).__init__()
		self.setRenderHint(QPainter.Antialiasing)
		self.__press_pos = QPoint()
		self.__ctrl_pressed=False#crtl滚轮水平缩放
		self.__shift_pressed=False#shift滚轮左右移动
		self.__alt_pressed=False#alt拖动图像不移动，这是为了拖动legend列表
		self.xmax_TickCount=15
		self.ymax_TickCount=6
		self.scroll_step=50


	def wheelEvent(self,event):
		"shift滚轮左右移动，crtl滚轮水平缩放，啥都不按正常缩放"
		super(MyChartView,self).wheelEvent(event)

		if event.delta()<0:
			mFactor=0.8
			right=-1
		else:
			mFactor=1.25
			right=1
		
		#crtl滚轮水平缩放
		if self.__ctrl_pressed==True:
			rect = self.chart().plotArea();
			c = self.chart().plotArea().center();
			rect.setWidth(1/mFactor*rect.width());
			rect.moveCenter(c);
			self.chart().zoomIn(rect);

			# 淦！zoom不会自动缩放QDateTimeAxis的TickCount
			# TickCount得自己手动设置
			# 所以放大之后依旧有很多轴，还以为QDateTimeAxis都没有变化呢
			#轴得有个上限，不然缩小了卡死你

			begin=self.chart().axisX().min()
			end=self.chart().axisX().max()
			n=begin.daysTo(end)
			if n>self.xmax_TickCount:
				n=self.xmax_TickCount
			else:
				n+=1
			self.chart().axisX().setTickCount(n)
			return
		
		#shift滚轮左右移动
		elif self.__shift_pressed==True:
			self.chart().scroll(right*self.scroll_step, 0)
			return
		
		#普通缩放模式
		else:
			self.chart().zoom(mFactor)
			
			# 淦！zoom不会自动缩放QDateTimeAxis的TickCount
			# TickCount得自己手动设置
			# 所以放大之后依旧有很多轴，还以为QDateTimeAxis都没有变化呢
			#轴得有个上限，不然缩小了卡死你
			
			n=int(self.chart().axisY().max())-int(self.chart().axisY().min())
			if n>self.ymax_TickCount:
				n=self.ymax_TickCount
			else:
				n+=1
			self.chart().axisY().setTickCount(n)

			begin=self.chart().axisX().min()
			end=self.chart().axisX().max()
			n=begin.daysTo(end)
			if n>self.xmax_TickCount:
				n=self.xmax_TickCount
			else:
				n+=1
			self.chart().axisX().setTickCount(n)
			return
	

	def keyPressEvent(self,event):
		"上下左右移动，加减号缩放"
		super(MyChartView,self).keyPressEvent(event)

		TYPE=event.key()
		if TYPE==Qt.Key_Control:
			self.__ctrl_pressed=True
		elif TYPE==Qt.Key_Shift:
			self.__shift_pressed=True
		elif TYPE==Qt.Key_Alt:
			self.__alt_pressed=True
		else:
			if TYPE==Qt.Key_Plus:
				self.chart().zoomIn()
				
			elif TYPE==Qt.Key_Minus:
				self.chart().zoomOut()
		
			elif TYPE==Qt.Key_Left:
				self.chart().scroll(-self.scroll_step, 0)
				
			elif TYPE==Qt.Key_Right:
				self.chart().scroll(self.scroll_step, 0)
				
			elif TYPE==Qt.Key_Up:
				self.chart().scroll(0, self.scroll_step)
				
			elif TYPE==Qt.Key_Down:
				self.chart().scroll(0, -self.scroll_step)
	
	def keyReleaseEvent(self,event):
		super(MyChartView,self).keyReleaseEvent(event)
		TYPE=event.key()
		if TYPE==Qt.Key_Control:
			self.__ctrl_pressed=False
		elif TYPE==Qt.Key_Shift:
			self.__shift_pressed=False
		elif TYPE==Qt.Key_Alt:
			self.__alt_pressed=False
	
	def mousePressEvent(self, event):
		"鼠标拖动"
		super(MyChartView,self).mousePressEvent(event)
		
		#alt拖动图像不移动，这是为了拖动legend列表
		if event.button() == Qt.LeftButton and self.__alt_pressed==False:
			self.__press_pos = event.pos()

	def mouseReleaseEvent(self, event):
		"鼠标拖动"
		super(MyChartView,self).mouseReleaseEvent(event)
		
		#alt拖动图像不移动，这是为了拖动legend列表
		if event.button() == Qt.LeftButton and self.__alt_pressed==False:
			self.__press_pos = QPoint()

	def mouseMoveEvent(self, event):
		"鼠标拖动"
		super(MyChartView,self).mouseMoveEvent(event)
		
		#alt拖动图像不移动，这是为了拖动legend列表
		if not self.__press_pos.isNull() and self.__alt_pressed==False:
			delta=event.pos() - self.__press_pos
			dx=delta.x()
			dy=delta.y()
			self.chart().scroll(-dx, dy)
			self.__press_pos = event.pos()



class MyTreeWidget(QTreeWidget):
	"RSS Tree用了这个"
	dropped=Signal()
	def __init__(self, parent):
		super(MyTreeWidget, self).__init__(parent)
	
	def dropEvent(self,event):
		super(MyTreeWidget,self).dropEvent(event)
		self.dropped.emit()

class MyLineEditList(QListWidget):
	#diary的文本块拖动得特殊定制！
	#多选的时候不能拖动，单选的时候可以拖动，出去的时候不接受drop in，进来的时候内部又可以drop
	#这东西是一旦DragEnabled==1后，就接受drop in（不管来自外部还是内部，设置了InternalMove都没用）了
	#所以得特殊情况特殊判断
	def __init__(self,parent):
		super(MyLineEditList,self).__init__(parent)
	
	#改变selection
	def mouseReleaseEvent(self, event):
		#drag and drop是一个一个放入的，而rowsMoved这个信号，如果移动了多行，就在第一个放入的时候触发了，导致只有第一个放入的行被正确重排了
		#所以干脆在多选的时候禁止drag and drop，功能不完善总比有bug好一些
		super(MyLineEditList,self).mouseReleaseEvent(event)
		if len([item.row() for item in self.selectedIndexes()])==1:
			self.setDragEnabled(1)
			self.setAcceptDrops(1)
		else:
			self.setDragEnabled(0)
			self.setAcceptDrops(0)
	
	def focusOutEvent(self, event):
		super(MyLineEditList,self).focusOutEvent(event)
		self.setDragEnabled(0)
		self.setAcceptDrops(0)

class MyPlainTextEdit(QPlainTextEdit):
	"""
	A TextEdit editor that sends editingFinished events 
	when the text was changed and focus is lost.
	"""

	editingFinished = Signal()
	receivedFocus = Signal()
	
	def __init__(self, parent):
		super(MyPlainTextEdit, self).__init__(parent)
		self._changed = False
		self.setTabChangesFocus( True )
		self.textChanged.connect( self._handle_text_changed )

	def focusInEvent(self, event):
		super(MyPlainTextEdit, self).focusInEvent( event )
		self.receivedFocus.emit()

	def focusOutEvent(self, event):
		if self._changed:
			self.editingFinished.emit()
		super(MyPlainTextEdit, self).focusOutEvent( event )

	def _handle_text_changed(self):
		self._changed = True

	def setTextChanged(self, state=True):
		self._changed = state

	def setHtml(self, html):
		QtGui.QPlainTextEdit.setHtml(self, html)
		self._changed = False


class MyTabFileLeafList(QListWidget):
	def __init__(self,parent):
		super(MyTabFileLeafList,self).__init__(parent)
		self.parent=parent
		self.setAcceptDrops(False)
		# self.setDragDropMode(QAbstractItemView.InternalMove)
		self.ctrl_pressed=False
		self.alt_pressed=False
	
	def dropEvent(self, event):
		#不让你在内部乱拖！
		QMessageBox.warning(self.parent,"Warning","不要拖文件到叶子区！")
	
	def startDrag(self, actions):
		######################################################################
		#MIME通信规则：
		#text/uri-list: file:///D:/图片/Desktop/52922207bigpolished.jpeg
		######################################################################
		indexes = self.selectedIndexes()
		drag = QDrag(self)
		mime = self.model().mimeData(indexes)
		
		urlList = []
		
		for itemindex in [item.row() for item in self.selectedIndexes()]:
			urlList.append(QUrl("file:///"+self.item(itemindex).toolTip()))
		
		mime.setUrls(urlList)
		drag.setMimeData(mime)
		drag.exec_(actions)
	
	def keyPressEvent(self,event):
		super(MyTabFileLeafList, self).keyPressEvent( event )
		if event.key()==Qt.Key_Control:
			self.ctrl_pressed=True
		if event.key()==Qt.Key_Alt:
			self.alt_pressed=True
	
	def keyReleaseEvent(self,event):
		super(MyTabFileLeafList, self).keyReleaseEvent( event )
		if event.key()==Qt.Key_Control:
			self.ctrl_pressed=False
		if event.key()==Qt.Key_Alt:
			self.alt_pressed=False


class MyConceptLinkedFileList(QListWidget):
	"包括concept linked file区、tab root file区、file manager区"
	dropped=Signal(list)
	enter_pressed=Signal()
	focusouted=Signal()
	focusined=Signal()
	def __init__(self,parent):
		super(MyConceptLinkedFileList,self).__init__(parent)
		self.setAcceptDrops(True)
		self.setDragDropMode(QAbstractItemView.InternalMove)
		self.ctrl_pressed=False
		self.alt_pressed=False
	
	def focusOutEvent(self, event):
		super(MyConceptLinkedFileList,self).focusOutEvent(event)
		self.focusouted.emit()
	
	def focusInEvent(self, event):
		super(MyConceptLinkedFileList,self).focusInEvent(event)
		self.focusined.emit()
	
	def startDrag(self, actions):
		######################################################################
		#MIME通信规则：
		#text/uri-list: file:///D:/图片/Desktop/52922207bigpolished.jpeg
		######################################################################
		indexes = self.selectedIndexes()
		drag = QDrag(self)
		mime = self.model().mimeData(indexes)
		
		urlList = []
		
		for itemindex in [item.row() for item in self.selectedIndexes()]:
			
			urlList.append(QUrl("file:///"+self.item(itemindex).toolTip()))
		
		mime.setUrls(urlList)
		drag.setMimeData(mime)
		drag.exec_(actions)

	def dragEnterEvent(self, event):

		if event.mimeData().hasUrls() or event.mimeData().hasText():
			event.acceptProposedAction()
		else:
			super(MyConceptLinkedFileList,self).dragEnterEvent(event)

	def dragMoveEvent(self, event):
		super(MyConceptLinkedFileList,self).dragMoveEvent(event)

	def dropEvent(self, event):
		
		if event.mimeData().hasUrls():
			event.setDropAction(Qt.CopyAction)
			event.accept()
			links=[]
			for url in event.mimeData().urls():
				url_str=url.toString()
				#注意这里的“|”被toString()解析出来成了%7C，如果是名字、文件路径的话，得用urllib.parse的unquote解码
				
				#如果是本地文件url
				if url_str[:4]=="file":
					url_str=url_str.replace("file:///","")
					
					#如果是内部已有link
					#只有名字中的%7C之类的要解码（导入进来的时候Title中的url编码是被转成utf-8了的），url部分的保持不变
					if "|" in unquote(url_str,'utf-8'):

						#最后一个|前的就是名字
						name=url_str[:url_str.rfind("%7C")]
						name=unquote(name,'utf-8')
						
						url=url_str[url_str.rfind("%7C")+3:]

						url_str=name+"|"+url
						
						links.append(url_str)
					
					#如果是文件url的话全部解码就行了
					else:
						url_str=unquote(url_str,'utf-8')
						links.append(url_str)
				
				#如果是外部link
				#这里十分巧妙！
				#url中的如果有那些特殊字符!|@#$%^&*，就保持%xx的形式，就不会与后面我加上去用来分隔Directory、title、url的特殊符号<和|冲突
				elif url_str[:4]=="http" or url_str[:5]=="https":
					links.append(url_str)
			
			self.dropped.emit(links)
		
		elif event.mimeData().hasText():
			event.setDropAction(Qt.CopyAction)
			event.accept()
			text=event.mimeData().text().strip()
			text=text.split("\n")
			links=[]
			#只接收网页链接
			for i in text:
				i=i.strip()
				if i[:7]=="http://" or i[:8]=="https://":
					links.append(i)
				else:
					continue
					# QMessageBox.warning(self,"Warning","文本导入方式仅支持网页链接！")
			self.dropped.emit(links)
		
		else:
			super(MyConceptLinkedFileList,self).dropEvent(event)
	
	def keyPressEvent(self,event):
		super(MyConceptLinkedFileList, self).keyPressEvent( event )
		if event.key()==Qt.Key_Control:
			self.ctrl_pressed=True
		if event.key()==Qt.Key_Alt:
			self.alt_pressed=True
		#按回车发出enter_press的信号，出去打开文件
		if event.key()==Qt.Key_Return:
			self.enter_pressed.emit()
		
	def keyReleaseEvent(self,event):
		super(MyConceptLinkedFileList, self).keyReleaseEvent( event )
		if event.key()==Qt.Key_Control:
			self.ctrl_pressed=False
		if event.key()==Qt.Key_Alt:
			self.alt_pressed=False


class MyImageViewer(QMainWindow):
	"MyImageViewer(pic_list,index)，传入包含所有url的pic_list，以及双击打开时的index"
	def __init__(self,pic_list,index,maxw,maxh):
		super().__init__()

		self.setWindowTitle("Dongli Teahouse Image Viewer")
		self.setWindowIcon(QIcon(":/icon/holoico.ico"))

		self.pic_list=pic_list
		self.index=index
		self.maxlen=len(pic_list)
		self.maxw=maxw-50
		self.maxh=maxh-50
		self.image_label=QLabel()
		self.setCentralWidget(self.image_label)
		
		#图片允许缩放
		self.image_label.setScaledContents(True)

		self.set_pic(self.pic_list[self.index])

	def set_pic(self,pic_url):
		pix=QPixmap(pic_url)
		self.setWindowTitle("Dongli Teahouse Image Viewer - %s"%pic_url)
		

		w=pix.width()
		h=pix.height()

		if w<self.maxw and h<self.maxh:
			self.setMinimumSize(w,h)
			self.resize(w,h)
			pix=pix.scaled(w,h,Qt.KeepAspectRatio)
			self.image_label.setPixmap(pix)
			return
		
		elif w>=self.maxw:
			k=self.maxw/w
			h=k*h
			w=self.maxw
			#如果h还是过大，再缩h
			if h>=self.maxh:
				
				k=self.maxh/h
				w=k*w
				h=self.maxh

				self.setMinimumSize(w,h)
				self.resize(w,h)
				pix=pix.scaled(w,h,Qt.KeepAspectRatio)
				self.image_label.setPixmap(pix)
				return
			else:
				self.setMinimumSize(w,h)
				self.resize(w,h)
				pix=pix.scaled(w,h,Qt.KeepAspectRatio)
				self.image_label.setPixmap(pix)
				return
		
		elif h>=self.maxh:
			k=self.maxh/h
			w=k*w
			h=self.maxh
			#如果w还是过大，再缩w
			if w>=self.maxw:
				k=self.maxw/w
				h=k*h
				w=self.maxw

				self.setMinimumSize(w,h)
				self.resize(w,h)
				pix=pix.scaled(w,h,Qt.KeepAspectRatio)
				self.image_label.setPixmap(pix)
				return
			else:
				self.setMinimumSize(w,h)
				self.resize(w,h)
				pix=pix.scaled(w,h,Qt.KeepAspectRatio)
				self.image_label.setPixmap(pix)
				return
		
		
	def keyPressEvent(self,event):
		super(MyImageViewer, self).keyPressEvent( event )
		
		#上一张
		if event.key()==Qt.Key_Left or event.key()==Qt.Key_Up:
			if self.index>0:
				self.index-=1
				self.set_pic(self.pic_list[self.index])
		#下一张
		elif event.key()==Qt.Key_Right or event.key()==Qt.Key_Down:
			if self.index<self.maxlen-1:
				self.index+=1
				self.set_pic(self.pic_list[self.index])
			
	def wheelEvent(self,event):
		super(MyImageViewer,self).wheelEvent(event)
		
		xscrolls = event.angleDelta().x()
		yscrolls = event.angleDelta().y()

		#上一张
		if xscrolls>0 or yscrolls>0:
			if self.index>0:
				self.index-=1
				self.set_pic(self.pic_list[self.index])
		#下一张
		elif xscrolls<0 or yscrolls<0:
			if self.index<self.maxlen-1:
				self.index+=1
				self.set_pic(self.pic_list[self.index])








###############################################################################################
###############################################################################################
###############################################################################################
###############################################################################################
###############################################################################################
###############################################################################################

# class WebEnginePage(QWebEnginePage):
# 	def javaScriptConsoleMessage(self, level, msg, line, sourceID):
# 		#重塑这个函数让它不要打印那么多js错误信息出来
# 		pass

# class MyWebBrowser(QWebEngineView):

# 	def __init__(self, parent):
# 		super(MyWebBrowser, self).__init__(parent)
# 		self.setMinimumWidth(200)
# 		
# 		self.load(QUrl("https://www.youtube.com/watch?v=RR0cDQalhus"))
		
# 		#但所幸这里重置了page，上面的网页也就不会显示出来
# 		page=WebEnginePage(self)
# 		self.setPage(page)
		
	
# 	def goto(self,url):
# 		print("qweqwe")
		
# 		# self.load(url)
# 		# self.setUrl(url)

# class MyTextLinkedFileList(QListWidget):
# 	def __init__(self,parent):
# 		super(MyTextLinkedFileList,self).__init__(parent)
# 		self.setAcceptDrops(False)
# 		self.setDragDropMode(QAbstractItemView.InternalMove)
# 		self.ctrl_pressed=False
	
# 	def startDrag(self, actions):
# 		######################################################################
# 		#MIME通信规则：
# 		#text/uri-list: file:///D:/图片/Desktop/52922207bigpolished.jpeg
# 		######################################################################
# 		indexes = self.selectedIndexes()
# 		drag = QDrag(self)
# 		mime = self.model().mimeData(indexes)
		
# 		urlList = []
		
# 		for itemindex in [item.row() for item in self.selectedIndexes()]:
# 			urlList.append(QUrl("file:///"+self.item(itemindex).toolTip()))
		
# 		mime.setUrls(urlList)
# 		drag.setMimeData(mime)
# 		drag.exec_(actions)
	
# 	def keyPressEvent(self,event):
# 		if event.key()==Qt.Key_Control:
# 			self.ctrl_pressed=True
	
# 	def keyReleaseEvent(self,event):
# 		if event.key()==Qt.Key_Control:
# 			self.ctrl_pressed=False


# class MyFileSearchTab(QTableWidget):
# 	dropped=Signal(list)
# 	def __init__(self,parent):
# 		super(MyFileSearchTab,self).__init__(parent)
# 		self.setAcceptDrops(True)
# 		self.setEditTriggers(QAbstractItemView.NoEditTriggers)
		
# 		# self.ctrl_pressed=False

# 	# def startDrag(self, actions):
# 	# 	######################################################################
# 	# 	#MIME通信规则：
# 	# 	#text/uri-list: file:///D:/图片/Desktop/52922207bigpolished.jpeg
# 	# 	######################################################################
# 	# 	indexes = self.selectedIndexes()
# 	# 	drag = QDrag(self)
# 	# 	mime = self.model().mimeData(indexes)
		
# 	# 	urlList = []
		
# 	# 	for itemindex in [item.row() for item in self.selectedIndexes()]:
# 	# 		urlList.append(QUrl("file:///"+self.item(itemindex).toolTip()))
		
# 	# 	mime.setUrls(urlList)
# 	# 	drag.setMimeData(mime)
# 	# 	drag.exec_(actions)

# 	#貌似self.setDragDropMode(QAbstractItemView.NoDragDrop)之后就不接受外部的dropin了，那就动态设置吧
# 	def focusOutEvent(self, event):
# 		super(MyFileSearchTab,self).focusOutEvent(event)
# 		self.setDragDropMode(QAbstractItemView.InternalMove)
	
# 	def focusInEvent(self, event):
# 		super(MyFileSearchTab,self).focusInEvent(event)
# 		self.setDragDropMode(QAbstractItemView.NoDragDrop)


# 	def dragEnterEvent(self, event):
	
# 		if event.mimeData().hasUrls():
# 			event.acceptProposedAction()
# 		else:
# 			super(MyFileSearchTab,self).dragEnterEvent(event)
	
# 	def dropEvent(self, event):
		
# 		if event.mimeData().hasUrls():
# 			event.setDropAction(Qt.CopyAction)
# 			event.accept()
# 			links=[]
# 			for url in event.mimeData().urls():
# 				links.append(str(url.toLocalFile()))
			
# 			self.dropped.emit(links)
# 		else:
# 			super(MyFileSearchTab,self).dropEvent(event)
