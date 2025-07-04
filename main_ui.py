# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLCDNumber,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMenuBar,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)


class Ui_atlottery(object):
    def setupUi(self, atlottery):
        if not atlottery.objectName():
            atlottery.setObjectName("atlottery")
        atlottery.setWindowModality(Qt.WindowModality.WindowModal)
        atlottery.resize(360, 220)
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(atlottery.sizePolicy().hasHeightForWidth())
        atlottery.setSizePolicy(sizePolicy)
        atlottery.setMinimumSize(QSize(360, 220))
        atlottery.setMaximumSize(QSize(360, 220))
        font = QFont()
        font.setFamilies(["Noto Sans KR"])
        font.setPointSize(10)
        atlottery.setFont(font)
        self.centralwidget = QWidget(atlottery)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 9, 261, 61))
        self.verticalLayout_id_password = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_id_password.setObjectName("verticalLayout_id_password")
        self.verticalLayout_id_password.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_id = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_id.setObjectName("lineEdit_id")
        self.lineEdit_id.setSizeIncrement(QSize(0, 0))
        self.lineEdit_id.setBaseSize(QSize(0, 0))

        self.verticalLayout_id_password.addWidget(self.lineEdit_id)

        self.lineEdit_password = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.lineEdit_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.verticalLayout_id_password.addWidget(self.lineEdit_password)

        self.pushButton_login = QPushButton(self.centralwidget)
        self.pushButton_login.setObjectName("pushButton_login")
        self.pushButton_login.setGeometry(QRect(280, 9, 71, 61))
        font1 = QFont()
        font1.setFamilies(["Noto Sans KR"])
        font1.setPointSize(10)
        font1.setBold(True)
        self.pushButton_login.setFont(font1)
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 80, 341, 41))
        self.horizontalLayout_balance = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_balance.setObjectName("horizontalLayout_balance")
        self.horizontalLayout_balance.setContentsMargins(0, 0, 0, 0)
        self.label_balance = QLabel(self.horizontalLayoutWidget)
        self.label_balance.setObjectName("label_balance")
        sizePolicy.setHeightForWidth(
            self.label_balance.sizePolicy().hasHeightForWidth()
        )
        self.label_balance.setSizePolicy(sizePolicy)
        self.label_balance.setMaximumSize(QSize(50, 16777215))
        self.label_balance.setFont(font1)
        self.label_balance.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_balance.setStyleSheet("")
        self.label_balance.setFrameShadow(QFrame.Shadow.Plain)
        self.label_balance.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_balance.addWidget(self.label_balance)

        self.lcdNumber_balance = QLCDNumber(self.horizontalLayoutWidget)
        self.lcdNumber_balance.setObjectName("lcdNumber_balance")

        self.horizontalLayout_balance.addWidget(self.lcdNumber_balance)

        self.horizontalLayoutWidget_2 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(10, 130, 341, 32))
        self.horizontalLayout_count_buy = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_count_buy.setObjectName("horizontalLayout_count_buy")
        self.horizontalLayout_count_buy.setContentsMargins(0, 0, 0, 0)
        self.spinBox_count = QSpinBox(self.horizontalLayoutWidget_2)
        self.spinBox_count.setObjectName("spinBox_count")
        self.spinBox_count.setEnabled(False)
        self.spinBox_count.setMinimumSize(QSize(0, 30))
        self.spinBox_count.setMaximumSize(QSize(75, 16777215))
        self.spinBox_count.setMinimum(1)
        self.spinBox_count.setMaximum(5)

        self.horizontalLayout_count_buy.addWidget(self.spinBox_count)

        self.pushButton_buy = QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_buy.setObjectName("pushButton_buy")
        self.pushButton_buy.setEnabled(False)
        self.pushButton_buy.setMinimumSize(QSize(0, 30))
        self.pushButton_buy.setFont(font1)

        self.horizontalLayout_count_buy.addWidget(self.pushButton_buy)

        atlottery.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(atlottery)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 360, 33))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName("menu")
        atlottery.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(atlottery)
        self.statusbar.setObjectName("statusbar")
        atlottery.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(atlottery)

        QMetaObject.connectSlotsByName(atlottery)

    # setupUi

    def retranslateUi(self, atlottery):
        atlottery.setWindowTitle(
            QCoreApplication.translate(
                "atlottery", "\uc790\ub3d9\uad6c\ub9e4 | \ub3d9\ud589\ubcf5\uad8c", None
            )
        )
        self.lineEdit_id.setPlaceholderText(
            QCoreApplication.translate("atlottery", "\uc544\uc774\ub514", None)
        )
        self.lineEdit_password.setText("")
        self.lineEdit_password.setPlaceholderText(
            QCoreApplication.translate("atlottery", "\ube44\ubc00\ubc88\ud638", None)
        )
        self.pushButton_login.setText(
            QCoreApplication.translate("atlottery", "\ub85c\uadf8\uc778", None)
        )
        self.label_balance.setText(
            QCoreApplication.translate("atlottery", "\uc608\uce58\uae08", None)
        )
        self.pushButton_buy.setText(
            QCoreApplication.translate("atlottery", "\uad6c\ub9e4", None)
        )
        self.menu.setTitle(
            QCoreApplication.translate(
                "atlottery", "\ub3d9\ud589\ubcf5\uad8c \ubc14\ub85c\uac00\uae30", None
            )
        )

    # retranslateUi
