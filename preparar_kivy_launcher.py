"""
🚀 GUIA RÁPIDO: CashControl no Celular via Kivy Launcher
========================================================

Esta é a maneira MAIS FÁCIL de testar o CashControl no celular!

📱 PASSO A PASSO:

1. INSTALAR KIVY LAUNCHER
   • Abra a Play Store no seu celular
   • Procure por "Kivy Launcher"
   • Instale o app (desenvolvido por Kivy team)
   
   Link direto: https://play.google.com/store/apps/details?id=org.kivy.pygame

2. PREPARAR ARQUIVOS NO PC
   • Crie uma pasta chamada "cashcontrol" 
   • Copie TODOS os arquivos .py do projeto
   • Copie as pastas: models/, views/, controllers/
   • Copie o arquivo: config.ini

3. TRANSFERIR PARA O CELULAR
   • Conecte o celular no PC via cabo USB
   • Copie a pasta "cashcontrol" para:
     /sdcard/kivy/ ou /storage/emulated/0/kivy/
   
   Estrutura final no celular:
   /sdcard/kivy/cashcontrol/
   ├── main.py
   ├── config.py
   ├── config.ini
   ├── models/
   │   ├── database.py
   │   └── transaction.py
   ├── views/
   │   ├── dashboard.py
   │   ├── transactions.py
   │   ├── categories.py
   │   └── reports.py
   └── controllers/
       └── finance_controller.py

4. EXECUTAR NO CELULAR
   • Abra o Kivy Launcher
   • Toque em "cashcontrol"
   • O app será carregado!

⚠️ LIMITAÇÕES DO KIVY LAUNCHER:
• Performance pode ser menor
• Alguns recursos podem não funcionar
• É apenas para testes
• Interface pode ter pequenos problemas

✅ VANTAGENS:
• Não precisa compilar APK
• Rápido para testar
• Não precisa configurar ambiente de desenvolvimento
• Funciona em qualquer Android

🔧 SOLUÇÃO DE PROBLEMAS:
• Se não funcionar, verifique se todos os arquivos foram copiados
• Certifique-se que a pasta está em /sdcard/kivy/
• Reinicie o Kivy Launcher
• Verifique se o celular tem espaço suficiente

"""

import os
import shutil
from pathlib import Path

def preparar_para_kivy_launcher():
    """Prepara os arquivos para uso com Kivy Launcher"""
    
    print("📁 Preparando arquivos para Kivy Launcher...")
    
    # Criar pasta de destino
    dest_folder = Path("cashcontrol_mobile")
    if dest_folder.exists():
        shutil.rmtree(dest_folder)
    dest_folder.mkdir()
    
    # Arquivos principais para copiar
    arquivos_principais = [
        "main.py",
        "config.py", 
        "config.ini"
    ]
    
    # Pastas para copiar
    pastas = [
        "models",
        "views", 
        "controllers"
    ]
    
    print("📋 Copiando arquivos...")
    
    # Copiar arquivos principais
    for arquivo in arquivos_principais:
        if os.path.exists(arquivo):
            shutil.copy2(arquivo, dest_folder)
            print(f"✅ {arquivo}")
        else:
            print(f"⚠️ {arquivo} não encontrado")
    
    # Copiar pastas
    for pasta in pastas:
        if os.path.exists(pasta):
            shutil.copytree(pasta, dest_folder / pasta)
            print(f"✅ {pasta}/")
        else:
            print(f"⚠️ {pasta}/ não encontrada")
    
    # Criar arquivo de instruções
    with open(dest_folder / "LEIA-ME.txt", "w", encoding="utf-8") as f:
        f.write("""
INSTRUÇÕES PARA INSTALAR NO CELULAR:

1. Instale o Kivy Launcher da Play Store
2. Copie esta pasta 'cashcontrol_mobile' para:
   /sdcard/kivy/cashcontrol/
3. Abra o Kivy Launcher no celular
4. Toque em 'cashcontrol'

ATENÇÃO: Renomeie a pasta de 'cashcontrol_mobile' para 'cashcontrol'
""")
    
    print(f"""
📦 Pasta preparada: {dest_folder.absolute()}

📲 PRÓXIMOS PASSOS:
1. Renomeie a pasta de 'cashcontrol_mobile' para 'cashcontrol'
2. Copie para /sdcard/kivy/ do seu celular
3. Abra o Kivy Launcher
4. Divirta-se!
""")

if __name__ == "__main__":
    print(__doc__)
    
    resposta = input("\n🤔 Deseja preparar os arquivos agora? (s/n): ")
    if resposta.lower() in ['s', 'sim', 'y', 'yes']:
        preparar_para_kivy_launcher()
    else:
        print("👍 Ok! Execute quando estiver pronto.")
