#!/bin/bash
# Script para compilar CashControl para Android
# Uso: ./compilar_android.sh

echo "🔧 CashControl - Compilação para Android"
echo "========================================"

# Verificar se está no WSL/Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ Este script deve ser executado no Linux ou WSL"
    echo "💡 Para instalar WSL no Windows:"
    echo "   1. Abra PowerShell como Administrador"
    echo "   2. Execute: wsl --install"
    echo "   3. Reinicie o PC"
    exit 1
fi

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado"
    echo "📦 Instalando Python3..."
    sudo apt update
    sudo apt install -y python3 python3-pip
fi

echo "📦 Instalando dependências do sistema..."
sudo apt update
sudo apt install -y \
    git \
    zip \
    unzip \
    openjdk-8-jdk \
    python3-pip \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev \
    build-essential \
    libltdl-dev

echo "🔧 Instalando Buildozer e Cython..."
pip3 install --user buildozer cython

# Verificar se buildozer está no PATH
if ! command -v buildozer &> /dev/null; then
    echo "⚠️ Adicionando buildozer ao PATH..."
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    export PATH="$HOME/.local/bin:$PATH"
fi

# Verificar se buildozer.spec existe
if [ ! -f "buildozer.spec" ]; then
    echo "❌ Arquivo buildozer.spec não encontrado"
    echo "💡 Execute este script na pasta do projeto CashControl"
    exit 1
fi

echo "🧹 Limpando builds anteriores..."
buildozer android clean

echo "📱 Iniciando compilação do APK..."
echo "⏱️ Este processo pode demorar 30-60 minutos na primeira vez..."

# Compilar APK
if buildozer android debug; then
    echo ""
    echo "✅ APK criado com sucesso!"
    echo ""
    echo "📦 Localização do APK:"
    ls -la bin/*.apk 2>/dev/null || echo "❌ APK não encontrado"
    echo ""
    echo "📲 PRÓXIMOS PASSOS:"
    echo "1. Copie o arquivo .apk para seu celular"
    echo "2. No celular, vá em Configurações > Segurança"
    echo "3. Habilite 'Fontes desconhecidas' ou 'Instalar apps desconhecidos'"
    echo "4. Abra o arquivo .apk no celular para instalar"
    echo ""
    echo "🎉 CashControl estará pronto para usar!"
else
    echo ""
    echo "❌ Erro na compilação"
    echo ""
    echo "🔍 SOLUÇÕES COMUNS:"
    echo "• Verifique se todas as dependências estão instaladas"
    echo "• Execute: buildozer android clean"
    echo "• Tente novamente"
    echo "• Verifique logs em .buildozer/android/platform/build-*/"
fi
