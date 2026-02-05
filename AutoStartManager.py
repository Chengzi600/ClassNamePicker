import sys
import os
import platform

class AutoStartManager:
    """开机自启动管理器（Windows）"""
    
    REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
    APP_NAME = "ClassNamePicker"
    
    @staticmethod
    def is_supported():
        """检查当前系统是否支持"""
        return platform.system() == "Windows"
    
    @staticmethod
    def is_enabled():
        """检查是否已设置开机自启动"""
        if not AutoStartManager.is_supported():
            return False
        
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, AutoStartManager.REG_PATH, 0, winreg.KEY_READ) as key:
                try:
                    winreg.QueryValueEx(key, AutoStartManager.APP_NAME)
                    return True
                except FileNotFoundError:
                    return False
        except Exception:
            return False
    
    @staticmethod
    def enable(app_path=None):
        """启用开机自启动"""
        if not AutoStartManager.is_supported():
            return False, "仅Windows系统支持此功能"
        
        if app_path is None:
            app_path = AutoStartManager._get_app_path()
        
        if not app_path:
            return False, "无法获取程序路径"
        
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, AutoStartManager.REG_PATH, 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, AutoStartManager.APP_NAME, 0, winreg.REG_SZ, app_path)
            return True, "设置成功"
        except PermissionError:
            return False, "权限不足，请以管理员身份运行"
        except Exception as e:
            return False, f"设置失败: {e}"
    
    @staticmethod
    def disable():
        """禁用开机自启动"""
        if not AutoStartManager.is_supported():
            return False, "仅Windows系统支持此功能"
        
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, AutoStartManager.REG_PATH, 0, winreg.KEY_SET_VALUE) as key:
                winreg.DeleteValue(key, AutoStartManager.APP_NAME)
            return True, "已禁用开机自启动"
        except FileNotFoundError:
            return True, "自启动已关闭"
        except Exception as e:
            return False, f"操作失败: {e}"
    
    @staticmethod
    def _get_app_path():
        """获取程序完整路径"""
        # 如果是打包后的exe
        if getattr(sys, 'frozen', False):
            return f'"{sys.executable}"'
        
        # 如果是Python脚本
        current_dir = os.path.dirname(os.path.abspath(__file__))
        main_script = os.path.join(current_dir, "ClassNamePicker.py")
        
        if os.path.exists(main_script):
            return f'"{sys.executable}" "{main_script}"'
        
        return None