"""
应用程序样式主题配置
"""

# 主题颜色
COLORS = {
    "primary": "#2979ff",           # 主色调
    "primary_light": "#75a7ff",     # 主色调亮色
    "primary_dark": "#004ecb",      # 主色调暗色
    "secondary": "#651fff",         # 次要色调
    "background": "#ffffff",        # 背景色
    "surface": "#f5f5f5",          # 表面色
    "error": "#B00020",            # 错误色
    "text": "#000000",             # 文本色
    "text_secondary": "#666666",    # 次要文本色
    "border": "#e0e0e0",           # 边框色
    "hover": "#f0f0f0",            # 悬停色
    "selected": "#e8e8e8",         # 选中色
    # macOS 风格的窗口按钮颜色
    "close": "#ff5f57",            # 关闭按钮
    "close_hover": "#ff4444",      # 关闭按钮悬停
    "minimize": "#febc2e",         # 最小化按钮
    "minimize_hover": "#f1b023",   # 最小化按钮悬停
    "maximize": "#28c840",         # 最大化按钮
    "maximize_hover": "#24b539",   # 最大化按钮悬停
}

# 布局尺寸
SIZES = {
    "icon": 32,                    # 图标大小
    "icon_container": 48,          # 图标容器大小
    "tool_item": 100,             # 工具项大小
    "grid": 110,                  # 网格大小
    "spacing": 10,                # 间距
    "margin": 2,                  # 边距
    "window_button": 12,          # 窗口按钮大小
    "window_button_margin": 8,    # 窗口按钮间距
    "window_radius": 10,          # 窗口圆角
}

# 全局样式
GLOBAL_STYLE = """
QWidget {
    background-color: transparent;
}

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
"""

# 主窗口样式
MAIN_WINDOW_STYLE = """
QMainWindow {
    background-color: """ + COLORS["background"] + """;
    border: 1px solid """ + COLORS["border"] + """;
    border-radius: """ + str(SIZES["window_radius"]) + """px;
}
"""

# 工具网格样式
TOOL_GRID_STYLE = """
QListWidget {
    background-color: """ + COLORS["background"] + """;
    border: none;
}

QListWidget::item {
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: 4px;
    padding: 4px;
}

QListWidget::item:hover {
    background-color: """ + COLORS["hover"] + """;
    border: 1px solid """ + COLORS["border"] + """;
}

QListWidget::item:selected {
    background-color: """ + COLORS["selected"] + """;
    border: 1px solid """ + COLORS["border"] + """;
}
"""

# 标签页样式
TAB_STYLE = """
QTabWidget::pane {
    border: none;
    background-color: """ + COLORS["background"] + """;
}

QTabWidget::tab-bar {
    alignment: left;
}

QTabBar::tab {
    background-color: """ + COLORS["surface"] + """;
    color: """ + COLORS["text"] + """;
    min-width: 100px;
    padding: 8px 16px;
    border: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar::tab:hover {
    background-color: """ + COLORS["hover"] + """;
}

QTabBar::tab:selected {
    background-color: """ + COLORS["background"] + """;
    border-bottom: 2px solid """ + COLORS["primary"] + """;
}
"""

# 工具项样式
TOOL_ITEM_STYLE = """
QFrame {
    background-color: transparent;
}

QLabel {
    color: """ + COLORS["text"] + """;
}
"""

# 菜单样式
MENU_STYLE = """
QMenu {
    background-color: """ + COLORS["background"] + """;
    border: 1px solid """ + COLORS["border"] + """;
    padding: 4px;
}

QMenu::item {
    padding: 4px 24px;
    border-radius: 2px;
}

QMenu::item:selected {
    background-color: """ + COLORS["hover"] + """;
}
"""
