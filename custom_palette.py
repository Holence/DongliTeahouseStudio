from PySide2.QtGui import QPalette,QColor
from PySide2.QtCore import Qt


class MyDarkPalette(QPalette):
	"""Dark palette for a Qt application meant to be used with the Fusion theme."""
	def __init__(self):
		super().__init__()
		self.setColor(QPalette.Window, QColor(53, 53, 53))
		self.setColor(QPalette.WindowText, Qt.white)
		self.setColor(QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127))
		self.setColor(QPalette.Base, QColor(42, 42, 42))
		self.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
		self.setColor(QPalette.ToolTipBase, Qt.white)
		self.setColor(QPalette.ToolTipText, Qt.white)
		self.setColor(QPalette.Text, Qt.white)
		self.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127))
		self.setColor(QPalette.Dark, QColor(35, 35, 35))
		self.setColor(QPalette.Shadow, QColor(20, 20, 20))
		self.setColor(QPalette.Button, QColor(53, 53, 53))
		self.setColor(QPalette.ButtonText, Qt.white)
		self.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127))
		self.setColor(QPalette.BrightText, Qt.red)
		self.setColor(QPalette.Link, QColor(42, 130, 218))
		self.setColor(QPalette.Highlight, QColor(42, 130, 218))
		self.setColor(QPalette.Disabled, QPalette.Highlight, QColor(80, 80, 80))
		self.setColor(QPalette.HighlightedText, Qt.white)
		self.setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(127, 127, 127))
