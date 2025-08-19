# SnapClass MSIX Build Script
param(
    [string]$Version = "1.0.0.0",
    [string]$Publisher = "CN=YourPublisherName",
    [string]$OutputPath = ".\dist\msix",
    [string]$AppIdentityName = "SnapClass.AI",
    [string]$DisplayName = "SnapClass AI",
    [string]$PublisherDisplayName = "carrycooldude",
    [switch]$IncludeModels
)

Write-Host "Starting SnapClass MSIX Build Process..." -ForegroundColor Green

# Create output directory
if (!(Test-Path $OutputPath)) {
    New-Item -ItemType Directory -Path $OutputPath -Force | Out-Null
    Write-Host "Created output directory: $OutputPath" -ForegroundColor Green
}

# Step 1: Build with PyInstaller
Write-Host "Building executable with PyInstaller..." -ForegroundColor Yellow
pyinstaller --clean --noconfirm --onedir --windowed --name SnapClass --distpath ".\\dist\\SnapClass" desktop_app.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "PyInstaller build failed!" -ForegroundColor Red
    exit 1
}
Write-Host "PyInstaller build completed successfully" -ForegroundColor Green

# Step 2: Copy required assets and models (models optional to keep MSIX small)
Write-Host "Copying required assets..." -ForegroundColor Yellow
$distPath = ".\\dist\\SnapClass\\SnapClass"

# Always copy minimal runtime dependencies
$alwaysDirs = @("poppler")
foreach ($dir in $alwaysDirs) {
    if (Test-Path $dir) {
        Copy-Item -Path $dir -Destination $distPath -Recurse -Force
        Write-Host "Copied $dir" -ForegroundColor Green
    }
}

# Optionally copy large AI model folders
if ($IncludeModels) {
    Write-Host "Including AI model folders (this can make the package very large)..." -ForegroundColor Yellow
    $optionalModelDirs = @("llama3", "whisper", "nougat", "blip")
    foreach ($dir in $optionalModelDirs) {
        if (Test-Path $dir) {
            Copy-Item -Path $dir -Destination $distPath -Recurse -Force
            Write-Host "Copied $dir" -ForegroundColor Green
        } else {
            Write-Host "Warning: $dir not found" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "Skipping large model folders. The app should download or locate them on first run." -ForegroundColor Cyan
}

# Copy templates and static
if (Test-Path "templates") {
    Copy-Item -Path "templates" -Destination $distPath -Recurse -Force
    Write-Host "Copied templates" -ForegroundColor Green
}
if (Test-Path "static") {
    Copy-Item -Path "static" -Destination $distPath -Recurse -Force
    Write-Host "Copied static" -ForegroundColor Green
}

# Ensure Assets are included
if (Test-Path "Assets") {
    Copy-Item -Path "Assets" -Destination $distPath -Recurse -Force
    Write-Host "Copied Assets" -ForegroundColor Green
} else {
    Write-Host "Warning: Assets folder not found" -ForegroundColor Yellow
}

# Trim unnecessary debug/build files to reduce size
Write-Host "Trimming debug files (__pycache__, *.pdb, *.lib, *.map)..." -ForegroundColor Yellow
Get-ChildItem -Path $distPath -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path $distPath -Recurse -File -Include *.pdb,*.lib,*.map -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue

# Step 3: Generate a clean manifest with current version and publisher
Write-Host "Generating AppxManifest.xml..." -ForegroundColor Yellow
$manifestXml = @"
<?xml version="1.0" encoding="utf-8"?>
<Package xmlns="http://schemas.microsoft.com/appx/manifest/foundation/windows10"
         xmlns:uap="http://schemas.microsoft.com/appx/manifest/uap/windows10"
         xmlns:rescap="http://schemas.microsoft.com/appx/manifest/foundation/windows10/restrictedcapabilities"
         IgnorableNamespaces="uap rescap">
  <Identity Name="$AppIdentityName" Publisher="$Publisher" Version="$Version" ProcessorArchitecture="x64" />
  <Properties>
    <DisplayName>$DisplayName</DisplayName>
    <PublisherDisplayName>$PublisherDisplayName</PublisherDisplayName>
    <Logo>Assets\StoreLogo.png</Logo>
    <Description>SnapClass is an advanced on-device edge AI solution designed for low-connectivity, high-density classroom environments. Powered by Snapdragon's Hexagon NPU, it runs open-source large language models (LLMs), image captioning, and audio transcription entirely offline.</Description>
  </Properties>
  <Dependencies>
    <TargetDeviceFamily Name="Windows.Desktop" MinVersion="10.0.19041.0" MaxVersionTested="10.0.26100.0" />
  </Dependencies>
  <Resources>
    <Resource Language="en-us" />
  </Resources>
  <Applications>
    <Application Id="SnapClass" Executable="SnapClass.exe" EntryPoint="Windows.FullTrustApplication">
      <uap:VisualElements DisplayName="$DisplayName"
                          Square150x150Logo="Assets\Square150x150Logo.png"
                          Square44x44Logo="Assets\Square44x44Logo.png"
                          Description="AI-powered classroom assistant"
                          BackgroundColor="transparent">
        <uap:DefaultTile Wide310x150Logo="Assets\Wide310x150Logo.png" />
        <uap:SplashScreen Image="Assets\SplashScreen.png" />
      </uap:VisualElements>
      <Extensions>
        <uap:Extension Category="windows.fileTypeAssociation">
          <uap:FileTypeAssociation Name="snapclassfiles">
            <uap:DisplayName>SnapClass Files</uap:DisplayName>
            <uap:SupportedFileTypes>
              <uap:FileType>.pdf</uap:FileType>
              <uap:FileType>.mp3</uap:FileType>
              <uap:FileType>.wav</uap:FileType>
              <uap:FileType>.mp4</uap:FileType>
              <uap:FileType>.jpg</uap:FileType>
              <uap:FileType>.png</uap:FileType>
            </uap:SupportedFileTypes>
          </uap:FileTypeAssociation>
        </uap:Extension>
      </Extensions>
    </Application>
  </Applications>
  <Capabilities>
    <rescap:Capability Name="runFullTrust" />
    <Capability Name="internetClient" />
    <Capability Name="privateNetworkClientServer" />
  </Capabilities>
</Package>
"@

# Write manifest to source and dist to keep them in sync
$sourceManifestPath = "Package.appxmanifest"
Set-Content -Path $sourceManifestPath -Value $manifestXml -NoNewline -Encoding UTF8
$distManifestPath = Join-Path $distPath "AppxManifest.xml"
Set-Content -Path $distManifestPath -Value $manifestXml -NoNewline -Encoding UTF8
Write-Host "Wrote manifest to: $distManifestPath" -ForegroundColor Green

# Step 5: Create MSIX package using MakeAppx
Write-Host "Creating MSIX package..." -ForegroundColor Yellow
$msixPath = "$OutputPath\SnapClass_$Version.msix"

# Remove existing package to avoid prompts
if (Test-Path $msixPath) {
    Remove-Item -Path $msixPath -Force -ErrorAction SilentlyContinue
    Write-Host "Removed existing package: $msixPath" -ForegroundColor Yellow
}

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
    Write-Host "Using MakeAppx: $makeAppxPath" -ForegroundColor Cyan
    
    # Create MSIX package with overwrite
    & $makeAppxPath pack /d "$distPath" /p "$msixPath" /o /l
    if ($LASTEXITCODE -eq 0) {
        Write-Host "MSIX package created: $msixPath" -ForegroundColor Green
    } else {
        Write-Host "MSIX package creation failed!" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "MakeAppx not found. Please install Windows SDK or use MSIX Packaging Tool" -ForegroundColor Yellow
    Write-Host "Dist directory ready at: $distPath" -ForegroundColor Cyan
    Write-Host "Manual steps:" -ForegroundColor Cyan
    Write-Host "1. Open MSIX Packaging Tool" -ForegroundColor White
    Write-Host "2. Select 'Create package' -> 'From existing files'" -ForegroundColor White
    Write-Host "3. Browse to: $distPath" -ForegroundColor White
    Write-Host "4. Set output location and create package" -ForegroundColor White
}

Write-Host "SnapClass MSIX build process completed!" -ForegroundColor Green
Write-Host "Output location: $OutputPath" -ForegroundColor Cyan
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Test the MSIX package locally" -ForegroundColor White
Write-Host "2. Sign the package with your certificate" -ForegroundColor White
Write-Host "3. Upload to Microsoft Store Partner Center" -ForegroundColor White
