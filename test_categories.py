"""
Script de teste para verificar a funcionalidade de categorias
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.finance_controller import FinanceController

def test_categories():
    """Testa as funcionalidades de categoria"""
    print("🧪 Testando funcionalidades de categorias...")
    
    # Inicializar controller
    controller = FinanceController()
    
    # Testar busca de categorias
    print("\n📋 Categorias existentes:")
    categories = controller.get_categories()
    for cat in categories:
        print(f"  - ID: {cat['id']}, Nome: {cat['name']}, Ícone: {cat['icon']}, Cor: {cat['color']}")
    
    # Testar criação de nova categoria
    print("\n➕ Criando nova categoria de teste...")
    try:
        result = controller.add_category(
            name="Teste Integração",
            icon="test",
            color="#FF5722"
        )
        print(f"✅ Categoria criada com sucesso! ID: {result}")
        
        # Verificar se foi criada
        categories_after = controller.get_categories()
        print(f"📊 Total de categorias após criação: {len(categories_after)}")
        
        # Mostrar a nova categoria
        new_cat = [cat for cat in categories_after if cat['name'] == "Teste Integração"]
        if new_cat:
            cat = new_cat[0]
            print(f"🆕 Nova categoria: ID={cat['id']}, Nome={cat['name']}, Ícone={cat['icon']}, Cor={cat['color']}")
        
    except Exception as e:
        print(f"❌ Erro ao criar categoria: {e}")
    
    print("\n✨ Teste de categorias concluído!")

if __name__ == "__main__":
    test_categories()
