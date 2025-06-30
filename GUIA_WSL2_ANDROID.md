# 🐧 CashControl - Configuração WSL2 para APK Android

## 📋 PASSO A PASSO COMPLETO

### 1. INSTALAR WSL2 (Execute como Administrador no PowerShell)

```powershell
# Instalar WSL2 com Ubuntu
wsl --install Ubuntu-20.04

# Se já tiver WSL, apenas instalar Ubuntu
wsl --install -d Ubuntu-20.04

# Verificar versão do WSL (deve ser 2)
wsl --list --verbose
```

**⚠️ IMPORTANTE:** Após a instalação, o Windows vai REINICIAR automaticamente.

### 2. CONFIGURAR UBUNTU (Primeira execução)

Quando o Ubuntu abrir pela primeira vez:
1. Criar um usuário (ex: rafael)
2. Definir uma senha
3. Aguardar a instalação finalizar

### 3. PREPARAR AMBIENTE DE DESENVOLVIMENTO

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependências essenciais
sudo apt install -y python3 python3-pip python3-venv git zip unzip curl wget

# Instalar Java Development Kit (necessário para Android)
sudo apt install -y openjdk-11-jdk

# Verificar Java
java -version
```

### 4. CONFIGURAR ANDROID SDK

```bash
# Criar diretório para Android SDK
mkdir -p ~/android-sdk
cd ~/android-sdk

# Baixar Android Command Line Tools
wget https://dl.google.com/android/repository/commandlinetools-linux-8512546_latest.zip

# Extrair
unzip commandlinetools-linux-8512546_latest.zip

# Configurar variáveis de ambiente
echo 'export ANDROID_HOME=~/android-sdk' >> ~/.bashrc
echo 'export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin' >> ~/.bashrc
echo 'export PATH=$PATH:$ANDROID_HOME/platform-tools' >> ~/.bashrc
echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.bashrc

# Recarregar configurações
source ~/.bashrc
```

### 5. PREPARAR PROJETO CASHCONTROL

```bash
# Navegar para o projeto (ajuste o caminho conforme necessário)
cd "/mnt/c/Users/Rafael/OneDrive/Projetos em Python/CashControl"

# Criar ambiente virtual Linux
python3 -m venv .venv_wsl
source .venv_wsl/bin/activate

# Instalar dependências
pip install --upgrade pip
pip install buildozer kivy kivymd plyer matplotlib

# Verificar buildozer
buildozer --version
```

### 6. CONFIGURAR BUILDOZER PARA LINUX

```bash
# Inicializar buildozer (se necessário)
buildozer init

# Instalar dependências do sistema para buildozer
sudo apt install -y build-essential ccache git libncurses5:i386 libstdc++6:i386 libgtk2.0-0:i386 libpangox-1.0-0:i386 libpangoxft-1.0-0:i386 libidn11:i386 python2.7 python2.7-dev openjdk-8-jdk unzip zlib1g-dev zlib1g:i386
```

### 7. COMPILAR APK

```bash
# Primeira compilação (demora bastante - 30-60 minutos)
buildozer android debug

# Aguardar conclusão...
# O APK será gerado em: bin/CashControl-*-debug.apk
```

### 8. TRANSFERIR APK PARA WINDOWS

```bash
# Copiar APK para área de trabalho do Windows
cp bin/*.apk /mnt/c/Users/Rafael/Desktop/

# Ou copiar para a pasta do projeto
cp bin/*.apk ./CashControl-mobile.apk
```

---

## 🔧 SCRIPT AUTOMATIZADO

Criei um script que faz tudo isso automaticamente:

```bash
#!/bin/bash
# setup_wsl_android.sh - Configuração automática

echo "🐧 Configurando WSL2 para desenvolvimento Android..."

# Atualizar sistema
sudo apt update -y

# Instalar dependências
sudo apt install -y python3 python3-pip python3-venv git zip unzip curl wget openjdk-11-jdk build-essential ccache libncurses5:i386 libstdc++6:i386

# Configurar Android SDK
mkdir -p ~/android-sdk
cd ~/android-sdk
wget -q https://dl.google.com/android/repository/commandlinetools-linux-8512546_latest.zip
unzip -q commandlinetools-linux-8512546_latest.zip

# Configurar variáveis
echo 'export ANDROID_HOME=~/android-sdk' >> ~/.bashrc
echo 'export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin' >> ~/.bashrc
echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.bashrc
source ~/.bashrc

echo "✅ Configuração concluída!"
echo "Execute: cd /mnt/c/Users/Rafael/OneDrive/Projetos\ em\ Python/CashControl"
echo "Depois: python3 -m venv .venv_wsl && source .venv_wsl/bin/activate"
echo "Por fim: pip install buildozer kivy && buildozer android debug"
```

---

## 📱 APÓS A COMPILAÇÃO

### Instalar no Celular:
1. **Ativar desenvolvedor:**
   - Configurações → Sobre o telefone
   - Toque 7x em "Número da versão"

2. **Ativar depuração USB:**
   - Configurações → Opções do desenvolvedor
   - Ativar "Depuração USB"
   - Ativar "Instalar apps desconhecidas"

3. **Instalar APK:**
   - Transfira o APK para o celular
   - Ou use: `adb install CashControl-debug.apk`

---

## 🚨 PROBLEMAS COMUNS E SOLUÇÕES

### WSL2 não instala:
```powershell
# Ativar recursos do Windows
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Reiniciar e tentar novamente
wsl --install Ubuntu-20.04
```

### Buildozer falha:
```bash
# Limpar cache
buildozer android clean

# Tentar novamente
buildozer android debug
```

### Erro de permissões:
```bash
# Corrigir permissões
sudo chown -R $USER:$USER ~/android-sdk
chmod +x ~/android-sdk/cmdline-tools/latest/bin/*
```

---

## ⏱️ TEMPO ESTIMADO

- **Instalação WSL2:** 10-15 minutos + reinicialização
- **Configuração ambiente:** 15-20 minutos
- **Primeira compilação:** 30-60 minutos
- **Compilações futuras:** 5-10 minutos

---

## 🎯 PRÓXIMO PASSO

Execute este comando no PowerShell como **Administrador**:

```powershell
wsl --install Ubuntu-20.04
```

Depois me avise quando o Ubuntu estiver funcionando!

---

**✅ Vantagens do WSL2:**
- APK real e instalável
- Performance nativa Linux
- Integração perfeita com Windows
- Ambiente de desenvolvimento completo
- Possibilidade de publicar na Play Store

**Desenvolvido para dar a você o melhor APK possível! 🚀**
