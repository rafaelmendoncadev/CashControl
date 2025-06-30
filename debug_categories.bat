@echo off
echo ====================================
echo  CASHCONTROL - MODO DEBUG CATEGORIAS
echo ====================================
echo.
echo Executando teste direto primeiro...
echo.
python test_direct_category.py
echo.
echo ====================================
echo Agora executando o aplicativo...
echo Observe as mensagens de debug no console!
echo ====================================
echo.
python main.py
pause
