import os

from PyQt6.QtWidgets import QTreeView, QVBoxLayout, QWidget, QLineEdit, QMainWindow, QApplication
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtCore import QDir, Qt, QSortFilterProxyModel


class FileSystemTreeViewer(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        HOME_DIR = os.path.expanduser("~")  # Домашняя директория

        # Настройки окна
        self.setWindowTitle("Отображение дерева файловой системы")
        self.setMaximumSize(1200, 1000)
        self.setMinimumSize(800, 600)
        self.app = QApplication.instance()

        # Настройка виджетов
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)

        # Модель для хранения элементов дерева
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Файловая система"])

        # Модель для фильтрации
        self.sortModel = QSortFilterProxyModel()
        self.sortModel.setSourceModel(self.model)

        # Отображение данных из модели
        self.treeView = QTreeView(self)
        self.treeView.setModel(self.sortModel)
        self.treeView.setSortingEnabled(True)  # Сортировка по первому символу
        self.treeView.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers)  # Запрет на редактирование пользователю

        # Поле для фильтрации элементов дерева
        self.filterLineEdit = QLineEdit(self)
        self.filterLineEdit.textChanged.connect(self.filter_tree)

        # Добавление виджетов
        self.layout.addWidget(self.filterLineEdit)
        self.layout.addWidget(self.treeView)

        self.load_tree(HOME_DIR)

    def load_tree(self, rootPath):
        MAX_HIDDEN_LENGTH = 7  # Глубина сканирования скрытых элементов
        dir = QDir(rootPath)  # Корневая директория
        self.add_items(self.model.invisibleRootItem(), dir, MAX_HIDDEN_LENGTH)

    def add_items(self, parent_item, dir, max_depth):
        for entry_info in dir.entryInfoList(QDir.Filter.AllEntries | QDir.Filter.Hidden | QDir.Filter.NoDotAndDotDot,
                                            QDir.SortFlag.Name):
            if max_depth == 0:
                break
            item = QStandardItem(entry_info.fileName())
            if entry_info.isDir():
                self.add_items(item, QDir(entry_info.filePath()), max_depth - 1)
            parent_item.appendRow(item)

    def filter_tree(self):
        text = self.filterLineEdit.text()
        self.sortModel.setFilterFixedString(text)
