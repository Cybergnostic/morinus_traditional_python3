# Builds the Windows program into dist\Morinus (Morinus.exe with the data
# folders next to it, as Morinus expects) and, if Inno Setup is installed,
# the installer dist\MorinusTraditional-<version>-setup.exe.
# Run from the repository root in a Python environment with
# wxPython, Pillow, setuptools, timezonefinder, tzdata and pyinstaller:
#
#   powershell -ExecutionPolicy Bypass -File packaging\windows\build.ps1 -Version 1.0.0
param([string]$Version = "dev")
$ErrorActionPreference = "Stop"
$root = Resolve-Path "$PSScriptRoot\..\.."
Set-Location $root

# the Swiss Ephemeris module, next to morinus.py
Push-Location SWEP\src
python setup.py -q build_ext --build-lib ..\.. --build-temp ..\..\build\swe
if ($LASTEXITCODE) { throw "building sweastrology failed" }
Remove-Item -Recurse -Force sweastrology.egg-info -ErrorAction SilentlyContinue
Pop-Location

python -c "from PIL import Image; Image.open('Res/morinus-icon.png').save('build/morinus.ico', sizes=[(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)])"
if ($LASTEXITCODE) { throw "making the icon failed" }

pyinstaller --noconfirm --clean --windowed --name Morinus --icon "$root\build\morinus.ico" `
    --contents-directory lib --collect-all timezonefinder --collect-data tzdata `
    --distpath dist --workpath build\pyinstaller --specpath build morinus.py
if ($LASTEXITCODE) { throw "pyinstaller failed" }

# Morinus reads and writes these relative to the folder of Morinus.exe
$app = "dist\Morinus"
New-Item -ItemType Directory -Force "$app\Res", "$app\SWEP\Ephem", "$app\Hors", "$app\Opts" | Out-Null
Copy-Item Res\* "$app\Res" -Recurse -Exclude placedb.dat
Copy-Item SWEP\Ephem\* "$app\SWEP\Ephem"
Copy-Item Hors\Morinus.hor "$app\Hors"
Copy-Item LICENSE, README.md $app

$iscc = Get-Command iscc -ErrorAction SilentlyContinue
if (-not $iscc -and (Test-Path "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe")) {
    $iscc = "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe"
}
if ($iscc) {
    & $iscc "/DAppVersion=$Version" packaging\windows\morinus.iss
    if ($LASTEXITCODE) { throw "Inno Setup failed" }
} else {
    Write-Host "Inno Setup not found: skipped the installer"
}
