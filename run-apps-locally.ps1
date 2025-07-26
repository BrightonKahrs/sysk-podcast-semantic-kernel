# ─── Free Port 7000 If Needed ─────────────────────
$process_id = Get-NetTCPConnection -LocalPort 7000 -ErrorAction SilentlyContinue |
    Where-Object { $_.State -eq 'Listen' } |
    Select-Object -ExpandProperty OwningProcess

if ($process_id) {
    Write-Host "Port 7000 is in use by PID $process_id. Stopping it..."
    Stop-Process -Id $process_id -Force
    Start-Sleep -Seconds 2
} else {
    Write-Host "Port 7000 is free. Continuing..."
}

# ─── Start Backend ────────────────────────────────
Write-Host "Starting backend..."
Start-Process powershell -ArgumentList "python -m backend.app"

# ─── Wait Until Port 7000 is Listening ────────────
$maxRetries = 30
$waitSeconds = 1
$retry = 0

Write-Host "Waiting for backend to start on port 7000..."

do {
    Start-Sleep -Seconds $waitSeconds
    $backendReady = Get-NetTCPConnection -LocalPort 7000 -ErrorAction SilentlyContinue |
        Where-Object { $_.State -eq 'Listen' }

    $retry++
} until ($backendReady -or $retry -ge $maxRetries)

if ($backendReady) {
    Write-Host "✅ Backend is up. Starting frontend..."
    Start-Process powershell -ArgumentList "streamlit run frontend/app.py"
} else {
    Write-Host "❌ Backend did not start within $($maxRetries * $waitSeconds) seconds."
}
