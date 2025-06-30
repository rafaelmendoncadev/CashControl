"""
Teste DIRETO do problema de categorias
Execute este arquivo para ver exatamente o que está acontecendo
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_direct_category_save():
    print("🔍 TESTE DIRETO - Cadastro de Categorias")
    print("=" * 60)
    
    from controllers.finance_controller import FinanceController
    
    # Inicializar controller
    controller = FinanceController()
    
    # 1. Ver categorias atuais
    print("\n1️⃣ CATEGORIAS ANTES DO TESTE:")
    categories_before = controller.get_categories()
    print(f"   📊 Total: {len(categories_before)}")
    
    # Mostrar últimas 3 categorias
    for cat in categories_before[-3:]:
        print(f"   📁 {cat['name']} (ID: {cat['id']})")
    
    # 2. Tentar criar nova categoria
    print("\n2️⃣ CRIANDO NOVA CATEGORIA:")
    test_name = "Teste Direto " + str(len(categories_before))
    print(f"   Nome: {test_name}")
    print(f"   Ícone: test")
    print(f"   Cor: #FF0000")
    
    result = controller.add_category(test_name, "test", "#FF0000")
    print(f"   📝 Resultado: {result}")
    
    # 3. Verificar se foi salva
    print("\n3️⃣ VERIFICANDO SE FOI SALVA:")
    categories_after = controller.get_categories()
    print(f"   📊 Total após: {len(categories_after)}")
    
    if len(categories_after) > len(categories_before):
        print("   ✅ Categoria foi salva no banco!")
        new_cat = categories_after[-1]
        print(f"   🆕 Nova categoria: {new_cat['name']} (ID: {new_cat['id']})")
    else:
        print("   ❌ Categoria NÃO foi salva!")
        return False
    
    # 4. Testar busca específica
    print("\n4️⃣ TESTANDO BUSCA DA NOVA CATEGORIA:")
    found = False
    for cat in categories_after:
        if cat['name'] == test_name:
            print(f"   ✅ Encontrada: {cat}")
            found = True
            break
    
    if not found:
        print("   ❌ Categoria não encontrada na lista!")
        return False
    
    print("\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
    print("   ✅ Controller funcionando perfeitamente")
    print("   ✅ Banco de dados salvando corretamente")
    print("   ✅ Busca retornando dados atualizados")
    print()
    print("💡 SE O PROBLEMA PERSISTE NA INTERFACE, É PROBLEMA DE UI!")
    print("   - Verifique se o formulário está chamando o controller")
    print("   - Verifique se a lista está sendo atualizada após salvar")
    print("   - Verifique as mensagens de debug no console do app")
    
    return True

if __name__ == "__main__":
    test_direct_category_save()
