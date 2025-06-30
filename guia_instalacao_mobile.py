"""
GUIA COMPLETO: Como Instalar CashControl no Celular
====================================================

🔧 OPÇÕES DISPONÍVEIS:

1. 📱 BUILDOZER (Recomendado) - Cria APK Android
2. 🌐 KIVY LAUNCHER - Teste rápido no Android
3. 💻 PYTHON MOBILE - Para dispositivos com Python
4. ☁️ WEB VERSION - Versão online (futuro)

====================================================
"""

print(__doc__)

print("📱 OPÇÃO 1: BUILDOZER (APK Android) - RECOMENDADO")
print("=" * 60)
print("""
O Buildozer é a ferramenta oficial do Kivy para criar APKs Android.

🔧 REQUISITOS:
• Linux ou WSL (Windows Subsystem for Linux)
• Python 3.8+
• Java JDK
• Android SDK
• Cython

📋 PASSOS:

1. Instalar WSL (se Windows):
   • Abra PowerShell como Admin
   • Execute: wsl --install
   • Reinicie o PC

2. No Linux/WSL, instalar dependências:
   sudo apt update
   sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

3. Instalar Buildozer:
   pip3 install --user buildozer
   pip3 install --user cython

4. Configurar projeto:
   buildozer init

5. Compilar APK:
   buildozer android debug

⏱️ TEMPO: 1-2 horas na primeira vez (downloads)
📦 RESULTADO: bin/CashControl-0.1-armeabi-v7a-debug.apk
""")

print("\n📱 OPÇÃO 2: KIVY LAUNCHER - TESTE RÁPIDO")
print("=" * 60)
print("""
Para testar rapidamente no Android sem compilar APK.

📋 PASSOS:

1. Baixar Kivy Launcher na Play Store:
   https://play.google.com/store/apps/details?id=org.kivy.pygame

2. Preparar pasta do projeto:
   • Criar pasta 'cashcontrol' no celular
   • Copiar todos os arquivos .py
   • Renomear main.py para main.py

3. Abrir no Kivy Launcher

⚠️ LIMITAÇÕES:
• Não funciona com todas as bibliotecas
• Interface pode ter problemas
• Apenas para testes básicos
""")

print("\n💻 OPÇÃO 3: TERMUX (Android) - AVANÇADO")
print("=" * 60)
print("""
Instalar Python diretamente no Android via Termux.

📋 PASSOS:

1. Instalar Termux da F-Droid ou Play Store

2. No Termux:
   pkg update && pkg upgrade
   pkg install python git
   pip install kivy
   pip install matplotlib sqlite3

3. Clonar projeto:
   git clone [seu_repositorio]
   cd cashcontrol
   python main.py

⚠️ NOTA: Interface pode não ser otimizada para touch
""")

print("\n🔧 CRIANDO APK COM BUILDOZER - DETALHADO")
print("=" * 60)

buildozer_spec = """
# Arquivo buildozer.spec (será criado automaticamente)

[app]
title = CashControl
package.name = cashcontrol
package.domain = com.financas.cashcontrol
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,db
version = 1.0
requirements = python3,kivy,sqlite3,matplotlib
icon.filename = assets/icon.png
presplash.filename = assets/presplash.png
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2

[android]
api = 31
minapi = 21
ndk = 23b
accept_sdk_license = True
"""

print("📝 ARQUIVO DE CONFIGURAÇÃO:")
print(buildozer_spec)

print("\n🚀 SCRIPT DE AUTOMATIZAÇÃO")
print("=" * 60)

script_content = '''#!/bin/bash
# Script para compilar CashControl para Android

echo "🔧 Iniciando compilação do CashControl para Android..."

# Verificar se está no WSL/Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ Este script deve ser executado no Linux ou WSL"
    exit 1
fi

# Instalar dependências
echo "📦 Instalando dependências..."
sudo apt update
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Instalar Buildozer
echo "🔧 Instalando Buildozer..."
pip3 install --user buildozer cython

# Verificar se buildozer.spec existe
if [ ! -f "buildozer.spec" ]; then
    echo "📝 Criando configuração do Buildozer..."
    buildozer init
fi

# Compilar APK
echo "📱 Compilando APK..."
buildozer android debug

if [ $? -eq 0 ]; then
    echo "✅ APK criado com sucesso!"
    echo "📦 Localização: bin/cashcontrol-1.0-armeabi-v7a-debug.apk"
    echo "📲 Transfira este arquivo para seu celular e instale"
else
    echo "❌ Erro na compilação"
fi
'''

print("💾 SALVANDO SCRIPTS...")
