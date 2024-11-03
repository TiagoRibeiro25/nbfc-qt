#!/usr/bin/env python

import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

if __name__ == "__main__":
    app: QApplication = QApplication(sys.argv)
    main_window: MainWindow = MainWindow()
    main_window.show()
    sys.exit(app.exec())
