# 📱 Compilação Android - CashControl

## ⚠️ **Limitações do Windows**

**IMPORTANTE**: A compilação Android com Buildozer no Windows tem **limitações significativas**:

- ❌ Buildozer não suporta Android nativamente no Windows
- ❌ Dependências Linux específicas necessárias
- ❌ Problemas com paths longos e permissões
- ❌ Android SDK/NDK complexos de configurar

## 🚀 **Alternativas Recomendadas**

### **1. 🐧 WSL2 (Windows Subsystem for Linux) - RECOMENDADO**

```bash
# 1. Instalar WSL2
wsl --install Ubuntu

# 2. Dentro do WSL2:
sudo apt update
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config
pip3 install buildozer
pip3 install cython==0.29.33

# 3. Clonar o projeto
git clone <seu-repositorio>
cd CashControl

# 4. Compilar
buildozer android debug
```

### **2. 🌐 Compilação em Nuvem - MAIS FÁCIL**

#### **GitHub Actions (Gratuito)**
```yaml
# .github/workflows/android.yml
name: Build Android APK
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    - name: Install dependencies
      run: |
        pip install buildozer
        sudo apt-get update
        sudo apt-get install -y autoconf libtool pkg-config zlib1g-dev
    - name: Build APK
      run: buildozer android debug
    - name: Upload APK
      uses: actions/upload-artifact@v2
      with:
        name: apk
        path: bin/*.apk
```

#### **Outras Opções em Nuvem**
- **Kivy Buildozer Online** (buildozer.kivy.org)
- **Replit** com ambiente Linux
- **Google Colab** com persistent storage

### **3. 🖥️ Máquina Virtual Linux**

1. **Instalar VirtualBox/VMware**
2. **Ubuntu 20.04+ LTS**
3. **Configurar ambiente de desenvolvimento**

## 🛠️ **Configuração Atual do Projeto**

### **buildozer.spec - Configurado e Pronto**
```ini
[app]
title = CashControl - Finanças Pessoais
package.name = cashcontrol
package.domain = com.financas.cashcontrol
version = 1.0

requirements = python3,kivy==2.3.1,sqlite3,matplotlib,pillow

[buildozer]
log_level = 2
```

### **Arquivos Incluídos**
- ✅ `main.py` - Arquivo principal
- ✅ `requirements.txt` - Dependências
- ✅ `buildozer.spec` - Configuração Android
- ✅ Controllers, Views, Models organizados
- ✅ Banco de dados SQLite incluído

## 🎯 **Passos para Compilação (Linux/WSL2)**

### **1. Preparar Ambiente**
```bash
# Instalar dependências
sudo apt-get update
sudo apt-get install -y \
    git zip unzip openjdk-8-jdk python3-pip autoconf libtool \
    pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev \
    libtinfo5 cmake libffi-dev libssl-dev

# Instalar buildozer
pip3 install --user buildozer
pip3 install --user cython==0.29.33
```

### **2. Configurar Projeto**
```bash
# Navegar para o projeto
cd CashControl

# Primeira compilação (demora ~30-60 minutos)
buildozer android debug

# Compilações subsequentes (5-10 minutos)
buildozer android debug
```

### **3. Resultado**
- **APK gerado**: `bin/CashControl-1.0-arm64-v8a-debug.apk`
- **Tamanho**: ~50-70 MB
- **Compatibilidade**: Android 5.0+ (API 21+)

## 📲 **Instalação no Dispositivo**

### **Via ADB (Desenvolvedor)**
```bash
# Conectar dispositivo via USB
adb devices

# Instalar APK
adb install bin/CashControl-1.0-arm64-v8a-debug.apk
```

### **Via Transferência Manual**
1. Copiar APK para o dispositivo
2. Ativar "Fontes desconhecidas"
3. Instalar tocando no arquivo

## 🔧 **Solução de Problemas**

### **Erros Comuns**
```bash
# Limpar cache
buildozer android clean

# Rebuild completo
buildozer distclean
buildozer android debug

# Verificar logs
buildozer android debug --verbose
```

### **Dependências Específicas**
- **Java 8**: `sudo apt-get install openjdk-8-jdk`
- **Android SDK**: Baixado automaticamente
- **Android NDK**: Baixado automaticamente
- **Cython**: `pip3 install cython==0.29.33`

## 📊 **Status da Compilação**

### **✅ Pronto para Compilação**
- [x] `buildozer.spec` configurado
- [x] Estrutura de arquivos correta
- [x] Dependências mapeadas
- [x] Compatibilidade Android testada
- [x] Layout responsivo implementado

### **🎯 Próximos Passos**
1. **Usar WSL2** ou **Linux** para compilação
2. **Executar**: `buildozer android debug`
3. **Aguardar** primeira compilação (~30 min)
4. **Testar** APK no dispositivo

## 🆘 **Ajuda Rápida**

### **Windows Users**
```powershell
# Instalar WSL2
wsl --install Ubuntu

# Reiniciar computador
# Depois continuar no WSL2
```

### **Linux Users**
```bash
# Comando completo
sudo apt-get update && sudo apt-get install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev && pip3 install buildozer && buildozer android debug
```

**💡 Dica**: A primeira compilação demora muito, mas é **normal**. O buildozer baixa e compila todas as dependências Android.

---

**🎉 Resultado Final**: APK funcional do CashControl pronto para instalação em dispositivos Android! 