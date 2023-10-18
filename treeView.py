import os

from PyQt6.QtWidgets import QTreeView, QVBoxLayout, QWidget, QLineEdit, QMainWindow
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtCore import QSortFilterProxyModel, QDir

class FileSystemTreeViewer(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.setWindowTitle("Отображение дерева файловой системы")
        self.setMaximumSize(1200, 1000)
        self.setMinimumSize(800, 600)
        # Главный виджет
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)
        # Модель данных
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Файловая система"])
        # Модель сортировки
        self.sortModel = QSortFilterProxyModel()
        self.sortModel.setSourceModel(self.model)
        self.sortModel.setFilterKeyColumn(0)
        
        # Отображение дерева
        self.treeView = QTreeView(self)
        self.treeView.setModel(self.sortModel)
        self.treeView.setSortingEnabled(True)
        self.treeView.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers)
        # Виджет для фильтрации
        self.filterLineEdit = QLineEdit(self)
        self.filterLineEdit.textChanged.connect(self.filter_tree)
        
        self.layout.addWidget(self.filterLineEdit)
        self.layout.addWidget(self.treeView)
        
        self.populate_tree()

    def populate_tree(self):
        rootPath = os.path.expanduser("~")
        dir = QDir(rootPath)
        self.add_items(self.model.invisibleRootItem(), dir)

    def add_items(self, parent_item, dir):
        for entry_info in dir.entryInfoList(QDir.Filter.AllEntries | QDir.Filter.NoDotAndDotDot, QDir.SortFlag.Name):
            item = QStandardItem(entry_info.fileName())
            parent_item.appendRow(item)
            if entry_info.isDir():
                self.add_items(item, QDir(entry_info.filePath()))

    def filter_tree(self):
        text = self.filterLineEdit.text()
        self.sortModel.setFilterFixedString(text)






