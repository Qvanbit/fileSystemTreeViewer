import sys
from PyQt6.QtWidgets import QApplication

from treeView import FileSystemTreeViewer

def main():
    sys.setrecursionlimit(5000)
    app = QApplication(sys.argv)
    window = FileSystemTreeViewer()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()


