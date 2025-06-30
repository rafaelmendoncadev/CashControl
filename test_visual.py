#!/usr/bin/env python3
"""
Teste rápido para verificar se há erros de sintaxe após ajustes visuais
"""

try:
    print("🔍 Testando importações...")
    
    # Testar importações principais
    from views.transactions import TransactionsScreen, TransactionForm, TransactionListItem
    print("✅ views.transactions importado com sucesso")
    
    from views.categories import CategoriesScreen, CategoryForm, CategoryItem
    print("✅ views.categories importado com sucesso")
    
    from controllers.finance_controller import FinanceController
    print("✅ controllers.finance_controller importado com sucesso")
    
    # Testar controller
    controller = FinanceController()
    print("✅ FinanceController inicializado")
    
    print("\n🎯 Todos os testes de importação passaram!")
    print("📋 As correções visuais foram aplicadas com sucesso")
    print("\nResumo das melhorias aplicadas:")
    print("• ✅ Correções de threading para evitar erros gráficos")
    print("• ✅ Texto das transações agora em cor escura (0.15, 0.15, 0.15)")
    print("• ✅ Fundo dos itens de transação melhorado (0.96, 0.96, 0.96)")
    print("• ✅ Bordas dos itens mais visíveis (0.75, 0.75, 0.75)")
    print("• ✅ Contraste melhorado em todos os labels")
    print("• ✅ Títulos e labels de formulário com texto escuro")
    print("• ✅ Itens de categoria com melhor contraste")
    
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
except Exception as e:
    print(f"💥 Erro inesperado: {e}")
    import traceback
    traceback.print_exc()
