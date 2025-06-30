"""
Aplicativo principal de controle financeiro pessoal
CashControl - Sistema completo de gestão de finanças
"""

import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.config import Config

# Configurações do Kivy
kivy.require('2.0.0')
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '700')
Config.set('graphics', 'resizable', True)

# Importar controladores e views
from controllers.finance_controller import FinanceController
from views.dashboard import DashboardScreen
from views.transactions import TransactionsScreen
from views.reports import ReportsScreen
from views.categories import CategoriesScreen

class NavigationBar(BoxLayout):
    """Barra de navegação inferior"""
    
    def __init__(self, screen_manager, **kwargs):
        super().__init__(orientation='horizontal', **kwargs)
        self.screen_manager = screen_manager
        self.size_hint_y = None
        self.height = '60dp'
        self.spacing = '2dp'
        
        # Cor de fundo
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        self.bind(size=self.update_rect, pos=self.update_rect)
        
        # Botões de navegação
        self.nav_buttons = {}
        
        # Dashboard
        dashboard_btn = Button(
            text='Home',
            font_size='11dp',
            background_color=(0.2, 0.6, 1, 1)
        )
        dashboard_btn.bind(on_press=lambda x: self.navigate_to('dashboard'))
        self.nav_buttons['dashboard'] = dashboard_btn
        
        # Transações
        transactions_btn = Button(
            text='Transações',
            font_size='10dp',
            background_color=(0.3, 0.3, 0.3, 1)
        )
        transactions_btn.bind(on_press=lambda x: self.navigate_to('transactions'))
        self.nav_buttons['transactions'] = transactions_btn
        
        # Categorias
        categories_btn = Button(
            text='Categorias',
            font_size='10dp',
            background_color=(0.3, 0.3, 0.3, 1)
        )
        categories_btn.bind(on_press=lambda x: self.navigate_to('categories'))
        self.nav_buttons['categories'] = categories_btn
        
        # Relatórios
        reports_btn = Button(
            text='Relatórios',
            font_size='10dp',
            background_color=(0.3, 0.3, 0.3, 1)
        )
        reports_btn.bind(on_press=lambda x: self.navigate_to('reports'))
        self.nav_buttons['reports'] = reports_btn
        
        # Configurações
        settings_btn = Button(
            text='Config',
            font_size='11dp',
            background_color=(0.3, 0.3, 0.3, 1)
        )
        settings_btn.bind(on_press=lambda x: self.show_settings())
        self.nav_buttons['settings'] = settings_btn
        
        # Adicionar botões
        self.add_widget(dashboard_btn)
        self.add_widget(transactions_btn)
        self.add_widget(categories_btn)
        self.add_widget(reports_btn)
        self.add_widget(settings_btn)
        
        # Destacar dashboard inicialmente
        self.highlight_button('dashboard')
    
    def update_rect(self, instance, value):
        """Atualiza o retângulo de fundo"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def navigate_to(self, screen_name):
        """Navega para uma tela específica"""
        self.screen_manager.current = screen_name
        self.highlight_button(screen_name)
    
    def highlight_button(self, screen_name):
        """Destaca o botão da tela atual"""
        for name, button in self.nav_buttons.items():
            if name == screen_name:
                button.background_color = (0.2, 0.6, 1, 1)
            else:
                button.background_color = (0.3, 0.3, 0.3, 1)
    
    def show_settings(self):
        """Mostra as configurações"""
        content = BoxLayout(orientation='vertical', spacing='20dp', padding='20dp')
        
        content.add_widget(Label(
            text='Configurações',
            font_size='20dp',
            bold=True,
            size_hint_y=None,
            height='40dp'
        ))
        
        # Opções de configuração
        options_layout = BoxLayout(orientation='vertical', spacing='15dp')
        
        # Gerenciar categorias
        categories_btn = Button(
            text='Gerenciar Categorias',
            size_hint_y=None,
            height='50dp',
            background_color=(0.6, 0.2, 0.8, 1)
        )
        categories_btn.bind(on_press=lambda x: self.navigate_to_categories(popup))
        
        # Backup
        backup_btn = Button(
            text='Criar Backup',
            size_hint_y=None,
            height='50dp',
            background_color=(0.2, 0.7, 0.2, 1)
        )
        backup_btn.bind(on_press=lambda x: self.create_backup(popup))
        
        # Restaurar backup
        restore_btn = Button(
            text='Restaurar Backup',
            size_hint_y=None,
            height='50dp',
            background_color=(0.7, 0.5, 0.2, 1)
        )
        restore_btn.bind(on_press=lambda x: self.restore_backup(popup))
        
        # Sobre
        about_btn = Button(
            text='Sobre o App',
            size_hint_y=None,
            height='50dp',
            background_color=(0.2, 0.6, 1, 1)
        )
        about_btn.bind(on_press=lambda x: self.show_about(popup))
        
        options_layout.add_widget(categories_btn)
        options_layout.add_widget(backup_btn)
        options_layout.add_widget(restore_btn)
        options_layout.add_widget(about_btn)
        content.add_widget(options_layout)
        
        # Botão fechar
        close_btn = Button(
            text='Fechar',
            size_hint_y=None,
            height='40dp',
            background_color=(0.5, 0.5, 0.5, 1)
        )
        content.add_widget(close_btn)
        
        popup = Popup(
            title='Configurações',
            content=content,
            size_hint=(0.9, 0.7),
            auto_dismiss=False
        )
        
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def navigate_to_categories(self, settings_popup):
        """Navega para a tela de categorias"""
        settings_popup.dismiss()
        self.screen_manager.current = 'categories'
        self.highlight_button('categories')
    
    def create_backup(self, settings_popup):
        """Cria backup do banco de dados"""
        settings_popup.dismiss()
        
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'backup_finance_{timestamp}.db'
        
        # Assumindo que temos acesso ao controlador através do app
        app = App.get_running_app()
        result = app.controller.create_backup(backup_filename)
        
        popup = Popup(
            title='Backup',
            content=Label(text=result['message']),
            size_hint=(0.8, 0.3),
            auto_dismiss=True
        )
        popup.open()
    
    def restore_backup(self, settings_popup):
        """Restaura backup (simplificado)"""
        settings_popup.dismiss()
        
        popup = Popup(
            title='Restaurar Backup',
            content=Label(text='Funcionalidade em desenvolvimento.\nColoque o arquivo backup.db na pasta do app.'),
            size_hint=(0.8, 0.3),
            auto_dismiss=True
        )
        popup.open()
    
    def show_about(self, settings_popup):
        """Mostra informações sobre o app"""
        settings_popup.dismiss()
        
        about_text = """
CashControl v1.0

Aplicativo completo de controle
de finanças pessoais.

Desenvolvido com Python e Kivy

Funcionalidades:
• Dashboard com resumos
• Gestão de transações
• Categorias personalizáveis
• Relatórios e gráficos
• Backup de dados

© 2024 - CashControl
        """
        
        popup = Popup(
            title='Sobre',
            content=Label(text=about_text.strip(), text_size=(None, None), halign='center'),
            size_hint=(0.8, 0.6),
            auto_dismiss=True
        )
        popup.open()

class SettingsScreen(Screen):
    """Tela de configurações avançadas"""
    
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.name = 'settings'
        self.controller = controller
        # Implementar mais configurações se necessário

class CashControlApp(App):
    """Aplicação principal"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = FinanceController()
        self.title = 'CashControl - Finanças Pessoais'
    
    def build(self):
        """Constrói a interface principal"""
        # Layout principal
        main_layout = BoxLayout(orientation='vertical')
        
        # Gerenciador de telas
        self.screen_manager = ScreenManager()
        
        # Criar e adicionar telas
        dashboard_screen = DashboardScreen(self.controller)
        transactions_screen = TransactionsScreen(self.controller)
        categories_screen = CategoriesScreen(self.controller)
        reports_screen = ReportsScreen(self.controller)
        
        self.screen_manager.add_widget(dashboard_screen)
        self.screen_manager.add_widget(transactions_screen)
        self.screen_manager.add_widget(categories_screen)
        self.screen_manager.add_widget(reports_screen)
        
        # Definir tela inicial
        self.screen_manager.current = 'dashboard'
        
        # Barra de navegação
        nav_bar = NavigationBar(self.screen_manager)
        
        # Monitorar mudanças de tela para atualizar navegação
        self.screen_manager.bind(current=self.on_screen_change)
        
        # Adicionar ao layout
        main_layout.add_widget(self.screen_manager)
        main_layout.add_widget(nav_bar)
        
        self.nav_bar = nav_bar
        
        # Verificar primeiro uso
        self.check_first_run()
        
        return main_layout
    
    def on_screen_change(self, screen_manager, screen_name):
        """Chamado quando a tela muda"""
        if hasattr(self, 'nav_bar'):
            self.nav_bar.highlight_button(screen_name)
    
    def check_first_run(self):
        """Verifica se é a primeira execução do app"""
        first_run = self.controller.get_setting('first_run')
        
        if first_run == 'true':
            # Mostrar boas-vindas
            Clock.schedule_once(self.show_welcome, 1)
            
            # Marcar como não sendo mais primeira execução
            self.controller.set_setting('first_run', 'false')
    
    def show_welcome(self, dt):
        """Mostra tela de boas-vindas"""
        welcome_text = """
Bem-vindo ao CashControl!

Seu aplicativo de controle financeiro pessoal.

Funcionalidades principais:
• Dashboard com resumo financeiro
• Gestão completa de transações
• Categorias personalizáveis
• Relatórios detalhados
• Backup de segurança

Dicas:
• Comece criando suas categorias personalizadas
• Adicione suas transações na aba "Transações"
• Veja seus gráficos em "Relatórios"

Toque em "Começar" para iniciar!
        """
        
        content = BoxLayout(orientation='vertical', spacing='20dp', padding='20dp')
        
        content.add_widget(Label(
            text=welcome_text.strip(),
            text_size=(None, None),
            halign='center',
            valign='middle'
        ))
        
        start_btn = Button(
            text='Começar',
            size_hint_y=None,
            height='50dp',
            background_color=(0.2, 0.7, 0.2, 1)
        )
        
        content.add_widget(start_btn)
        
        popup = Popup(
            title='Bem-vindo ao CashControl!',
            content=content,
            size_hint=(0.9, 0.8),
            auto_dismiss=False
        )
        
        start_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def on_pause(self):
        """Chamado quando o app é pausado (Android)"""
        return True
    
    def on_resume(self):
        """Chamado quando o app é retomado (Android)"""
        pass

if __name__ == '__main__':
    try:
        # Inicializar e executar o aplicativo
        CashControlApp().run()
    except Exception as e:
        print(f"Erro ao iniciar aplicativo: {e}")
        import traceback
        traceback.print_exc()
