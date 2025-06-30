# 🐧 CashControl - Instalador WSL2 para Android
# Execute este script como ADMINISTRADOR

Write-Host "🚀 CashControl - Configuração WSL2 para Android" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green
Write-Host ""

# Verificar se está executando como administrador
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ Este script deve ser executado como ADMINISTRADOR!" -ForegroundColor Red
    Write-Host "Clique com botão direito no PowerShell e selecione 'Executar como administrador'" -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host "✅ Executando como administrador" -ForegroundColor Green
Write-Host ""

# Verificar versão do Windows
$windowsVersion = [System.Environment]::OSVersion.Version
if ($windowsVersion.Major -lt 10) {
    Write-Host "❌ WSL2 requer Windows 10 versão 1903 ou superior" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Windows compatível com WSL2" -ForegroundColor Green

# 1. Ativar recursos necessários
Write-Host "🔧 Ativando recursos do Windows..." -ForegroundColor Yellow
try {
    dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
    dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
    Write-Host "✅ Recursos ativados com sucesso" -ForegroundColor Green
}
catch {
    Write-Host "❌ Erro ao ativar recursos: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# 2. Verificar se WSL já está instalado
Write-Host "🔍 Verificando WSL existente..." -ForegroundColor Yellow
$wslCheck = wsl --list --verbose 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ WSL já está instalado" -ForegroundColor Green
    Write-Host $wslCheck
    
    # Verificar se Ubuntu-20.04 já existe
    if ($wslCheck -match "Ubuntu-20.04") {
        Write-Host "✅ Ubuntu-20.04 já está instalado" -ForegroundColor Green
        $useExisting = Read-Host "Deseja usar a instalação existente? (s/N)"
        if ($useExisting -eq "s" -or $useExisting -eq "S") {
            Write-Host "👍 Usando Ubuntu existente" -ForegroundColor Green
            Write-Host ""
            Write-Host "📋 PRÓXIMOS PASSOS:" -ForegroundColor Cyan
            Write-Host "1. Abra o Ubuntu no menu iniciar" -ForegroundColor White
            Write-Host "2. Execute: wget https://raw.githubusercontent.com/seu-repo/setup_wsl_android.sh" -ForegroundColor White
            Write-Host "3. Execute: chmod +x setup_wsl_android.sh && ./setup_wsl_android.sh" -ForegroundColor White
            Read-Host "Pressione Enter para continuar"
            exit 0
        }
    }
}

# 3. Instalar WSL2 e Ubuntu
Write-Host "📥 Instalando WSL2 e Ubuntu-20.04..." -ForegroundColor Yellow
try {
    wsl --install Ubuntu-20.04
    Write-Host "✅ Instalação iniciada com sucesso" -ForegroundColor Green
}
catch {
    Write-Host "❌ Erro na instalação: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Tentando método alternativo..." -ForegroundColor Yellow
    
    # Método alternativo
    try {
        wsl --install -d Ubuntu-20.04
        Write-Host "✅ Instalação alternativa bem-sucedida" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Falha na instalação alternativa" -ForegroundColor Red
        Write-Host "Execute manualmente: wsl --install Ubuntu-20.04" -ForegroundColor Yellow
        Read-Host "Pressione Enter para sair"
        exit 1
    }
}

# 4. Configurar WSL2 como padrão
Write-Host "⚙️ Configurando WSL2 como padrão..." -ForegroundColor Yellow
try {
    wsl --set-default-version 2
    Write-Host "✅ WSL2 definido como padrão" -ForegroundColor Green
}
catch {
    Write-Host "⚠️ Aviso: Não foi possível definir WSL2 como padrão" -ForegroundColor Yellow
}

# 5. Criar arquivo de setup na pasta do projeto
$setupContent = @'
#!/bin/bash
# Download e execução automática do setup
echo "📥 Baixando script de configuração..."
cd "/mnt/c/Users/Rafael/OneDrive/Projetos em Python/CashControl"
if [ -f "setup_wsl_android.sh" ]; then
    echo "✅ Script encontrado localmente"
    chmod +x setup_wsl_android.sh
    ./setup_wsl_android.sh
else
    echo "❌ Script não encontrado!"
    echo "Certifique-se de que setup_wsl_android.sh está na pasta do projeto"
fi
'@

$setupPath = "C:\Users\Rafael\OneDrive\Projetos em Python\CashControl\run_setup_wsl.sh"
$setupContent | Out-File -FilePath $setupPath -Encoding UTF8
Write-Host "📜 Script de inicialização criado: run_setup_wsl.sh" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 INSTALAÇÃO WSL2 CONCLUÍDA!" -ForegroundColor Green
Write-Host "============================" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️ REINICIALIZAÇÃO NECESSÁRIA" -ForegroundColor Red
Write-Host "O Windows precisa ser reiniciado para completar a instalação." -ForegroundColor Yellow
Write-Host ""
Write-Host "📋 APÓS REINICIAR:" -ForegroundColor Cyan
Write-Host "1. Ubuntu será iniciado automaticamente" -ForegroundColor White
Write-Host "2. Crie um usuário e senha quando solicitado" -ForegroundColor White
Write-Host "3. No Ubuntu, execute:" -ForegroundColor White
Write-Host "   cd '/mnt/c/Users/Rafael/OneDrive/Projetos em Python/CashControl'" -ForegroundColor White
Write-Host "   ./run_setup_wsl.sh" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Isso configurará automaticamente o ambiente Android!" -ForegroundColor Green
Write-Host ""

$restart = Read-Host "Deseja reiniciar agora? (s/N)"
if ($restart -eq "s" -or $restart -eq "S") {
    Write-Host "🔄 Reiniciando sistema..." -ForegroundColor Yellow
    Restart-Computer -Force
}
else {
    Write-Host "👍 Lembre-se de reiniciar manualmente!" -ForegroundColor Yellow
    Write-Host "Após reiniciar, abra o Ubuntu e execute os comandos acima." -ForegroundColor White
}

Read-Host "Pressione Enter para finalizar"
