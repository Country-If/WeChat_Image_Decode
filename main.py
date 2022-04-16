#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Maylon"


import os
import sys
import re
from threading import Thread
from PySide2.QtWidgets import *
from PySide2.QtCore import QFile, Signal, QObject
from PySide2.QtUiTools import QUiLoader


# os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = 'platforms'   # 打包取消注释


class MySignal(QObject):
    success_signal = Signal()


class main_ui:
    def __init__(self):
        qfile = QFile("ui/main_ui.ui")
        qfile.open(qfile.ReadOnly)
        qfile.close()
        self.ui = QUiLoader().load(qfile)
        self.files_list = None
        self.default_path = "./"
        self.save_path = ""
        self.key = ""
        self.my_signal = MySignal()

        self.ui.decode_btn.clicked.connect(self.decode)
        self.ui.get_key_btn.clicked.connect(self.get_key)
        self.ui.set_default_btn.clicked.connect(self.set_default_path)
        self.my_signal.success_signal.connect(self.success)

    def decode(self):
        """
        batch decode dat files

        :return: None
        """
        try:
            if self.key == "":
                QMessageBox.critical(self.ui, '错误', '请先获取加密密钥')
            else:
                f = QFileDialog.getOpenFileNames(self.ui, '选择文件', '')
                if f:
                    if self.save_path == "":
                        sp = QFileDialog.getExistingDirectory(self.ui, '请选择一个文件夹作为文件存放路径')
                        if sp:
                            self.save_path = sp
                            self.files_list = f[0]
                            file_name_list = [re.findall(r'([^<>/\\\|:""\*\?]+)\.\w+$', f) for f in self.files_list]
                            if not os.path.exists(self.save_path):
                                os.mkdir(self.save_path)

                            def threadFunc():
                                for i in range(len(self.files_list)):
                                    self.imageDecode(self.files_list[i], file_name_list[i][0])
                                self.my_signal.success_signal.emit()

                            thread = Thread(target=threadFunc)
                            thread.start()
        except Exception as e:
            QMessageBox.critical(self.ui, '错误', str(e))

    def get_key(self):
        """
        get the encode key

        :return: None
        """
        try:
            file = QFileDialog.getOpenFileName(self.ui, '请打开一个bat文件用于获取加密密钥', self.default_path, 'dat files(*.dat)')[0]
            if file:
                xor_code = get_xor_code(file)
                if xor_code == "":
                    QMessageBox.critical(self.ui, '错误', '获取dat十六进制值失败')
                else:
                    self.key = hex(int(xor_code, 16) ^ int('ffd8', 16))[-2:]
                    QMessageBox.information(self.ui, '成功', '解密密钥为 0x' + self.key)
        except Exception as e:
            QMessageBox.critical(self.ui, '错误', str(e))

    def set_default_path(self):
        """
        set a default path

        :return: None
        """
        p = QFileDialog.getExistingDirectory(self.ui, '请选择一个文件夹作为默认路径')
        if p:
            self.default_path = p

    def imageDecode(self, filename, output_filename):
        """
        main decode function: transfer a dat file to png file

        :param filename: the absolute file path
        :param output_filename: only the file name
        :return: None
        """
        dat = open(filename, 'rb')
        out = self.save_path + '/' + output_filename + ".png"
        png = open(out, 'wb')
        for now in dat:
            for nowByte in now:
                newByte = nowByte ^ int(self.key, 16)
                png.write(bytes([newByte]))
        dat.close()
        png.close()

    def success(self):
        QMessageBox.information(self.ui, '成功', '处理完成')


def get_xor_code(filename):
    """
    open file and get its xor code

    :param filename: the absolute file path
    :return: xor code if success else ""
    """
    f = open(filename, "rb")
    res = ""
    for i in range(1, 3):
        c = f.read(1)
        if not c:
            break
        if i % 32 != 0:
            if ord(c) <= 15:
                res += ("0x0" + hex(ord(c))[2:])[2:]
            else:
                res += (hex(ord(c)))[2:]
    f.close()
    return res


if __name__ == '__main__':
    app = QApplication()
    Window = main_ui()
    Window.ui.show()
    sys.exit(app.exec_())
