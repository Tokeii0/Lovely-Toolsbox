import os
from PySide6.QtCore import QFileInfo
from PySide6.QtWidgets import QFileIconProvider
from PySide6.QtGui import QIcon, QPixmap
from loguru import logger

class IconManager:
    _icon_provider = None

    @classmethod
    def get_icon_provider(cls):
        """获取图标提供者单例"""
        if cls._icon_provider is None:
            cls._icon_provider = QFileIconProvider()
        return cls._icon_provider

    @classmethod
    def get_file_icon(cls, file_path: str, size: int = 32) -> QPixmap:
        """
        获取文件的图标
        
        Args:
            file_path: 文件路径
            size: 图标大小
            
        Returns:
            QPixmap: 文件图标
        """
        try:
            if not os.path.exists(file_path):
                return None

            # 获取文件信息
            file_info = QFileInfo(file_path)
            
            # 获取图标
            icon = cls.get_icon_provider().icon(file_info)
            
            if icon.isNull():
                return None
                
            # 转换为指定大小的QPixmap
            pixmap = icon.pixmap(size, size)
            
            return pixmap

        except Exception as e:
            logger.error(f"获取图标失败: {str(e)}")
            return None
