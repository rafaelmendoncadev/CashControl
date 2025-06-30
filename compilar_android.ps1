# Script PowerShell para compilar APK Android
# CashControl - Compilação para Android usando Buildozer

Write-Host "=== CashControl - Compilação Android ===" -ForegroundColor Green
Write-Host ""

# Verificar se o Python está instalado
Write-Host "Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python não encontrado! Instale o Python primeiro." -ForegroundColor Red
    exit 1
}

# Verificar se o pip está disponível
Write-Host "Verificando pip..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✓ pip encontrado: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ pip não encontrado!" -ForegroundColor Red
    exit 1
}

# Instalar/atualizar Buildozer se necessário
Write-Host "Verificando Buildozer..." -ForegroundColor Yellow
$buildozerCheck = pip show buildozer 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Buildozer não encontrado. Instalando..." -ForegroundColor Yellow
    pip install buildozer
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Erro ao instalar Buildozer!" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Buildozer instalado com sucesso!" -ForegroundColor Green
} else {
    Write-Host "✓ Buildozer já está instalado" -ForegroundColor Green
}

# Verificar se o arquivo buildozer.spec existe
if (-not (Test-Path "buildozer.spec")) {
    Write-Host "✗ Arquivo buildozer.spec não encontrado!" -ForegroundColor Red
    Write-Host "Execute primeiro: buildozer init" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Arquivo buildozer.spec encontrado" -ForegroundColor Green

# Verificar estrutura do projeto
Write-Host "Verificando estrutura do projeto..." -ForegroundColor Yellow
$requiredFiles = @("main.py", "requirements.txt")
$requiredDirs = @("controllers", "views", "models")

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✓ $file encontrado" -ForegroundColor Green
    } else {
        Write-Host "✗ $file não encontrado!" -ForegroundColor Red
    }
}

foreach ($dir in $requiredDirs) {
    if (Test-Path $dir) {
        Write-Host "✓ Diretório $dir encontrado" -ForegroundColor Green
    } else {
        Write-Host "✗ Diretório $dir não encontrado!" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=== IMPORTANTE ===" -ForegroundColor Red
Write-Host "A compilação Android com Buildozer no Windows tem limitações." -ForegroundColor Yellow
Write-Host "Recomendações:" -ForegroundColor Yellow
Write-Host "1. Use WSL2 (Windows Subsystem for Linux) para melhor compatibilidade" -ForegroundColor White
Write-Host "2. Use uma máquina virtual Linux" -ForegroundColor White
Write-Host "3. Use um serviço de build em nuvem" -ForegroundColor White
Write-Host ""

# Perguntar se deseja continuar
$continuar = Read-Host "Deseja tentar compilar mesmo assim? (s/N)"
if ($continuar -ne "s" -and $continuar -ne "S") {
    Write-Host "Compilação cancelada." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Iniciando compilação..." -ForegroundColor Green
Write-Host "Isso pode demorar muito tempo na primeira execução..." -ForegroundColor Yellow
Write-Host ""

# Executar buildozer
Write-Host "Executando: buildozer android debug" -ForegroundColor Cyan
buildozer android debug

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✓ Compilação concluída com sucesso!" -ForegroundColor Green
    Write-Host "APK gerado em: bin/CashControl-*-debug.apk" -ForegroundColor Green
    Write-Host ""
    Write-Host "Para instalar no dispositivo:" -ForegroundColor Yellow
    Write-Host "1. Ative 'Opções do desenvolvedor' no Android" -ForegroundColor White
    Write-Host "2. Ative 'Depuração USB' e 'Instalar apps desconhecidas'" -ForegroundColor White
    Write-Host "3. Conecte o dispositivo via USB" -ForegroundColor White
    Write-Host "4. Execute: adb install bin/CashControl-*-debug.apk" -ForegroundColor White
    Write-Host ""
    Write-Host "Ou transfira o APK para o dispositivo e instale manualmente." -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "✗ Erro durante a compilação!" -ForegroundColor Red
    Write-Host "Verifique os logs acima para mais detalhes." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Problemas comuns no Windows:" -ForegroundColor Yellow
    Write-Host "- Falta de dependências do Android SDK" -ForegroundColor White
    Write-Host "- Problemas com paths longos" -ForegroundColor White
    Write-Host "- Incompatibilidades com NDK" -ForegroundColor White
    Write-Host ""
    Write-Host "Considere usar WSL2 ou Linux para compilação Android." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Script finalizado." -ForegroundColor Green
