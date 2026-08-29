#!/usr/bin/env python3
"""
EA Manager Module
Handles Expert Advisor operations
"""

import MetaTrader5 as mt5
from datetime import datetime


class EAManager:
    """Manages Expert Advisor operations"""
    
    def __init__(self):
        self.active_eas = {}
    
    def start_ea(self, symbol, timeframe):
        """
        Start EA on a symbol
        
        Args:
            symbol: Trading symbol
            timeframe: Chart timeframe
        """
        try:
            # This would typically involve sending commands to MT5
            # via API or direct terminal manipulation
            ea_key = f"{symbol}_{timeframe}"
            self.active_eas[ea_key] = {
                "symbol": symbol,
                "timeframe": timeframe,
                "status": "running",
                "start_time": datetime.now(),
                "trades": 0,
                "profit": 0.0
            }
            print(f"EA started on {symbol} {timeframe}")
            return True
        except Exception as e:
            print(f"Error starting EA: {str(e)}")
            return False
    
    def stop_ea(self, symbol):
        """
        Stop EA on a symbol
        
        Args:
            symbol: Trading symbol
        """
        try:
            # Find and stop EA
            keys_to_remove = [k for k in self.active_eas.keys() if symbol in k]
            for key in keys_to_remove:
                self.active_eas[key]["status"] = "stopped"
                del self.active_eas[key]
            
            print(f"EA stopped on {symbol}")
            return True
        except Exception as e:
            print(f"Error stopping EA: {str(e)}")
            return False
    
    def get_active_eas(self):
        """Get list of active EAs"""
        return self.active_eas
    
    def get_ea_statistics(self, symbol=None):
        """
        Get EA statistics
        
        Args:
            symbol: Optional symbol filter
            
        Returns:
            dict: Statistics
        """
        if not symbol:
            return self.active_eas
        
        stats = {}
        for key, ea in self.active_eas.items():
            if symbol in key:
                stats[key] = ea
        
        return stats
