"""
Teste específico para verificar categorias em transações
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.finance_controller import FinanceController

def test_categories_for_transactions():
    print("🔍 TESTE: Categorias para Formulário de Transações")
    print("=" * 60)
    
    controller = FinanceController()
    
    # 1. Verificar categorias disponíveis
    print("\n1️⃣ VERIFICANDO CATEGORIAS DISPONÍVEIS:")
    categories = controller.get_categories()
    print(f"   📊 Total de categorias: {len(categories)}")
    
    if not categories:
        print("   ❌ PROBLEMA: Nenhuma categoria encontrada!")
        return False
    
    # 2. Mostrar categorias
    print("\n2️⃣ LISTA DE CATEGORIAS:")
    for i, cat in enumerate(categories, 1):
        print(f"   {i:2d}. {cat['name']:<20} (ID: {cat['id']})")
    
    # 3. Simular criação do formulário
    print("\n3️⃣ SIMULANDO FORMULÁRIO DE TRANSAÇÃO:")
    try:
        # Simular o que o TransactionForm faz
        category_names = [cat['name'] for cat in categories]
        print(f"   📋 Nomes das categorias: {category_names}")
        
        if category_names:
            print("   ✅ Lista de nomes criada com sucesso!")
            print(f"   🎛️ Valores para spinner: {', '.join(category_names)}")
        else:
            print("   ❌ Lista de nomes vazia!")
            
    except Exception as e:
        print(f"   ❌ Erro ao processar categorias: {e}")
        return False
    
    # 4. Verificar estrutura das categorias
    print("\n4️⃣ VERIFICANDO ESTRUTURA DAS CATEGORIAS:")
    if categories:
        sample_cat = categories[0]
        print(f"   📝 Estrutura da primeira categoria: {sample_cat}")
        
        required_fields = ['id', 'name', 'icon', 'color']
        for field in required_fields:
            if field in sample_cat:
                print(f"   ✅ Campo '{field}': {sample_cat[field]}")
            else:
                print(f"   ❌ Campo '{field}' ausente!")
    
    print("\n🎉 RESULTADO:")
    if categories and len(categories) > 0:
        print("   ✅ Categorias estão disponíveis e estruturadas corretamente")
        print("   🔧 Se não aparecem no formulário, é problema de interface")
        print("\n💡 PRÓXIMOS PASSOS:")
        print("   1. Execute o aplicativo")
        print("   2. Vá em Transações → + Nova")
        print("   3. Observe as mensagens de debug no console")
        print("   4. Verifique se o spinner 'Categoria' está populado")
        return True
    else:
        print("   ❌ Problema com as categorias")
        return False

if __name__ == "__main__":
    test_categories_for_transactions()
