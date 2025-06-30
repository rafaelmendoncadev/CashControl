"""
Configurações globais do CashControl
"""

import os

# Configurações do aplicativo
APP_NAME = "CashControl"
APP_VERSION = "1.0.0"
APP_AUTHOR = "CashControl Team"

# Configurações do banco de dados
DB_NAME = "finance.db"
DB_PATH = os.path.join(os.path.dirname(__file__), DB_NAME)

# Configurações da interface
DEFAULT_WINDOW_SIZE = (400, 700)
MIN_WINDOW_SIZE = (350, 600)

# Configurações de backup
BACKUP_DIR = "backups"
MAX_BACKUPS = 10

# Cores do tema
COLORS = {
    'primary': (0.2, 0.6, 1, 1),
    'success': (0.2, 0.7, 0.2, 1),
    'danger': (0.7, 0.2, 0.2, 1),
    'warning': (1, 0.6, 0, 1),
    'info': (0.2, 0.8, 0.8, 1),
    'light': (0.9, 0.9, 0.9, 1),
    'dark': (0.1, 0.1, 0.1, 1),
    'background': (0.95, 0.95, 0.95, 1)
}

# Configurações de formato
CURRENCY_SYMBOL = "R$"
DATE_FORMAT = "%d/%m/%Y"
DECIMAL_PLACES = 2

# Categorias padrão com ícones
DEFAULT_CATEGORIES = [
    {'name': 'Alimentação', 'icon': 'restaurant', 'color': '#FF5722'},
    {'name': 'Transporte', 'icon': 'car', 'color': '#2196F3'},
    {'name': 'Lazer', 'icon': 'movie', 'color': '#9C27B0'},
    {'name': 'Saúde', 'icon': 'medical-bag', 'color': '#4CAF50'},
    {'name': 'Educação', 'icon': 'school', 'color': '#FF9800'},
    {'name': 'Casa', 'icon': 'home', 'color': '#795548'},
    {'name': 'Roupas', 'icon': 'tshirt-crew', 'color': '#E91E63'},
    {'name': 'Salário', 'icon': 'cash', 'color': '#4CAF50'},
    {'name': 'Freelance', 'icon': 'laptop', 'color': '#00BCD4'},
    {'name': 'Investimentos', 'icon': 'trending-up', 'color': '#607D8B'},
    {'name': 'Outros', 'icon': 'help-circle', 'color': '#9E9E9E'}
]
