import sys
from guide_ui import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
import requests

class Guide(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()  # 初始化QMainWindow
        self.setupUi(self)  # 使用UI设置界面

        self.version = 'v1.4.4'

        self.setWindowTitle("设置向导- ClassNamePicker - v{}".format(self.version))

        # 初始化页面索引
        self.current_page_index = 0

        # 禁用最大化按钮
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        # 禁用最小化按钮
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinimizeButtonHint)
        super().__init__()
        self.setupUi(self)  # 初始化 UI

        # 连接按钮信号和槽函数
        self.next_button.clicked.connect(self.next_page)
        self.back_button.clicked.connect(self.previous_page)
        #self.choose_file.clicked.connect(self.choose_file_dialog)
        #self.github_button.clicked.connect(self.open_github)
        #self.download.clicked.connect(self.download_update)

        # 初始化按钮状态
        self.update_buttons()

    def next_page(self):
        """切换到下一页"""
        if self.current_page_index < self.stackedWidget.count() - 1:
            self.current_page_index += 1
            self.stackedWidget.setCurrentIndex(self.current_page_index)
        self.update_buttons()

    def previous_page(self):
        """切换到上一页"""
        if self.current_page_index > 0:
            self.current_page_index -= 1
            self.stackedWidget.setCurrentIndex(self.current_page_index)
        self.update_buttons()

    def update_buttons(self):
        """更新按钮状态"""
        self.back_button.setEnabled(self.current_page_index > 0)
        self.next_button.setEnabled(self.current_page_index < self.stackedWidget.count() - 1)

        # 如果是最后一页，修改“下一步”按钮为“完成”
        if self.current_page_index == self.stackedWidget.count() - 1:
            self.next_button.setText("完成")
            # self.next_button.clicked.disconnect()
            # self.next_button.clicked.connect(self.finish)
        else:
            self.next_button.setText("下一步")
            self.next_button.clicked.disconnect()
            self.next_button.clicked.connect(self.next_page)

        if self.current_page_index == 1:
            self.check_update()

    def check_update(self):
        """更新检查"""
        self.progress_bar.setValue(0)
        self.download.setEnabled(False)
        # 使用 QTimer 模拟进度条更新
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(250)

        # try:
        #     response = requests.get("https://api.github.com/repos/Chengzi600/ClassNamePicker/releases/latest")
        #     latest_version = response.json()['tag_name']
        #     latest_version_info = response.json()['body']
        #     if latest_version == self.version:
        #         self.timer.stop()
        #         self.progress_bar.setValue(100)
        #         self.update_info.setText("当前已是最新版本！\n版本号:{}\n点击【下一步】以继续".format(self.version))
        #     else:
        #         self.timer.stop()
        #         self.progress_bar.setValue(100)
        #         self.update_info.setText("发现新版本！建议先升级\n当前版本:{}\n最新版本:{}\n更新信息:{}\n点击【下载新版本】跳转到 Github 下载，或点击底部【下一步】跳过".format(self.version, latest_version, latest_version_info))
        #         self.download.setEnabled(True)
        # except Exception as e:
        #     print('检查更新失败:', e)
        #     self.timer.stop()
        #     self.progress_bar.setValue(100)
        #     self.update_info.setText("检查失败！\n错误信息:{}\n您可在稍后配置完成后重试，点击【下一步】以继续".format(str(e)))


    def update_progress(self):
        """更新进度条"""
        current_value = self.progress_bar.value()
        if current_value < 100:
            self.progress_bar.setValue(current_value + 5)
        else:
            self.timer.stop()
            self.update_info.setText("检查超时！您可在稍后配置完成后重试，点击【下一步】以继续")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Guide()
    window.show()
    sys.exit(app.exec_())
