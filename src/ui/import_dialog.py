from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QFileDialog, QComboBox,
    QMessageBox
)
from PySide6.QtCore import Qt
from pathlib import Path

class ImportToolDialog(QDialog):
    def __init__(self, parent=None, categories=None):
        super().__init__(parent)
        self.categories = categories or []
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("导入工具")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # 工具名称
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("工具名称:"))
        self.name_edit = QLineEdit()
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)
        
        # 工具路径
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("工具路径:"))
        self.path_edit = QLineEdit()
        path_layout.addWidget(self.path_edit)
        self.browse_btn = QPushButton("浏览...")
        self.browse_btn.clicked.connect(self.browse_file)
        path_layout.addWidget(self.browse_btn)
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
        
        # 启动命令（可选）
        command_layout = QHBoxLayout()
        command_layout.addWidget(QLabel("启动命令:"))
        self.command_edit = QLineEdit()
        self.command_edit.setPlaceholderText("可选，默认使用工具路径")
        command_layout.addWidget(self.command_edit)
        layout.addLayout(command_layout)
        
        # 命令参数（可选）
        layout.addWidget(QLabel("命令参数:"))
        self.args_edit = QLineEdit()
        self.args_edit.setPlaceholderText("可选，用空格分隔多个参数")
        layout.addWidget(self.args_edit)
        
        # 按钮
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("确定")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择工具文件",
            str(Path.home()),
            "所有文件 (*.*)"
        )
        if file_path:
            self.path_edit.setText(file_path)
            # 如果名称为空，使用文件名作为工具名称
            if not self.name_edit.text():
                self.name_edit.setText(Path(file_path).stem)

    def get_tool_info(self):
        """获取用户输入的工具信息"""
        args = self.args_edit.text().split() if self.args_edit.text() else []
        return {
            "name": self.name_edit.text(),
            "path": self.path_edit.text(),
            "category": self.category_combo.currentText(),
            "description": self.description_edit.toPlainText(),
            "command": self.command_edit.text(),
            "args": args
        }

    def validate(self) -> bool:
        """验证输入数据"""
        if not self.name_edit.text():
            QMessageBox.warning(self, "错误", "请输入工具名称")
            return False
        if not self.path_edit.text():
            QMessageBox.warning(self, "错误", "请选择工具文件")
            return False
        if not self.category_combo.currentText():
            QMessageBox.warning(self, "错误", "请选择或输入工具分类")
            return False
        if not Path(self.path_edit.text()).exists():
            QMessageBox.warning(self, "错误", "工具文件不存在")
            return False
        return True

    def accept(self):
        if self.validate():
            super().accept()
