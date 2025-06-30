"""
Módulo de gerenciamento do banco de dados SQLite
Responsável por criar e gerenciar as tabelas do sistema financeiro
"""

import sqlite3
import os
from datetime import datetime

class Database:
    """Classe para gerenciar o banco de dados SQLite"""
    
    def __init__(self, db_path="finance.db"):
        """
        Inicializa a conexão com o banco de dados
        
        Args:
            db_path (str): Caminho para o arquivo do banco de dados
        """
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """
        Retorna uma conexão com o banco de dados
        
        Returns:
            sqlite3.Connection: Conexão com o banco
        """
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Inicializa o banco de dados criando as tabelas necessárias"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabela de categorias
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                icon TEXT DEFAULT 'folder',
                color TEXT DEFAULT '#2196F3',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de transações
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
                amount REAL NOT NULL,
                description TEXT,
                category_id INTEGER,
                date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        ''')
        
        # Tabela de orçamentos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER,
                monthly_limit REAL NOT NULL,
                month INTEGER NOT NULL,
                year INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories (id),
                UNIQUE(category_id, month, year)
            )
        ''')
        
        # Tabela de metas financeiras
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                target_amount REAL NOT NULL,
                current_amount REAL DEFAULT 0,
                target_date DATE,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de configurações
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        ''')
        
        # Inserir categorias padrão se não existirem
        self._insert_default_categories(cursor)
        
        # Inserir configurações padrão
        self._insert_default_settings(cursor)
        
        conn.commit()
        conn.close()
    
    def _insert_default_categories(self, cursor):
        """Insere categorias padrão no banco de dados"""
        default_categories = [
            ('Alimentação', 'restaurant', '#FF5722'),
            ('Transporte', 'car', '#2196F3'),
            ('Lazer', 'movie', '#9C27B0'),
            ('Saúde', 'medical-bag', '#4CAF50'),
            ('Educação', 'school', '#FF9800'),
            ('Casa', 'home', '#795548'),
            ('Roupas', 'tshirt-crew', '#E91E63'),
            ('Salário', 'cash', '#4CAF50'),
            ('Freelance', 'laptop', '#00BCD4'),
            ('Investimentos', 'trending-up', '#607D8B'),
            ('Outros', 'help-circle', '#9E9E9E')
        ]
        
        for name, icon, color in default_categories:
            cursor.execute('''
                INSERT OR IGNORE INTO categories (name, icon, color)
                VALUES (?, ?, ?)
            ''', (name, icon, color))
    
    def _insert_default_settings(self, cursor):
        """Insere configurações padrão"""
        default_settings = [
            ('theme', 'light'),
            ('currency', 'R$'),
            ('backup_enabled', 'true'),
            ('first_run', 'true')
        ]
        
        for key, value in default_settings:
            cursor.execute('''
                INSERT OR IGNORE INTO settings (key, value)
                VALUES (?, ?)
            ''', (key, value))
    
    def backup_database(self, backup_path):
        """
        Cria um backup do banco de dados
        
        Args:
            backup_path (str): Caminho para salvar o backup
        """
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            return True
        except Exception as e:
            print(f"Erro ao criar backup: {e}")
            return False
    
    def restore_database(self, backup_path):
        """
        Restaura o banco de dados a partir de um backup
        
        Args:
            backup_path (str): Caminho do arquivo de backup
        """
        try:
            import shutil
            if os.path.exists(backup_path):
                shutil.copy2(backup_path, self.db_path)
                return True
            return False
        except Exception as e:
            print(f"Erro ao restaurar backup: {e}")
            return False
