from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTextEdit, QComboBox,
    QMessageBox
)
from ..core.tool_manager import Tool

class ConfigureToolDialog(QDialog):
    def __init__(self, tool: Tool, parent=None, categories=None):
        super().__init__(parent)
        self.tool = tool
        self.categories = categories or []
        self.setup_ui()
        self.load_tool_data()
        
    def setup_ui(self):
        self.setWindowTitle(f"配置工具 - {self.tool.name}")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # 工具名称（只读）
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("工具名称:"))
        self.name_label = QLabel(self.tool.name)
        name_layout.addWidget(self.name_label)
        layout.addLayout(name_layout)
        
        # 工具路径
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("工具路径:"))
        self.path_edit = QLineEdit()
        path_layout.addWidget(self.path_edit)
        layout.addLayout(path_layout)
        
        # 工具分类
        category_layout = QHBoxLayout()
        category_layout.addWidget(QLabel("工具分类:"))
        self.category_combo = QComboBox()
        self.category_combo.setEditable(True)
        self.category_combo.addItems(self.categories)
        category_layout.addWidget(self.category_combo)
        layout.addLayout(category_layout)
        
        # 工具描述
        layout.addWidget(QLabel("工具描述:"))
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        layout.addWidget(self.description_edit)
        
        # 启动命令
        command_layout = QHBoxLayout()
        command_layout.addWidget(QLabel("启动命令:"))
        self.command_edit = QLineEdit()
        command_layout.addWidget(self.command_edit)
        layout.addLayout(command_layout)
        
        # 命令参数
        layout.addWidget(QLabel("命令参数:"))
        self.args_edit = QLineEdit()
        layout.addWidget(self.args_edit)
        
        # 按钮
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("保存")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

    def load_tool_data(self):
        """加载工具数据到界面"""
        self.path_edit.setText(self.tool.path)
        self.category_combo.setCurrentText(self.tool.category)
        self.description_edit.setText(self.tool.description)
        self.command_edit.setText(self.tool.command)
        self.args_edit.setText(" ".join(self.tool.args))

    def get_tool_info(self):
        """获取修改后的工具信息"""
        return {
            "name": self.tool.name,  # 名称不允许修改
            "path": self.path_edit.text(),
            "category": self.category_combo.currentText(),
            "description": self.description_edit.toPlainText(),
            "command": self.command_edit.text(),
            "args": self.args_edit.text().split() if self.args_edit.text() else []
        }

    def validate(self) -> bool:
        """验证输入数据"""
        if not self.path_edit.text():
            QMessageBox.warning(self, "错误", "请输入工具路径")
            return False
        if not self.category_combo.currentText():
            QMessageBox.warning(self, "错误", "请选择或输入工具分类")
            return False
        return True

    def accept(self):
        if self.validate():
            super().accept()
