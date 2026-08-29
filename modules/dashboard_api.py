#!/usr/bin/env python3
"""
Dashboard API Module
Handles communication with FastAPI dashboard
"""

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime


class DashboardAPI:
    """Communicates with FastAPI dashboard"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def send_signal(self, signal_data: Dict):
        """
        Send trading signal to dashboard
        
        Args:
            signal_data: Signal data dictionary
            
        Returns:
            bool: Success status
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/signals",
                json=signal_data,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Error sending signal: {str(e)}")
            return False
    
    def get_statistics(self):
        """
        Get trading statistics from dashboard
        
        Returns:
            dict: Statistics data
        """
        try:
            response = self.session.get(
                f"{self.base_url}/api/statistics",
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            print(f"Error getting statistics: {str(e)}")
            return {}
    
    def get_positions(self):
        """
        Get open positions from dashboard
        
        Returns:
            list: Positions data
        """
        try:
            response = self.session.get(
                f"{self.base_url}/api/positions",
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error getting positions: {str(e)}")
            return []
    
    def update_ea_config(self, config: Dict):
        """
        Update EA configuration on dashboard
        
        Args:
            config: Configuration dictionary
            
        Returns:
            bool: Success status
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/config",
                json=config,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Error updating config: {str(e)}")
            return False
    
    def health_check(self):
        """
        Check if dashboard is accessible
        
        Returns:
            bool: Dashboard availability
        """
        try:
            response = self.session.get(
                f"{self.base_url}/health",
                timeout=5
            )
            return response.status_code == 200
        except Exception:
            return False
