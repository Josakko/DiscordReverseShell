@echo off

mkdir build

::rm -rf venv
::python -m venv venv


curl -o req.txt https://raw.githubusercontent.com/Josakko/DiscordReverseShell/main/requirements.txt 
::.\venv\scripts\pip install -r req.txt
pip install -r req.txt

::.\venv\scripts\python -m nuitka builder.py --clang --clean-cache=all --remove-output --output-dir=build --onefile --standalone --windows-icon-from-ico=icon.png
python -m nuitka builder.py --clang --clean-cache=all --remove-output --output-dir=build --onefile --standalone --windows-icon-from-ico=icon.png
:: --follow-imports

:: rm -rf venv
rm -rf req.txt


echo "Compiling finished!"