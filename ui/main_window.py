import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSpacerItem, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QComboBox, QMessageBox, QLabel
from constants.main import GITHUB_LINK
from core.config_loader import load_configs
from core.system_checker import get_nbfc_status, is_nbfc_installed, get_pc_model, get_current_config, apply_nbfc_config, restart_nbfc, start_nbfc, stop_nbfc

class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Notebook FanControl GUI")
        self.setFixedSize(400, 220)

        main_layout = QVBoxLayout()

        if not is_nbfc_installed():
            QMessageBox.critical(self, "Error", "The nbfc package is not installed.")
            sys.exit(1)

        self.pc_model_label = QLabel("PC Model: " + get_pc_model())
        main_layout.addWidget(self.pc_model_label)

        main_layout.addItem(QSpacerItem(20, 20))

        current_config_label = QLabel("Current config:")
        main_layout.addWidget(current_config_label)

        # Horizontal layout for the combo box and refresh button
        config_layout = QHBoxLayout()

        self.config_combo = QComboBox()
        config_layout.addWidget(self.config_combo)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_state)
        config_layout.addWidget(self.refresh_button)

        main_layout.addLayout(config_layout)

        self.apply_button = QPushButton("Apply config")
        self.apply_button.clicked.connect(self.apply_config)
        main_layout.addWidget(self.apply_button)

        main_layout.addItem(QSpacerItem(20, 20))

        # Horizontal layout for the start, restart and stop buttons
        button_layout = QHBoxLayout()

        self.start_button = QPushButton("Start")
        button_layout.addWidget(self.start_button)
        self.start_button.clicked.connect(self.start_nbfc)

        self.restart_button = QPushButton("Restart")
        button_layout.addWidget(self.restart_button)
        self.restart_button.clicked.connect(self.restart_nbfc)

        self.stop_button = QPushButton("Stop")
        button_layout.addWidget(self.stop_button)
        self.stop_button.clicked.connect(self.stop_nbfc)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.populate_configs()
        self.update_button_states(None)

        main_layout.addItem(QSpacerItem(20, 5))

        footer_layout = QHBoxLayout()
        footer_label = QLabel(f'Made by <a href="{GITHUB_LINK}">Tiago Ribeiro</a>')
        footer_label.setOpenExternalLinks(True)
        footer_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        footer_layout.addWidget(footer_label)
        main_layout.addLayout(footer_layout)

    def refresh_state(self) -> None:
        self.update_button_states(None)
        self.populate_configs()

    def populate_configs(self) -> None:
        try:
            config_names: list[str] = load_configs()
            if not config_names:
                raise Exception("No configs found")

            self.config_combo.clear()
            self.config_combo.addItems(config_names)

            current_config: str | None = get_current_config()
            if current_config in config_names:
                self.config_combo.setCurrentText(current_config)

        except Exception as e:
            error_msg: str = "Failed to load configs."

            if str(e) == "No configs found":
                error_msg = "No configs found"

            QMessageBox.critical(self, "Error", f"{error_msg}:\n{e}")
            self.close()

    def apply_config(self) -> None:
        selected_config: str = self.config_combo.currentText()
        if not selected_config:
            QMessageBox.warning(self, "Warning", "No config selected.")
            return

        try:
            apply_nbfc_config(selected_config)
            QMessageBox.information(self, "Success", f"Config '{selected_config}' applied successfully.")
        except RuntimeError as e:
            QMessageBox.critical(self, "Error", str(e))

    def update_button_states(self, current_state: str | None):
        if current_state is None:
            current_state = get_nbfc_status()

        if current_state == "running":
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
        else:
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)

    def trigger_nbfc_service(self, action: str) -> None:
        try:
            if action == "start":
                start_nbfc()
                self.update_button_states("running")
            elif action == "stop":
                stop_nbfc()
                self.update_button_states("stopped")
            else: # restart
                restart_nbfc()
                self.update_button_states("running")

            QMessageBox.information(self, "Success", f"nbfc {action}ed successfully.")
        except RuntimeError as e:
            QMessageBox.critical(self, "Error", str(e))

    def start_nbfc(self) -> None:
        self.trigger_nbfc_service("start")
    
    def stop_nbfc(self) -> None:
        self.trigger_nbfc_service("stop")

    def restart_nbfc(self) -> None:
        self.trigger_nbfc_service("restart")
