[Setup]
AppName=ORCAView
AppVersion=1.0
DefaultDirName={pf}\ORCAView
DefaultGroupName=ORCAView
OutputBaseFilename=ORCAView-Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\ORCAView\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{group}\ORCAView"; Filename: "{app}\ORCAView.exe"
Name: "{group}\Uninstall ORCAView"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\ORCAView.exe"; Description: "Launch ORCAView"; Flags: nowait postinstall skipifsilent
