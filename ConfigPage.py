import json
import webbrowser
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from config_ui import *

CONFIG_FILE = "config.json"


class ConfigWindow(QtWidgets.QMainWindow, Ui_ConfigMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 初始化配置
        self.config = self.load_config()
        self.init_ui()

        # 连接信号槽
        self.save_button.clicked.connect(self.save_config)
        #self.name_button.clicked.connect(self.load_name_list)
        #self.gname_button.clicked.connect(self.load_girls_list)
        self.update_button.clicked.connect(self.check_update)

        # 输入验证器
        self.setup_validators()

    def init_ui(self):
        """从配置文件初始化界面状态"""
        # 基本设置
        self.save_checkbox.setChecked(self.config.get("auto_save", False))
        self.speak_checkbox.setChecked(self.config.get("speak", True))
        self.float_chackbox.setChecked(self.config.get("show_float", True))

        # 高级设置
        self.ani_time_edit.setText(str(self.config.get("animation_time", 0.3)))
        self.floatsize_edit.setText(str(self.config.get("float_size", 200)))

        # 多音字设置
        polyphones = self.config.get("polyphones", [])
        for i, (orig, repl) in enumerate(polyphones[:3]):  # 最多三组
            getattr(self, f"a{i + 1}").setText(orig)
            getattr(self, f"a{i + 1}2").setText(repl)

    def setup_validators(self):
        """设置输入验证器"""
        # 动画时长验证器（0.1-5.0秒）
        self.ani_time_edit.setValidator(QtGui.QDoubleValidator(0.1, 5.0, 1))

        # 悬浮窗大小验证器（50-1000像素）
        self.floatsize_edit.setValidator(QtGui.QIntValidator(50, 1000))

        # 多音字输入验证（禁止特殊字符）
        regex = QtCore.QRegExp("^[\u4e00-\u9fa5a-zA-Z0-9]+$")
        for field in [self.a1, self.a2, self.b1, self.b2, self.c1, self.c2]:
            field.setValidator(QtGui.QRegExpValidator(regex))

    def load_config(self):
        """加载配置文件"""
        file_dir = r'./PickNameConfig/config.json'
        file_dir_2 = r'./PickNameConfig/name_changes.json'
        with open(file_dir, encoding='utf-8') as config_file:
            config = json.load(config_file)
            self.is_save = config['is_save']
            self.animation = config['animation']
            self.animation_time = config['animation_time']
            self.speak_name = config['speak_name']
            self.floating_size = config['floating_size']

        with open(file_dir_2, encoding='utf-8') as config_file_2:
            config_2 = json.load(config_file_2)
            self.speak_change_a1 = config_2['speak_change_a1']
            self.speak_change_a2 = config_2['speak_change_a2']
            self.speak_change_b1 = config_2['speak_change_b1']
            self.speak_change_b2 = config_2['speak_change_b2']
            self.speak_change_c1 = config_2['speak_change_c1']
            self.speak_change_c2 = config_2['speak_change_c2']

        return config

    def save_config(self):
        """保存配置"""
        try:
            file_dir = r'./PickNameConfig/config.json'
            with open(file_dir, 'r', encoding='utf-8') as config_file:
                config = json.load(config_file)
                config['is_save'] = self.is_save
                config['animation'] = self.animation
                config['speak_name'] = self.speak_name
            with open(file_dir, 'w', encoding='utf-8') as config_file:
                json.dump(config, config_file, ensure_ascii=False)
        except Exception as e:
            QMessageBox.critical(self, '错误', '配置文件写入错误！')
            print("配置文件写入错误:", e)

    def get_polyphones(self):
        """获取多音字配置"""
        polyphones = []
        for group in ["a", "b", "c"]:
            orig = getattr(self, f"{group}1").text().strip()
            repl = getattr(self, f"{group}2").text().strip()
            if orig and repl:
                polyphones.append((orig, repl))
        return polyphones

    def validate_inputs(self, config):
        """验证输入有效性"""
        errors = []

        if not 0.1 <= config["animation_time"] <= 10.0:
            errors.append("动画时长需在0.5-10.0秒之间")

        if not 20 <= config["floating_size"] <= 1000:
            errors.append("悬浮窗大小需在20-1000像素之间")

        for orig, repl in config["polyphones"]:
            if not orig or not repl:
                errors.append("多音字替换需要填写完整的两边内容")
                break

        if errors:
            QMessageBox.warning(self, "输入错误", "\n".join(errors))
            return False
        return True

    def open_name_file(self):
        """加载总名单"""


    def open_girls_list(self):
        """加载女生名单"""


    def check_update(self):
        """检查更新"""
        try:
            response = requests.get("https://api.github.com/repos/Chengzi600/ClassNamePicker/releases/latest")
            latest_version = response.json()['tag_name']
            if latest_version == self.version:
                latest_version = latest_version + '(已是最新版本)'
            else:
                latest_version = latest_version + '(发现新版本)'
            latest_version_info = response.json()['body']
        except Exception as e:
            print('检查更新失败:', e)
            latest_version = '检测失败'
            latest_version_info = '获取更新失败'

        reply = QMessageBox.question(self, '检查更新',
                                     '检查更新:\n'
                                     '当前最新版本: {}\n最新版本信息:\n{}\n\n'
                                     '单击“是”打开 GitHub Releases 界面下载最新版本'.format(latest_version,
                                                                                            latest_version_info),
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            webbrowser.open("https://github.com/Chengzi600/ClassNamePicker/releases")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = ConfigWindow()
    window.show()
    sys.exit(app.exec_())