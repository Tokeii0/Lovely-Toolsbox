"""
字体配置
"""
from PySide6.QtGui import QFont

class Fonts:
    """字体管理类"""
    FAMILY = "Microsoft YaHei"
    DEFAULT_SIZE = 10
    TITLE_SIZE = 12
    SMALL_SIZE = 9
    
    @classmethod
    def get_default(cls) -> QFont:
        """获取默认字体"""
        font = QFont(cls.FAMILY, cls.DEFAULT_SIZE)
        font.setHintingPreference(QFont.HintingPreference.PreferFullHinting)
        return font
    
    @classmethod
    def get_title(cls) -> QFont:
        """获取标题字体"""
        font = QFont(cls.FAMILY, cls.TITLE_SIZE)
        font.setHintingPreference(QFont.HintingPreference.PreferFullHinting)
        return font
    
    @classmethod
    def get_small(cls) -> QFont:
        """获取小字体"""
        font = QFont(cls.FAMILY, cls.SMALL_SIZE)
        font.setHintingPreference(QFont.HintingPreference.PreferFullHinting)
        return font
