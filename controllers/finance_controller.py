"""
Controlador principal da aplicação financeira
Gerencia a lógica de negócio e comunicação entre views e models
"""

from datetime import datetime, date
from models.database import Database
from models.transaction import Transaction, Category
import csv
import os

class FinanceController:
    """Controlador principal para operações financeiras"""
    
    def __init__(self):
        """Inicializa o controlador"""
        self.db = Database()
    
    # TRANSAÇÕES
    def add_transaction(self, type_transaction, amount, description, category_id, date_transaction=None):
        """
        Adiciona uma nova transação
        
        Args:
            type_transaction (str): 'income' ou 'expense'
            amount (float): Valor da transação
            description (str): Descrição
            category_id (int): ID da categoria
            date_transaction (date): Data da transação
        
        Returns:
            dict: Resultado com sucesso/erro
        """
        try:
            # Validações
            if not amount or amount <= 0:
                return {'success': False, 'message': 'Valor deve ser maior que zero'}
            
            if not category_id:
                return {'success': False, 'message': 'Categoria é obrigatória'}
            
            if type_transaction not in ['income', 'expense']:
                return {'success': False, 'message': 'Tipo de transação inválido'}
            
            # Criar transação
            transaction = Transaction.create(
                type_transaction=type_transaction,
                amount=float(amount),
                description=description or '',
                category_id=int(category_id),
                date_transaction=date_transaction or date.today()
            )
            
            return {
                'success': True, 
                'message': 'Transação adicionada com sucesso',
                'transaction': transaction.to_dict()
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Erro ao adicionar transação: {str(e)}'}
    
    def get_transactions(self, limit=None, offset=0):
        """
        Obtém lista de transações
        
        Args:
            limit (int): Limite de resultados
            offset (int): Offset para paginação
        
        Returns:
            list: Lista de transações
        """
        try:
            transactions = Transaction.get_all(limit=limit, offset=offset)
            return [t.to_dict() for t in transactions]
        except Exception as e:
            print(f"Erro ao buscar transações: {e}")
            return []
    
    def update_transaction(self, transaction_id, type_transaction, amount, description, category_id, date_transaction):
        """
        Atualiza uma transação existente
        
        Args:
            transaction_id (int): ID da transação
            type_transaction (str): Tipo da transação
            amount (float): Valor
            description (str): Descrição
            category_id (int): ID da categoria
            date_transaction (date): Data
        
        Returns:
            dict: Resultado da operação
        """
        try:
            transaction = Transaction.get_by_id(transaction_id)
            if not transaction:
                return {'success': False, 'message': 'Transação não encontrada'}
            
            # Validações
            if not amount or amount <= 0:
                return {'success': False, 'message': 'Valor deve ser maior que zero'}
            
            # Atualizar dados
            transaction.type = type_transaction
            transaction.amount = float(amount)
            transaction.description = description
            transaction.category_id = int(category_id)
            transaction.date = date_transaction
            
            transaction.update()
            
            return {'success': True, 'message': 'Transação atualizada com sucesso'}
            
        except Exception as e:
            return {'success': False, 'message': f'Erro ao atualizar transação: {str(e)}'}
    
    def delete_transaction(self, transaction_id):
        """
        Remove uma transação
        
        Args:
            transaction_id (int): ID da transação
        
        Returns:
            dict: Resultado da operação
        """
        try:
            transaction = Transaction.get_by_id(transaction_id)
            if not transaction:
                return {'success': False, 'message': 'Transação não encontrada'}
            
            transaction.delete()
            return {'success': True, 'message': 'Transação removida com sucesso'}
            
        except Exception as e:
            return {'success': False, 'message': f'Erro ao remover transação: {str(e)}'}
    
    # CATEGORIAS
    def get_categories(self):
        """
        Obtém todas as categorias
        
        Returns:
            list: Lista de categorias
        """
        try:
            categories = Category.get_all()
            return [c.to_dict() for c in categories]
        except Exception as e:
            print(f"Erro ao buscar categorias: {e}")
            return []
    
    def add_category(self, name, icon='folder', color='#2196F3'):
        """
        Adiciona uma nova categoria
        
        Args:
            name (str): Nome da categoria
            icon (str): Ícone
            color (str): Cor
        
        Returns:
            dict: Resultado da operação
        """
        try:
            if not name or not name.strip():
                return {'success': False, 'message': 'Nome da categoria é obrigatório'}
            
            name = name.strip()
            
            # Verificar se já existe uma categoria com esse nome
            existing_categories = self.get_categories()
            for category in existing_categories:
                existing_name = category.get('name', '')
                if existing_name and existing_name.lower() == name.lower():
                    return {
                        'success': False, 
                        'message': f'Já existe uma categoria chamada "{name}". Escolha outro nome.'
                    }
            
            category = Category.create(name, icon, color)
            return {
                'success': True, 
                'message': 'Categoria criada com sucesso',
                'category': category.to_dict()
            }
            
        except Exception as e:
            error_msg = str(e)
            if 'UNIQUE constraint failed' in error_msg:
                return {
                    'success': False, 
                    'message': f'Já existe uma categoria com o nome "{name}". Escolha outro nome.'
                }
            return {'success': False, 'message': f'Erro ao criar categoria: {error_msg}'}
    
    def update_category(self, category_id, name, icon='folder', color='#2196F3'):
        """
        Atualiza uma categoria existente
        
        Args:
            category_id (int): ID da categoria
            name (str): Nome da categoria
            icon (str): Ícone
            color (str): Cor
        
        Returns:
            dict: Resultado da operação
        """
        try:
            if not name or not name.strip():
                return {'success': False, 'message': 'Nome da categoria é obrigatório'}
            
            name = name.strip()
            
            # Verificar se a categoria existe
            category = Category.get_by_id(category_id)
            if not category:
                return {'success': False, 'message': 'Categoria não encontrada'}
            
            # Verificar se já existe outra categoria com esse nome (exceto a atual)
            existing_categories = self.get_categories()
            for existing_category in existing_categories:
                existing_name = existing_category.get('name', '')
                if (existing_category.get('id') != category_id and 
                    existing_name and existing_name.lower() == name.lower()):
                    return {
                        'success': False, 
                        'message': f'Já existe uma categoria chamada "{name}". Escolha outro nome.'
                    }
            
            # Atualizar categoria
            category.name = name
            category.icon = icon
            category.color = color
            category.update()
            
            return {
                'success': True, 
                'message': 'Categoria atualizada com sucesso',
                'category': category.to_dict()
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Erro ao atualizar categoria: {str(e)}'}
    
    # DASHBOARD
    def get_dashboard_data(self):
        """
        Obtém dados para o dashboard
        
        Returns:
            dict: Dados do dashboard
        """
        try:
            now = datetime.now()
            current_month = now.month
            current_year = now.year
            
            # Resumo mensal
            monthly_summary = Transaction.get_monthly_summary(current_month, current_year)
            
            # Últimas transações
            recent_transactions = self.get_transactions(limit=5)
            
            # Gastos por categoria
            category_expenses = Transaction.get_category_expenses(current_month, current_year)
            
            return {
                'monthly_summary': monthly_summary,
                'recent_transactions': recent_transactions,
                'category_expenses': category_expenses,
                'current_month': now.strftime('%B %Y')
            }
            
        except Exception as e:
            print(f"Erro ao obter dados do dashboard: {e}")
            return {
                'monthly_summary': {'income': 0, 'expense': 0, 'balance': 0},
                'recent_transactions': [],
                'category_expenses': [],
                'current_month': datetime.now().strftime('%B %Y')
            }
    
    # RELATÓRIOS
    def get_monthly_report(self, month, year):
        """
        Gera relatório mensal
        
        Args:
            month (int): Mês
            year (int): Ano
        
        Returns:
            dict: Dados do relatório
        """
        try:
            # Resumo do mês
            summary = Transaction.get_monthly_summary(month, year)
            
            # Transações do período
            start_date = date(year, month, 1)
            if month == 12:
                end_date = date(year + 1, 1, 1)
            else:
                end_date = date(year, month + 1, 1)
            
            transactions = Transaction.get_by_date_range(start_date, end_date)
            
            # Gastos por categoria
            category_expenses = Transaction.get_category_expenses(month, year)
            
            return {
                'period': f'{month:02d}/{year}',
                'summary': summary,
                'transactions': [t.to_dict() for t in transactions],
                'category_expenses': category_expenses
            }
            
        except Exception as e:
            print(f"Erro ao gerar relatório: {e}")
            return None
    
    def export_to_csv(self, start_date, end_date, file_path):
        """
        Exporta transações para CSV
        
        Args:
            start_date (date): Data inicial
            end_date (date): Data final
            file_path (str): Caminho do arquivo
        
        Returns:
            dict: Resultado da operação
        """
        try:
            transactions = Transaction.get_by_date_range(start_date, end_date)
            
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Data', 'Tipo', 'Valor', 'Descrição', 'Categoria']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for transaction in transactions:
                    writer.writerow({
                        'Data': transaction.date,
                        'Tipo': 'Receita' if transaction.type == 'income' else 'Despesa',
                        'Valor': transaction.amount,
                        'Descrição': transaction.description,
                        'Categoria': getattr(transaction, 'category_name', 'N/A')
                    })
            
            return {'success': True, 'message': f'Relatório exportado: {file_path}'}
            
        except Exception as e:
            return {'success': False, 'message': f'Erro ao exportar: {str(e)}'}
    
    # ORÇAMENTO
    def set_budget(self, category_id, monthly_limit, month=None, year=None):
        """
        Define orçamento para uma categoria
        
        Args:
            category_id (int): ID da categoria
            monthly_limit (float): Limite mensal
            month (int): Mês (padrão: atual)
            year (int): Ano (padrão: atual)
        
        Returns:
            dict: Resultado da operação
        """
        try:
            if month is None:
                month = datetime.now().month
            if year is None:
                year = datetime.now().year
            
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO budgets (category_id, monthly_limit, month, year)
                VALUES (?, ?, ?, ?)
            ''', (category_id, monthly_limit, month, year))
            
            conn.commit()
            conn.close()
            
            return {'success': True, 'message': 'Orçamento definido com sucesso'}
            
        except Exception as e:
            return {'success': False, 'message': f'Erro ao definir orçamento: {str(e)}'}
    
    def get_budget_status(self, month=None, year=None):
        """
        Obtém status dos orçamentos
        
        Args:
            month (int): Mês
            year (int): Ano
        
        Returns:
            list: Status dos orçamentos
        """
        try:
            if month is None:
                month = datetime.now().month
            if year is None:
                year = datetime.now().year
            
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT b.category_id, c.name, b.monthly_limit, 
                       COALESCE(SUM(t.amount), 0) as spent
                FROM budgets b
                JOIN categories c ON b.category_id = c.id
                LEFT JOIN transactions t ON t.category_id = b.category_id 
                    AND t.type = 'expense'
                    AND strftime('%m', t.date) = ?
                    AND strftime('%Y', t.date) = ?
                WHERE b.month = ? AND b.year = ?
                GROUP BY b.category_id, c.name, b.monthly_limit
            ''', (f'{month:02d}', str(year), month, year))
            
            results = cursor.fetchall()
            conn.close()
            
            budget_status = []
            for row in results:
                category_id, category_name, limit, spent = row
                percentage = (spent / limit * 100) if limit > 0 else 0
                
                budget_status.append({
                    'category_id': category_id,
                    'category_name': category_name,
                    'limit': limit,
                    'spent': spent,
                    'remaining': limit - spent,
                    'percentage': percentage,
                    'over_budget': spent > limit
                })
            
            return budget_status
            
        except Exception as e:
            print(f"Erro ao obter status do orçamento: {e}")
            return []
    
    # BACKUP E RESTORE
    def create_backup(self, backup_path):
        """
        Cria backup do banco de dados
        
        Args:
            backup_path (str): Caminho para o backup
        
        Returns:
            dict: Resultado da operação
        """
        try:
            success = self.db.backup_database(backup_path)
            if success:
                return {'success': True, 'message': 'Backup criado com sucesso'}
            else:
                return {'success': False, 'message': 'Erro ao criar backup'}
        except Exception as e:
            return {'success': False, 'message': f'Erro: {str(e)}'}
    
    def restore_backup(self, backup_path):
        """
        Restaura backup do banco de dados
        
        Args:
            backup_path (str): Caminho do backup
        
        Returns:
            dict: Resultado da operação
        """
        try:
            success = self.db.restore_database(backup_path)
            if success:
                return {'success': True, 'message': 'Backup restaurado com sucesso'}
            else:
                return {'success': False, 'message': 'Erro ao restaurar backup'}
        except Exception as e:
            return {'success': False, 'message': f'Erro: {str(e)}'}
    
    # CONFIGURAÇÕES
    def get_setting(self, key):
        """
        Obtém uma configuração
        
        Args:
            key (str): Chave da configuração
        
        Returns:
            str: Valor da configuração
        """
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else None
            
        except Exception as e:
            print(f"Erro ao obter configuração: {e}")
            return None
    
    def set_setting(self, key, value):
        """
        Define uma configuração
        
        Args:
            key (str): Chave da configuração
            value (str): Valor da configuração
        
        Returns:
            bool: Sucesso da operação
        """
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO settings (key, value)
                VALUES (?, ?)
            ''', (key, value))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao definir configuração: {e}")
            return False
