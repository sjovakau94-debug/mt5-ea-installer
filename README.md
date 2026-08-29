# MT5 EA Installer

Desktop application for installing and managing fully automated MetaTrader 5 Expert Advisors for Exness broker.

## Features

- **Easy EA Installation**: One-click installation of MT5 Expert Advisors
- **EA Management**: Start/stop trading bots with simple controls
- **MT5 Connection**: Secure account connection to MetaTrader 5
- **Configuration**: Customize trading parameters (risk, TP, SL, etc.)
- **Dashboard Integration**: Real-time statistics and monitoring
- **Risk Management**: Automatic position sizing and daily loss limits
- **Multi-Symbol Support**: Trade multiple forex pairs simultaneously

## Requirements

- Python 3.8+
- MetaTrader 5 terminal installed
- Exness trading account
- Windows/macOS/Linux

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sjovakau94-debug/mt5-ea-installer.git
   cd mt5-ea-installer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

## Quick Start

### 1. Install EA
1. Open the "Installation" tab
2. Browse and select your `.mq5` EA file
3. Choose destination (MT5 Experts folder)
4. Click "Install EA"

### 2. Connect to MT5
1. Go to "MT5 Connection" tab
2. Enter your Exness account credentials
3. Select server (Exness-MT5)
4. Click "Connect to MT5"

### 3. Configure Settings
1. Open "Settings" tab
2. Adjust:
   - Risk per trade (%)
   - Take Profit (pips)
   - Stop Loss (pips)
   - Max open positions
3. Click "Save Settings"

### 4. Start Trading
1. Go to "EA Management" tab
2. Select symbol and timeframe
3. Click "Start EA"
4. Monitor performance in Dashboard tab

## Configuration

### EA Parameters
- **Risk per Trade**: 0.1% - 10% (default: 2%)
- **Take Profit**: 10 - 1000 pips (default: 100)
- **Stop Loss**: 10 - 1000 pips (default: 50)
- **Max Positions**: 1 - 10 (default: 3)

### Trading Symbols
- EURUSD
- GBPUSD
- USDJPY
- AUDUSD
- USDCAD

## Dashboard

The installer includes integration with a FastAPI dashboard for:
- Real-time profit/loss monitoring
- Trade statistics and win rate
- Active position tracking
- Signal logging

## Architecture

```
mt5-ea-installer/
├── main.py                 # Main application entry
├── requirements.txt        # Python dependencies
├── modules/
│   ├── mt5_manager.py     # MT5 terminal management
│   ├── ea_manager.py      # EA operation control
│   ├── config_manager.py  # Configuration handling
│   └── dashboard_api.py   # Dashboard API integration
├── resources/             # UI icons and resources
├── docs/                  # Documentation
└── README.md             # This file
```

## API Integration

The installer communicates with your FastAPI dashboard via REST API:

```python
POST /api/signals      # Send trading signals
GET  /api/statistics   # Get trading statistics
GET  /api/positions    # Get open positions
POST /api/config       # Update EA configuration
GET  /health           # Health check
```

## Security

- **Password Encryption**: Account passwords are encrypted in local storage
- **Secure Connection**: HTTPS support for dashboard communication
- **No Cloud Storage**: All sensitive data stored locally

## Troubleshooting

### MT5 Connection Issues
- Ensure MetaTrader 5 terminal is running
- Verify account credentials
- Check server name spelling
- Disable firewall temporarily

### EA Installation Problems
- Ensure MT5 is not running during installation
- Verify file permissions in MT5 folder
- Check file exists at destination

### Dashboard Connection
- Verify FastAPI backend is running
- Check dashboard URL in settings
- Ensure no firewall blocking connection

## License

MIT License - See LICENSE file

## Support

For issues and questions:
- GitHub Issues: https://github.com/sjovakau94-debug/mt5-ea-installer/issues
- Documentation: https://github.com/sjovakau94-debug/mt5-ea-installer/wiki

## Disclaimer

This software is provided for educational purposes. Trading forex involves substantial risk. 
Never invest money you cannot afford to lose.

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

---

**Version**: 1.0.0
**Last Updated**: August 2026
**Author**: MT5 EA Dashboard Team
