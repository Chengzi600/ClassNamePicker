from PyQt5.QtGui import QPainter, QBrush, QColor, QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPoint, QRect


class FloatingWindow(QWidget):
    def __init__(self, size, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(size, size)  # 悬浮窗大小

        # 用于记录鼠标位置
        self.old_pos = QPoint()

        # 父窗口（主窗口）
        self.parent_window = parent

        # 吸附距离
        self.snap_distance = 20
        # 默认透明度
        self.default_opacity = 1.0
        self.snap_opacity = 0.7

        # 标志：是否正在拖动
        self.is_dragging = False

    def paintEvent(self, event):
        # 绘制圆形和文字
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制蓝色圆形
        brush = QBrush(QColor(100, 200, 255, 200))  # 设置颜色和透明度
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, self.width(), self.height())

        # 绘制文字
        painter.setPen(QColor(255, 255, 255))
        font = QFont("黑体", 10, QFont.Bold)
        painter.setFont(font)
        text = "随机点名"
        painter.drawText(self.rect(), Qt.AlignCenter, text)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos() - self.pos()  # 记录鼠标点击时的位置
            self.is_dragging = False  # 初始为未拖动
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.is_dragging = True  # 标志正在拖动
            self.move(event.globalPos() - self.old_pos)  # 更新窗口位置
            self.snap_to_edge()
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if not self.is_dragging:
                self.hide()  # 如果没有拖动，触发单击事件
                if self.parent_window:
                    self.parent_window.show()
            event.accept()

    def snap_to_edge(self):
        # 获取屏幕大小
        screen_geometry = QApplication.primaryScreen().geometry()
        screen_rect = QRect(0, 0, screen_geometry.width(), screen_geometry.height())

        # 当前窗口中心点
        center = self.geometry().center()

        # 计算与各边缘的距离
        distances = {
            "left": abs(center.x() - screen_rect.left()),
            "right": abs(center.x() - screen_rect.right()),
            "top": abs(center.y() - screen_rect.top()),
            "bottom": abs(center.y() - screen_rect.bottom())
        }

        # 找到最近的边缘
        nearest_edge = min(distances, key=distances.get)

        # 吸附到最近边缘并只显示半圆
        if distances[nearest_edge] < self.snap_distance:
            if nearest_edge == "left":
                self.move(screen_rect.left() - self.width() // 2, self.y())  # 左边吸附
            elif nearest_edge == "right":
                self.move(screen_rect.right() - self.width() // 2, self.y())  # 右边吸附
            elif nearest_edge == "top":
                self.move(self.x(), screen_rect.top() - self.height() // 2)  # 顶部吸附
            elif nearest_edge == "bottom":
                self.move(self.x(), screen_rect.bottom() - self.height() // 2)  # 底部吸附

            # 提高透明度
            self.setWindowOpacity(self.snap_opacity)
        else:
            # 恢复默认透明度
            self.setWindowOpacity(self.default_opacity)
