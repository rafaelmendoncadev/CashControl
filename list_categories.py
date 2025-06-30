"""
Lista todas as categorias existentes no banco de dados
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.finance_controller import FinanceController

def list_existing_categories():
    print("📋 CATEGORIAS EXISTENTES NO BANCO DE DADOS")
    print("=" * 50)
    
    controller = FinanceController()
    categories = controller.get_categories()
    
    print(f"Total de categorias: {len(categories)}")
    print()
    
    for i, category in enumerate(categories, 1):
        print(f"{i:2d}. {category['name']:<20} (ID: {category['id']}, Cor: {category['color']})")
    
    print()
    print("💡 DICA: Para criar uma nova categoria, use um nome que NÃO esteja na lista acima.")
    print()
    print("✅ Sugestões de nomes únicos:")
    suggestions = [
        "Academia", "Uber", "Farmácia", "Recarga Celular", "Netflix", 
        "Conta de Luz", "Conta de Água", "Internet", "Combustível",
        "Supermercado", "Delivery", "Cosméticos", "Veterinário",
        "Manutenção Casa", "Presentes", "Livros", "Cursos Online"
    ]
    
    # Filtrar sugestões que já existem
    existing_names = [cat['name'].lower() for cat in categories]
    available_suggestions = [name for name in suggestions if name.lower() not in existing_names]
    
    for suggestion in available_suggestions[:10]:
        print(f"  • {suggestion}")

if __name__ == "__main__":
    list_existing_categories()
