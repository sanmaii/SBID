@echo off

IF EXIST sbid_env (
    echo
) ELSE (
    echo Creating venv...
    python -m venv sbid_env
)

call sbid_env\Scripts\activate

pip install -r requirements.txt

echo.
echo venv created successfully, exiting...
pause