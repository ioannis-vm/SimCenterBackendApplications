# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Symbology_Window.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Symbology_Dialog(object):
    def setupUi(self, Symbology_Dialog):
        Symbology_Dialog.setObjectName('Symbology_Dialog')
        Symbology_Dialog.resize(491, 410)
        self.buttonBox = QtWidgets.QDialogButtonBox(Symbology_Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(180, 360, 161, 31))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok
        )
        self.buttonBox.setObjectName('buttonBox')
        self.range_table = QtWidgets.QTableWidget(Symbology_Dialog)
        self.range_table.setGeometry(QtCore.QRect(30, 80, 311, 261))
        self.range_table.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection
        )
        self.range_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.range_table.setObjectName('range_table')
        self.range_table.setColumnCount(3)
        self.range_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.range_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.range_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.range_table.setHorizontalHeaderItem(2, item)
        self.range_table.horizontalHeader().setStretchLastSection(True)
        self.method_combo = QtWidgets.QComboBox(Symbology_Dialog)
        self.method_combo.setGeometry(QtCore.QRect(30, 40, 111, 22))
        self.method_combo.setObjectName('method_combo')
        self.method_combo.addItem('')
        self.method_combo.addItem('')
        self.method_combo.addItem('')
        self.label = QtWidgets.QLabel(Symbology_Dialog)
        self.label.setGeometry(QtCore.QRect(30, 20, 47, 13))
        self.label.setObjectName('label')
        self.add_below_button = QtWidgets.QPushButton(Symbology_Dialog)
        self.add_below_button.setGeometry(QtCore.QRect(350, 110, 61, 23))
        self.add_below_button.setObjectName('add_below_button')
        self.remove_button = QtWidgets.QPushButton(Symbology_Dialog)
        self.remove_button.setGeometry(QtCore.QRect(350, 140, 61, 23))
        self.remove_button.setObjectName('remove_button')
        self.no_clases_line = QtWidgets.QLineEdit(Symbology_Dialog)
        self.no_clases_line.setGeometry(QtCore.QRect(220, 40, 61, 20))
        self.no_clases_line.setObjectName('no_clases_line')
        self.label_2 = QtWidgets.QLabel(Symbology_Dialog)
        self.label_2.setGeometry(QtCore.QRect(220, 20, 61, 16))
        self.label_2.setObjectName('label_2')
        self.sample_legend_widget = QtWidgets.QWidget(Symbology_Dialog)
        self.sample_legend_widget.setGeometry(QtCore.QRect(350, 220, 131, 111))
        self.sample_legend_widget.setObjectName('sample_legend_widget')
        self.color_combo = QtWidgets.QComboBox(Symbology_Dialog)
        self.color_combo.setGeometry(QtCore.QRect(350, 190, 91, 22))
        self.color_combo.setObjectName('color_combo')
        self.color_combo.addItem('')
        self.color_combo.addItem('')
        self.color_combo.addItem('')
        self.color_combo.addItem('')
        self.color_combo.addItem('')
        self.color_combo.addItem('')
        self.color_combo.addItem('')
        self.color_combo.addItem('')
        self.color_combo.addItem('')
        self.color_combo.addItem('')
        self.color_combo.addItem('')
        self.color_combo.addItem('')
        self.color_combo.addItem('')
        self.color_combo.addItem('')
        self.color_combo.addItem('')
        self.color_combo.addItem('')
        self.color_combo.addItem('')
        self.color_combo.addItem('')
        self.label_3 = QtWidgets.QLabel(Symbology_Dialog)
        self.label_3.setGeometry(QtCore.QRect(350, 170, 81, 20))
        self.label_3.setObjectName('label_3')
        self.add_up_button = QtWidgets.QPushButton(Symbology_Dialog)
        self.add_up_button.setGeometry(QtCore.QRect(350, 80, 61, 23))
        self.add_up_button.setObjectName('add_up_button')

        self.retranslateUi(Symbology_Dialog)
        self.buttonBox.accepted.connect(Symbology_Dialog.accept)
        self.buttonBox.rejected.connect(Symbology_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Symbology_Dialog)

    def retranslateUi(self, Symbology_Dialog):
        _translate = QtCore.QCoreApplication.translate
        Symbology_Dialog.setWindowTitle(_translate('Symbology_Dialog', 'Dialog'))
        item = self.range_table.horizontalHeaderItem(0)
        item.setText(_translate('Symbology_Dialog', 'Begining'))
        item = self.range_table.horizontalHeaderItem(1)
        item.setText(_translate('Symbology_Dialog', 'End'))
        item = self.range_table.horizontalHeaderItem(2)
        item.setText(_translate('Symbology_Dialog', 'Counts'))
        self.method_combo.setItemText(
            0, _translate('Symbology_Dialog', 'FisherJenks')
        )
        self.method_combo.setItemText(
            1, _translate('Symbology_Dialog', 'Equal Interval')
        )
        self.method_combo.setItemText(
            2, _translate('Symbology_Dialog', 'User Defined')
        )
        self.label.setText(_translate('Symbology_Dialog', 'Method'))
        self.add_below_button.setText(_translate('Symbology_Dialog', 'Add-Below'))
        self.remove_button.setText(_translate('Symbology_Dialog', 'Remove'))
        self.label_2.setText(_translate('Symbology_Dialog', 'No. of clasess'))
        self.color_combo.setItemText(0, _translate('Symbology_Dialog', 'Blues'))
        self.color_combo.setItemText(1, _translate('Symbology_Dialog', 'Greens'))
        self.color_combo.setItemText(2, _translate('Symbology_Dialog', 'Greys'))
        self.color_combo.setItemText(3, _translate('Symbology_Dialog', 'Reds'))
        self.color_combo.setItemText(4, _translate('Symbology_Dialog', 'Oranges'))
        self.color_combo.setItemText(5, _translate('Symbology_Dialog', 'binary'))
        self.color_combo.setItemText(6, _translate('Symbology_Dialog', 'gist_grey'))
        self.color_combo.setItemText(7, _translate('Symbology_Dialog', 'Seismic'))
        self.color_combo.setItemText(8, _translate('Symbology_Dialog', 'hsv'))
        self.color_combo.setItemText(9, _translate('Symbology_Dialog', 'Pastel1'))
        self.color_combo.setItemText(10, _translate('Symbology_Dialog', 'Pastel2'))
        self.color_combo.setItemText(11, _translate('Symbology_Dialog', 'Set1'))
        self.color_combo.setItemText(12, _translate('Symbology_Dialog', 'Set2'))
        self.color_combo.setItemText(13, _translate('Symbology_Dialog', 'Set3'))
        self.color_combo.setItemText(14, _translate('Symbology_Dialog', 'tab10'))
        self.color_combo.setItemText(15, _translate('Symbology_Dialog', 'tab20'))
        self.color_combo.setItemText(16, _translate('Symbology_Dialog', 'tab20b'))
        self.color_combo.setItemText(17, _translate('Symbology_Dialog', 'tab20c'))
        self.label_3.setText(_translate('Symbology_Dialog', 'Color Scheme'))
        self.add_up_button.setText(_translate('Symbology_Dialog', 'Add-Up'))


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Symbology_Dialog = QtWidgets.QDialog()
    ui = Ui_Symbology_Dialog()
    ui.setupUi(Symbology_Dialog)
    Symbology_Dialog.show()
    sys.exit(app.exec_())
