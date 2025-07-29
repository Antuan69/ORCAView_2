[Setup]
AppName=ORCAView
AppVersion=1.0
DefaultDirName={pf}\ORCAView
DefaultGroupName=ORCAView
OutputBaseFilename=ORCAView-Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "C:\Windsurf stuff\ORCAView\dist\main\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{group}\ORCAView"; Filename: "{app}\main.exe"
Name: "{group}\Uninstall ORCAView"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\main.exe"; Description: "Launch ORCAView"; Flags: nowait postinstall skipifsilent
