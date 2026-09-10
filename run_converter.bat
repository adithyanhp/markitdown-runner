
@REM  Batch script to run the Markdown conversion script

@echo off
cd /d "%~dp0"
call .venv\Scripts\activate
python "markitdown run-script.py"
pause


@REM  or use the below code if you want to specify the full path to the script:

@REM  @REM  Batch script to run the Markdown conversion script

@REM  @echo off
@REM  cd /d "C:\Users\adith\Documents\MarkitDown"
@REM  call .venv\Scripts\activate
@REM  python batch_convert.py
@REM  pause
