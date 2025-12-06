@echo off
echo Compiling Legacy System...
if not exist bin mkdir bin
javac -d bin -sourcepath src src/*.java

if %errorlevel% neq 0 (
    echo Compilation failed!
    pause
    exit /b %errorlevel%
)

echo Running Legacy System...
java -cp bin Register
pause