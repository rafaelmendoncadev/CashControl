"""
Script de instalação do CashControl
"""

import os
import sys
import subprocess
import venv

def create_virtual_environment():
    """Cria ambiente virtual"""
    print("Criando ambiente virtual...")
    
    venv_path = os.path.join(os.getcwd(), ".venv")
    
    if os.path.exists(venv_path):
        print("Ambiente virtual já existe.")
        return venv_path
    
    try:
        venv.create(venv_path, with_pip=True)
        print("✓ Ambiente virtual criado com sucesso")
        return venv_path
    except Exception as e:
        print(f"✗ Erro ao criar ambiente virtual: {e}")
        return None

def install_dependencies(venv_path):
    """Instala dependências"""
    print("Instalando dependências...")
    
    if os.name == 'nt':  # Windows
        pip_path = os.path.join(venv_path, "Scripts", "pip.exe")
        python_path = os.path.join(venv_path, "Scripts", "python.exe")
    else:  # Linux/Mac
        pip_path = os.path.join(venv_path, "bin", "pip")
        python_path = os.path.join(venv_path, "bin", "python")
    
    # Lista de dependências
    dependencies = [
        "kivy>=2.0.0",
        "matplotlib>=3.5.0",
        "kivymd>=1.0.0",
        "pillow>=8.0.0"
    ]
    
    try:
        # Atualizar pip
        subprocess.check_call([python_path, "-m", "pip", "install", "--upgrade", "pip"])
        print("✓ Pip atualizado")
        
        # Instalar dependências
        for dep in dependencies:
            print(f"Instalando {dep}...")
            subprocess.check_call([pip_path, "install", dep])
            print(f"✓ {dep} instalado")
        
        print("✓ Todas as dependências foram instaladas")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Erro ao instalar dependências: {e}")
        return False

def create_desktop_shortcut():
    """Cria atalho na área de trabalho (Windows)"""
    if os.name != 'nt':
        return
    
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        path = os.path.join(desktop, "CashControl.lnk")
        target = os.path.join(os.getcwd(), "run_app.bat")
        wDir = os.getcwd()
        icon = target
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = wDir
        shortcut.IconLocation = icon
        shortcut.save()
        
        print("✓ Atalho criado na área de trabalho")
        
    except ImportError:
        print("ℹ Módulos para criar atalho não encontrados (opcional)")
    except Exception as e:
        print(f"⚠ Erro ao criar atalho: {e}")

def setup_database():
    """Configura o banco de dados"""
    print("Configurando banco de dados...")
    
    try:
        from models.database import Database
        
        # Criar instância do banco (isso criará as tabelas)
        db = Database()
        print("✓ Banco de dados configurado com sucesso")
        return True
        
    except Exception as e:
        print(f"✗ Erro ao configurar banco de dados: {e}")
        return False

def main():
    """Função principal de instalação"""
    print("="*50)
    print("CASHCONTROL - INSTALAÇÃO")
    print("="*50)
    
    # Verificar Python
    if sys.version_info < (3, 7):
        print("✗ Python 3.7 ou superior é necessário")
        return
    
    print(f"✓ Python {sys.version} detectado")
    
    # Criar ambiente virtual
    venv_path = create_virtual_environment()
    if not venv_path:
        return
    
    # Instalar dependências
    if not install_dependencies(venv_path):
        return
    
    # Configurar banco de dados
    if not setup_database():
        return
    
    # Criar atalho (Windows)
    create_desktop_shortcut()
    
    print("\n" + "="*50)
    print("INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
    print("="*50)
    print("\nPara executar o CashControl:")
    print("1. Execute 'run_app.bat' (Windows)")
    print("2. Ou execute 'python main.py' no ambiente virtual")
    print("\nPara criar dados de exemplo:")
    print("Execute 'python setup_util.py' no ambiente virtual")
    print("="*50)

if __name__ == "__main__":
    main()
