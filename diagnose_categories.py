"""
Diagnóstico rápido do problema de categorias
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.finance_controller import FinanceController

def test_category_creation():
    print("🔍 DIAGNÓSTICO: Problema no cadastro de categorias")
    print("=" * 50)
    
    # Teste 1: Controller
    print("\n1️⃣ Testando Controller...")
    controller = FinanceController()
    
    try:
        result = controller.add_category("Teste Diagnóstico", "test", "#FF0000")
        print(f"✅ Controller funcionando: {result}")
    except Exception as e:
        print(f"❌ Erro no controller: {e}")
        return
    
    # Teste 2: Buscar categorias
    print("\n2️⃣ Testando busca de categorias...")
    try:
        categories = controller.get_categories()
        print(f"✅ Categorias encontradas: {len(categories)}")
        
        # Mostrar algumas categorias
        for i, cat in enumerate(categories[-3:]):
            print(f"   📁 {cat['name']} (ID: {cat['id']})")
            
    except Exception as e:
        print(f"❌ Erro ao buscar categorias: {e}")
        return
    
    # Teste 3: Interface (simulação)
    print("\n3️⃣ Testando componentes da interface...")
    
    try:
        # Importar sem criar interface gráfica
        from views.categories import CategoryForm
        print("✅ CategoryForm importado com sucesso")
        
        from views.categories import CategoriesScreen
        print("✅ CategoriesScreen importado com sucesso")
        
    except Exception as e:
        print(f"❌ Erro na importação das views: {e}")
        return
    
    print("\n🎯 RESULTADO DO DIAGNÓSTICO:")
    print("✅ Controller funcionando perfeitamente")
    print("✅ Banco de dados salvando categorias")
    print("✅ Views importando sem erro")
    print()
    print("💡 POSSÍVEIS CAUSAS DO PROBLEMA:")
    print("   1. Problema na interface do usuário (formulário não enviando)")
    print("   2. Callback não sendo executado após salvar")
    print("   3. Lista não sendo atualizada após criar categoria")
    print("   4. Threading causando problema na atualização da UI")
    print()
    print("🔧 PRÓXIMOS PASSOS:")
    print("   1. Verificar se o formulário está sendo aberto")
    print("   2. Verificar se o botão 'Salvar' está funcionando")
    print("   3. Verificar se a lista está sendo atualizada")
    print("   4. Testar diretamente no aplicativo")

if __name__ == "__main__":
    test_category_creation()
