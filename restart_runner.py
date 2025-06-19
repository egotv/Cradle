#!/usr/bin/env python3
"""
Restart Runner Script for Cradle RDR2
This script will continuously restart your runner.py when it stops
"""

import subprocess
import time
import argparse
import sys
from datetime import datetime


def write_log(message, log_file="restart_log.txt"):
    """Write timestamped log message to console and file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {message}"
    print(log_entry)
    
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    except Exception as e:
        print(f"Warning: Could not write to log file: {e}")


def main():
    parser = argparse.ArgumentParser(description="Auto-restart script for Cradle RDR2")
    parser.add_argument(
        "--envConfig", 
        default="./conf/env_config_rdr2_main_storyline.json",
        help="Environment config file path"
    )
    parser.add_argument(
        "--restart-delay", 
        type=int, 
        default=5,
        help="Delay in seconds between restarts"
    )
    parser.add_argument(
        "--max-restarts",
        type=int,
        default=0,
        help="Maximum number of restarts (0 for unlimited)"
    )
    
    args = parser.parse_args()
    
    command = ["python", "runner.py", "--envConfig", args.envConfig]
    
    write_log("Starting Cradle RDR2 Auto-Restart Script")
    write_log(f"Command: {' '.join(command)}")
    write_log(f"Restart delay: {args.restart_delay} seconds")
    write_log(f"Max restarts: {'unlimited' if args.max_restarts == 0 else args.max_restarts}")
    write_log("Press Ctrl+C to stop the restart loop")
    
    restart_count = 0
    
    try:
        while True:
            restart_count += 1
            
            # Check max restarts limit
            if args.max_restarts > 0 and restart_count > args.max_restarts:
                write_log(f"Reached maximum restart limit ({args.max_restarts}). Exiting.")
                break
                
            write_log(f"=== Restart #{restart_count} ===")
            
            try:
                # Start the process
                process = subprocess.run(
                    command,
                    cwd=".",
                    capture_output=False,  # Let output go directly to console
                    text=True
                )
                
                exit_code = process.returncode
                write_log(f"Process exited with code: {exit_code}")
                
                if exit_code == 0:
                    write_log("Process completed successfully")
                else:
                    write_log(f"Process exited with error code: {exit_code}")
                    
            except FileNotFoundError:
                write_log("Error: Python or runner.py not found. Check your paths.")
                break
            except Exception as e:
                write_log(f"Error occurred: {str(e)}")
            
            if args.max_restarts > 0 and restart_count >= args.max_restarts:
                write_log("Reached maximum restart limit. Exiting.")
                break
                
            write_log(f"Waiting {args.restart_delay} seconds before restart...")
            time.sleep(args.restart_delay)
            
    except KeyboardInterrupt:
        write_log("Restart loop interrupted by user (Ctrl+C)")
    except Exception as e:
        write_log(f"Unexpected error: {str(e)}")
    
    write_log("Auto-restart script ended")


if __name__ == "__main__":
    main() 