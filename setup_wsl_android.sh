#!/bin/bash
# 🐧 CashControl - Setup WSL2 para Android
# Script automatizado para configurar ambiente de desenvolvimento

echo "🚀 CashControl - Configuração WSL2 para Android"
echo "================================================"
echo ""

# Verificar se está no WSL
if [[ ! $(uname -r) =~ WSL ]]; then
    echo "❌ Este script deve ser executado no WSL2!"
    echo "Instale o WSL2 primeiro com: wsl --install Ubuntu-20.04"
    exit 1
fi

echo "✅ WSL2 detectado! Iniciando configuração..."
echo ""

# Função para verificar se comando foi bem-sucedido
check_success() {
    if [ $? -eq 0 ]; then
        echo "✅ $1"
    else
        echo "❌ Erro em: $1"
        exit 1
    fi
}

# 1. Atualizar sistema
echo "📦 Atualizando sistema..."
sudo apt update -y > /dev/null 2>&1
check_success "Sistema atualizado"

# 2. Instalar dependências essenciais
echo "🔧 Instalando dependências..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    zip \
    unzip \
    curl \
    wget \
    openjdk-11-jdk \
    build-essential \
    ccache \
    libncurses5:i386 \
    libstdc++6:i386 \
    libgtk2.0-0:i386 \
    libpangox-1.0-0:i386 \
    libpangoxft-1.0-0:i386 \
    libidn11:i386 \
    zlib1g-dev \
    zlib1g:i386 > /dev/null 2>&1

check_success "Dependências instaladas"

# 3. Verificar Java
echo "☕ Verificando Java..."
java -version > /dev/null 2>&1
check_success "Java configurado"

# 4. Configurar Android SDK
echo "📱 Configurando Android SDK..."
mkdir -p ~/android-sdk
cd ~/android-sdk

# Baixar Android Command Line Tools
if [ ! -f "commandlinetools-linux-8512546_latest.zip" ]; then
    echo "📥 Baixando Android Command Line Tools..."
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-8512546_latest.zip
    check_success "Android Command Line Tools baixado"
fi

# Extrair se ainda não foi extraído
if [ ! -d "cmdline-tools" ]; then
    echo "📂 Extraindo Command Line Tools..."
    unzip -q commandlinetools-linux-8512546_latest.zip
    check_success "Command Line Tools extraído"
fi

# 5. Configurar variáveis de ambiente
echo "🌍 Configurando variáveis de ambiente..."
if ! grep -q "ANDROID_HOME" ~/.bashrc; then
    echo 'export ANDROID_HOME=~/android-sdk' >> ~/.bashrc
    echo 'export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin' >> ~/.bashrc
    echo 'export PATH=$PATH:$ANDROID_HOME/platform-tools' >> ~/.bashrc
    echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.bashrc
    check_success "Variáveis de ambiente configuradas"
else
    echo "✅ Variáveis de ambiente já configuradas"
fi

# Aplicar variáveis na sessão atual
export ANDROID_HOME=~/android-sdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin
export PATH=$PATH:$ANDROID_HOME/platform-tools
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# 6. Navegar para o projeto
echo "📁 Configurando projeto CashControl..."
PROJECT_PATH="/mnt/c/Users/Rafael/OneDrive/Projetos em Python/CashControl"

if [ -d "$PROJECT_PATH" ]; then
    cd "$PROJECT_PATH"
    echo "✅ Projeto encontrado: $PROJECT_PATH"
else
    echo "❌ Projeto não encontrado em: $PROJECT_PATH"
    echo "Ajuste o caminho e execute novamente"
    exit 1
fi

# 7. Criar ambiente virtual
echo "🐍 Configurando ambiente Python..."
if [ ! -d ".venv_wsl" ]; then
    python3 -m venv .venv_wsl
    check_success "Ambiente virtual criado"
fi

# Ativar ambiente virtual
source .venv_wsl/bin/activate
check_success "Ambiente virtual ativado"

# 8. Instalar dependências Python
echo "📦 Instalando dependências Python..."
pip install --upgrade pip > /dev/null 2>&1
pip install buildozer kivy kivymd plyer matplotlib > /dev/null 2>&1
check_success "Dependências Python instaladas"

# 9. Verificar buildozer
echo "🔨 Verificando Buildozer..."
buildozer --version > /dev/null 2>&1
check_success "Buildozer funcionando"

# 10. Verificar buildozer.spec
if [ -f "buildozer.spec" ]; then
    echo "✅ buildozer.spec encontrado"
else
    echo "📝 Criando buildozer.spec..."
    buildozer init > /dev/null 2>&1
    check_success "buildozer.spec criado"
fi

echo ""
echo "🎉 CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!"
echo "======================================"
echo ""
echo "📋 PRÓXIMOS PASSOS:"
echo ""
echo "1. Para compilar o APK:"
echo "   cd '$PROJECT_PATH'"
echo "   source .venv_wsl/bin/activate"
echo "   buildozer android debug"
echo ""
echo "2. O APK será gerado em: bin/CashControl-*-debug.apk"
echo ""
echo "3. Para compilar rapidamente no futuro:"
echo "   ./compilar_wsl.sh"
echo ""
echo "⏱️  PRIMEIRA COMPILAÇÃO: 30-60 minutos"
echo "⚡ COMPILAÇÕES FUTURAS: 5-10 minutos"
echo ""
echo "🚀 Ambiente pronto para desenvolvimento Android!"

# Criar script de compilação rápida
cat > compilar_wsl.sh << 'EOF'
#!/bin/bash
# Script de compilação rápida para WSL2

echo "🔨 Compilando CashControl para Android..."
cd "/mnt/c/Users/Rafael/OneDrive/Projetos em Python/CashControl"
source .venv_wsl/bin/activate

echo "🚀 Iniciando buildozer..."
buildozer android debug

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ COMPILAÇÃO CONCLUÍDA!"
    echo "📱 APK gerado em: bin/"
    ls -la bin/*.apk 2>/dev/null || echo "❌ APK não encontrado"
    echo ""
    echo "📋 Para instalar no celular:"
    echo "1. Copie o APK para o celular"
    echo "2. Ative 'Fontes desconhecidas' nas configurações"
    echo "3. Instale o APK"
else
    echo "❌ Erro na compilação!"
    echo "Verifique os logs acima"
fi
EOF

chmod +x compilar_wsl.sh
echo "📜 Script de compilação criado: ./compilar_wsl.sh"
