$ErrorActionPreference = "Stop"

$networkName = "sysk-network"
$backendName = "sysk-backend"
$frontendName = "sysk-frontend"

Write-Host "Building backend..."
docker build -t $backendName -f Dockerfile.backend .

Write-Host "Building frontend..."
docker build -t $frontendName -f Dockerfile.frontend .

# Check if network exists
$networkExists = docker network ls --format '{{.Name}}' | Select-String -Pattern $networkName

if (-not $networkExists) {
    Write-Host "Creating Docker network $networkName..."
    docker network create $networkName
}

# Remove old containers (if exist)
Write-Host "Cleaning up old containers..."
docker rm -f "$backendName"
docker rm -f "$frontendName"

# Run backend container
Write-Host "Starting backend..."
docker run -d `
  --name $backendName `
  --env-file .env `
  --network $networkName `
  -p 7000:7000 `
  $backendName

# Run frontend container
Write-Host "Starting frontend..."
docker run -d `
  --name $frontendName `
  --env-file .env `
  --network $networkName `
  -p 80:80 `
  $frontendName

Write-Host "All containers are up and running!"