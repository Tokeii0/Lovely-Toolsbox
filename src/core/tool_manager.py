import os
import json
from pathlib import Path
from typing import Dict, List, Optional
from .tool import Tool

class ToolManager:
    """工具管理器"""
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self.config_dir = Path("config")
        self.tools_file = self.config_dir / "tools.json"
        self.load_tools()
        
    def load_tools(self):
        """加载工具配置"""
        # 确保配置目录存在
        self.config_dir.mkdir(exist_ok=True)
        
        # 如果配置文件不存在，创建空文件
        if not self.tools_file.exists():
            self.save_tools()
            return
            
        try:
            # 读取工具配置
            with open(self.tools_file, 'r', encoding='utf-8') as f:
                tools_data = json.load(f)
                
            # 清空当前工具列表
            self.tools.clear()
            
            # 如果是列表格式，转换为字典格式
            if isinstance(tools_data, list):
                tools_data = {item['name']: item for item in tools_data}
                
            # 加载工具
            for name, data in tools_data.items():
                self.tools[name] = Tool.from_dict(data)
                
        except Exception as e:
            print(f"加载工具配置失败: {e}")
            # 如果加载失败，创建空配置
            self.tools.clear()
            self.save_tools()
            
    def save_tools(self):
        """保存工具配置"""
        try:
            # 转换工具为字典
            tools_data = {}
            for name, tool in self.tools.items():
                tools_data[name] = tool.to_dict()
                
            # 保存到文件
            with open(self.tools_file, 'w', encoding='utf-8') as f:
                json.dump(tools_data, f, ensure_ascii=False, indent=4)
                
        except Exception as e:
            print(f"保存工具配置失败: {e}")
            
    def add_tool(self, tool: Tool):
        """添加工具"""
        self.tools[tool.name] = tool
        self.save_tools()
        
    def remove_tool(self, name: str):
        """移除工具"""
        if name in self.tools:
            del self.tools[name]
            self.save_tools()
            
    def update_tool(self, name: str, tool: Tool):
        """更新工具"""
        if name in self.tools:
            self.tools[name] = tool
            self.save_tools()
            
    def get_tool(self, name: str) -> Optional[Tool]:
        """获取工具"""
        return self.tools.get(name)
        
    def get_tools(self) -> List[Tool]:
        """获取所有工具"""
        return list(self.tools.values())
        
    def get_categories(self) -> List[str]:
        """获取所有类别"""
        categories = set()
        for tool in self.tools.values():
            categories.add(tool.category)
        return sorted(list(categories))
