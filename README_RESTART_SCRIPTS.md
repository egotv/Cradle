# Auto-Restart Scripts for Cradle RDR2

These scripts will automatically restart your `runner.py` program when it stops, helping to keep your automation running continuously.

## Available Scripts

### 1. PowerShell Script (`restart_runner.ps1`)
**Recommended for advanced users**

Features:
- Detailed logging to both console and file
- Customizable parameters
- Error handling
- Restart counting

Usage:
```powershell
# Basic usage (uses default config)
.\restart_runner.ps1

# Custom config file
.\restart_runner.ps1 -EnvConfig "./conf/your_config.json"

# Custom restart delay (10 seconds)
.\restart_runner.ps1 -RestartDelay 10

# Both custom config and delay
.\restart_runner.ps1 -EnvConfig "./conf/your_config.json" -RestartDelay 10
```

### 2. Python Script (`restart_runner.py`)
**Recommended for Python users**

Features:
- Cross-platform compatibility
- Command-line arguments
- Optional restart limits
- Logging to file

Usage:
```bash
# Basic usage
python restart_runner.py

# Custom config file
python restart_runner.py --envConfig "./conf/your_config.json"

# Custom restart delay (10 seconds)
python restart_runner.py --restart-delay 10

# Limit to 50 restarts
python restart_runner.py --max-restarts 50

# All options combined
python restart_runner.py --envConfig "./conf/your_config.json" --restart-delay 10 --max-restarts 100
```

### 3. Batch File (`restart_runner.bat`)
**Recommended for simple usage**

Features:
- Simple and lightweight
- No additional dependencies
- Easy to modify

Usage:
```cmd
# Just double-click the file or run from command prompt
restart_runner.bat
```

To customize the batch file, edit these variables at the top:
- `ENV_CONFIG`: Path to your environment config file
- `RESTART_DELAY`: Seconds to wait between restarts

## How to Stop the Scripts

- **All scripts**: Press `Ctrl+C` to stop the restart loop
- The current running instance of `runner.py` will complete, then the script will exit

## Log Files

- PowerShell and Python scripts create a `restart_log.txt` file with timestamps
- This helps you track when restarts occurred and any error messages

## Troubleshooting

1. **"Python not found"**: Make sure Python is in your PATH or activate your virtual environment first
2. **"runner.py not found"**: Make sure you're running the script from the Cradle directory
3. **Config file not found**: Check that your config file path is correct

## Example Output

```
2025-06-19 15:35:00 - Starting Cradle RDR2 Auto-Restart Script
2025-06-19 15:35:00 - Command: python runner.py --envConfig "./conf/env_config_rdr2_main_storyline.json"
2025-06-19 15:35:00 - Restart delay: 5 seconds
2025-06-19 15:35:00 - Press Ctrl+C to stop the restart loop
2025-06-19 15:35:00 - === Restart #1 ===
... your program output ...
2025-06-19 15:40:25 - Process exited with code: 0
2025-06-19 15:40:25 - Process completed successfully
2025-06-19 15:40:25 - Waiting 5 seconds before restart...
2025-06-19 15:40:30 - === Restart #2 ===
```

## Tips

- Start with the batch file for simplicity
- Use the PowerShell script for better logging and control
- Use the Python script if you need cross-platform compatibility
- Check the log files to monitor restart patterns and identify issues 