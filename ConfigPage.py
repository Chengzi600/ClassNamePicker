import os
import webbrowser
from PyQt5 import QtWidgets
import requests
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from config_ui import Ui_ConfigMainWindow
from PickerConfigManager import ConfigManager
from AutoStartManager import AutoStartManager
from PyQt5 import QtGui, QtCore
from version import APP_VERSION, APP_VERSION_TIME, APP_VERSION_INFO, CONFIG_VERSION
from loguru import logger

class ConfigWindow(QtWidgets.QMainWindow, Ui_ConfigMainWindow):
    closed = QtCore.pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle('配置面板')
        self.version = APP_VERSION
        self.legal_close = False

        window_flags = self.windowFlags()
        window_flags &= ~Qt.WindowMaximizeButtonHint
        window_flags &= ~Qt.WindowMinimizeButtonHint
        window_flags &= ~Qt.WindowCloseButtonHint
        # 应用新的窗口标志
        self.setWindowFlags(window_flags)
        self.setWindowFlags(
            self.windowFlags() |  # 保留原有属性
            QtCore.Qt.WindowStaysOnTopHint  # 添加置顶属性
        )

        # 初始化配置
        self.load_config()
        self.init_ui()

        # 连接信号槽
        self.save_button.clicked.connect(self.save_config)
        self.name_button.clicked.connect(self.open_name_file)
        self.gname_button.clicked.connect(self.open_girls_file)
        self.update_button.clicked.connect(self.check_update)
        self.cancel_button.clicked.connect(self.cancel)

        # 输入验证器
        self.setup_validators()

        # 检查系统支持
        if not AutoStartManager.is_supported():
            self.auto_start_checkbox.setEnabled(False)
            self.auto_start_checkbox.setToolTip("仅Windows系统支持开机自启动")

    def init_ui(self):
        """从配置文件初始化界面状态"""
        # 基本设置
        self.save_checkbox.setChecked(self.is_save)
        self.speak_checkbox.setChecked(self.speak_name)
        self.float_chackbox.setChecked(self.show_floating)
        self.animation_checkBox.setChecked(self.animation)
        # 添加自启动复选框状态
        self.auto_start_checkbox.setChecked(self.auto_start)

        # 高级设置
        self.ani_time_edit.setText(str(self.animation_time))
        self.floatsize_x_edit.setText(str(self.floating_x_size))
        self.floatsize_y_edit.setText(str(self.floating_y_size))
        self.speed_edit.setText(str(self.speak_speed))

        # 多音字设置
        self.a1.setText(self.speak_change_a1)
        self.a2.setText(self.speak_change_a2)
        self.b1.setText(self.speak_change_b1)
        self.b2.setText(self.speak_change_b2)
        self.c1.setText(self.speak_change_c1)
        self.c2.setText(self.speak_change_c2)

    def setup_validators(self):
        """设置输入验证器"""
        # 动画时长 0.1-5.0秒
        self.ani_time_edit.setValidator(QtGui.QDoubleValidator(0.1, 5.0, 2))
        # 语速 50-300
        self.speed_edit.setValidator(QtGui.QIntValidator(50, 300))
        # 悬浮窗尺寸 50-1000px
        self.floatsize_x_edit.setValidator(QtGui.QIntValidator(50, 1000))
        self.floatsize_y_edit.setValidator(QtGui.QIntValidator(50, 1000))
        # 多音字支持中文和字母，允许空格
        regex = QtCore.QRegExp(r"^[\u4e00-\u9fa5a-zA-Z0-9\s]*$")
        validator = QtGui.QRegExpValidator(regex)
        for field in [self.a1, self.a2, self.b1, self.b2, self.c1, self.c2]:
            field.setValidator(validator)
            field.setMaxLength(10)  # 限制长度

    def load_config(self):
        """加载配置文件"""
        config = ConfigManager.load_safe()
        self.is_save = config.get(ConfigManager.KEY_IS_SAVE, False)
        self.animation = config.get(ConfigManager.KEY_ANIMATION, True)
        self.animation_time = config.get(ConfigManager.KEY_ANIMATION_TIME, 0.8)
        self.speak_name = config.get(ConfigManager.KEY_SPEAK_NAME, True)
        self.show_floating = config.get(ConfigManager.KEY_SHOW_FLOATING, True)
        self.floating_x_size = config.get(ConfigManager.KEY_FLOATING_X_SIZE, 130)
        self.floating_y_size = config.get(ConfigManager.KEY_FLOATING_Y_SIZE, 130)
        self.speak_speed = config.get(ConfigManager.KEY_SPEAK_SPEED, 170)

        # 添加自启动配置加载
        self.auto_start = config.get(ConfigManager.KEY_AUTO_START, False)
        actual_state = AutoStartManager.is_enabled()
        # 如果实际状态与配置文件不符，弹窗提示并同步
        if actual_state != self.auto_start:
            msg = ("检测到自启动配置与实际状态不一致，已自动同步。\n"
                   f"配置文件: {'已启用' if self.auto_start else '未启用'}\n"
                   f"实际状态: {'已启用' if actual_state else '未启用'}")
            QMessageBox.information(self, "自启动状态同步", msg)
            self.auto_start = actual_state
            # 同步配置文件
            config[ConfigManager.KEY_AUTO_START] = actual_state
            try:
                ConfigManager.save(config)
            except Exception as e:
                QMessageBox.warning(self, "配置保存失败", f"同步自启动状态时保存配置失败: {e}")

        # 读取多音字替换
        try:
            name_changes = ConfigManager.load_name_changes()
            self.speak_change_a1 = name_changes.get('speak_change_a1', '')
            self.speak_change_a2 = name_changes.get('speak_change_a2', '')
            self.speak_change_b1 = name_changes.get('speak_change_b1', '')
            self.speak_change_b2 = name_changes.get('speak_change_b2', '')
            self.speak_change_c1 = name_changes.get('speak_change_c1', '')
            self.speak_change_c2 = name_changes.get('speak_change_c2', '')
        except Exception:
            self.speak_change_a1 = self.speak_change_a2 = ''
            self.speak_change_b1 = self.speak_change_b2 = ''
            self.speak_change_c1 = self.speak_change_c2 = ''

    def save_config(self):
        """配置保存"""
        try:
            config = ConfigManager.load()

            # 基本设置
            config[ConfigManager.KEY_IS_SAVE] = self.save_checkbox.isChecked()
            config[ConfigManager.KEY_SHOW_FLOATING] = self.float_chackbox.isChecked()
            config[ConfigManager.KEY_ANIMATION] = self.animation_checkBox.isChecked()
            config[ConfigManager.KEY_SPEAK_NAME] = self.speak_checkbox.isChecked()
            # 处理自启动设置
            old_state = config.get('auto_start', False)
            new_state = self.auto_start_checkbox.isChecked()

            if old_state != new_state:
                success, msg = AutoStartManager.enable() if new_state else AutoStartManager.disable()
                if success:
                    config['auto_start'] = new_state
                    QMessageBox.information(self, "提示", msg)
                else:
                    QMessageBox.warning(self, "自启动设置失败", msg)
                    # 恢复复选框状态
                    self.auto_start_checkbox.setChecked(old_state)
                    return  # 不保存配置

            # 高级设置
            try:
                config[ConfigManager.KEY_ANIMATION_TIME] = float(self.ani_time_edit.text())
                config[ConfigManager.KEY_FLOATING_X_SIZE] = int(self.floatsize_x_edit.text())
                config[ConfigManager.KEY_FLOATING_Y_SIZE] = int(self.floatsize_y_edit.text())
                config[ConfigManager.KEY_SPEAK_SPEED] = int(self.speed_edit.text())
            except Exception as e:
                QMessageBox.warning(self, "输入错误", f"高级设置输入格式有误: {e}")
                return

            # 验证
            if not self.validate_inputs(config):
                return

            try:
                ConfigManager.save(config)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存配置文件失败: {e}")
                return

            # 保存多音字配置
            name_changes = {
                'speak_change_a1': self.a1.text(),
                'speak_change_a2': self.a2.text(),
                'speak_change_b1': self.b1.text(),
                'speak_change_b2': self.b2.text(),
                'speak_change_c1': self.c1.text(),
                'speak_change_c2': self.c2.text(),
            }
            try:
                ConfigManager.save_name_changes(name_changes)
            except Exception as e:
                QMessageBox.warning(self, "多音字保存失败", f"多音字配置保存失败: {e}")

            QMessageBox.information(self, "成功", "配置已保存并生效！")
            self.legal_close = True
            # self.closed.emit(True)
            self.close()

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            QMessageBox.critical(self, "错误", f"保存失败: {e}")
    
    def validate_inputs(self, config):
        """验证输入有效性"""
        errors = []
        
        if not (0.1 <= config[ConfigManager.KEY_ANIMATION_TIME] <= 5.0):
            errors.append("动画时长需在0.1-5.0秒之间")
        
        size_x = config[ConfigManager.KEY_FLOATING_X_SIZE]
        size_y = config[ConfigManager.KEY_FLOATING_Y_SIZE]
        if not (50 <= size_x <= 500) or not (50 <= size_y <= 500):
            errors.append("悬浮窗尺寸需在50-500像素之间")
        
        speed = config[ConfigManager.KEY_SPEAK_SPEED]
        if not (50 <= speed <= 300):
            errors.append("播报速度需在50-300之间")
        
        # 检查多音字配对
        pairs = [(self.a1.text(), self.a2.text()),
                 (self.b1.text(), self.b2.text()),
                 (self.c1.text(), self.c2.text())]
        
        for orig, repl in pairs:
            if bool(orig) != bool(repl):  # 只有一个有值
                errors.append(f"多音字替换必须成对填写")
                break
        
        if errors:
            QMessageBox.warning(self, "输入错误", "\n".join(errors))
            return False
        
        return True

    def open_name_file(self):
        """加载总名单"""
        ConfigManager.initialize()
        QMessageBox.information(self, '提示', '保存名单后，请手动点击重置按钮，避免出现问题')
        #path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'PickNameConfig', 'names.txt'))
        try:
            os.startfile(r'.\PickNameConfig\names.txt')#(path)
        except Exception as e:
            QMessageBox.warning(self, '打开失败', f'无法打开名单文件: {e}')

    def open_girls_file(self):
        """加载女生名单"""
        ConfigManager.initialize()
        QMessageBox.information(self, '提示', '保存名单后，请手动点击重置按钮，避免出现问题')
        #path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'PickNameConfig', 'g_names.txt'))
        try:
            os.startfile(r'.\PickNameConfig\g_names.txt')#(path)
        except Exception as e:
            QMessageBox.warning(self, '打开失败', f'无法打开女生名单文件: {e}')


    def check_update(self):
        """检查更新"""
        try:
            response = requests.get("https://api.github.com/repos/Chengzi600/ClassNamePicker/releases/latest")
            latest_version = response.json()['tag_name']
            # if latest_version == self.version:
            #     latest_version = latest_version + '(已是最新版本)'
            # else:
            #     latest_version = latest_version + '(发现新版本)'
            latest_version_info = response.json()['body']
        except Exception as e:
            print('检查更新失败:', e)
            latest_version = '检测失败'
            latest_version_info = '获取更新失败'

        reply = QMessageBox.question(self, '检查更新',
                                     '当前版本: {}\n'
                                     '最新版本: {}\n版本信息:\n{}\n\n'
                                     '单击 Yes 打开 GitHub Releases 界面'.format(self.version, latest_version,
                                                                                            latest_version_info),
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            webbrowser.open("https://github.com/Chengzi600/ClassNamePicker/releases")

    def cancel(self):
        self.legal_close = True
        self.close()

    def closeEvent(self, event):
        """重写关闭事件"""
        if self.legal_close:
            # 发射关闭信号（True表示需要刷新，False不需要）
            logger.info('用户关闭配置窗口')
            self.closed.emit(True)
        else:
            logger.warning("配置窗口被非法关闭，已拦截")
            event.ignore()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = ConfigWindow()
    window.show()
    sys.exit(app.exec_())
