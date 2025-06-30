"""
Script utilitário para configuração e testes do CashControl
"""

import sys
import os
from datetime import datetime, date
import random

# Adicionar pasta do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.finance_controller import FinanceController

def create_sample_data():
    """Cria dados de exemplo para teste"""
    controller = FinanceController()
    
    print("Criando dados de exemplo...")
    
    # Obter categorias existentes
    categories = controller.get_categories()
    if not categories:
        print("Erro: Nenhuma categoria encontrada")
        return
    
    # Dados de exemplo
    sample_transactions = [
        # Receitas
        {'type': 'income', 'amount': 3500.00, 'description': 'Salário', 'category': 'Salário'},
        {'type': 'income', 'amount': 800.00, 'description': 'Freelance Design', 'category': 'Freelance'},
        {'type': 'income', 'amount': 150.00, 'description': 'Venda de item usado', 'category': 'Outros'},
        
        # Despesas
        {'type': 'expense', 'amount': 450.00, 'description': 'Supermercado', 'category': 'Alimentação'},
        {'type': 'expense', 'amount': 120.00, 'description': 'Combustível', 'category': 'Transporte'},
        {'type': 'expense', 'amount': 80.00, 'description': 'Cinema', 'category': 'Lazer'},
        {'type': 'expense', 'amount': 200.00, 'description': 'Consulta médica', 'category': 'Saúde'},
        {'type': 'expense', 'amount': 95.00, 'description': 'Curso online', 'category': 'Educação'},
        {'type': 'expense', 'amount': 350.00, 'description': 'Aluguel', 'category': 'Casa'},
        {'type': 'expense', 'amount': 180.00, 'description': 'Roupas', 'category': 'Roupas'},
        {'type': 'expense', 'amount': 75.00, 'description': 'Restaurante', 'category': 'Alimentação'},
        {'type': 'expense', 'amount': 45.00, 'description': 'Uber', 'category': 'Transporte'},
        {'type': 'expense', 'amount': 60.00, 'description': 'Streaming', 'category': 'Lazer'},
    ]
    
    # Criar mapeamento de categorias
    category_map = {cat['name']: cat['id'] for cat in categories}
    
    created_count = 0
    for transaction_data in sample_transactions:
        category_name = transaction_data['category']
        
        if category_name in category_map:
            result = controller.add_transaction(
                type_transaction=transaction_data['type'],
                amount=transaction_data['amount'],
                description=transaction_data['description'],
                category_id=category_map[category_name],
                date_transaction=date.today()
            )
            
            if result['success']:
                created_count += 1
                print(f"✓ Criada: {transaction_data['description']} - R$ {transaction_data['amount']:.2f}")
            else:
                print(f"✗ Erro ao criar: {transaction_data['description']} - {result['message']}")
        else:
            print(f"⚠ Categoria não encontrada: {category_name}")
    
    print(f"\nDados de exemplo criados: {created_count}/{len(sample_transactions)} transações")

def show_database_info():
    """Mostra informações do banco de dados"""
    controller = FinanceController()
    
    print("=== INFORMAÇÕES DO BANCO DE DADOS ===")
    
    # Categorias
    categories = controller.get_categories()
    print(f"\nCategorias ({len(categories)}):")
    for cat in categories:
        print(f"  - {cat['name']} (ID: {cat['id']})")
    
    # Transações
    transactions = controller.get_transactions(limit=10)
    print(f"\nÚltimas Transações ({len(transactions)}):")
    for trans in transactions:
        type_text = "Receita" if trans['type'] == 'income' else "Despesa"
        print(f"  - {trans['date']} | {type_text} | R$ {trans['amount']:.2f} | {trans['description']}")
    
    # Resumo do dashboard
    dashboard_data = controller.get_dashboard_data()
    summary = dashboard_data['monthly_summary']
    print(f"\nResumo do Mês Atual:")
    print(f"  - Receitas: R$ {summary['income']:.2f}")
    print(f"  - Despesas: R$ {summary['expense']:.2f}")
    print(f"  - Saldo: R$ {summary['balance']:.2f}")

def backup_database():
    """Cria backup do banco de dados"""
    controller = FinanceController()
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f'backup_cashcontrol_{timestamp}.db'
    
    result = controller.create_backup(backup_filename)
    
    if result['success']:
        print(f"✓ Backup criado com sucesso: {backup_filename}")
    else:
        print(f"✗ Erro ao criar backup: {result['message']}")

def reset_database():
    """Reseta o banco de dados"""
    print("⚠ ATENÇÃO: Esta operação irá apagar todos os dados!")
    confirm = input("Digite 'CONFIRMAR' para continuar: ")
    
    if confirm == 'CONFIRMAR':
        try:
            # Remover arquivo do banco
            if os.path.exists('finance.db'):
                os.remove('finance.db')
                print("✓ Banco de dados resetado com sucesso")
                
                # Recriar banco
                from models.database import Database
                db = Database()
                print("✓ Novo banco de dados criado")
            else:
                print("ℹ Arquivo do banco não encontrado")
        except Exception as e:
            print(f"✗ Erro ao resetar banco: {e}")
    else:
        print("Operação cancelada")

def run_tests():
    """Executa testes básicos"""
    print("=== EXECUTANDO TESTES BÁSICOS ===")
    
    controller = FinanceController()
    
    # Teste 1: Verificar categorias
    categories = controller.get_categories()
    if categories:
        print("✓ Teste 1: Categorias carregadas")
    else:
        print("✗ Teste 1: Falha ao carregar categorias")
    
    # Teste 2: Criar transação de teste
    if categories:
        result = controller.add_transaction(
            type_transaction='expense',
            amount=10.0,
            description='Teste unitário',
            category_id=categories[0]['id']
        )
        
        if result['success']:
            print("✓ Teste 2: Transação criada")
            
            # Teste 3: Buscar transações
            transactions = controller.get_transactions(limit=1)
            if transactions:
                print("✓ Teste 3: Transações recuperadas")
                
                # Teste 4: Deletar transação de teste
                delete_result = controller.delete_transaction(transactions[0]['id'])
                if delete_result['success']:
                    print("✓ Teste 4: Transação removida")
                else:
                    print("✗ Teste 4: Falha ao remover transação")
            else:
                print("✗ Teste 3: Falha ao recuperar transações")
        else:
            print("✗ Teste 2: Falha ao criar transação")
    
    # Teste 5: Dashboard
    dashboard_data = controller.get_dashboard_data()
    if dashboard_data:
        print("✓ Teste 5: Dashboard carregado")
    else:
        print("✗ Teste 5: Falha ao carregar dashboard")
    
    print("Testes concluídos!")

def main():
    """Função principal do utilitário"""
    print("=== CASHCONTROL - UTILITÁRIO DE CONFIGURAÇÃO ===")
    print()
    print("Opções disponíveis:")
    print("1. Criar dados de exemplo")
    print("2. Mostrar informações do banco")
    print("3. Criar backup")
    print("4. Resetar banco de dados")
    print("5. Executar testes")
    print("6. Sair")
    print()
    
    while True:
        try:
            opcao = input("Escolha uma opção (1-6): ").strip()
            
            if opcao == '1':
                create_sample_data()
            elif opcao == '2':
                show_database_info()
            elif opcao == '3':
                backup_database()
            elif opcao == '4':
                reset_database()
            elif opcao == '5':
                run_tests()
            elif opcao == '6':
                print("Saindo...")
                break
            else:
                print("Opção inválida!")
            
            print("\n" + "="*50 + "\n")
            
        except KeyboardInterrupt:
            print("\nSaindo...")
            break
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == '__main__':
    main()
