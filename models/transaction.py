"""
Módulo de modelo para transações financeiras
Define a estrutura e operações relacionadas às transações
"""

from datetime import datetime, date
from models.database import Database

class Transaction:
    """Classe para representar uma transação financeira"""
    
    def __init__(self, transaction_id=None, type_transaction=None, amount=None, 
                 description=None, category_id=None, date_transaction=None):
        """
        Inicializa uma transação
        
        Args:
            transaction_id (int): ID da transação
            type_transaction (str): Tipo ('income' ou 'expense')
            amount (float): Valor da transação
            description (str): Descrição da transação
            category_id (int): ID da categoria
            date_transaction (date): Data da transação
        """
        self.id = transaction_id
        self.type = type_transaction
        self.amount = amount
        self.description = description
        self.category_id = category_id
        self.date = date_transaction
        self.db = Database()
    
    @classmethod
    def create(cls, type_transaction, amount, description, category_id, date_transaction=None):
        """
        Cria uma nova transação
        
        Args:
            type_transaction (str): 'income' ou 'expense'
            amount (float): Valor da transação
            description (str): Descrição
            category_id (int): ID da categoria
            date_transaction (date): Data da transação (padrão: hoje)
        
        Returns:
            Transaction: Nova transação criada
        """
        if date_transaction is None:
            date_transaction = date.today()
        
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO transactions (type, amount, description, category_id, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (type_transaction, amount, description, category_id, date_transaction))
        
        transaction_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return cls(transaction_id, type_transaction, amount, description, 
                  category_id, date_transaction)
    
    @classmethod
    def get_all(cls, limit=None, offset=0):
        """
        Busca todas as transações
        
        Args:
            limit (int): Limite de resultados
            offset (int): Offset para paginação
        
        Returns:
            list: Lista de transações
        """
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT t.id, t.type, t.amount, t.description, t.category_id, t.date,
                   c.name as category_name, c.icon, c.color
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            ORDER BY t.date DESC, t.created_at DESC
        '''
        
        if limit:
            query += f' LIMIT {limit} OFFSET {offset}'
        
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        
        transactions = []
        for row in rows:
            transaction = cls(row[0], row[1], row[2], row[3], row[4], row[5])
            transaction.category_name = row[6]
            transaction.category_icon = row[7]
            transaction.category_color = row[8]
            transactions.append(transaction)
        
        return transactions
    
    @classmethod
    def get_by_id(cls, transaction_id):
        """
        Busca uma transação pelo ID
        
        Args:
            transaction_id (int): ID da transação
        
        Returns:
            Transaction: Transação encontrada ou None
        """
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT t.id, t.type, t.amount, t.description, t.category_id, t.date,
                   c.name as category_name
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE t.id = ?
        ''', (transaction_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            transaction = cls(row[0], row[1], row[2], row[3], row[4], row[5])
            transaction.category_name = row[6]
            return transaction
        return None
    
    @classmethod
    def get_by_date_range(cls, start_date, end_date):
        """
        Busca transações por período
        
        Args:
            start_date (date): Data inicial
            end_date (date): Data final
        
        Returns:
            list: Lista de transações no período
        """
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT t.id, t.type, t.amount, t.description, t.category_id, t.date,
                   c.name as category_name, c.icon, c.color
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE t.date BETWEEN ? AND ?
            ORDER BY t.date DESC
        ''', (start_date, end_date))
        
        rows = cursor.fetchall()
        conn.close()
        
        transactions = []
        for row in rows:
            transaction = cls(row[0], row[1], row[2], row[3], row[4], row[5])
            transaction.category_name = row[6]
            transaction.category_icon = row[7]
            transaction.category_color = row[8]
            transactions.append(transaction)
        
        return transactions
    
    @classmethod
    def get_monthly_summary(cls, month, year):
        """
        Obtém resumo mensal das transações
        
        Args:
            month (int): Mês (1-12)
            year (int): Ano
        
        Returns:
            dict: Resumo com receitas, despesas e saldo
        """
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as total_income,
                SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as total_expense
            FROM transactions 
            WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
        ''', (f'{month:02d}', str(year)))
        
        result = cursor.fetchone()
        conn.close()
        
        total_income = result[0] or 0
        total_expense = result[1] or 0
        balance = total_income - total_expense
        
        return {
            'income': total_income,
            'expense': total_expense,
            'balance': balance
        }
    
    @classmethod
    def get_category_expenses(cls, month=None, year=None):
        """
        Obtém gastos por categoria
        
        Args:
            month (int): Mês para filtrar (opcional)
            year (int): Ano para filtrar (opcional)
        
        Returns:
            list: Lista com gastos por categoria
        """
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT c.name, c.color, SUM(t.amount) as total
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE t.type = 'expense'
        '''
        params = []
        
        if month and year:
            query += " AND strftime('%m', t.date) = ? AND strftime('%Y', t.date) = ?"
            params.extend([f'{month:02d}', str(year)])
        
        query += " GROUP BY c.id, c.name, c.color ORDER BY total DESC"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        
        return [{'category': row[0], 'color': row[1], 'amount': row[2]} 
                for row in results]
    
    def update(self):
        """Atualiza a transação no banco de dados"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE transactions 
            SET type = ?, amount = ?, description = ?, category_id = ?, date = ?
            WHERE id = ?
        ''', (self.type, self.amount, self.description, self.category_id, 
              self.date, self.id))
        
        conn.commit()
        conn.close()
    
    def delete(self):
        """Remove a transação do banco de dados"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM transactions WHERE id = ?', (self.id,))
        
        conn.commit()
        conn.close()
    
    def to_dict(self):
        """
        Converte a transação para dicionário
        
        Returns:
            dict: Dados da transação
        """
        return {
            'id': self.id,
            'type': self.type,
            'amount': self.amount,
            'description': self.description,
            'category_id': self.category_id,
            'date': self.date.isoformat() if isinstance(self.date, date) else self.date,
            'category_name': getattr(self, 'category_name', None),
            'category_icon': getattr(self, 'category_icon', None),
            'category_color': getattr(self, 'category_color', None)
        }

class Category:
    """Classe para representar uma categoria"""
    
    def __init__(self, category_id=None, name=None, icon=None, color=None):
        """
        Inicializa uma categoria
        
        Args:
            category_id (int): ID da categoria
            name (str): Nome da categoria
            icon (str): Ícone da categoria
            color (str): Cor da categoria
        """
        self.id = category_id
        self.name = name
        self.icon = icon
        self.color = color
        self.db = Database()
    
    @classmethod
    def get_all(cls):
        """
        Busca todas as categorias
        
        Returns:
            list: Lista de categorias
        """
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, name, icon, color FROM categories ORDER BY name')
        rows = cursor.fetchall()
        conn.close()
        
        return [cls(row[0], row[1], row[2], row[3]) for row in rows]
    
    @classmethod
    def get_by_id(cls, category_id):
        """
        Busca uma categoria pelo ID
        
        Args:
            category_id (int): ID da categoria
        
        Returns:
            Category: Categoria encontrada ou None
        """
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, name, icon, color FROM categories WHERE id = ?', (category_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls(row[0], row[1], row[2], row[3])
        return None
    
    @classmethod
    def create(cls, name, icon='folder', color='#2196F3'):
        """
        Cria uma nova categoria
        
        Args:
            name (str): Nome da categoria
            icon (str): Ícone da categoria
            color (str): Cor da categoria
        
        Returns:
            Category: Nova categoria criada
        """
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO categories (name, icon, color)
            VALUES (?, ?, ?)
        ''', (name, icon, color))
        
        category_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return cls(category_id, name, icon, color)
    
    def update(self):
        """Atualiza a categoria no banco de dados"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE categories 
            SET name = ?, icon = ?, color = ?
            WHERE id = ?
        ''', (self.name, self.icon, self.color, self.id))
        
        conn.commit()
        conn.close()
    
    def to_dict(self):
        """
        Converte a categoria para dicionário
        
        Returns:
            dict: Dados da categoria
        """
        return {
            'id': self.id,
            'name': self.name,
            'icon': self.icon,
            'color': self.color
        }
