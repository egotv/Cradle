# Restart Runner Script for Cradle RDR2
# This script will continuously restart your runner.py when it stops

param(
    [string]$EnvConfig = "./conf/env_config_rdr2_main_storyline.json",
    [int]$RestartDelay = 5
)

$LogFile = "restart_log.txt"
$Command = "python"
$Arguments = "runner.py --envConfig `"$EnvConfig`""

function Write-Log {
    param($Message)
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogEntry = "$Timestamp - $Message"
    Write-Host $LogEntry
    Add-Content -Path $LogFile -Value $LogEntry
}

Write-Log "Starting Cradle RDR2 Auto-Restart Script"
Write-Log "Command: $Command $Arguments"
Write-Log "Restart delay: $RestartDelay seconds"
Write-Log "Press Ctrl+C to stop the restart loop"

$RestartCount = 0

while ($true) {
    try {
        $RestartCount++
        Write-Log "=== Restart #$RestartCount ==="
        
        # Start the process
        $Process = Start-Process -FilePath $Command -ArgumentList $Arguments -NoNewWindow -PassThru -Wait
        
        $ExitCode = $Process.ExitCode
        Write-Log "Process exited with code: $ExitCode"
        
        if ($ExitCode -eq 0) {
            Write-Log "Process completed successfully"
        } else {
            Write-Log "Process exited with error code: $ExitCode"
        }
        
        Write-Log "Waiting $RestartDelay seconds before restart..."
        Start-Sleep -Seconds $RestartDelay
        
    } catch {
        Write-Log "Error occurred: $($_.Exception.Message)"
        Write-Log "Waiting $RestartDelay seconds before retry..."
        Start-Sleep -Seconds $RestartDelay
    }
} 