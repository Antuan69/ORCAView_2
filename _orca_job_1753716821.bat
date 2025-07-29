@echo on
echo Running: "C:\ORCA_6.1.0\orca.exe" "C:\Windsurf stuff\ORCAView\test1.inp" > "C:\Windsurf stuff\ORCAView\test1.out" 2>&1
"C:\ORCA_6.1.0\orca.exe" "C:\Windsurf stuff\ORCAView\test1.inp" > "C:\Windsurf stuff\ORCAView\test1.out" 2>&1
echo Exit code: %errorlevel%
pause
