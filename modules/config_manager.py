#!/usr/bin/env python3
"""
Configuration Manager Module
Handles application configuration
"""

import json
import os
from pathlib import Path
from datetime import datetime


class ConfigManager:
    """Manages application configuration"""
    
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config_dir = Path.home() / ".mt5_ea_installer"
        self.config_path = self.config_dir / config_file
        
        # Create config directory if it doesn't exist
        self.config_dir.mkdir(exist_ok=True)
    
    def load(self):
        """Load configuration from file"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            return self.get_default_config()
        except Exception as e:
            print(f"Error loading config: {str(e)}")
            return self.get_default_config()
    
    def save(self, config):
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"Configuration saved to {self.config_path}")
            return True
        except Exception as e:
            print(f"Error saving config: {str(e)}")
            return False
    
    @staticmethod
    def get_default_config():
        """Get default configuration"""
        return {
            "risk_percentage": 2.0,
            "take_profit": 100,
            "stop_loss": 50,
            "max_positions": 3,
            "dashboard_url": "http://localhost:8000",
            "trading_symbols": ["EURUSD", "GBPUSD", "USDJPY"],
            "trading_enabled": True,
            "last_updated": datetime.now().isoformat()
        }
