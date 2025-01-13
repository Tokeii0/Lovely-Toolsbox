from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon, QPixmap
from .style import COLORS, SIZES
from .fonts import Fonts

class WindowButton(QPushButton):
    """窗口控制按钮"""
    def __init__(self, color, hover_color, parent=None):
        super().__init__(parent)
        self.color = color
        self.hover_color = hover_color
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI"""
        self.setFixedSize(SIZES["window_button"], SIZES["window_button"])
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.color};
                border: none;
                border-radius: {SIZES["window_button"] // 2}px;
            }}
            QPushButton:hover {{
                background-color: {self.hover_color};
            }}
        """)

class SearchBox(QLineEdit):
    """搜索框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        # 设置样式
        self.setPlaceholderText("搜索工具...")
        self.setFixedWidth(200)
        
        # 设置字体
        self.setFont(Fonts.get_default())
        
        self.setStyleSheet("""
            QLineEdit {
                border: 1px solid """ + COLORS["border"] + """;
                border-radius: 15px;
                padding: 5px 10px;
                background: """ + COLORS["background"] + """;
                selection-background-color: """ + COLORS["primary_light"] + """;
            }
            QLineEdit:focus {
                border: 1px solid """ + COLORS["primary"] + """;
            }
        """)

class TitleBar(QWidget):
    """自定义标题栏"""
    # 定义信号
    minimizeClicked = Signal()
    maximizeClicked = Signal()
    closeClicked = Signal()
    searchTextChanged = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.is_maximized = False
        self.pressing = False
        self.start_pos = None
        self.window_pos = None
        
    def setup_ui(self):
        # 设置样式
        self.setFixedHeight(40)
        self.setStyleSheet("background: transparent;")
        
        # 创建水平布局
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(SIZES["window_button_margin"])
        
        # 窗口控制按钮
        self.close_button = WindowButton(COLORS["close"], COLORS["close_hover"])
        self.min_button = WindowButton(COLORS["minimize"], COLORS["minimize_hover"])
        self.max_button = WindowButton(COLORS["maximize"], COLORS["maximize_hover"])
        
        # 添加窗口按钮
        button_layout = QHBoxLayout()
        button_layout.setSpacing(SIZES["window_button_margin"])
        button_layout.addWidget(self.close_button)
        button_layout.addWidget(self.min_button)
        button_layout.addWidget(self.max_button)
        layout.addLayout(button_layout)
        
        # 添加图标
        icon_label = QLabel()
        icon = QIcon("res/logo.ico")
        pixmap = icon.pixmap(24, 24)  # 设置图标大小为24x24
        icon_label.setPixmap(pixmap)
        layout.addWidget(icon_label)
        
        # 添加标题
        title_label = QLabel("Lovely-ToolsBox")
        title_label.setStyleSheet(f"""
            color: {COLORS["text"]};
            font-size: 14px;
            font-weight: bold;
            margin-left: 5px;
        """)
        layout.addWidget(title_label)
        
        # 弹性空间
        layout.addStretch()
        
        # 添加搜索框
        self.search_box = SearchBox()
        self.search_box.textChanged.connect(self.searchTextChanged.emit)
        layout.addWidget(self.search_box)
            
        # 连接信号
        self.min_button.clicked.connect(self.minimizeClicked.emit)
        self.max_button.clicked.connect(self.toggle_maximize)
        self.close_button.clicked.connect(self.closeClicked.emit)
        
    def toggle_maximize(self):
        """切换最大化状态"""
        self.is_maximized = not self.is_maximized
        self.maximizeClicked.emit()
        
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self.pressing = True
            self.start_pos = event.globalPosition().toPoint()
            window = self.window()
            if window:
                self.window_pos = window.pos()
            
    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if self.pressing and self.start_pos and self.window_pos:
            if not self.is_maximized:
                window = self.window()
                if window:
                    diff = event.globalPosition().toPoint() - self.start_pos
                    window.move(self.window_pos + diff)
                
    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        self.pressing = False
        self.start_pos = None
        self.window_pos = None
            
    def mouseDoubleClickEvent(self, event):
        """鼠标双击事件"""
        if event.button() == Qt.LeftButton:
            self.toggle_maximize()
