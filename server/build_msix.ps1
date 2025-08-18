# SnapClass MSIX Build Script
# This script builds the SnapClass application as an MSIX package for Microsoft Store

param(
    [string]$Version = "1.0.0.0",
    [string]$Publisher = "CN=YourPublisherName",
    [string]$OutputPath = ".\dist\msix"
)

Write-Host "🚀 Starting SnapClass MSIX Build Process..." -ForegroundColor Green

# Create output directory
if (!(Test-Path $OutputPath)) {
    New-Item -ItemType Directory -Path $OutputPath -Force | Out-Null
    Write-Host "✅ Created output directory: $OutputPath" -ForegroundColor Green
}

# Step 1: Build with PyInstaller
Write-Host "📦 Building executable with PyInstaller..." -ForegroundColor Yellow
pyinstaller --clean --noconfirm --onedir --windowed --name SnapClass --distpath ".\dist\SnapClass" desktop_app.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ PyInstaller build failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ PyInstaller build completed successfully" -ForegroundColor Green

# Step 2: Copy required assets and models
Write-Host "📁 Copying required assets and models..." -ForegroundColor Yellow
$distPath = ".\dist\SnapClass\SnapClass"

# Copy model directories
$modelDirs = @("llama3", "whisper", "nougat", "blip", "poppler")
foreach ($dir in $modelDirs) {
    if (Test-Path $dir) {
        Copy-Item -Path $dir -Destination $distPath -Recurse -Force
        Write-Host "  ✅ Copied $dir" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  Warning: $dir not found" -ForegroundColor Yellow
    }
}

# Copy templates and static
if (Test-Path "templates") {
    Copy-Item -Path "templates" -Destination $distPath -Recurse -Force
    Write-Host "  ✅ Copied templates" -ForegroundColor Green
}
if (Test-Path "static") {
    Copy-Item -Path "static" -Destination $distPath -Recurse -Force
    Write-Host "  ✅ Copied static" -ForegroundColor Green
}

# Step 3: Update manifest with current version and publisher
Write-Host "📝 Updating Package.appxmanifest..." -ForegroundColor Yellow
$manifestPath = "Package.appxmanifest"
$manifestContent = Get-Content $manifestPath -Raw
$manifestContent = $manifestContent -replace 'Version="[^"]*"', "Version=`"$Version`""
$manifestContent = $manifestContent -replace 'Publisher="[^"]*"', "Publisher=`"$Publisher`""
Set-Content -Path $manifestPath -Value $manifestContent
Write-Host "  ✅ Updated manifest version to $Version" -ForegroundColor Green

# Step 4: Copy manifest to dist directory
Copy-Item -Path "Package.appxmanifest" -Destination $distPath -Force
Write-Host "  ✅ Copied manifest to dist directory" -ForegroundColor Green

# Step 5: Create MSIX package using MakeAppx
Write-Host "📦 Creating MSIX package..." -ForegroundColor Yellow
$msixPath = "$OutputPath\SnapClass_$Version.msix"

# Check if MakeAppx is available
$makeAppxPath = "${env:ProgramFiles(x86)}\Windows Kits\10\bin\10.0.19041.0\x64\MakeAppx.exe"
if (!(Test-Path $makeAppxPath)) {
    # Try to find MakeAppx in common locations
    $sdkPaths = @(
        "${env:ProgramFiles(x86)}\Windows Kits\10\bin\*\x64\MakeAppx.exe",
        "${env:ProgramFiles}\Windows Kits\10\bin\*\x64\MakeAppx.exe"
    )
    
    foreach ($path in $sdkPaths) {
        $found = Get-ChildItem -Path $path -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($found) {
            $makeAppxPath = $found.FullName
            break
        }
    }
}

if (Test-Path $makeAppxPath) {
    Write-Host "  🔧 Using MakeAppx: $makeAppxPath" -ForegroundColor Cyan
    
    # Create MSIX package
    & $makeAppxPath pack /d "$distPath" /p "$msixPath" /l
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ MSIX package created: $msixPath" -ForegroundColor Green
    } else {
        Write-Host "  ❌ MSIX package creation failed!" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "  ⚠️  MakeAppx not found. Please install Windows SDK or use MSIX Packaging Tool" -ForegroundColor Yellow
    Write-Host "  📁 Dist directory ready at: $distPath" -ForegroundColor Cyan
    Write-Host "  📋 Manual steps:" -ForegroundColor Cyan
    Write-Host "     1. Open MSIX Packaging Tool" -ForegroundColor White
    Write-Host "     2. Select 'Create package' -> 'From existing files'" -ForegroundColor White
    Write-Host "     3. Browse to: $distPath" -ForegroundColor White
    Write-Host "     4. Set output location and create package" -ForegroundColor White
}

Write-Host "🎉 SnapClass MSIX build process completed!" -ForegroundColor Green
Write-Host "📁 Output location: $OutputPath" -ForegroundColor Cyan
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Test the MSIX package locally" -ForegroundColor White
Write-Host "   2. Sign the package with your certificate" -ForegroundColor White
Write-Host "   3. Upload to Microsoft Store Partner Center" -ForegroundColor White
