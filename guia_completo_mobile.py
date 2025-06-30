"""
📱 CASHCONTROL NO CELULAR - GUIA COMPLETO
=========================================

Escolha a melhor opção para você:

🟢 FÁCIL   - Kivy Launcher (teste rápido)
🟡 MÉDIO   - Termux (Python no Android) 
🔴 DIFÍCIL - Buildozer (APK profissional)

=========================================
"""

def mostrar_opcoes():
    print("📱 COMO INSTALAR CASHCONTROL NO CELULAR")
    print("=" * 50)
    
    opcoes = {
        "1": {
            "nome": "🟢 KIVY LAUNCHER (Mais Fácil)",
            "tempo": "⏱️ 10 minutos",
            "dificuldade": "⭐ Fácil",
            "descricao": "Teste rápido sem compilar"
        },
        "2": {
            "nome": "🟡 TERMUX (Médio)",
            "tempo": "⏱️ 30 minutos", 
            "dificuldade": "⭐⭐ Médio",
            "descricao": "Python completo no Android"
        },
        "3": {
            "nome": "🔴 BUILDOZER (Profissional)",
            "tempo": "⏱️ 1-2 horas",
            "dificuldade": "⭐⭐⭐ Difícil", 
            "descricao": "APK instalável como app"
        }
    }
    
    for num, info in opcoes.items():
        print(f"\n{num}. {info['nome']}")
        print(f"   {info['tempo']} | {info['dificuldade']}")
        print(f"   {info['descricao']}")
    
    return opcoes

def mostrar_detalhes_opcao(opcao):
    detalhes = {
        "1": {
            "titulo": "🟢 KIVY LAUNCHER - OPÇÃO MAIS FÁCIL",
            "passos": [
                "📱 Instale 'Kivy Launcher' da Play Store",
                "📁 Execute: python preparar_kivy_launcher.py", 
                "📂 Copie pasta 'cashcontrol' para /sdcard/kivy/",
                "🚀 Abra Kivy Launcher e toque em 'cashcontrol'"
            ],
            "pros": [
                "✅ Muito fácil e rápido",
                "✅ Não precisa compilar nada",
                "✅ Funciona em qualquer Android"
            ],
            "contras": [
                "❌ Performance limitada",
                "❌ Alguns recursos podem não funcionar",
                "❌ Interface pode ter problemas"
            ]
        },
        "2": {
            "titulo": "🟡 TERMUX - PYTHON NO ANDROID",
            "passos": [
                "📱 Instale 'Termux' da F-Droid ou Play Store",
                "⌨️ No Termux: pkg install python git",
                "📦 pip install kivy matplotlib",
                "📁 git clone [repositório] ou copie arquivos",
                "🚀 python main.py"
            ],
            "pros": [
                "✅ Python completo no celular",
                "✅ Boa performance",
                "✅ Controle total"
            ],
            "contras": [
                "❌ Interface não otimizada para touch",
                "❌ Requer conhecimento de terminal",
                "❌ Configuração mais complexa"
            ]
        },
        "3": {
            "titulo": "🔴 BUILDOZER - APK PROFISSIONAL",
            "passos": [
                "🐧 Instale WSL (Windows) ou use Linux",
                "📦 sudo apt install dependências...",
                "🔧 pip install buildozer cython", 
                "⚙️ Configure buildozer.spec",
                "📱 Execute: ./compilar_android.sh",
                "📲 Instale o APK gerado no celular"
            ],
            "pros": [
                "✅ App nativo instalável",
                "✅ Melhor performance",
                "✅ Interface otimizada",
                "✅ Distribuível na Play Store"
            ],
            "contras": [
                "❌ Configuração complexa",
                "❌ Requer Linux/WSL",
                "❌ Primeira compilação demora muito",
                "❌ Pode ter erros de dependências"
            ]
        }
    }
    
    if opcao in detalhes:
        info = detalhes[opcao]
        print(f"\n{info['titulo']}")
        print("=" * len(info['titulo']))
        
        print(f"\n📋 PASSOS:")
        for i, passo in enumerate(info['passos'], 1):
            print(f"{i}. {passo}")
        
        print(f"\n✅ VANTAGENS:")
        for pro in info['pros']:
            print(f"  {pro}")
            
        print(f"\n❌ DESVANTAGENS:")
        for contra in info['contras']:
            print(f"  {contra}")

def main():
    print(__doc__)
    
    opcoes = mostrar_opcoes()
    
    print(f"\n📋 ARQUIVOS DISPONÍVEIS:")
    print("• preparar_kivy_launcher.py - Para opção 1")
    print("• compilar_android.sh - Para opção 3") 
    print("• buildozer.spec - Configuração do APK")
    
    while True:
        print(f"\n🤔 Qual opção você escolhe?")
        escolha = input("Digite 1, 2, 3 ou 'q' para sair: ").strip()
        
        if escolha.lower() == 'q':
            print("👋 Até mais!")
            break
        elif escolha in opcoes:
            mostrar_detalhes_opcao(escolha)
            
            if escolha == "1":
                resposta = input(f"\n🚀 Executar preparar_kivy_launcher.py agora? (s/n): ")
                if resposta.lower() in ['s', 'sim', 'y', 'yes']:
                    import subprocess
                    subprocess.run(["python", "preparar_kivy_launcher.py"])
            elif escolha == "3":
                print(f"\n💡 DICA: Execute no Linux/WSL:")
                print("chmod +x compilar_android.sh")
                print("./compilar_android.sh")
        else:
            print("❌ Opção inválida. Digite 1, 2, 3 ou 'q'")

if __name__ == "__main__":
    main()
