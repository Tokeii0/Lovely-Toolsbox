import os
import subprocess
from typing import Dict, List

class Tool:
    """工具类"""
    def __init__(self, name: str, path: str, category: str = "默认", 
                 description: str = "", command: str = "", 
                 args: List[str] = None, work_dir: str = ""):
        self.name = name
        self.path = path
        self.category = category
        self.description = description
        self.command = command or path
        self.args = args or []
        self.work_dir = work_dir or os.path.dirname(path)
        
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "name": self.name,
            "path": self.path,
            "category": self.category,
            "description": self.description,
            "command": self.command,
            "args": self.args,
            "work_dir": self.work_dir
        }
        
    @classmethod
    def from_dict(cls, data: Dict) -> 'Tool':
        """从字典创建工具"""
        return cls(
            name=data["name"],
            path=data["path"],
            category=data.get("category", "默认"),
            description=data.get("description", ""),
            command=data.get("command", ""),
            args=data.get("args", []),
            work_dir=data.get("work_dir", "")
        )
        
    def launch(self) -> bool:
        """启动工具"""
        try:
            # 获取工作目录
            work_dir = self.work_dir or os.path.dirname(self.path)
            
            # 如果是Python文件
            if self.path.endswith('.py'):
                cmd = ['python', self.path] + self.args
            # 如果是可执行文件
            elif self.path.endswith('.exe'):
                cmd = [self.path] + self.args
            # 其他情况，使用command
            else:
                cmd = [self.command] + self.args
                
            # 启动进程
            subprocess.Popen(
                cmd,
                cwd=work_dir,
                shell=True,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            return True
        except Exception as e:
            print(f"启动工具失败: {str(e)}")
            return False
