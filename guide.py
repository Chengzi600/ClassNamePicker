import sys
from PyQt5.QtWidgets import QApplication, QTableView, QVBoxLayout, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class TableViewExample(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("QTableView 示例")
        self.setGeometry(100, 100, 400, 300)

        # 创建布局
        layout = QVBoxLayout()

        # 创建 QTableView
        self.tableView = QTableView(self)

        # 创建数据模型
        self.model = QStandardItemModel(1, 2)  # 4 行 3 列


        # 填充数据
        for row in range(4):
            for col in range(3):
                item = QStandardItem(f"行{row + 1}, 列{col + 1}")
                self.model.setItem(row, col, item)

        # 将模型设置到 QTableView
        self.tableView.setModel(self.model)

        # 将 QTableView 添加到布局
        layout.addWidget(self.tableView)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TableViewExample()
    window.show()
    sys.exit(app.exec_())