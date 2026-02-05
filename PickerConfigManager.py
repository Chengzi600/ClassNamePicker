# PickerConfigManager.py
import json
import os
from pathlib import Path
from loguru import logger

class ConfigManager:
    CONFIG_DIR = Path("./PickNameConfig")
    CONFIG_FILE = CONFIG_DIR / "config.json"
    NAME_CHANGES_FILE = CONFIG_DIR / "name_changes.json"
    NAMES_FILE = CONFIG_DIR / "names.txt"
    G_NAMES_FILE = CONFIG_DIR / "g_names.txt"
    
    # 配置键名常量
    KEY_PICK_AGAIN = "pick_again"
    KEY_ANIMATION = "animation"
    KEY_ANIMATION_TIME = "animation_time"
    KEY_IS_SAVE = "is_save"
    KEY_PICK_BALANCED = "pick_balanced"
    KEY_PICKED_COUNT = "picked_count"
    KEY_SPEAK_NAME = "speak_name"
    KEY_SPEAK_SPEED = "speak_speed"
    KEY_SHOW_FLOATING = "show_floating"
    KEY_FLOATING_X_SIZE = "floating_x_size"
    KEY_FLOATING_Y_SIZE = "floating_y_size"
    KEY_CAN_PICK_NAMES = "can_pick_names"
    KEY_CONFIG_VERSION = "config_version"
    KEY_WINDOW_WIDTH = "window_width"
    KEY_WINDOW_HEIGHT = "window_height"
    KEY_AUTO_START = "auto_start"
    
    DEFAULT_CONFIG = {
        KEY_PICK_AGAIN: False,
        KEY_ANIMATION: True,
        KEY_ANIMATION_TIME: 0.8,
        KEY_IS_SAVE: False,
        KEY_PICK_BALANCED: False,
        KEY_PICKED_COUNT: 0,
        KEY_SPEAK_NAME: True,
        KEY_SPEAK_SPEED: 170,
        KEY_SHOW_FLOATING: True,
        KEY_FLOATING_X_SIZE: 130,
        KEY_FLOATING_Y_SIZE: 130,
        KEY_CAN_PICK_NAMES: [],
        KEY_CONFIG_VERSION: "1.1.5",
        KEY_WINDOW_WIDTH: 577,
        KEY_WINDOW_HEIGHT: 601,
        KEY_AUTO_START: False,
    }
    
    @classmethod
    def initialize(cls):
        """初始化配置目录和文件"""
        cls.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        
        # 创建默认配置
        if not cls.CONFIG_FILE.exists():
            with open(cls.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(cls.DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)
        
        # 创建名单文件
        if not cls.NAMES_FILE.exists():
            cls.NAMES_FILE.write_text("名字1\n名字2\n名字3\n", encoding='utf-8')
        
        if not cls.G_NAMES_FILE.exists():
            cls.G_NAMES_FILE.write_text("女名1\n女名2\n女名3\n", encoding='utf-8')
        
        # 创建多音字配置
        if not cls.NAME_CHANGES_FILE.exists():
            with cls.NAME_CHANGES_FILE.open('w', encoding='utf-8') as f:
                json.dump({
                    'speak_change_a1': '', 'speak_change_a2': '',
                    'speak_change_b1': '', 'speak_change_b2': '',
                    'speak_change_c1': '', 'speak_change_c2': '',
                }, f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load(cls):
        """加载配置"""
        cls.initialize()
        
        try:
            config = json.loads(cls.CONFIG_FILE.read_text(encoding='utf-8'))
            # 版本升级处理
            if config.get(cls.KEY_CONFIG_VERSION) != cls.DEFAULT_CONFIG[cls.KEY_CONFIG_VERSION]:
                logger.warning('开始升级配置')
                config = cls._migrate_config(config)
            return config
        except Exception as e:
            logger.error(f'配置文件加载失败')
            raise RuntimeError(f"配置文件加载失败: {e}")

    @classmethod
    def load_safe(cls):
        """安全加载配置，加载失败时返回默认配置并尝试修复文件"""
        try:
            return cls.load()
        except Exception as e:
            logger.error(f'读配置出错，尝试修复:{e}')
            # 尝试修复：写入默认配置并返回一份拷贝
            try:
                cls.save(cls.DEFAULT_CONFIG.copy())
            except Exception as e:
                logger.error(f'无法修复配置:{e}')
                pass
            return cls.DEFAULT_CONFIG.copy()
    
    @classmethod
    def _migrate_config(cls, old_config):
        """配置版本迁移"""
        logger.warning('开始配置迁移')
        new_config = cls.DEFAULT_CONFIG.copy()
        new_config.update({k: v for k, v in old_config.items() if k in new_config})
        cls.save(new_config)
        return new_config
    
    @classmethod
    def save(cls, config):
        """保存配置"""
        try:
            # 原子写入：先写入临时文件，再替换目标文件
            tmp_file = cls.CONFIG_FILE.with_suffix('.tmp')
            with tmp_file.open('w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            # 原子替换
            os.replace(str(tmp_file), str(cls.CONFIG_FILE))
            logger.info(f'配置文件读写完成:{config}')
        except Exception as e:
            logger.error('配置文件读写失败')
            raise RuntimeError(f"配置文件保存失败: {e}")
    
    @classmethod
    def load_name_changes(cls):
        """加载多音字配置"""
        return json.loads(cls.NAME_CHANGES_FILE.read_text(encoding='utf-8'))
    
    @classmethod
    def save_name_changes(cls, data):
        """保存多音字配置"""
        json.dump(data, cls.NAME_CHANGES_FILE.open('w', encoding='utf-8'), ensure_ascii=False, indent=2)
        logger.info(f'保存多音字配置:{data}')