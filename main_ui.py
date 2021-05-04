import sys
import PySide2.QtWidgets as QtWidgets
from ui_utils import webview, highlighter
from neo4j_utils import neo4j
import ner.getEntities as entity
import data_utils as util


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("信息挖掘")
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
        self.button3 = QtWidgets.QPushButton(text='保存信息')
        self.button3.clicked.connect(self.click3)
        # 按钮4：打开h5页面
        self.button4 = QtWidgets.QPushButton(text='图谱页面')
        self.button4.clicked.connect(self.click4)
        self.mainlayout.addWidget(self.button4)
        # 文本框：显示文本信息
        self.textEdit = QtWidgets.QTextEdit()
        self.textEdit.setWindowOpacity(0.1)
        self.textEdit.setPlaceholderText('//请导入文本')

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
        # 定义高亮方法
        self.highLighter = highlighter.MyHighlighter(self.textEdit)
        # 保存实体类别和二元组
        self.covid = []
        self.gene = []
        self.phen = []
        self.protein = []
        self.doubles = []

    # 打开文件
    def click1(self):
        str = '新冠中ACE2和受体基因血管紧张素转化酶2有关，且会导致发热现象。'
        # fileDialog = QtWidgets.QFileDialog()
        # path = fileDialog.getOpenFileName(dir='/Users/yucheng', filter='(*.txt)')
        # with open(path[0], 'r') as f:
        #     str = f.read()
        self.textEdit.setPlainText(str)
        # self.label.setText('导入文件 {}'.format(path))

    # 开始分析
    def click2(self):
        text = self.textEdit.toPlainText()
        sentences = util.split_text_to_sentences(text)
        for sen in sentences:  # 删除空元素
            if not sen:
                sentences.remove(sen)
        hl = []
        for sentence in sentences:
            predict = entity.predict(sentence)
            self.covid, self.gene, self.phen, self.protein = util.classify_kind_to_list(predict)
            hl = hl+util.handle_list_to_highlight(self.covid, self.gene, self.phen, self.protein)
            sentence_double = util.getDouble_by_sentence(predict)
            for sd in sentence_double:
                if sd not in self.doubles:
                    self.doubles.append(sd)
            print('predict:{}'.format(predict))
        self.highLighter.setHighLightData(hl)
        self.highLighter.highlightBlock(self.textEdit.toPlainText())
        self.textEdit.setText(self.textEdit.toPlainText())
        self.label.setText('分析完成！')

    # 保存信息
    def click3(self):
        neo = neo4j.Neo4j()
        if neo.insertNeo4j(self.doubles):
            self.label.setText('保存成功！')
        else:
            self.label.setText('请打开neo4j服务...')

    # 图谱h5
    def click4(self):
        webWin = QtWidgets.QMainWindow(self)
        webWin.setFixedSize(900, 600)
        wv = webview.WebView(webWin)
        wv.setFixedSize(webWin.size())
        webWin.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    # 预先初始化实体抽取模型
    entity.predict('世界卫生组织命名为"2019冠状病毒病"，是指2019新型冠状病毒感染导致的肺炎。')
    mainWin.label.setText('初始化完成，欢迎使用！')
    sys.exit(app.exec_())