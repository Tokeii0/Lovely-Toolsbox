from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QStatusBar, QApplication,
    QPushButton, QLabel
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from .tool_grid import ToolGrid
from .properties_dialog import ToolPropertiesDialog
from .title_bar import TitleBar
from ..core.tool_manager import ToolManager
from .style import MAIN_WINDOW_STYLE, TAB_STYLE, GLOBAL_STYLE, TOOL_GRID_STYLE, SIZES, COLORS

class VerticalLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(24, 100)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(self.palette().color(self.foregroundRole()))
        painter.translate(0, self.height())  # 移动到左下角
        painter.rotate(-90)  # 逆时针旋转90度
        rect = self.rect()
        rect.setWidth(self.height())  # 交换宽高
        rect.setHeight(self.width())
        painter.drawText(rect, Qt.AlignCenter, self.text())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tool_manager = ToolManager()
        self.category_buttons = []  # 保存所有分类按钮
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI"""
        # 设置全局样式
        QApplication.instance().setStyleSheet(GLOBAL_STYLE)
        
        # 设置窗口属性和图标
        self.setWindowTitle("Lovely-ToolsBox")
        self.setWindowIcon(QIcon("res/logo.ico"))
        self.setMinimumSize(460, 700)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框窗口
        self.setStyleSheet(MAIN_WINDOW_STYLE)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 创建标题栏
        self.title_bar = TitleBar(self)
        layout.addWidget(self.title_bar)
        
        # 连接标题栏信号
        self.title_bar.minimizeClicked.connect(self.showMinimized)
        self.title_bar.maximizeClicked.connect(self.toggle_maximize)
        self.title_bar.closeClicked.connect(self.close)
        self.title_bar.searchTextChanged.connect(self.filter_tools)
        
        # 创建内容区域
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(SIZES["margin"], SIZES["margin"], 
                                        SIZES["margin"], SIZES["margin"])
        layout.addWidget(content_widget)
        
        # 创建左侧按钮栏
        button_widget = QWidget()
        button_widget.setObjectName("button_widget")  # 为按钮栏添加名称
        button_layout = QVBoxLayout(button_widget)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(2)
        button_layout.setAlignment(Qt.AlignTop)  # 设置顶部对齐
        button_widget.setFixedWidth(100)
        content_layout.addWidget(button_widget)
        
        # 创建堆叠部件
        self.stack_widget = QStackedWidget()
        content_layout.addWidget(self.stack_widget)
        
        # 设置按钮样式
        self.button_style = """
            QPushButton {
                padding: 8px;
                border: 1px solid """ + COLORS["border"] + """;
                border-radius: 4px;
                background-color: transparent;
                text-align: left;
                min-height: 32px;
            }
            QPushButton:checked {
                background-color: """ + COLORS["selected"] + """;
            }
            QPushButton:hover:!checked {
                background-color: """ + COLORS["hover"] + """;
            }
        """
        
        # 创建工具网格和按钮
        self.create_tool_grids(button_layout)
        
        # 创建状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        # 加载工具
        self.load_tools()
        
    def create_tool_grids(self, button_layout):
        """创建工具网格"""
        # 创建所有工具的网格
        self.all_tools_grid = ToolGrid()
        self.all_tools_grid.toolDoubleClicked.connect(self.launch_tool)
        self.all_tools_grid.importToolRequested.connect(self.import_tool)
        self.all_tools_grid.refreshRequested.connect(self.refresh_tools)
        self.all_tools_grid.toolPropertiesRequested.connect(self.show_tool_properties)
        self.all_tools_grid.launchToolRequested.connect(self.launch_tool)
        self.all_tools_grid.toolDeleteRequested.connect(self.delete_tool)
        self.all_tools_grid.setStyleSheet(TOOL_GRID_STYLE)
        
        # 添加"所有工具"按钮和网格
        all_tools_btn = QPushButton("所有工具")
        all_tools_btn.setCheckable(True)
        all_tools_btn.setChecked(True)
        all_tools_btn.setStyleSheet(self.button_style)
        all_tools_btn.clicked.connect(lambda: self.switch_category(all_tools_btn, self.all_tools_grid))
        button_layout.addWidget(all_tools_btn)
        self.stack_widget.addWidget(self.all_tools_grid)
        self.category_buttons.append(all_tools_btn)
        
        # 为每个类别创建网格和按钮
        self.category_grids = {}
        for category in self.tool_manager.get_categories():
            grid = ToolGrid()
            grid.toolDoubleClicked.connect(self.launch_tool)
            grid.importToolRequested.connect(self.import_tool)
            grid.refreshRequested.connect(self.refresh_tools)
            grid.toolPropertiesRequested.connect(self.show_tool_properties)
            grid.launchToolRequested.connect(self.launch_tool)
            grid.toolDeleteRequested.connect(self.delete_tool)
            grid.setStyleSheet(TOOL_GRID_STYLE)
            self.category_grids[category] = grid
            
            # 添加类别按钮和网格
            btn = QPushButton(category)
            btn.setCheckable(True)
            btn.setStyleSheet(self.button_style)
            btn.clicked.connect(lambda checked, b=btn, g=grid: self.switch_category(b, g))
            button_layout.addWidget(btn)
            self.stack_widget.addWidget(grid)
            self.category_buttons.append(btn)
            
        # 添加弹簧
        button_layout.addStretch()
        
    def switch_category(self, clicked_button, grid):
        """切换分类"""
        # 取消其他按钮的选中状态
        for btn in self.category_buttons:
            if btn != clicked_button:
                btn.setChecked(False)
        
        # 确保当前按钮被选中
        clicked_button.setChecked(True)
        self.stack_widget.setCurrentWidget(grid)
        
    def refresh_categories(self):
        """刷新分类"""
        # 清除旧的按钮和网格
        for btn in self.category_buttons:
            btn.deleteLater()
        self.category_buttons.clear()
        
        for grid in self.category_grids.values():
            grid.deleteLater()
        self.category_grids.clear()
        
        # 获取现有的布局
        button_widget = self.findChild(QWidget, "button_widget")
        button_layout = button_widget.layout()
        
        # 清除布局中的所有项目，但保留布局本身
        while button_layout.count():
            item = button_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # 使用现有的布局重新创建按钮和网格
        self.create_tool_grids(button_layout)
        
    def import_tool(self):
        """导入工具"""
        dialog = ToolPropertiesDialog(self)
        if dialog.exec():
            tool = dialog.get_tool()
            self.tool_manager.add_tool(tool)
            self.refresh_tools()  # 先刷新工具
            self.refresh_categories()  # 然后刷新分类
            self.statusBar.showMessage(f"工具 {tool.name} 导入成功", 3000)
            return True
        return False
    
    def load_tools(self):
        """加载工具"""
        # 清空所有网格
        self.all_tools_grid.clear()
        for grid in self.category_grids.values():
            grid.clear()
            
        # 加载工具
        for tool in self.tool_manager.get_tools():
            # 添加到所有工具网格
            self.all_tools_grid.add_tool(tool)
            
            # 添加到对应类别的网格
            if tool.category in self.category_grids:
                self.category_grids[tool.category].add_tool(tool)
    
    def filter_tools(self, text: str):
        """过滤工具"""
        text = text.lower()
        
        # 过滤所有工具网格
        for i in range(self.all_tools_grid.count()):
            item = self.all_tools_grid.item(i)
            tool_name = item.data(Qt.UserRole)
            tool = self.tool_manager.get_tool(tool_name)
            
            if tool:
                match = (
                    text in tool.name.lower() or
                    text in tool.description.lower() or
                    text in tool.category.lower()
                )
                item.setHidden(not match)
                
        # 过滤分类网格
        for grid in self.category_grids.values():
            for i in range(grid.count()):
                item = grid.item(i)
                tool_name = item.data(Qt.UserRole)
                tool = self.tool_manager.get_tool(tool_name)
                
                if tool:
                    match = (
                        text in tool.name.lower() or
                        text in tool.description.lower() or
                        text in tool.category.lower()
                    )
                    item.setHidden(not match)
    
    def toggle_maximize(self):
        """切换最大化状态"""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
    
    def launch_tool(self, tool_name):
        """启动工具"""
        tool = self.tool_manager.get_tool(tool_name)
        if tool:
            success = tool.launch()
            if success:
                self.statusBar.showMessage(f"已启动工具：{tool_name}", 3000)
            else:
                self.statusBar.showMessage(f"工具启动失败：{tool_name}", 3000)
                
    def show_tool_properties(self, tool_name):
        """显示工具属性"""
        tool = self.tool_manager.get_tool(tool_name)
        if tool:
            dialog = ToolPropertiesDialog(self, tool)
            if dialog.exec():
                updated_tool = dialog.get_tool()
                self.tool_manager.update_tool(tool_name, updated_tool)
                self.refresh_tools()
                self.statusBar.showMessage("工具属性已更新", 3000)
                
    def delete_tool(self, tool_name):
        """删除工具"""
        # 从工具管理器中删除
        self.tool_manager.remove_tool(tool_name)
        # 保存更改
        self.tool_manager.save_tools()
        # 刷新显示
        self.refresh_tools()
    
    def refresh_tools(self):
        """刷新工具列表"""
        self.tool_manager.load_tools()
        self.load_tools()
        self.statusBar.showMessage("工具列表已刷新", 3000)
