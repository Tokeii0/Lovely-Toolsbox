import sys
import os
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication, QIcon,QAction
from src.ui.main_window import MainWindow
from src.ui.fonts import Fonts

def main():
    # 设置高DPI支持
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    
    # 设置应用程序级别的字体
    app.setFont(Fonts.get_default())
    
    # 创建系统托盘图标
    tray_icon = QSystemTrayIcon()
    tray_icon.setIcon(QIcon("res/logo.ico"))
    
    # 创建托盘菜单
    tray_menu = QMenu()
    show_action = QAction("显示", app)
    quit_action = QAction("退出", app)
    tray_menu.addAction(show_action)
    tray_menu.addAction(quit_action)
    tray_icon.setContextMenu(tray_menu)
    
    window = MainWindow()
    window.show()
    
    # 连接信号
    show_action.triggered.connect(window.show)
    quit_action.triggered.connect(app.quit)
    tray_icon.activated.connect(lambda reason: window.show() if reason == QSystemTrayIcon.ActivationReason.DoubleClick else None)
    
    # 显示托盘图标
    tray_icon.show()
    
    return app.exec()

if __name__ == '__main__':
    main()
