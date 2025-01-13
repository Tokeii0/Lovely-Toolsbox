import subprocess
import sys
from pathlib import Path
from typing import List, Optional
from loguru import logger

class ToolLauncher:
    @staticmethod
    def launch_tool(command: str, args: List[str] = None, cwd: Optional[str] = None) -> subprocess.Popen:
        """
        启动工具
        
        Args:
            command: 工具命令或路径
            args: 命令行参数列表
            cwd: 工作目录
        
        Returns:
            subprocess.Popen: 启动的进程对象
        """
        try:
            # 如果没有指定工作目录，使用工具所在目录
            if not cwd and command:
                cwd = str(Path(command).parent)

            # 准备完整的命令
            full_command = [command]
            if args:
                full_command.extend(args)

            # 在Windows上，如果是.py文件，使用python解释器运行
            if sys.platform == 'win32' and command.endswith('.py'):
                full_command.insert(0, sys.executable)

            # 启动进程
            process = subprocess.Popen(
                full_command,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
            )

            return process

        except Exception as e:
            logger.error(f"启动工具失败: {e}")
            raise
