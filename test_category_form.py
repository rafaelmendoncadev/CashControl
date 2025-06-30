"""
Script de teste específico para o formulário de categorias
"""

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

# Configurações do Kivy
kivy.require('2.0.0')

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.finance_controller import FinanceController
from views.categories import CategoryForm

class TestCategoryApp(App):
    def build(self):
        controller = FinanceController()
        
        layout = BoxLayout(orientation='vertical', padding='20dp', spacing='20dp')
        
        # Botão para testar formulário
        test_btn = Button(
            text='Testar Formulário de Categoria',
            size_hint_y=None,
            height='50dp'
        )
        test_btn.bind(on_press=self.test_form)
        
        # Botão para testar controller direto
        test_controller_btn = Button(
            text='Testar Controller Direto',
            size_hint_y=None,
            height='50dp'
        )
        test_controller_btn.bind(on_press=self.test_controller)
        
        layout.add_widget(test_btn)
        layout.add_widget(test_controller_btn)
        
        self.controller = controller
        return layout
    
    def test_form(self, instance):
        """Testa o formulário"""
        print("🧪 Testando formulário de categoria...")
        
        def callback():
            print("✅ Callback do formulário chamado!")
        
        try:
            form = CategoryForm(self.controller, callback=callback)
            print("✅ Formulário criado com sucesso!")
            
            # Simular preenchimento
            form.name_input.text = "Categoria Teste"
            form.color_spinner.text = "#FF5722"
            form.icon_spinner.text = "test"
            
            print("✅ Formulário preenchido!")
            
            # Simular salvamento
            form.save_category(None)
            print("✅ Método save_category chamado!")
            
        except Exception as e:
            print(f"❌ Erro no formulário: {e}")
            import traceback
            traceback.print_exc()
    
    def test_controller(self, instance):
        """Testa o controller direto"""
        print("🧪 Testando controller direto...")
        
        try:
            result = self.controller.add_category("Teste App", "test", "#00FF00")
            print(f"✅ Resultado: {result}")
            
            # Verificar se foi criada
            categories = self.controller.get_categories()
            print(f"📊 Total de categorias: {len(categories)}")
            
            # Mostrar a última categoria
            if categories:
                last_cat = categories[-1]
                print(f"🆕 Última categoria: {last_cat}")
                
        except Exception as e:
            print(f"❌ Erro no controller: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    TestCategoryApp().run()
