import json
import os
import random
import sys
import time
import pyttsx3
import threading

from ui import Ui_MainWindow
from FloatingWindow import *
from ConfigPage import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, Qt


class PickName(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # 版本信息
        self.version = 'v1.4.5'
        self.version_time = '2025.4.19'
        self.version_info = ''
        self.config_version = '1.1.5'

        # 初始名单
        self.names = []
        self.g_names = []
        self.b_names = []

        # print(len(self.g_names)+len(self.b_names))
        # print(len(self.b_names))
        # print(len(self.b_names_bak))
        # print(len(self.names))

        # 初始化已抽取的名字列表
        self.can_pick_names = self.names.copy()

        # 初始化变量
        self.pick_again = False
        self.animation = True
        self.recite = False
        self.is_save = False
        self.pick_only_g = False
        self.pick_only_b = False
        self.speak_name = False
        self.pick_balanced = False
        self.is_show_floating = True
        self.animation_time = 1.0
        self.picked_count = 0
        self.wait_recite_time = 3
        self.floating_size = 130
        self.speak_speed = 170

        self.start_time = 0
        self.elapsed_time = 0
        self.is_running = False
        self.selected_name = ''

        self.config_window = None

        super().__init__()  # 初始化QMainWindow
        self.setupUi(self)  # 使用UI设置界面
        self.setWindowTitle(
            "课堂随机点名{}- ClassNamePicker - {}({})".format(self.version_info, self.version, self.version_time))
        # 禁用最大化按钮
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        # 禁用最小化按钮
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinimizeButtonHint)
        self.setWindowFlags(
            self.windowFlags() |  # 保留原有属性
            QtCore.Qt.WindowStaysOnTopHint  # 添加置顶属性
        )

        # 抽取名字按钮
        self.pick_name_button.clicked.connect(self.pick_name)

        # 重置按钮
        self.reset_button.clicked.connect(self.reset)

        # 复选框，是否背书模式
        self.pick_time_checkbox.stateChanged.connect(self.set_recite)
        self.timer_label.hide()

        # 复选框，是否只抽男/女
        self.b_names_pick_checkbox.stateChanged.connect(self.set_pick_group_b)
        self.g_names_pick_checkbox.stateChanged.connect(self.set_pick_group_g)

        # 复选框，是否重复抽取
        self.pick_again_checkbox.stateChanged.connect(self.set_pick_again)

        # 链接 Action
        self.about_action.triggered.connect(self.about_menu)
        self.github_action.triggered.connect(self.github_menu)
        self.exit_action.triggered.connect(self.exit)
        self.config_action.triggered.connect(self.open_config_page)

        # 播报
        self.engine = pyttsx3.init()
        # 设置语速
        self.engine.setProperty('rate', self.speak_speed)
        self.lock = threading.Lock()  # 核心锁

        self.read_config()
        self.update_stats()

        # 创建悬浮窗实例
        self.floating_window = FloatingWindow(size=self.floating_size, parent=self)

        # 当前配置窗口引用
        self.config_window = None

        # 防抖动定时器配置
        self.save_timer = QTimer()
        self.save_timer.setSingleShot(True)  # 单次触发模式
        self.save_timer.timeout.connect(self.save_config)

    def read_config(self):
        """配置文件读取"""

        def create_config(is_upgrade=False):
            if is_upgrade:
                config_v['picked_count'] = self.picked_count
                with open(file_dir, 'w+', encoding='utf-8') as config_file_c:
                    json.dump(config_v, config_file_c)

            if not os.path.exists(file_dir):
                with open(file_dir, 'w+', encoding='utf-8') as config_file_c:
                    json.dump(config_v, config_file_c)
            if not os.path.exists(names_file_dir):
                with open(names_file_dir, 'w', encoding='utf-8') as names_file_c:
                    names_file_c.write(example_names)
            if not os.path.exists(g_names_file_dir):
                with open(g_names_file_dir, 'w', encoding='utf-8') as g_names_file_c:
                    g_names_file_c.write(g_example_names)
            if not os.path.exists(file_dir_2):
                with open(file_dir_2, 'w', encoding='utf-8') as config_file_2_c:
                    json.dump(config_v2, config_file_2_c)

        try:
            os.makedirs('./PickNameConfig/', exist_ok=True)
            file_dir = r'./PickNameConfig/config.json'
            file_dir_2 = r'./PickNameConfig/name_changes.json'
            names_file_dir = './PickNameConfig/names.txt'
            g_names_file_dir = './PickNameConfig/g_names.txt'
            example_names = '名字1\n名字2\n名字3\n'
            g_example_names = '女名1\n女名2\n女名3\n'

            config_v = {
                'pick_again': self.pick_again,
                'animation': self.animation,
                'animation_time': self.animation_time,
                'is_save': self.is_save,
                'show_floating': self.is_show_floating,
                'floating_size': self.floating_size,
                'pick_balanced': self.pick_balanced,
                'picked_count': self.picked_count,
                'speak_name': self.speak_name,
                'speak_speed': self.speak_speed,
                "window_width": self.width(),
                "window_height": self.height(),
                'config_version': self.config_version,
                'can_pick_names': self.names,
            }
            config_v2 = {
                'speak_change_a1': '',
                'speak_change_a2': '',
                'speak_change_b1': '',
                'speak_change_b2': '',
                'speak_change_c1': '',
                'speak_change_c2': '',
            }

            try:
                with open(names_file_dir, 'r', encoding='utf-8') as names_file:
                    self.names = [line.strip() for line in names_file if line.strip()]
                with open(g_names_file_dir, 'r', encoding='utf-8') as g_names_file:
                    self.g_names = [line.strip() for line in g_names_file if line.strip()]

                for name in self.names:
                    if name not in self.g_names:
                        self.b_names.append(name)

                with open(file_dir, encoding='utf-8') as config_file:
                    config = json.load(config_file)
                    if not config['config_version'] == self.config_version:
                        self.picked_count = config['picked_count']
                        create_config(True)
                        QMessageBox.information(self, '提示', '配置文件更新成功!')
                        return
                    self.block_signals()
                    self.is_save = config['is_save']
                    self.pick_again = config['pick_again']
                    self.animation = config['animation']
                    self.animation_time = config['animation_time']
                    self.can_pick_names = config['can_pick_names']
                    self.picked_count = config['picked_count']
                    self.speak_name = config['speak_name']
                    self.speak_speed = config['speak_speed']
                    self.pick_balanced = config['pick_balanced']
                    self.floating_size = config['floating_size']
                    window_height = config['window_height']
                    window_width = config['window_width']
                    self.is_show_floating = config['show_floating']
                    self.resize(window_width, window_height)
                    self.pick_again_checkbox.setChecked(self.pick_again)
                    self.engine.setProperty('rate', self.speak_speed)
                    self.block_signals(False)

                with open(file_dir_2, encoding='utf-8') as config_file_2:
                    config_2 = json.load(config_file_2)
                    self.speak_change_a1 = config_2['speak_change_a1']
                    self.speak_change_a2 = config_2['speak_change_a2']
                    self.speak_change_b1 = config_2['speak_change_b1']
                    self.speak_change_b2 = config_2['speak_change_b2']
                    self.speak_change_c1 = config_2['speak_change_c1']
                    self.speak_change_c2 = config_2['speak_change_c2']

            except FileNotFoundError:
                create_config()
                # QMessageBox.information(self, '提示', '配置文件创建成功!请在names.txt文件中编辑名单!')
                # print(e)
                # sys.exit('CREATED_CONFIG_SUCCESSFULLY')

        except Exception as e:
            QMessageBox.critical(self, '错误',
                                 '配置文件读写错误!\n请尝试删除配置文件夹中的config.json\n错误信息:' + str(
                                     e))
            print("错误信息:", e)
            sys.exit('FAILED_TO_LOAD_CONFIG')

    def save_config(self):
        """配置文件写入"""
        try:
            file_dir = r'./PickNameConfig/config.json'
            with open(file_dir, 'r', encoding='utf-8') as config_file:
                config = json.load(config_file)
                config['pick_again'] = self.pick_again
                config['pick_balanced'] = self.pick_balanced
                if self.is_save:
                    config['can_pick_names'] = self.can_pick_names
                else:
                    config['can_pick_names'] = self.names
                config['picked_count'] = self.picked_count
                config['window_width'] = self.width()
                config['window_height'] = self.height()
            with open(file_dir, 'w', encoding='utf-8') as config_file:
                json.dump(config, config_file, ensure_ascii=False)
            print('配置文件已保存')
        except Exception as e:
            QMessageBox.critical(self, '错误', '配置文件写入错误！')
            print("配置文件写入错误:", e)

    def set_pick_again(self):
        if not self.pick_again:
            self.pick_again = True
            if self.pick_only_g:
                self.can_pick_names = self.g_names.copy()
            elif self.pick_only_b:
                self.can_pick_names = self.b_names.copy()
            else:
                self.can_pick_names = self.names.copy()
        elif self.pick_again:
            self.pick_again = False
        self.update_stats()

    def set_animation(self):
        if not self.animation:
            self.animation = True
        elif self.animation:
            self.animation = False

    def set_recite(self):
        if not self.recite:
            self.recite = True
            self.timer_label.show()

        elif self.recite:
            self.recite = False
            self.is_running = False
            self.timer_label.hide()

    def set_save(self):
        if not self.is_save:
            self.is_save = True
        else:
            self.is_save = False

    def set_speak(self):
        if not self.speak_name:
            self.speak_name = True
        else:
            self.speak_name = False

    def set_pick_group_g(self):
        self.block_signals(True)
        if not self.pick_only_g:
            if QMessageBox.question(self, "继续吗",
                                    "该操作将清空已抽取的名字",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
                self.pick_again = False
                self.pick_again_checkbox.setCheckState(False)
                # self.pick_again_checkbox.setDisabled(True)
                self.pick_only_g = True
                self.set_pick_group('g')
                self.can_pick_names = self.g_names.copy()
                self.update_stats()
            else:
                self.g_names_pick_checkbox.setCheckState(False)
        else:
            self.set_pick_group('clear')
        self.block_signals(False)

    def set_pick_group_b(self):
        self.block_signals()
        if not self.pick_only_b:
            if QMessageBox.question(self, "继续吗",
                                    "该操作将清空已抽取的名字",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
                self.pick_again = False
                self.pick_again_checkbox.setCheckState(False)
                # self.pick_again_checkbox.setDisabled(True)
                self.pick_only_b = True
                self.set_pick_group('b')
                self.can_pick_names = self.b_names.copy()
                self.update_stats()

            else:
                self.b_names_pick_checkbox.setCheckState(False)
        else:
            self.set_pick_group('clear')
        self.block_signals(False)

    def set_pick_group(self, ab):
        # 如果两个复选框都被选中，则取消另一个的选中状态
        if self.pick_only_b and self.pick_only_g:
            if ab == 'g':
                self.pick_only_b = False
                self.b_names_pick_checkbox.setCheckState(False)
            elif ab == 'b':
                self.pick_only_g = False
                self.g_names_pick_checkbox.setCheckState(False)
        elif ab == 'clear':
            self.pick_only_g = False
            self.g_names_pick_checkbox.setCheckState(False)
            self.pick_only_b = False
            self.b_names_pick_checkbox.setCheckState(False)
            self.can_pick_names = self.names.copy()
            self.update_stats()

    def pick_name(self):
        self.is_running = False

        self.pick_name_button.setDisabled(True)
        self.reset_button.setDisabled(True)

        if not self.can_pick_names:
            QMessageBox.information(self, "提示", "所有名字已抽取完毕，请重置")
            self.name_label.setText("请重置")
            self.name_label.setStyleSheet("color: red")
            self.reset_button.setDisabled(False)
            return

        self.selected_name = random.choice(self.can_pick_names)

        if self.animation:
            self.start_time = time.time()
            self.pick_animation()
        else:
            self.name_label.setText(self.selected_name)
            self.pick_name_button.setDisabled(False)
            self.reset_button.setDisabled(False)
            if self.speak_name:
                self.say(self.selected_name)
            if self.recite:
                self.is_running = False
                self.perform_countdown(self.wait_recite_time)

        if not self.pick_again:
            self.can_pick_names.remove(self.selected_name)

        # 更新统计信息
        self.picked_count += 1
        self.update_stats()
        # self.save_config()

    def perform_countdown(self, seconds):
        self.pick_name_button.setDisabled(True)
        self.reset_button.setDisabled(True)
        self.timer_label.setStyleSheet("color=red")
        self.timer_label.setText(f"{seconds:.1f}s")
        if seconds > 0:
            QTimer.singleShot(100, lambda: self.perform_countdown(seconds - 0.1))
        else:
            self.pick_name_button.setDisabled(False)
            self.reset_button.setDisabled(False)
            self.timer_label.setStyleSheet("color: black")
            self.is_running = True
            self.start_time = time.time()
            self.update_timer()

    def update_timer(self):
        if self.is_running:
            self.elapsed_time = time.time() - self.start_time
            self.timer_label.setText(f"{self.elapsed_time:.1f}s")
            QTimer.singleShot(100, self.update_timer)

    def reset(self, no_tip=False):
        self.block_signals()

        def perform_reset():
            if self.is_running:
                self.is_running = False
            if self.recite:
                self.timer_label.setText("0.0s")
            self.set_pick_group('clear')
            self.can_pick_names = self.names.copy()
            self.name_label.setText("请抽取")
            self.name_label.setStyleSheet("color: black")
            self.pick_name_button.setDisabled(False)
            self.save_config()
            self.update_stats()

        if no_tip:
            perform_reset()
        else:
            reply = QMessageBox.question(self, '提示', '你确定要重置已抽取名单吗?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                perform_reset()
                QMessageBox.information(self, "提示", "已清空已抽取名单!")
        self.block_signals(False)

    def pick_animation(self):
        if len(self.can_pick_names) <= 2:
            self.name_label.setText(self.selected_name)
            self.pick_name_button.setEnabled(True)
            self.reset_button.setEnabled(True)
            return

        rdm_name = random.choice(self.can_pick_names)
        self.name_label.setText(rdm_name)
        if time.time() - self.start_time < self.animation_time:  # 动画时间内不断变化
            QTimer.singleShot(10, self.pick_animation)  # 每 10 毫秒重新调用
        else:
            self.name_label.setText(self.selected_name)
            self.pick_name_button.setEnabled(True)
            self.reset_button.setEnabled(True)
            if self.speak_name:
                self.say(self.selected_name)
            if self.recite:
                self.is_running = False
                self.perform_countdown(self.wait_recite_time)
            return

    def update_stats(self):
        if not self.pick_again:
            try:
                if self.pick_only_g:
                    stats_text = "已抽取人数: {}  可抽取人数: {} 总抽取次数: {}\n被抽概率: {}%".format(
                        len(self.g_names) - len(self.can_pick_names),
                        len(self.can_pick_names), self.picked_count, round(1 / len(self.can_pick_names) * 100, 2))
                elif self.pick_only_b:
                    stats_text = "已抽取人数: {}  可抽取人数: {} 总抽取次数: {}\n被抽概率: {}%".format(
                        len(self.b_names) - len(self.can_pick_names),
                        len(self.can_pick_names), self.picked_count, round(1 / len(self.can_pick_names) * 100, 2))
                else:
                    stats_text = "已抽取人数: {}  可抽取人数: {} 总抽取次数: {}\n被抽概率: {}%".format(
                        len(self.names) - len(self.can_pick_names),
                        len(self.can_pick_names), self.picked_count, round(1 / len(self.can_pick_names) * 100, 2))
            except ZeroDivisionError:
                stats_text = "已抽取人数: {}  可抽取人数: {} 总抽取次数: {}\n被抽概率: {}%".format(
                    "抽完了", len(self.can_pick_names), self.picked_count, '0')

        else:
            stats_text = "总抽取次数: {}".format(self.picked_count)

        # 显示统计信息在状态栏
        self.statusBar().showMessage(stats_text)

    def about_menu(self):
        QMessageBox.information(self, "程序简介",
                                "ClassNamePicker 是一款开源的功能强大的课堂随机点名工具\n使用 Python + PyQt5 编写，界面简洁\n前往 Github 界面了解更多")

    def check_update_menu(self):
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

    @staticmethod
    def github_menu():
        webbrowser.open("https://github.com/Chengzi600/ClassNamePicker/releases")

    def closeEvent(self, event):
        if not self.is_show_floating:
            self.exit()
        if self.pick_only_g or self.pick_only_b or self.pick_again:
            self.reset(no_tip=True)
            self.hide()
            self.floating_window.show()
        else:
            self.save_config()
            self.hide()
            self.floating_window.show()
        event.ignore()

    def resizeEvent(self, event):
        """重写窗口大小变化事件处理"""
        super().resizeEvent(event)
        # 取消未执行的保存操作，重新开始计时
        self.save_timer.stop()
        # 延迟500毫秒后触发保存
        self.save_timer.start(500)
        # print(f"窗口尺寸已改变 → 宽度: {current_width}px, 高度: {current_height}px")

    def exit(self):
        if self.pick_only_g or self.pick_only_b or self.pick_again:
            self.reset(no_tip=True)
            QApplication.exit()
        else:
            self.save_config()
            QApplication.exit()

    def open_config_page(self):
        """打开配置窗口"""
        if not self.config_window:
            self.config_window = ConfigWindow()
            # 连接关闭信号
            self.config_window.closed.connect(self.read_config)
            # 窗口关闭时自动解除引用
            self.config_window.destroyed.connect(
                lambda: setattr(self, 'config_window', None)
            )
        self.config_window.show()
        self.config_window.raise_()  # 窗口置顶

    def block_signals(self, state=True):
        if state:
            self.b_names_pick_checkbox.stateChanged.disconnect()
            self.pick_again_checkbox.stateChanged.disconnect()
            self.g_names_pick_checkbox.stateChanged.disconnect()
        else:
            self.b_names_pick_checkbox.stateChanged.connect(self.set_pick_group_b)
            self.g_names_pick_checkbox.stateChanged.connect(self.set_pick_group_g)
            self.pick_again_checkbox.stateChanged.connect(self.set_pick_again)

    def say(self, text):
        # 线程锁 by deepseek-r1
        if text == self.speak_change_a1:
            text = self.speak_change_a2
        elif text == self.speak_change_b1:
            text = self.speak_change_b2
        elif text == self.speak_change_c1:
            text = self.speak_change_c2

        def _speak():
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"语音错误: {e}")
            finally:
                self.lock.release()

        if self.lock.acquire(blocking=False):  # 非阻塞获取锁
            threading.Thread(target=_speak, daemon=True).start()
        else:
            print("当前有语音正在播放，忽略新请求")


if __name__ == "__main__":
    # QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    # QGuiApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    # QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)  # 创建应用
    window = PickName()  # 创建主窗口
    window.show()  # 显示窗口
    sys.exit(app.exec_())  # 进入应用的主循环
