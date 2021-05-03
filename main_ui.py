import sys
import PySide2.QtWidgets as QtWidgets
import PySide2.QtGui as QtGui
import PySide2.QtCore as QtCore
import PySide2.QtNetwork as QtNetwork
import PySide2.QtUiTools as QtUiTools
from ui_utils import highlighter, webview
import time
import ner.getEntities as ent


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("新冠信息挖掘")
        self.setFixedSize(600, 400)
        # 建立一个窗口，居中MainWindow
        self.mainWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.mainWidget)
        # 主要布局器，纵向布局
        self.mainlayout = QtWidgets.QVBoxLayout()
        self.mainWidget.setLayout(self.mainlayout)
        # 标签：存放提示、进度等
        self.label = QtWidgets.QLabel('程序构建中...')
        # 按钮1：打开文件
        self.button1 = QtWidgets.QPushButton(text='打开文件')
        self.button1.clicked.connect(self.click1)
        self.mainlayout.addWidget(self.button1)
        # 按钮2：分析文本
        self.button2 = QtWidgets.QPushButton(text='开始分析')
        self.button2.clicked.connect(self.click2)
        # 按钮3：查看文本关系
        self.button3 = QtWidgets.QPushButton(text='三元组关系')
        self.button3.clicked.connect(self.click3)
        # 按钮4：打开h5页面
        self.button4 = QtWidgets.QPushButton(text='图谱页面')
        self.button4.clicked.connect(self.click4)
        self.mainlayout.addWidget(self.button4)
        # 文本框：显示文本信息
        self.textEdit = QtWidgets.QTextEdit()
        self.textEdit.setWindowOpacity(0.1)
        self.textEdit.setPlaceholderText('//请输入文本')

        # 布局
        # 横向布局，保存分析、三元组、图谱按钮
        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.button2)
        self.hbox.addWidget(self.button3)
        self.hbox.addWidget(self.button4)
        self.mainlayout.addWidget(self.button1)
        self.mainlayout.addLayout(self.hbox)
        self.mainlayout.addWidget(self.label)
        self.mainlayout.addWidget(self.textEdit)
        # 其他的初始化
        # 定义高亮显示
        self.highLighter = highlighter.MyHighlighter(self.textEdit)

    def click1(self):
        # fileDialog = QtWidgets.QFileDialog()
        # path = fileDialog.getOpenFileName(dir='/Users/yucheng', filter='(*.txt)')
        # path = ['/Users/yucheng/Downloads/test.txt']
        str = '世界卫生组织命名为"2019冠状病毒病"，是指2019新型冠状病毒感染导致的肺炎。'
        # with open(path[0], 'r') as f:
        #     str = f.read()
        self.textEdit.setPlainText(str)

    def click2(self):
        # hl = [
        #     ['COVID', '新冠'],
        #     ['GENE', 'ACE'],
        #     ['PHEN', '咳嗽']
        # ]
        # self.highLighter.setHighLightData(hl)
        # self.highLighter.highlightBlock(self.textEdit.toPlainText().strip())
        print(ent.predict(self.textEdit.toPlainText()))

    def click3(self):
        pass

    def click4(self):
        webWin = QtWidgets.QMainWindow(self)
        webWin.setFixedSize(900,600)
        wv = webview.WebView(webWin)
        wv.setFixedSize(webWin.size())
        webWin.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    # 预先初始化实体抽取模型
    ent.predict('世界卫生组织命名为"2019冠状病毒病"，是指2019新型冠状病毒感染导致的肺炎。')
    mainWin.label.setText('初始化完成，欢迎使用！')
    sys.exit(app.exec_())