from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, 
    QLineEdit, QTextEdit, QPushButton,
    QDialogButtonBox, QFileDialog
)
from PySide6.QtCore import Qt
from ..core.tool import Tool
from .fonts import Fonts
from .style import COLORS

class ToolPropertiesDialog(QDialog):
    """工具属性对话框"""
    def __init__(self, parent=None, tool=None):
        super().__init__(parent)
        self.tool = tool
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI"""
        # 设置窗口标题和样式
        self.setWindowTitle("导入工具" if not self.tool else f"属性 - {self.tool.name}")
        self.setMinimumWidth(400)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {COLORS["background"]};
                color: {COLORS["text"]};
            }}
            QLineEdit, QTextEdit {{
                background-color: {COLORS["surface"]};
                color: {COLORS["text"]};
                border: 1px solid {COLORS["border"]};
                border-radius: 4px;
                padding: 4px;
            }}
            QLineEdit:focus, QTextEdit:focus {{
                border: 1px solid {COLORS["primary"]};
            }}
            QPushButton {{
                background-color: {COLORS["surface"]};
                color: {COLORS["text"]};
                border: 1px solid {COLORS["border"]};
                border-radius: 4px;
                padding: 4px 8px;
            }}
            QPushButton:hover {{
                background-color: {COLORS["hover"]};
            }}
            QPushButton:pressed {{
                background-color: {COLORS["selected"]};
            }}
        """)
        
        # 设置字体
        self.setFont(Fonts.get_default())
        
        # 创建布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(8)
        
        # 创建输入控件
        self.name_edit = QLineEdit()
        self.path_edit = QLineEdit()
        self.category_edit = QLineEdit()
        self.description_edit = QTextEdit()
        self.description_edit.setMinimumHeight(80)
        self.command_edit = QLineEdit()
        self.args_edit = QLineEdit()
        self.work_dir_edit = QLineEdit()
        
        # 添加浏览按钮
        browse_button = QPushButton("浏览...")
        browse_button.clicked.connect(self.browse_file)
        
        path_layout = QVBoxLayout()
        path_layout.setSpacing(4)
        path_layout.addWidget(self.path_edit)
        path_layout.addWidget(browse_button)
        
        # 添加到表单布局
        form_layout.addRow("名称:", self.name_edit)
        form_layout.addRow("路径:", path_layout)
        form_layout.addRow("类别:", self.category_edit)
        form_layout.addRow("描述:", self.description_edit)
        form_layout.addRow("命令:", self.command_edit)
        form_layout.addRow("参数:", self.args_edit)
        form_layout.addRow("工作目录:", self.work_dir_edit)
        
        # 添加表单布局
        layout.addLayout(form_layout)
        
        # 添加按钮
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_box.button(QDialogButtonBox.Ok).setText("确定")
        button_box.button(QDialogButtonBox.Cancel).setText("取消")
        layout.addWidget(button_box)
        
        # 如果是编辑模式，填充数据
        if self.tool:
            self.name_edit.setText(self.tool.name)
            self.path_edit.setText(self.tool.path)
            self.category_edit.setText(self.tool.category)
            self.description_edit.setText(self.tool.description)
            self.command_edit.setText(self.tool.command)
            self.args_edit.setText(" ".join(self.tool.args or []))
            self.work_dir_edit.setText(self.tool.work_dir)
            
    def browse_file(self):
        """浏览文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择工具", "", 
            "所有文件 (*);;可执行文件 (*.exe);;Python文件 (*.py)"
        )
        if file_path:
            self.path_edit.setText(file_path)
            # 如果名称为空，使用文件名作为工具名
            if not self.name_edit.text():
                self.name_edit.setText(file_path.split("/")[-1].split("\\")[-1])
            
    def get_tool(self) -> Tool:
        """获取工具数据"""
        return Tool(
            name=self.name_edit.text(),
            path=self.path_edit.text(),
            category=self.category_edit.text() or "默认",
            description=self.description_edit.toPlainText(),
            command=self.command_edit.text(),
            args=self.args_edit.text().split() if self.args_edit.text() else [],
            work_dir=self.work_dir_edit.text()
        )
