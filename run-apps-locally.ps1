# Find the process ID (PID) using port 7000
$process_id = Get-NetTCPConnection -LocalPort 7000 -ErrorAction SilentlyContinue |
    Where-Object { $_.State -eq 'Listen' } |
    Select-Object -ExpandProperty OwningProcess

# If a process is using the port, kill it
if ($process_id) {
    Write-Host "Port 7000 is in use by PID $process_id. Stopping it..."
    Stop-Process -Id $process_id -Force
    Start-Sleep -Seconds 2
} else {
    Write-Host "Port 7000 is free. Continuing..."
}

# Start backend in a new window
Start-Process powershell -ArgumentList "python -m backend.app"
Start-Sleep -Seconds 5

# Start frontend in a new window
Start-Process powershell -ArgumentList "streamlit run frontend/app.py"