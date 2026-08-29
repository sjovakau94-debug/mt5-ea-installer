#!/usr/bin/env python3
"""
MT5 Manager Module
Handles MT5 terminal connections and operations
"""

import MetaTrader5 as mt5
import os
import subprocess
import sys
from pathlib import Path


class MT5Manager:
    """Manages MT5 terminal connections and operations"""
    
    def __init__(self):
        self.is_connected = False
        self.account_info = None
    
    def connect(self, account, password, server):
        """
        Connect to MT5 terminal
        
        Args:
            account: Account number
            password: Account password
            server: Server name
            
        Returns:
            bool: Connection status
        """
        try:
            # Initialize MT5
            if not mt5.initialize():
                print(f"Initialize failed, error code = {mt5.last_error()}")
                return False
            
            # Login to account
            if mt5.login(int(account), password, server):
                self.is_connected = True
                self.account_info = mt5.account_info()
                print(f"Connected to account {account} on {server}")
                return True
            else:
                print(f"Login failed, error code = {mt5.last_error()}")
                return False
                
        except Exception as e:
            print(f"Connection error: {str(e)}")
            return False
    
    def disconnect(self):
        """Disconnect from MT5 terminal"""
        try:
            mt5.shutdown()
            self.is_connected = False
            print("Disconnected from MT5")
        except Exception as e:
            print(f"Disconnect error: {str(e)}")
    
    def compile_ea(self, ea_file):
        """
        Compile MQ5 file using MetaEditor
        
        Args:
            ea_file: Path to MQ5 file
            
        Returns:
            bool: Compilation status
        """
        try:
            metaeditor_path = self.get_metaeditor_path()
            
            if not metaeditor_path:
                print("MetaEditor not found")
                return False
            
            # Compile using MetaEditor
            result = subprocess.run(
                [metaeditor_path, "/compile:" + ea_file],
                capture_output=True,
                timeout=30
            )
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"Compilation error: {str(e)}")
            return False
    
    def get_account_info(self):
        """Get account information"""
        if self.is_connected:
            return self.account_info
        return None
    
    def get_symbols(self):
        """Get list of available symbols"""
        if not self.is_connected:
            return []
        
        symbols = mt5.symbols_get()
        return [s.name for s in symbols]
    
    def get_positions(self):
        """Get open positions"""
        if not self.is_connected:
            return []
        
        positions = mt5.positions_get()
        return positions if positions else []
    
    @staticmethod
    def get_metaeditor_path():
        """Get MetaEditor executable path"""
        if sys.platform == "win32":
            # Common MT5 installation paths on Windows
            common_paths = [
                os.path.expanduser(r"AppData\Local\Apps\MetaTrader 5\metaeditor64.exe"),
                os.path.expanduser(r"Program Files\MetaTrader 5\metaeditor64.exe"),
                os.path.expanduser(r"Program Files (x86)\MetaTrader 5\metaeditor.exe"),
            ]
            
            for path in common_paths:
                if os.path.exists(path):
                    return path
        
        elif sys.platform == "darwin":
            # macOS path
            path = os.path.expanduser("/Applications/MetaTrader 5/metaeditor")
            if os.path.exists(path):
                return path
        
        return None
