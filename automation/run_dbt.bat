@echo off

cd /d C:\Users\dhwan\Downloads\Projects\Atmosync\dbt_project\atmosync

C:\Users\dhwan\anaconda3\Scripts\dbt.exe run

exit /b %ERRORLEVEL%