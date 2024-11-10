import json
import os
import random
import sys
import time
import requests
import webbrowser
import pyttsx3

from ui import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, Qt


class PickName(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # 版本信息
        self.version = '1.4.1'
        self.version_time = '2024.11.10'
        self.version_info = ''
        self.config_version = '1.1.4'

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
        self.animation_time = 1.0
        self.picked_count = 0
        self.wait_recite_time = 3

        self.start_time = 0
        self.elapsed_time = 0
        self.is_running = False
        self.selected_name = ''

        super().__init__()  # 初始化QMainWindow
        self.setupUi(self)  # 使用UI设置界面
        self.setWindowTitle(
            "课堂随机点名{}- ClassNamePicker - v{}({})".format(self.version_info, self.version, self.version_time))
        # 禁止调整窗口大小
        self.setFixedSize(self.size())  # 使窗口大小固定
        # 禁用最大化按钮
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        # 抽取名字按钮
        self.pick_name_button.clicked.connect(self.pick_name)

        # 重置按钮
        self.reset_button.clicked.connect(self.reset)

        # 复选框，是否保存
        self.is_save_checkbox.stateChanged.connect(self.set_save)

        # 复选框，是否背书模式
        self.pick_time_checkbox.stateChanged.connect(self.set_recite)
        self.timer_label.hide()

        # 复选框，是否只抽男/女
        self.b_names_pick_checkbox.stateChanged.connect(self.set_pick_group_b)
        self.g_names_pick_checkbox.stateChanged.connect(self.set_pick_group_g)

        # 复选框，是否重复抽取
        self.pick_again_checkbox.stateChanged.connect(self.set_pick_again)

        # 复选框，是否显示动画
        self.pick_animation_checkbox.stateChanged.connect(self.set_animation)

        # 复选框，是否读名字
        self.pick_read_checkbox.stateChanged.connect(self.set_speak)

        # 链接 Action
        self.about_action.triggered.connect(self.about_menu)
        self.update_action.triggered.connect(self.check_update_menu)
        self.github_action.triggered.connect(self.github_menu)

        # 播报
        self.engine = pyttsx3.init()
        # 设置语速
        self.engine.setProperty('rate', 190)
        # 设置音量
        self.engine.setProperty('volume', 1.0)
        # 设置语音合成器
        self.engine.setProperty('voice', "3")

        self.read_config()
        self.update_stats()

    # 配置文件读取
    def read_config(self):
        def create_config(is_upgrade=False):
            if is_upgrade:
                config_v['picked_count'] = self.picked_count
            with open(file_dir, 'w+', encoding='utf-8') as config_file_c:
                json.dump(config_v, config_file_c)
            if not os.path.exists(names_file_dir):
                with open(names_file_dir, 'w', encoding='utf-8') as names_file_c:
                    names_file_c.write(example_names)
            if not os.path.exists(g_names_file_dir):
                with open(g_names_file_dir, 'w', encoding='utf-8') as g_names_file_c:
                    g_names_file_c.write(g_example_names)
            # with open(file_dir) as config_file_r:
            # config = json.load(config_file_r)
            # config_d = json.dumps(config, sort_keys=True, indent=4, separators=(',', ': '))

        try:
            os.makedirs('./PickNameConfig/', exist_ok=True)
            file_dir = r'./PickNameConfig/config.json'
            # 创建names.txt和g_names.txt文件并写入示例内容
            names_file_dir = './PickNameConfig/names.txt'
            g_names_file_dir = './PickNameConfig/g_names.txt'
            example_names = '名字1\n名字2\n名字3\n'
            g_example_names = '女名1\n女名2\n女名3\n'

            config_v = {
                'pick_again': self.pick_again,
                'animation': self.animation,
                'animation_time': self.animation_time,
                'is_save': self.is_save,
                'speak_name': self.speak_name,
                'pick_balanced': self.pick_balanced,
                'picked_count': self.picked_count,
                'config_version': self.config_version,
                'can_pick_names': self.names,
            }
            try:
                with open(names_file_dir, 'r', encoding='utf-8') as names_file:
                    # 逐行读取文件并去掉每行末尾的换行符
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
                    self.is_save_checkbox.setChecked(self.is_save)
                    self.pick_again = config['pick_again']
                    self.animation = config['animation']
                    self.animation_time = config['animation_time']
                    self.can_pick_names = config['can_pick_names']
                    self.picked_count = config['picked_count']
                    self.speak_name = config['speak_name']
                    self.pick_balanced = config['pick_balanced']
                    self.pick_read_checkbox.setChecked(self.speak_name)
                    self.pick_again_checkbox.setChecked(self.pick_again)
                    self.pick_animation_checkbox.setChecked(self.animation)
                    self.block_signals(False)

            except FileNotFoundError as e:
                create_config()
                QMessageBox.information(self, '提示', '配置文件夹创建成功!\n请在names.txt文件中编辑名单!')
                print(e)
                sys.exit('CREATED_CONFIG_SUCCESSFULLY')
        except Exception as e:
            QMessageBox.critical(self, '错误',
                                 '配置文件创建或读取错误!\n请检查程序是否有对当前文件夹的读写权限\n或尝试删除配置文件夹中的config.json\n错误信息:' + str(
                                     e))
            print("错误信息:", e)
            sys.exit('FAILED_TO_LOAD_CONFIG')

    # 配置文件写入
    def save_config(self):
        try:
            file_dir = r'./PickNameConfig/config.json'
            with open(file_dir, 'r', encoding='utf-8') as config_file:
                config = json.load(config_file)
                config['is_save'] = self.is_save
                config['pick_again'] = self.pick_again
                config['animation'] = self.animation
                config['speak_name'] = self.speak_name
                config['pick_balanced'] = self.pick_balanced
                if self.is_save:
                    config['can_pick_names'] = self.can_pick_names
                else:
                    config['can_pick_names'] = self.names
                config['picked_count'] = self.picked_count
            with open(file_dir, 'w', encoding='utf-8') as config_file:
                json.dump(config, config_file, ensure_ascii=False)
        except Exception as e:
            QMessageBox.critical(self, '错误', '配置文件写入错误！')
            print("配置文件写入错误:", e)

    def set_pick_again(self):
        if not self.pick_again:
            self.pick_again = True
            self.can_pick_names = self.names.copy()
            QMessageBox.information(self, '提示', '切换成功,已清空已抽取名单')
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
                                    "该操作将清空已抽取的名字，继续吗？\n 这次将无法再使用重复抽取功能，如有需要请重启",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
                self.pick_again = False
                self.pick_again_checkbox.setCheckState(False)
                self.pick_again_checkbox.setDisabled(True)
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
                                    "该操作将清空已抽取的名字，继续吗？\n 这次将无法再使用重复抽取功能，如有需要请重启",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
                self.pick_again = False
                self.pick_again_checkbox.setCheckState(False)
                self.pick_again_checkbox.setDisabled(True)
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
            QMessageBox.information(self, "提示", "所有名字已抽取完毕，请重置名单")
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
            # if self.speak_name:
            #     self.say(self.selected_name)
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
        if self.pick_only_g or self.pick_only_b or self.pick_again:
            self.reset(no_tip=True)
            QApplication.quit()
        else:
            self.save_config()
            QApplication.quit()

    def block_signals(self, state=True):
        if state:
            self.b_names_pick_checkbox.stateChanged.disconnect()
            self.pick_again_checkbox.stateChanged.disconnect()
            self.g_names_pick_checkbox.stateChanged.disconnect()
            self.pick_animation_checkbox.stateChanged.disconnect()
            self.pick_read_checkbox.stateChanged.disconnect()
            self.is_save_checkbox.stateChanged.disconnect()
        else:
            self.b_names_pick_checkbox.stateChanged.connect(self.set_pick_group_b)
            self.g_names_pick_checkbox.stateChanged.connect(self.set_pick_group_g)
            self.pick_again_checkbox.stateChanged.connect(self.set_pick_again)
            self.pick_animation_checkbox.stateChanged.connect(self.set_animation)
            self.pick_read_checkbox.stateChanged.connect(self.set_speak)
            self.is_save_checkbox.stateChanged.connect(self.set_save)

    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()




if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建应用
    window = PickName()  # 创建主窗口
    window.show()  # 显示窗口
    sys.exit(app.exec_())  # 进入应用的主循环
