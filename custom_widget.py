# -*- coding: utf-8 -*-

import os

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


import resource_rc

class MyTreeWidget(QTreeWidget):
	dropped=Signal()
	def __init__(self, parent):
		super(MyTreeWidget, self).__init__(parent)
	
	def dropEvent(self,event):
		super(MyTreeWidget,self).dropEvent(event)
		self.dropped.emit()


# class WebEnginePage(QWebEnginePage):
# 	def javaScriptConsoleMessage(self, level, msg, line, sourceID):
# 		#重塑这个函数让它不要打印那么多js错误信息出来
# 		pass

# class MyWebBrowser(QWebEngineView):
# 	def __init__(self, parent):
# 		super(MyWebBrowser, self).__init__(parent)
# 		self.setMinimumWidth(200)
# 		###不知道为什么，如果这里不加一句load，打开部分网页就会立刻崩溃
# 		self.load(QUrl("https://www.youtube.com/watch?v=RR0cDQalhus"))
		
# 		#但所幸这里重置了page，上面的网页也就不会显示出来
# 		page=WebEnginePage(self)
# 		self.setPage(page)
		
	
	# def goto(self,url):
	# 	print("qweqwe")
		
	# 	# self.load(url)
	# 	# self.setUrl(url)

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
	
	def keyReleaseEvent(self,event):
		super(MyTabFileLeafList, self).keyReleaseEvent( event )
		if event.key()==Qt.Key_Control:
			self.ctrl_pressed=False




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

		if event.mimeData().hasUrls():
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
				#如果是本地文件url
				if url_str[:4]=="file":
					links.append(str(url.toLocalFile()))
				#如果是网页url
				elif url_str[:4]=="http" or url_str[:5]=="https":
					links.append(url_str)
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
		
		
	
	def wheelEvent(self,event):
		super(MyImageViewer,self).wheelEvent(event)
		
		xscrolls = event.angleDelta().x()
		yscrolls = event.angleDelta().y()

		#下一张
		if xscrolls<0 or yscrolls<0:
			if self.index<self.maxlen-1:
				self.index+=1
				self.set_pic(self.pic_list[self.index])
		#上一张
		elif xscrolls>0 or yscrolls>0:
			if self.index>0:
				self.index-=1
				self.set_pic(self.pic_list[self.index])
			

###############################################################################################
###############################################################################################
###############################################################################################
###############################################################################################
###############################################################################################
###############################################################################################

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
