; Inno Setup script for the Windows installer; build.ps1 runs it after
; PyInstaller. Installs per user into a writable folder, because Morinus
; keeps its settings (Opts), charts (Hors) and places (Res) beside the exe.

#ifndef AppVersion
  #define AppVersion "dev"
#endif

[Setup]
AppId={{6F4B7E2A-3C1D-4E8F-9A2B-7D5C1E3F8A90}
AppName=Morinus Traditional
AppVersion={#AppVersion}
AppPublisher=Cybergnostic
AppPublisherURL=https://github.com/Cybergnostic/morinus_traditional_python3
DefaultDirName={localappdata}\Programs\Morinus Traditional
DefaultGroupName=Morinus Traditional
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
LicenseFile=..\..\LICENSE
SetupIconFile=..\..\build\morinus.ico
UninstallDisplayIcon={app}\Morinus.exe
OutputDir=..\..\dist
OutputBaseFilename=MorinusTraditional-{#AppVersion}-setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\..\dist\Morinus\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

[Dirs]
; settings and charts are the user's: kept on uninstall
Name: "{app}\Opts"; Flags: uninsneveruninstall
Name: "{app}\Hors"; Flags: uninsneveruninstall

[Icons]
Name: "{group}\Morinus Traditional"; Filename: "{app}\Morinus.exe"; WorkingDir: "{app}"
Name: "{group}\Uninstall Morinus Traditional"; Filename: "{uninstallexe}"
Name: "{userdesktop}\Morinus Traditional"; Filename: "{app}\Morinus.exe"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{app}\Morinus.exe"; WorkingDir: "{app}"; Description: "{cm:LaunchProgram,Morinus Traditional}"; Flags: nowait postinstall skipifsilent
