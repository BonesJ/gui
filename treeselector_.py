# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'treeselector.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!


from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

DB = "Alpha.db"

class Ui_(QtGui.QWidget):
    def __init__(self, parent=None):
        super(QtGui.QWidget,self).__init__(parent)
        self.layoutWidget = QtGui.QWidget()
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 624, 165))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_25 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_25.setObjectName(_fromUtf8("verticalLayout_25"))
        self.horizontalLayout_23 = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_23.setObjectName(_fromUtf8("horizontalLayout_23"))
        self.pushButton_16 = QtGui.QPushButton("Add Item")
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_16.sizePolicy().hasHeightForWidth())
        self.pushButton_16.setSizePolicy(sizePolicy)
        self.pushButton_16.setObjectName(_fromUtf8("pushButton_16"))
        self.horizontalLayout_23.addWidget(self.pushButton_16)
        self.pushButton_17 = QtGui.QPushButton("Add Subitem")
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_17.sizePolicy().hasHeightForWidth())
        self.pushButton_17.setSizePolicy(sizePolicy)
        self.pushButton_17.setObjectName(_fromUtf8("pushButton_17"))
        self.horizontalLayout_23.addWidget(self.pushButton_17)
        self.pushButton_18 = QtGui.QPushButton("Delete Item")
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_18.sizePolicy().hasHeightForWidth())
        self.pushButton_18.setSizePolicy(sizePolicy)
        self.pushButton_18.setObjectName(_fromUtf8("pushButton_18"))
        self.horizontalLayout_23.addWidget(self.pushButton_18)
        self.verticalLayout_25.addLayout(self.horizontalLayout_23)
        self.treeWidget_4 = QtGui.QTreeView(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget_4.sizePolicy().hasHeightForWidth())
        self.treeWidget_4.setSizePolicy(sizePolicy)
        self.treeWidget_4.setSizeIncrement(QtCore.QSize(0, 1))
        self.treeWidget_4.setAlternatingRowColors(False)
        self.treeWidget_4.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.treeWidget_4.setObjectName(_fromUtf8("treeWidget_4"))
        self.treeWidget_4.header().setStretchLastSection(True)
        self.verticalLayout_25.addWidget(self.treeWidget_4)
        self.horizontalLayout.addLayout(self.verticalLayout_25)
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.radioButton_7 = QtGui.QRadioButton("Unit Price ($/unit)")
        self.radioButton_7.setObjectName(_fromUtf8("radioButton_7"))
        self.verticalLayout_8.addWidget(self.radioButton_7)
        self.horizontalLayout_28 = QtGui.QHBoxLayout()
        self.horizontalLayout_28.setObjectName(_fromUtf8("horizontalLayout_28"))
        self.doubleSpinBox_7 = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.doubleSpinBox_7.setMaximum(999999999.99)
        self.doubleSpinBox_7.setSingleStep(10000.0)
        self.doubleSpinBox_7.setObjectName(_fromUtf8("doubleSpinBox_7"))
        self.horizontalLayout_28.addWidget(self.doubleSpinBox_7)
        self.pushButton_6 = QtGui.QPushButton("Edit")
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy)
        self.pushButton_6.setMinimumSize(QtCore.QSize(28, 23))
        self.pushButton_6.setMaximumSize(QtCore.QSize(28, 23))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.horizontalLayout_28.addWidget(self.pushButton_6)
        self.verticalLayout_8.addLayout(self.horizontalLayout_28)
        self.label_20 = QtGui.QLabel(self.layoutWidget)
        self.label_20.setAlignment(QtCore.Qt.AlignCenter)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.verticalLayout_8.addWidget(self.label_20)
        self.radioButton_8 = QtGui.QRadioButton("Rate ($/hr)")
        self.radioButton_8.setObjectName(_fromUtf8("radioButton_8"))
        self.verticalLayout_8.addWidget(self.radioButton_8)
        self.horizontalLayout_29 = QtGui.QHBoxLayout()
        self.horizontalLayout_29.setObjectName(_fromUtf8("horizontalLayout_29"))
        self.doubleSpinBox_8 = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.doubleSpinBox_8.setMaximum(999999999.99)
        self.doubleSpinBox_8.setSingleStep(10000.0)
        self.doubleSpinBox_8.setObjectName(_fromUtf8("doubleSpinBox_8"))
        self.horizontalLayout_29.addWidget(self.doubleSpinBox_8)
        self.pushButton_15 = QtGui.QPushButton("Edit")
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_15.sizePolicy().hasHeightForWidth())
        self.pushButton_15.setSizePolicy(sizePolicy)
        self.pushButton_15.setMinimumSize(QtCore.QSize(28, 23))
        self.pushButton_15.setMaximumSize(QtCore.QSize(28, 23))
        self.pushButton_15.setObjectName(_fromUtf8("pushButton_15"))
        self.horizontalLayout_29.addWidget(self.pushButton_15)
        self.verticalLayout_8.addLayout(self.horizontalLayout_29)
        spacerItem = QtGui.QSpacerItem(88, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        self.verticalLayout_8.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_8)
        self.setLayout(self.horizontalLayout)
        print "\n<<Successfully Added Tree selector>>\n"

        # connection = sqlite3.connect(DB)
        # cursor = connection.cursor()
        # # # UNCOMMENT SECTION FOR DEBUGGING /START/
        # # cursor.execute("""SELECT * FROM client""")
        # # result_all = cursor.fetchall()
        # # print "result all:", result_all
        # # # UNCOMMENT SECTION FOR DEBUGGING /END/

        # cursor.execute("""SELECT DISTINCT "Code Client" FROM client""")
        # result_key = cursor.fetchall()
        # connection.close()
        # # clients table ...
        # cursor.execute("""
        #     CREATE TABLE if not exisits "PRODUCTS STRUCT" (
        #     "key" INTEGER PRIMARY KEY AUTOINCREMENT,
        #     "Code Client" VARCHAR(30),
        #     "Nom" VARCHAR(30),
        #     "Societe" VARCHAR(30),
        #     "Telephone" VARCHAR(30),
        #     "Factures Payees" INTEGER(1),
        #     "Factures Recues" INTEGER(1),
        #     "Email" VARCHAR(40),
        #     UNIQUE ("key") );""")

        # # Populate db with some data ...
        # cursor = connection.cursor()
        # staff_data = [
        #     (55, "James", "kaloumba", "021 69 74 49", 5, 8, "ceemss.saiatgmail"),
        #     (7, "WilliamNOT", "sadoomba", "021 69 74 49", 5, 8, "cf.saiatgmail"),
        #     (7, "William", "badoomba", "021 69 74 49", 5, 8, "ceems.saiatgmail"),
        #     (7, "Williwas", "frambounda", "021 69 74 49", 5, 8, "ceemssatgmail")
        # ]
        # cursor.executemany("""
        #     INSERT INTO client ("key","Code Client", "Nom", "Societe", "Telephone",
        #         "Factures Payees", "Factures Recues", "Email")
        #     VALUES(NULL,?,?,?,?,?,?,?)""", staff_data)
        # connection.commit()
        # print "\n<<Successfully Created `PRODUCTS STRUCT` table>>\n"
