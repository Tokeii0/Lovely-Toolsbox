from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLineEdit, QComboBox,
    QPushButton
)
from PySide6.QtCore import Signal

class SearchWidget(QWidget):
    """搜索工具栏"""
    
    searchRequested = Signal(str, str)  # 信号：搜索文本, 搜索类型

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 搜索类型选择
        self.search_type = QComboBox()
        self.search_type.addItems(["全部", "工具名", "描述", "分类"])
        layout.addWidget(self.search_type)
        
        # 搜索输入框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索工具...")
        self.search_input.textChanged.connect(self.on_search_changed)
        layout.addWidget(self.search_input)
        
        # 搜索按钮
        self.search_button = QPushButton("搜索")
        self.search_button.clicked.connect(self.on_search_clicked)
        layout.addWidget(self.search_button)
        
        # 清除按钮
        self.clear_button = QPushButton("清除")
        self.clear_button.clicked.connect(self.clear_search)
        layout.addWidget(self.clear_button)
        
    def on_search_changed(self, text: str):
        """搜索文本改变时触发搜索"""
        self.searchRequested.emit(text, self.search_type.currentText())
        
    def on_search_clicked(self):
        """点击搜索按钮时触发搜索"""
        self.searchRequested.emit(
            self.search_input.text(),
            self.search_type.currentText()
        )
        
    def clear_search(self):
        """清除搜索"""
        self.search_input.clear()
        self.search_type.setCurrentText("全部")
