# Script para configurar ambiente de compilação Android
# CashControl - Setup WSL2 + Buildozer

Write-Host "=== CashControl - Setup Compilação Android ===" -ForegroundColor Green
Write-Host ""

# Verificar se está executando como administrador
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "Este script precisa ser executado como Administrador!" -ForegroundColor Red
    Write-Host "Clique com o botão direito no PowerShell e selecione 'Executar como administrador'" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "✓ Executando como administrador" -ForegroundColor Green

# Verificar se WSL2 está instalado
Write-Host "Verificando WSL2..." -ForegroundColor Yellow
$wslStatus = wsl --status 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ WSL2 já está instalado" -ForegroundColor Green
} else {
    Write-Host "WSL2 não encontrado. Instalando..." -ForegroundColor Yellow
    
    # Instalar WSL2
    wsl --install Ubuntu
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ WSL2 instalado com sucesso!" -ForegroundColor Green
        Write-Host "IMPORTANTE: Reinicie o computador antes de continuar!" -ForegroundColor Red
        Write-Host "Após reiniciar, execute este script novamente." -ForegroundColor Yellow
        pause
        exit 0
    } else {
        Write-Host "✗ Erro ao instalar WSL2" -ForegroundColor Red
        exit 1
    }
}

# Verificar se Ubuntu está instalado
Write-Host "Verificando Ubuntu no WSL2..." -ForegroundColor Yellow
$ubuntuCheck = wsl -l -v | Select-String "Ubuntu"
if ($ubuntuCheck) {
    Write-Host "✓ Ubuntu encontrado no WSL2" -ForegroundColor Green
} else {
    Write-Host "Instalando Ubuntu..." -ForegroundColor Yellow
    wsl --install Ubuntu
    Write-Host "✓ Ubuntu instalado. Reinicie o computador!" -ForegroundColor Green
    pause
    exit 0
}

Write-Host ""
Write-Host "=== Configurando Ambiente de Compilação ===" -ForegroundColor Cyan
Write-Host ""

# Criar script de setup para o WSL2
$wslSetupScript = @'
#!/bin/bash
echo "=== Configurando ambiente Android no WSL2 ==="
echo ""

# Atualizar sistema
echo "Atualizando sistema..."
sudo apt-get update -y
sudo apt-get upgrade -y

# Instalar dependências
echo "Instalando dependências..."
sudo apt-get install -y \
    git zip unzip openjdk-8-jdk python3-pip autoconf libtool \
    pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev \
    libtinfo5 cmake libffi-dev libssl-dev build-essential

# Instalar buildozer
echo "Instalando buildozer..."
pip3 install --user buildozer
pip3 install --user cython==0.29.33

# Adicionar ao PATH
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
source ~/.bashrc

# Verificar instalação
echo ""
echo "=== Verificando instalação ==="
python3 --version
pip3 --version
~/.local/bin/buildozer --version

echo ""
echo "✓ Ambiente configurado com sucesso!"
echo ""
echo "Para compilar o APK:"
echo "1. Copie o projeto CashControl para o WSL2"
echo "2. Execute: cd CashControl"
echo "3. Execute: ~/.local/bin/buildozer android debug"
echo ""
echo "Primeira compilação pode demorar 30-60 minutos."
'@

# Salvar script no WSL2
$wslSetupScript | Out-File -FilePath "wsl_setup.sh" -Encoding UTF8
wsl -- dos2unix wsl_setup.sh
wsl -- chmod +x wsl_setup.sh

Write-Host "Executando configuração no WSL2..." -ForegroundColor Yellow
wsl -- ./wsl_setup.sh

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✓ Configuração concluída com sucesso!" -ForegroundColor Green
    Write-Host ""
    Write-Host "=== Próximos Passos ===" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. Copiar projeto para WSL2:" -ForegroundColor Yellow
    Write-Host "   wsl" -ForegroundColor White
    Write-Host "   cp -r /mnt/c/Users/$env:USERNAME/OneDrive/Projetos*/CashControl ~/" -ForegroundColor White
    Write-Host "   cd ~/CashControl" -ForegroundColor White
    Write-Host ""
    Write-Host "2. Compilar APK:" -ForegroundColor Yellow
    Write-Host "   ~/.local/bin/buildozer android debug" -ForegroundColor White
    Write-Host ""
    Write-Host "3. O APK será gerado em:" -ForegroundColor Yellow
    Write-Host "   ~/CashControl/bin/CashControl-*-debug.apk" -ForegroundColor White
    Write-Host ""
    Write-Host "4. Copiar APK de volta para Windows:" -ForegroundColor Yellow
    Write-Host "   cp bin/*.apk /mnt/c/Users/$env:USERNAME/Downloads/" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 Dica: A primeira compilação demora muito, mas é normal!" -ForegroundColor Green
} else {
    Write-Host "✗ Erro na configuração" -ForegroundColor Red
    Write-Host "Tente executar manualmente no WSL2:" -ForegroundColor Yellow
    Write-Host "wsl" -ForegroundColor White
    Write-Host "./wsl_setup.sh" -ForegroundColor White
}

# Limpar arquivos temporários
Remove-Item "wsl_setup.sh" -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "Setup finalizado!" -ForegroundColor Green
pause 