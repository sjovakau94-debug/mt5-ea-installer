#!/usr/bin/env python3
"""
MT5 EA Installer - Main Application
Desktop GUI for installing and managing Exness trading EAs
"""

import sys
import os
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

import PyQt6
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QComboBox, QTextEdit, QFileDialog,
    QProgressBar, QTabWidget, QTableWidget, QTableWidgetItem, QDialog,
    QMessageBox, QCheckBox, QSpinBox, QDoubleSpinBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QIcon, QFont, QColor

# Import custom modules
from modules.mt5_manager import MT5Manager
from modules.ea_manager import EAManager
from modules.config_manager import ConfigManager
from modules.dashboard_api import DashboardAPI


class InstallerWorker(QThread):
    """Worker thread for installation tasks"""
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, task_type, params):
        super().__init__()
        self.task_type = task_type
        self.params = params
        self.mt5_manager = MT5Manager()
        self.ea_manager = EAManager()
    
    def run(self):
        try:
            if self.task_type == "install_ea":
                self._install_ea()
            elif self.task_type == "compile_ea":
                self._compile_ea()
            elif self.task_type == "connect_mt5":
                self._connect_mt5()
            elif self.task_type == "start_ea":
                self._start_ea()
            elif self.task_type == "stop_ea":
                self._stop_ea()
            
            self.finished.emit(True, "Task completed successfully")
        except Exception as e:
            self.finished.emit(False, f"Error: {str(e)}")
    
    def _install_ea(self):
        """Install EA file"""
        self.status.emit("Installing EA...")
        self.progress.emit(25)
        
        source = self.params.get("source")
        destination = self.params.get("destination")
        
        # Copy EA file
        shutil.copy(source, destination)
        self.progress.emit(50)
        
        self.status.emit("EA installed successfully")
        self.progress.emit(100)
    
    def _compile_ea(self):
        """Compile MQ5 file using MT5 MetaEditor"""
        self.status.emit("Compiling EA...")
        self.progress.emit(25)
        
        ea_file = self.params.get("ea_file")
        result = self.mt5_manager.compile_ea(ea_file)
        
        self.progress.emit(100)
        
        if result:
            self.status.emit("Compilation successful")
        else:
            raise Exception("Compilation failed")
    
    def _connect_mt5(self):
        """Connect to MT5 terminal"""
        self.status.emit("Connecting to MT5...")
        self.progress.emit(25)
        
        account = self.params.get("account")
        password = self.params.get("password")
        server = self.params.get("server")
        
        connected = self.mt5_manager.connect(account, password, server)
        self.progress.emit(100)
        
        if connected:
            self.status.emit("Connected to MT5")
        else:
            raise Exception("Failed to connect to MT5")
    
    def _start_ea(self):
        """Start EA on symbol"""
        self.status.emit("Starting EA...")
        self.progress.emit(50)
        
        symbol = self.params.get("symbol")
        timeframe = self.params.get("timeframe")
        
        self.ea_manager.start_ea(symbol, timeframe)
        self.progress.emit(100)
        self.status.emit("EA started")
    
    def _stop_ea(self):
        """Stop EA on symbol"""
        self.status.emit("Stopping EA...")
        self.progress.emit(50)
        
        symbol = self.params.get("symbol")
        self.ea_manager.stop_ea(symbol)
        self.progress.emit(100)
        self.status.emit("EA stopped")


class InstallerApp(QMainWindow):
    """Main installer application window"""
    
    def __init__(self):
        super().__init__()
        self.config = ConfigManager()
        self.mt5_manager = MT5Manager()
        self.ea_manager = EAManager()
        self.dashboard_api = DashboardAPI()
        self.worker = None
        
        self.init_ui()
        self.load_config()
    
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle("MT5 EA Installer - Exness Trading Bot Manager")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout()
        
        # Create tabs
        tabs = QTabWidget()
        
        # Tab 1: Installation
        tabs.addTab(self.create_installation_tab(), "Installation")
        
        # Tab 2: EA Management
        tabs.addTab(self.create_management_tab(), "EA Management")
        
        # Tab 3: MT5 Connection
        tabs.addTab(self.create_connection_tab(), "MT5 Connection")
        
        # Tab 4: Settings
        tabs.addTab(self.create_settings_tab(), "Settings")
        
        # Tab 5: Dashboard
        tabs.addTab(self.create_dashboard_tab(), "Dashboard")
        
        main_layout.addWidget(tabs)
        
        # Status bar
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        main_layout.addWidget(self.status_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        central_widget.setLayout(main_layout)
    
    def create_installation_tab(self):
        """Create installation tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # EA file selection
        layout.addWidget(QLabel("EA File Path:"))
        ea_layout = QHBoxLayout()
        self.ea_path_input = QLineEdit()
        ea_browse_btn = QPushButton("Browse")
        ea_browse_btn.clicked.connect(self.browse_ea_file)
        ea_layout.addWidget(self.ea_path_input)
        ea_layout.addWidget(ea_browse_btn)
        layout.addLayout(ea_layout)
        
        # Destination path
        layout.addWidget(QLabel("Destination (MT5 Experts folder):"))
        dest_layout = QHBoxLayout()
        self.dest_path_input = QLineEdit()
        self.dest_path_input.setText(self.get_mt5_experts_path())
        dest_browse_btn = QPushButton("Browse")
        dest_browse_btn.clicked.connect(self.browse_destination)
        dest_layout.addWidget(self.dest_path_input)
        dest_layout.addWidget(dest_browse_btn)
        layout.addLayout(dest_layout)
        
        # Compile option
        self.compile_checkbox = QCheckBox("Compile EA after installation")
        self.compile_checkbox.setChecked(True)
        layout.addWidget(self.compile_checkbox)
        
        # Install button
        install_btn = QPushButton("Install EA")
        install_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        install_btn.clicked.connect(self.install_ea)
        layout.addWidget(install_btn)
        
        # Log output
        layout.addWidget(QLabel("Installation Log:"))
        self.install_log = QTextEdit()
        self.install_log.setReadOnly(True)
        layout.addWidget(self.install_log)
        
        widget.setLayout(layout)
        return widget
    
    def create_management_tab(self):
        """Create EA management tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Symbol selection
        symbol_layout = QHBoxLayout()
        symbol_layout.addWidget(QLabel("Symbol:"))
        self.symbol_combo = QComboBox()
        self.symbol_combo.addItems(["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD"])
        symbol_layout.addWidget(self.symbol_combo)
        layout.addLayout(symbol_layout)
        
        # Timeframe selection
        tf_layout = QHBoxLayout()
        tf_layout.addWidget(QLabel("Timeframe:"))
        self.timeframe_combo = QComboBox()
        self.timeframe_combo.addItems(["M5", "M15", "M30", "H1", "H4", "D1"])
        self.timeframe_combo.setCurrentText("M15")
        tf_layout.addWidget(self.timeframe_combo)
        layout.addLayout(tf_layout)
        
        # Control buttons
        button_layout = QHBoxLayout()
        start_btn = QPushButton("Start EA")
        start_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        start_btn.clicked.connect(self.start_ea)
        
        stop_btn = QPushButton("Stop EA")
        stop_btn.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        stop_btn.clicked.connect(self.stop_ea)
        
        button_layout.addWidget(start_btn)
        button_layout.addWidget(stop_btn)
        layout.addLayout(button_layout)
        
        # EA Status Table
        layout.addWidget(QLabel("Active EAs:"))
        self.ea_table = QTableWidget()
        self.ea_table.setColumnCount(5)
        self.ea_table.setHorizontalHeaderLabels(["Symbol", "Timeframe", "Status", "Profit", "Trades"])
        layout.addWidget(self.ea_table)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh Status")
        refresh_btn.clicked.connect(self.refresh_ea_status)
        layout.addWidget(refresh_btn)
        
        widget.setLayout(layout)
        return widget
    
    def create_connection_tab(self):
        """Create MT5 connection tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Account credentials
        layout.addWidget(QLabel("MT5 Account Settings:"))
        
        account_layout = QHBoxLayout()
        account_layout.addWidget(QLabel("Account:"))
        self.account_input = QLineEdit()
        self.account_input.setPlaceholderText("Enter your MT5 account number")
        account_layout.addWidget(self.account_input)
        layout.addLayout(account_layout)
        
        password_layout = QHBoxLayout()
        password_layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter your MT5 password")
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)
        
        server_layout = QHBoxLayout()
        server_layout.addWidget(QLabel("Server:"))
        self.server_combo = QComboBox()
        self.server_combo.addItems([
            "Exness-MT5",
            "Exness-MT5 Trial",
            "Exness-MT5-Cent",
            "Custom"
        ])
        server_layout.addWidget(self.server_combo)
        layout.addLayout(server_layout)
        
        # Connection buttons
        button_layout = QHBoxLayout()
        connect_btn = QPushButton("Connect to MT5")
        connect_btn.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold;")
        connect_btn.clicked.connect(self.connect_mt5)
        
        disconnect_btn = QPushButton("Disconnect")
        disconnect_btn.setStyleSheet("background-color: #9C27B0; color: white; font-weight: bold;")
        disconnect_btn.clicked.connect(self.disconnect_mt5)
        
        button_layout.addWidget(connect_btn)
        button_layout.addWidget(disconnect_btn)
        layout.addLayout(button_layout)
        
        # Connection status
        layout.addWidget(QLabel("Connection Status:"))
        self.connection_status = QTextEdit()
        self.connection_status.setReadOnly(True)
        self.connection_status.setMaximumHeight(100)
        layout.addWidget(self.connection_status)
        
        # Account info
        layout.addWidget(QLabel("Account Information:"))
        self.account_info = QTextEdit()
        self.account_info.setReadOnly(True)
        layout.addWidget(self.account_info)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_settings_tab(self):
        """Create settings tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # EA Settings
        layout.addWidget(QLabel("EA Configuration:"))
        
        risk_layout = QHBoxLayout()
        risk_layout.addWidget(QLabel("Risk per Trade (%):"))
        self.risk_spinbox = QDoubleSpinBox()
        self.risk_spinbox.setValue(2.0)
        self.risk_spinbox.setRange(0.1, 10.0)
        self.risk_spinbox.setSingleStep(0.1)
        risk_layout.addWidget(self.risk_spinbox)
        layout.addLayout(risk_layout)
        
        tp_layout = QHBoxLayout()
        tp_layout.addWidget(QLabel("Take Profit (pips):"))
        self.tp_spinbox = QSpinBox()
        self.tp_spinbox.setValue(100)
        self.tp_spinbox.setRange(10, 1000)
        tp_layout.addWidget(self.tp_spinbox)
        layout.addLayout(tp_layout)
        
        sl_layout = QHBoxLayout()
        sl_layout.addWidget(QLabel("Stop Loss (pips):"))
        self.sl_spinbox = QSpinBox()
        self.sl_spinbox.setValue(50)
        self.sl_spinbox.setRange(10, 1000)
        sl_layout.addWidget(self.sl_spinbox)
        layout.addLayout(sl_layout)
        
        max_pos_layout = QHBoxLayout()
        max_pos_layout.addWidget(QLabel("Max Open Positions:"))
        self.max_pos_spinbox = QSpinBox()
        self.max_pos_spinbox.setValue(3)
        self.max_pos_spinbox.setRange(1, 10)
        max_pos_layout.addWidget(self.max_pos_spinbox)
        layout.addLayout(max_pos_layout)
        
        # Dashboard settings
        layout.addWidget(QLabel("Dashboard Settings:"))
        
        dashboard_url_layout = QHBoxLayout()
        dashboard_url_layout.addWidget(QLabel("Dashboard URL:"))
        self.dashboard_url_input = QLineEdit()
        self.dashboard_url_input.setText("http://localhost:8000")
        dashboard_url_layout.addWidget(self.dashboard_url_input)
        layout.addLayout(dashboard_url_layout)
        
        # Save settings button
        save_btn = QPushButton("Save Settings")
        save_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_dashboard_tab(self):
        """Create dashboard tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Dashboard Statistics:"))
        
        # Statistics table
        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(4)
        self.stats_table.setHorizontalHeaderLabels(["Metric", "Value", "Status", "Updated"])
        layout.addWidget(self.stats_table)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh Dashboard Data")
        refresh_btn.clicked.connect(self.refresh_dashboard)
        layout.addWidget(refresh_btn)
        
        # Open dashboard in browser
        open_browser_btn = QPushButton("Open Dashboard in Browser")
        open_browser_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        open_browser_btn.clicked.connect(self.open_dashboard_browser)
        layout.addWidget(open_browser_btn)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    # Event handlers
    def browse_ea_file(self):
        """Browse for EA file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select EA File", "", "MQL5 Files (*.mq5);;All Files (*)"
        )
        if file_path:
            self.ea_path_input.setText(file_path)
    
    def browse_destination(self):
        """Browse for destination folder"""
        folder = QFileDialog.getExistingDirectory(
            self, "Select MT5 Experts Folder"
        )
        if folder:
            self.dest_path_input.setText(folder)
    
    def install_ea(self):
        """Install EA"""
        source = self.ea_path_input.text()
        destination = self.dest_path_input.text()
        
        if not source or not destination:
            QMessageBox.warning(self, "Error", "Please select both source and destination paths")
            return
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        params = {
            "source": source,
            "destination": destination
        }
        
        self.worker = InstallerWorker("install_ea", params)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.status.connect(self.update_status)
        self.worker.finished.connect(self.on_install_finished)
        self.worker.start()
    
    def start_ea(self):
        """Start EA"""
        symbol = self.symbol_combo.currentText()
        timeframe = self.timeframe_combo.currentText()
        
        params = {
            "symbol": symbol,
            "timeframe": timeframe
        }
        
        self.worker = InstallerWorker("start_ea", params)
        self.worker.status.connect(self.update_status)
        self.worker.finished.connect(self.on_task_finished)
        self.worker.start()
    
    def stop_ea(self):
        """Stop EA"""
        symbol = self.symbol_combo.currentText()
        
        params = {"symbol": symbol}
        
        self.worker = InstallerWorker("stop_ea", params)
        self.worker.status.connect(self.update_status)
        self.worker.finished.connect(self.on_task_finished)
        self.worker.start()
    
    def connect_mt5(self):
        """Connect to MT5"""
        account = self.account_input.text()
        password = self.password_input.text()
        server = self.server_combo.currentText()
        
        params = {
            "account": account,
            "password": password,
            "server": server
        }
        
        self.worker = InstallerWorker("connect_mt5", params)
        self.worker.status.connect(self.update_status)
        self.worker.finished.connect(self.on_connect_finished)
        self.worker.start()
    
    def disconnect_mt5(self):
        """Disconnect from MT5"""
        self.mt5_manager.disconnect()
        self.connection_status.setText("Disconnected from MT5")
        self.update_status("Disconnected from MT5")
    
    def refresh_ea_status(self):
        """Refresh EA status"""
        # TODO: Implement status refresh
        pass
    
    def refresh_dashboard(self):
        """Refresh dashboard data"""
        # TODO: Implement dashboard refresh
        pass
    
    def open_dashboard_browser(self):
        """Open dashboard in web browser"""
        url = self.dashboard_url_input.text()
        import webbrowser
        webbrowser.open(url)
    
    def save_settings(self):
        """Save settings"""
        settings = {
            "risk_percentage": self.risk_spinbox.value(),
            "take_profit": self.tp_spinbox.value(),
            "stop_loss": self.sl_spinbox.value(),
            "max_positions": self.max_pos_spinbox.value(),
            "dashboard_url": self.dashboard_url_input.text()
        }
        
        self.config.save(settings)
        QMessageBox.information(self, "Success", "Settings saved successfully")
        self.update_status("Settings saved")
    
    def load_config(self):
        """Load configuration"""
        config = self.config.load()
        if config:
            self.risk_spinbox.setValue(config.get("risk_percentage", 2.0))
            self.tp_spinbox.setValue(config.get("take_profit", 100))
            self.sl_spinbox.setValue(config.get("stop_loss", 50))
            self.max_pos_spinbox.setValue(config.get("max_positions", 3))
            self.dashboard_url_input.setText(config.get("dashboard_url", "http://localhost:8000"))
    
    # Utility methods
    def update_status(self, message):
        """Update status label"""
        self.status_label.setText(message)
    
    def on_install_finished(self, success, message):
        """Handle installation completion"""
        self.progress_bar.setVisible(False)
        if success:
            QMessageBox.information(self, "Success", message)
            self.install_log.append(f"[{datetime.now()}] {message}")
        else:
            QMessageBox.critical(self, "Error", message)
            self.install_log.append(f"[{datetime.now()}] {message}")
    
    def on_task_finished(self, success, message):
        """Handle task completion"""
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.critical(self, "Error", message)
        self.update_status(message)
    
    def on_connect_finished(self, success, message):
        """Handle MT5 connection completion"""
        if success:
            self.connection_status.setText("✓ Connected to MT5")
            self.connection_status.setStyleSheet("color: green;")
            # Get account info
            # TODO: Implement account info retrieval
        else:
            self.connection_status.setText(f"✗ {message}")
            self.connection_status.setStyleSheet("color: red;")
        self.update_status(message)
    
    @staticmethod
    def get_mt5_experts_path():
        """Get default MT5 experts folder path"""
        if sys.platform == "win32":
            return os.path.expanduser(r"AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts")
        elif sys.platform == "darwin":
            return os.path.expanduser("~/Library/Application Support/MetaTrader 5/MQL5/Experts")
        else:
            return os.path.expanduser("~/.config/MetaTrader 5/MQL5/Experts")


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    installer = InstallerApp()
    installer.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
