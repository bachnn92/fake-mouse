@echo off
rmdir /s /q build
rmdir /s /q dist
del main.spec

pyinstaller --onefile --name fake-mouse main.py