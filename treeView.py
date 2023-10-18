import os
import re

from PyQt6.QtWidgets import QTreeView, QVBoxLayout, QWidget, QLineEdit, QMainWindow, QApplication
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtCore import QDir, Qt, QSortFilterProxyModel, QRegularExpression
import concurrent.futures


class FileSystemTreeViewer(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Отображение дерева файловой системы")
        self.setMaximumSize(1200, 1000)
        self.setMinimumSize(800, 600)
        self.app = QApplication.instance()

        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Файловая система"])

        self.sortModel = QSortFilterProxyModel()
        self.sortModel.setSourceModel(self.model)
        self.sortModel.setFilterKeyColumn(0)

        self.treeView = QTreeView(self)
        self.treeView.setModel(self.sortModel)
        self.treeView.setSortingEnabled(True)
        self.treeView.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers)

        self.filterLineEdit = QLineEdit(self)
        self.filterLineEdit.textChanged.connect(self.filter_tree)

        self.layout.addWidget(self.filterLineEdit)
        self.layout.addWidget(self.treeView)

        self.load_tree(os.path.expanduser("~"))
        rootIndex = self.sortModel.mapFromSource(self.model.index(0, 0))
        self.treeView.setExpanded(rootIndex, True)

    def load_tree(self, rootPath):
        self.cache = {}
        dir = QDir(rootPath)
        root_item = self.model.invisibleRootItem()
        item = QStandardItem(dir.dirName())
        item.setData(rootPath, Qt.ItemDataRole.UserRole)
        root_item.appendRow(item)
        self.cache[rootPath] = item
        self.add_items(item, dir)

    def add_items(self, parent_item, dir):
        for entry_info in dir.entryInfoList(QDir.Filter.AllEntries | QDir.Filter.Hidden | QDir.Filter.NoDotAndDotDot,
                                            QDir.SortFlag.Name):
            item = QStandardItem(entry_info.fileName())
            item.setData(entry_info.filePath(), Qt.ItemDataRole.UserRole)
            if entry_info.isDir():
                self.cache[entry_info.filePath()] = item
                self.add_items(item, QDir(entry_info.filePath()))
            parent_item.appendRow(item)

    def filter_tree(self):
        text = self.filterLineEdit.text()
        self.sortModel.setFilterFixedString(text)
