# ClassNamePicker 主程序
# ClassNamePicker.py

import random
import sys
import time
import requests
import webbrowser
import psutil

from ui import Ui_MainWindow
from FloatingWindow import FloatingWindow
from ConfigPage import ConfigWindow
from PickerConfigManager import ConfigManager
from AutoStartManager import AutoStartManager
from version import APP_VERSION, APP_VERSION_TIME, APP_VERSION_INFO, CONFIG_VERSION

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal, QPoint, QRect
from PyQt5.QtGui import QCursor
from PyQt5 import QtCore
from loguru import logger

class SpeechThread(QThread):
    """
    异步语音播报线程
    用于在后台线程中调用 pyttsx3 播报姓名，避免阻塞主界面。
    播报结束后通过 finished 信号通知主线程。
    """
    finished = pyqtSignal()
    
    def __init__(self, text, speak_speed=170):
        super().__init__()
        self.text = text
        self.speak_speed = speak_speed

    def run(self):
        try:
            import pyttsx3
            engine = pyttsx3.init(driverName='sapi5')
            engine.setProperty('rate', self.speak_speed)
            logger.info(f'触发语音播报 - 内容:"{self.text}"')
            engine.say(self.text)
            engine.runAndWait()
        except Exception as e:
            logger.error(f"语音错误: {e}")
        finally:
            self.finished.emit()

class PickName(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # 配置窗口实例
        self.config_window = None
        # 语音线程实例
        self.speech_thread = None

        # 版本信息（集中管理）
        self.version = APP_VERSION
        self.version_time = APP_VERSION_TIME
        self.version_info = APP_VERSION_INFO
        self.config_version = CONFIG_VERSION

        # 名单相关
        self.names = []      # 全部名单
        self.g_names = []    # 女生名单
        self.b_names = []    # 男生名单
        self.can_pick_names = self.names.copy()  # 可抽取名单

        # 功能状态变量
        self.pick_again = False         # 是否允许重复抽取
        self.animation = True           # 是否启用动画
        self.recite = False             # 是否背书模式
        self.is_save = False            # 是否保存抽取结果
        self.pick_only_g = False        # 只抽女生
        self.pick_only_b = False        # 只抽男生
        self.speak_name = True          # 是否语音播报
        self.pick_balanced = False      # 是否平衡抽取
        self.is_show_floating = True    # 是否显示悬浮窗
        self.animation_time = 0.8       # 动画时长
        self.picked_count = 0           # 已抽取次数
        self.wait_recite_time = 3       # 背书倒计时
        self.floating_x_size = 130      # 悬浮窗宽度
        self.floating_y_size = 130      # 悬浮窗高度
        self.speak_speed = 170          # 语音播报速度
        self.start_time = 0             # 计时起点
        self.elapsed_time = 0           # 已用时间
        self.is_running = False         # 是否正在运行
        self.anti_block = False         # 防希沃管家拦截

        super().__init__()  # 初始化QMainWindow
        self.setupUi(self)  # 使用UI设置界面
        self.setWindowTitle(
            "课堂随机点名{}- ClassNamePicker - {}({})".format(self.version_info, self.version, self.version_time))
        # 禁用最大化按钮
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        # 禁用最小化按钮
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinimizeButtonHint)
        self.setWindowFlags(
            self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

        # 绑定控件信号
        self.pick_name_button.clicked.connect(self.pick_name)  # 抽取按钮
        self.reset_button.setEnabled(True)
        self.reset_button.clicked.connect(self.reset)           # 重置按钮
        self.pick_time_checkbox.stateChanged.connect(self.set_recite)  # 背书模式
        self.timer_label.hide()
        self.b_names_pick_checkbox.stateChanged.connect(self.set_pick_group_b)  # 只抽男生
        self.g_names_pick_checkbox.stateChanged.connect(self.set_pick_group_g)  # 只抽女生
        self.pick_again_checkbox.stateChanged.connect(self.set_pick_again)      # 允许重复抽取
        self.about_action.triggered.connect(self.about_menu)
        self.github_action.triggered.connect(self.github_menu)
        self.exit_action.triggered.connect(self.exit)
        self.config_action.triggered.connect(self.open_config_page)
        # ... 其他信号绑定 ...
        self.b_names_pick_checkbox.stateChanged.connect(self.set_pick_group_b)
        self.g_names_pick_checkbox.stateChanged.connect(self.set_pick_group_g)

        # 复选框，是否重复抽取
        self.pick_again_checkbox.stateChanged.connect(self.set_pick_again)

        # 链接 Action
        self.about_action.triggered.connect(self.about_menu)
        self.github_action.triggered.connect(self.github_menu)
        self.exit_action.triggered.connect(self.exit)
        self.config_action.triggered.connect(self.open_config_page)

        # 语音播报相关（见 SpeechThread）
        self.speak_speed = 170  # Default speak speed

        self.read_config()
        self.update_stats()

        # 创建悬浮窗实例
        self.floating_window = FloatingWindow(size_x=self.floating_x_size,size_y=self.floating_y_size, parent=self)

        # 当前配置窗口引用
        self.config_window = None

        # 防抖动定时器配置
        self.save_timer = QTimer()
        self.save_timer.setSingleShot(True)  # 单次触发模式
        self.save_timer.timeout.connect(self.save_config)

        # 检测希沃管家
        for proc in psutil.process_iter(['name','pid']):
            try:
                # logger.debug(proc.info)
                if proc.info['name'].lower() == 'wininit.exe'.lower():
                    self.anti_block = True
                    name = proc.info['name']
                    pid = proc.info['pid']
                    logger.warning(f'检测到希沃集控进程: {name}，PID: {pid}，已开启弹窗拦截保护')
            except Exception:
                pass

        logger.info('初始化完成')

    def read_config(self):
        """统一使用 ConfigManager 加载并应用配置"""
        # 确保配置目录和基础文件存在
        ConfigManager.initialize()

        # 读取名单文件
        try:
            names_text = ConfigManager.NAMES_FILE.read_text(encoding='utf-8')
            self.names = [line.strip() for line in names_text.splitlines() if line.strip()]
        except Exception:
            self.names = []

        try:
            g_names_text = ConfigManager.G_NAMES_FILE.read_text(encoding='utf-8')
            self.g_names = [line.strip() for line in g_names_text.splitlines() if line.strip()]
        except Exception:
            self.g_names = []

        # 计算男生名单
        self.b_names = [n for n in self.names if n not in set(self.g_names)]

        # 加载配置（安全模式）
        config = ConfigManager.load_safe()

        # 应用配置到界面/状态
        self.block_signals()
        self.is_save = config.get(ConfigManager.KEY_IS_SAVE, self.is_save)
        self.pick_again = config.get(ConfigManager.KEY_PICK_AGAIN, self.pick_again)
        self.animation = config.get(ConfigManager.KEY_ANIMATION, self.animation)
        self.animation_time = config.get(ConfigManager.KEY_ANIMATION_TIME, self.animation_time)
        self.can_pick_names = config.get(ConfigManager.KEY_CAN_PICK_NAMES, self.names.copy())
        self.picked_count = config.get(ConfigManager.KEY_PICKED_COUNT, self.picked_count)
        self.speak_name = config.get(ConfigManager.KEY_SPEAK_NAME, self.speak_name)
        self.speak_speed = config.get(ConfigManager.KEY_SPEAK_SPEED, self.speak_speed)
        self.pick_balanced = config.get(ConfigManager.KEY_PICK_BALANCED, self.pick_balanced)
        self.floating_x_size = config.get(ConfigManager.KEY_FLOATING_X_SIZE, self.floating_x_size)
        self.floating_y_size = config.get(ConfigManager.KEY_FLOATING_Y_SIZE, self.floating_y_size)
        window_width = config.get(ConfigManager.KEY_WINDOW_WIDTH, self.width())
        window_height = config.get(ConfigManager.KEY_WINDOW_HEIGHT, self.height())
        self.is_show_floating = config.get(ConfigManager.KEY_SHOW_FLOATING, self.is_show_floating)
        self.resize(window_width, window_height)
        self.pick_again_checkbox.setChecked(self.pick_again)
        #self.engine.setProperty('rate', self.speak_speed)
        self.block_signals(False)

        # 读取多音字替换配置
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

        # 在加载配置后添加自启动状态同步
        self.auto_start = config.get(ConfigManager.KEY_AUTO_START, False)
        actual_state = AutoStartManager.is_enabled()
        if self.auto_start != actual_state:
            # 状态不一致，以注册表为准并更新配置
            self.auto_start = actual_state
            config[ConfigManager.KEY_AUTO_START] = actual_state
            try:
                ConfigManager.save(config)
            except Exception:
                pass

    def save_config(self):
        """配置文件写入"""
        try:
            config = ConfigManager.load_safe()
            config[ConfigManager.KEY_PICK_AGAIN] = self.pick_again
            config[ConfigManager.KEY_PICK_BALANCED] = self.pick_balanced
            config[ConfigManager.KEY_CAN_PICK_NAMES] = self.can_pick_names if self.is_save else self.names
            config[ConfigManager.KEY_PICKED_COUNT] = self.picked_count
            config[ConfigManager.KEY_WINDOW_WIDTH] = self.width()
            config[ConfigManager.KEY_WINDOW_HEIGHT] = self.height()
            config[ConfigManager.KEY_SPEAK_SPEED] = self.speak_speed
            ConfigManager.save(config)
        except Exception as e:
            QMessageBox.critical(self, '错误', '配置文件写入错误！')
            logger.error(f"配置文件写入错误: {e}")

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

    def set_pick_group_g(self):
        self.block_signals(True)
        if not self.pick_only_g:
            if QMessageBox.question(self, "继续吗",
                                    "该操作将清空已抽取的名字",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
                self.pick_again = False
                self.pick_again_checkbox.setCheckState(False)
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

        if not self.can_pick_names:
            self._show_completion_message()
            return

        if self.animation:
            self.start_time = time.time()
            self.pick_animation()
        else:
            self._display_result()

        # 更新统计信息
        self.update_stats()
        # self.save_config()
    
    def _show_completion_message(self):
        """显示完成提示"""
        self.name_label.setText("请重置")
        self.name_label.setStyleSheet("color: red")
        QMessageBox.information(self, "提示", "所有名字已抽取完毕，请重置")
        self.reset_button.setEnabled(True)
        self.pick_name_button.setEnabled(False)
    
    def _display_result(self):
        """显示最终结果"""
        random_name_memory = random_name = random.choice(self.can_pick_names)
        logger.info(f'random函数调用结果:{random_name_memory} | 抽选列表长度:{len(self.can_pick_names)} | 列表内容:{self.can_pick_names}')
        # if ( len(self.can_pick_names) > 1 ) and ( not random.randint(0,random_name.count(' ') + 1) < 1 ) :
        #     while random_name == random_name_memory:
        #         logger.warning('侦测到与上次抽选结果相同，重新抽取!')
        #         random_name = random.choice(self.can_pick_names)
        #         logger.info(f'random函数调用结果:{random_name_memory}')
        #         logger.info(f'抽选列表长度:{len(self.can_pick_names)}')
        #         logger.info(f'列表内容:{self.can_pick_names}')
        #         logger.info('='*10)
        #         #print('2333')
        # #else:
        # #    print(random_name)
        
        self.name_label.setText(random_name)
        
        # 异步语音播报
        if self.speak_name:
            self._speak_name_async(random_name)
        
        # 更新状态
        if ( random_name in self.can_pick_names ) and ( not self.pick_again ):
            self.can_pick_names.remove(random_name)
            self.reset_button.setEnabled(True)
        
        self.picked_count += 1
        self.update_stats()
        self.pick_name_button.setEnabled(True)
        
        if self.recite:
            self.perform_countdown(self.wait_recite_time)
    
    def _speak_name_async(self, text):
        """异步播报，确保同一时刻只有一个语音线程，避免 run loop already started 错误"""
        # 多音字替换
        name_changes = ConfigManager.load_name_changes()
        for i in range(1, 4):
            orig = name_changes.get(f'speak_change_{chr(96+i)}1', '')
            repl = name_changes.get(f'speak_change_{chr(96+i)}2', '')
            if text == orig and repl:
                text = repl
                break

        # 如果有语音线程在运行，直接返回，避免并发
        if self.speech_thread and self.speech_thread.isRunning():
            # 可选：弹窗提示或直接 return，防止 run loop already started
            logger.warning("语音线程正在播报，等待播报结束")
            return

        self.speech_thread = SpeechThread(text, speak_speed=self.speak_speed)
        self.speech_thread.finished.connect(self._on_speech_finished)
        self.pick_name_button.setEnabled(False)  # 语音播报时禁用按钮
        self.speech_thread.start()

    def _on_speech_finished(self):
        self.pick_name_button.setEnabled(True)

    def perform_countdown(self, seconds):
        self.timer_label.setStyleSheet("color=red")
        self.timer_label.setText(f"{seconds:.1f}s")
        if seconds > 0:
            QTimer.singleShot(100, lambda: self.perform_countdown(seconds - 0.1))
        else:
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
                self.reset_button.setEnabled(False)
        self.block_signals(False)

    def pick_animation(self):
        if len(self.can_pick_names) <= 2:
            self._display_result()
            return
        
        if time.time() - self.start_time < self.animation_time:  # 动画时间内不断变化
            rdm_name = random.choice(self.can_pick_names)
            self.name_label.setText(rdm_name)
            QTimer.singleShot(10, self.pick_animation)  # 每 10 毫秒重新调用
        else:
            self._display_result()
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
            logger.error(f'检查更新失败: {e}')
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
        """重写关闭事件，释放资源并调用父类方法"""
        logger.info('触发关闭事件')
        if self.anti_block:
            # 获取鼠标在屏幕上的位置
            mouse_global_pos = QCursor.pos()
            logger.debug(f'鼠标位置:{mouse_global_pos}')

            # 获取窗口的框架几何（包括标题栏和边框）
            frame_rect = self.frameGeometry()

            close_button_width = 600
            close_button_height = 600
            close_button_rect = QRect(
                frame_rect.right() - close_button_width,
                frame_rect.top(),
                close_button_width,
                close_button_height
            )
            logger.debug(f'关闭按钮位置:{close_button_rect}')

            # 判断鼠标是否在关闭按钮区域内
            if close_button_rect.contains(mouse_global_pos):
                logger.info("检测为用户点击关闭按钮，执行正常关闭流程")
            else:
                logger.warning("检测到非法关闭，已拦截")
                event.ignore()
                return

        # 停止语音线程
        if hasattr(self, 'speech_thread') and self.speech_thread and self.speech_thread.isRunning():
            self.speech_thread.quit()
            self.speech_thread.wait()
        # 停止定时器
        if hasattr(self, 'save_timer') and self.save_timer:
            self.save_timer.stop()

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
        # 调用父类关闭事件，确保彻底关闭
        #super().closeEvent(event)
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

if __name__ == "__main__":
    # QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    # QGuiApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    # QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)  # 创建应用
    window = PickName()  # 创建主窗口
    window.show()  # 显示窗口
    sys.exit(app.exec_())  # 进入应用的主循环
