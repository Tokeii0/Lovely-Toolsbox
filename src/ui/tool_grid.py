from PySide6.QtWidgets import QListWidget, QListWidgetItem, QLabel, QVBoxLayout, QWidget, QMenu, QGridLayout
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon
from .style import COLORS, SIZES, TOOL_GRID_STYLE
from .fonts import Fonts
from ..utils.icon_manager import IconManager

class ToolItem(QWidget):
    """工具项组件"""
    def __init__(self, tool, parent=None):
        super().__init__(parent)
        self.tool = tool
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI"""
        # 使用网格布局
        layout = QGridLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)
        
        # 图标标签
        icon_label = QLabel()
        icon_label.setFixedSize(SIZES["icon"], SIZES["icon"])
        pixmap = IconManager.get_file_icon(self.tool.path, SIZES["icon"])
        if pixmap and not pixmap.isNull():
            icon_label.setPixmap(pixmap)
            icon_label.setScaledContents(True)
        else:
            icon_label.setText("🔧")
            icon_label.setStyleSheet("""
                QLabel {
                    font-size: 24px;
                    qproperty-alignment: AlignCenter;
                }
            """)
        
        # 名称标签
        name_label = QLabel(self.tool.name)
        name_label.setWordWrap(True)
        name_label.setFixedWidth(SIZES["tool_item"] - 16)  # 减去左右边距
        name_label.setStyleSheet("""
            QLabel {
                qproperty-alignment: AlignCenter;
                padding: 2px;
            }
        """)
        name_label.setFont(Fonts.get_default())
        
        # 添加到布局
        layout.addWidget(icon_label, 0, 0, 1, 1, Qt.AlignCenter)
        layout.addWidget(name_label, 1, 0, 1, 1, Qt.AlignCenter)
        
        # 设置行列拉伸
        layout.setRowStretch(0, 2)  # 图标占更多空间
        layout.setRowStretch(1, 1)  # 文字占较少空间

class ToolGrid(QListWidget):
    """工具网格"""
    toolDoubleClicked = Signal(str)  # 工具双击信号
    importToolRequested = Signal()   # 导入工具信号
    refreshRequested = Signal()      # 刷新信号
    toolPropertiesRequested = Signal(str)  # 工具属性信号
    launchToolRequested = Signal(str)      # 启动工具信号
    toolDeleteRequested = Signal(str)      # 删除工具信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI"""
        self.setViewMode(QListWidget.IconMode)
        self.setIconSize(QSize(SIZES["icon"], SIZES["icon"]))
        self.setSpacing(SIZES["spacing"])
        self.setResizeMode(QListWidget.Adjust)
        self.setMovement(QListWidget.Static)
        self.setUniformItemSizes(True)
        self.setStyleSheet(TOOL_GRID_STYLE)
        
        # 设置网格大小
        self.setGridSize(QSize(SIZES["grid"], SIZES["grid"]))
        
        # 设置字体
        self.setFont(Fonts.get_default())
        
        # 启用上下文菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
    def add_tool(self, tool):
        """添加工具到网格"""
        # 创建列表项
        item = QListWidgetItem(self)
        item.setSizeHint(QSize(SIZES["tool_item"], SIZES["tool_item"]))
        
        # 创建工具项组件
        tool_item = ToolItem(tool)
        
        # 设置数据
        item.setData(Qt.UserRole, tool.name)
        
        # 添加到网格
        self.setItemWidget(item, tool_item)
        
    def mouseDoubleClickEvent(self, event):
        """鼠标双击事件"""
        item = self.itemAt(event.pos())
        if item:
            tool_name = item.data(Qt.UserRole)
            self.launchToolRequested.emit(tool_name)
            
    def show_context_menu(self, pos):
        """显示上下文菜单"""
        menu = QMenu(self)
        menu.setFont(Fonts.get_default())
        menu.setStyleSheet("""
            QMenu {
                background-color: """ + COLORS["background"] + """;
                border: 1px solid """ + COLORS["border"] + """;
                padding: 5px;
            }
            QMenu::item {
                padding: 5px 20px;
                border-radius: 2px;
            }
            QMenu::item:selected {
                background-color: """ + COLORS["hover"] + """;
            }
        """)
        
        # 获取点击位置的项
        item = self.itemAt(pos)
        
        if item:
            # 如果点击在工具项上
            tool_name = item.data(Qt.UserRole)
            launch_action = menu.addAction("启动")
            launch_action.triggered.connect(
                lambda: self.launchToolRequested.emit(tool_name)
            )
            properties_action = menu.addAction("属性")
            properties_action.triggered.connect(
                lambda: self.toolPropertiesRequested.emit(tool_name)
            )
            
            menu.addSeparator()
            delete_action = menu.addAction("删除")
            delete_action.triggered.connect(
                lambda: self.remove_tool(tool_name)
            )
        
        # 无论是否点击在工具项上，都显示这些选项
        menu.addSeparator()
        import_action = menu.addAction("导入工具")
        import_action.triggered.connect(self.importToolRequested.emit)
        
        refresh_action = menu.addAction("刷新")
        refresh_action.triggered.connect(self.refreshRequested.emit)
        
        menu.exec_(self.viewport().mapToGlobal(pos))
        
    def remove_tool(self, tool_name):
        """删除工具"""
        # 发送删除信号
        self.toolDeleteRequested.emit(tool_name)
        # 找到对应的项并删除
        for i in range(self.count()):
            item = self.item(i)
            if item.data(Qt.UserRole) == tool_name:
                self.takeItem(i)
                break
