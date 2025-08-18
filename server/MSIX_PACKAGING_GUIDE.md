# SnapClass MSIX Packaging Guide

This guide will walk you through packaging SnapClass as an MSIX package for submission to the Microsoft Store.

## Prerequisites

### 1. Windows Development Environment
- Windows 10/11 (version 1903 or later)
- Visual Studio 2019/2022 or Windows SDK 10.0.19041.0 or later
- PowerShell 5.0 or later

### 2. Microsoft Store Developer Account
- Active Microsoft Partner Center account
- App identity and publisher information
- Code signing certificate

### 3. Python Environment
- Python 3.10+ with required packages
- PyInstaller for executable creation

## Quick Start

### Option 1: Automated Build (Recommended)
```powershell
# Run the automated build script
.\build_msix.ps1 -Version "1.0.0.0" -Publisher "CN=YourPublisherName"
```

### Option 2: Manual Build
```powershell
# 1. Build executable
pyinstaller --clean --noconfirm --onedir --windowed --name SnapClass desktop_app.py

# 2. Copy assets and models
# 3. Use MSIX Packaging Tool or MakeAppx
```

## Detailed Steps

### Step 1: Prepare Your Environment

1. **Install Windows SDK**
   - Download from: https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/
   - Ensure MakeAppx.exe is available

2. **Install MSIX Packaging Tool** (Alternative to MakeAppx)
   - Download from Microsoft Store
   - Provides GUI interface for packaging

3. **Verify Python Dependencies**
   ```powershell
   pip install -r requirements_msix.txt
   ```

### Step 2: Configure App Identity

1. **Update Package.appxmanifest**
   - Replace `YourPublisherName` with your actual publisher name
   - Update version number as needed
   - Customize app description and capabilities

2. **Publisher Information**
   - Publisher name format: `CN=YourCompanyName`
   - Must match your Microsoft Partner Center account

### Step 3: Build the Application

1. **Run PyInstaller**
   ```powershell
   pyinstaller --clean --noconfirm --onedir --windowed --name SnapClass desktop_app.py
   ```

2. **Verify Output**
   - Check `dist/SnapClass/SnapClass/` directory
   - Ensure all required files are present

### Step 4: Create MSIX Package

#### Using MakeAppx (Command Line)
```powershell
# Navigate to Windows SDK bin directory
cd "C:\Program Files (x86)\Windows Kits\10\bin\10.0.19041.0\x64"

# Create MSIX package
.\MakeAppx.exe pack /d "C:\path\to\SnapClass\dist\SnapClass\SnapClass" /p "C:\output\SnapClass.msix" /l
```

#### Using MSIX Packaging Tool (GUI)
1. Open MSIX Packaging Tool
2. Select "Create package" → "From existing files"
3. Browse to your dist directory
4. Set output location and create package

### Step 5: Sign the Package

1. **Obtain Code Signing Certificate**
   - Purchase from trusted CA (DigiCert, Sectigo, etc.)
   - Or use Microsoft's certificate for Store apps

2. **Sign the Package**
   ```powershell
   # Using SignTool
   signtool sign /f "certificate.pfx" /p "password" /fd SHA256 "SnapClass.msix"
   ```

### Step 6: Test the Package

1. **Local Testing**
   ```powershell
   # Install package locally
   Add-AppxPackage -Path "SnapClass.msix"
   
   # Test functionality
   # Uninstall when done
   Remove-AppxPackage "SnapClass.AI"
   ```

2. **Validation**
   - Test all features work correctly
   - Verify file associations
   - Check permissions and capabilities

### Step 7: Submit to Microsoft Store

1. **Microsoft Partner Center**
   - Log in to https://partner.microsoft.com
   - Create new app submission

2. **App Information**
   - App name: SnapClass AI
   - Description: Use the description from manifest
   - Category: Education or Productivity

3. **Package Upload**
   - Upload your signed MSIX package
   - Set minimum OS version (Windows 10, version 1903)
   - Configure pricing and availability

4. **Store Listing**
   - Screenshots and promotional images
   - App description and keywords
   - Privacy policy and terms of use

## Troubleshooting

### Common Issues

1. **MakeAppx Not Found**
   - Install Windows SDK
   - Check PATH environment variable
   - Use MSIX Packaging Tool as alternative

2. **Package Validation Errors**
   - Verify manifest syntax
   - Check file paths and references
   - Ensure all required assets exist

3. **Code Signing Issues**
   - Verify certificate validity
   - Check timestamp server connectivity
   - Ensure proper certificate chain

4. **Store Submission Rejected**
   - Review certification requirements
   - Check app functionality
   - Verify privacy policy compliance

### Validation Commands

```powershell
# Validate MSIX package
Get-AppxPackageManifest -Package "SnapClass.msix"

# Check package contents
Expand-AppxPackage -Path "SnapClass.msix" -DestinationPath ".\expanded"

# Verify digital signature
Get-AuthenticodeSignature "SnapClass.msix"
```

## Store Requirements

### Technical Requirements
- Windows 10 version 1903 or later
- x64 architecture support
- Proper app identity and publisher
- Valid code signature

### Content Requirements
- Accurate app description
- Appropriate content rating
- Privacy policy
- Terms of use
- Support contact information

### Certification Requirements
- App must function as described
- No crashes or critical errors
- Proper error handling
- Appropriate permissions usage

## Resources

- [MSIX Documentation](https://docs.microsoft.com/en-us/windows/msix/)
- [Microsoft Store Policies](https://docs.microsoft.com/en-us/legal/windows/agreements/store-policies)
- [App Certification Requirements](https://docs.microsoft.com/en-us/windows/uwp/publish/app-certification-requirements)
- [MSIX Packaging Tool](https://docs.microsoft.com/en-us/windows/msix/packaging-tool/create-an-msix-package)

## Support

For technical issues:
- Check Windows SDK documentation
- Review MSIX packaging guides
- Consult Microsoft Store support

For business questions:
- Contact Microsoft Partner Center support
- Review store policies and requirements
