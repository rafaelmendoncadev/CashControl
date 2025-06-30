"""
Tela de gerenciamento de transações
Permite adicionar, editar, listar e filtrar transações
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.switch import Switch
from kivy.graphics import Color, Rectangle
from datetime import datetime, date
import threading

class TransactionForm(BoxLayout):
    """Formulário para adicionar/editar transações"""
    
    def __init__(self, controller, callback=None, transaction=None, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.controller = controller
        self.callback = callback
        self.transaction = transaction  # Para edição
        self.categories = []
        print("🏗️ Inicializando formulário de transação...")
        self.build_form()
        print("🔄 Carregando categorias no formulário...")
        self.load_categories()
        
        if transaction:
            self.populate_form(transaction)
        print("✅ Formulário de transação inicializado!")
    
    def build_form(self):
        """Constrói o formulário"""
        self.padding = '20dp'
        self.spacing = '15dp'
        
        # Fundo do formulário
        with self.canvas.before:
            Color(0.98, 0.98, 0.98, 1)  # Fundo bem claro
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        
        self.bind(size=self.update_bg_rect, pos=self.update_bg_rect)
        
        # Tipo de transação (Receita/Despesa)
        type_layout = BoxLayout(orientation='vertical', size_hint_y=None, height='70dp', spacing='5dp')
        
        type_label = Label(
            text='Tipo de Transação:',
            font_size='16dp',
            bold=True,
            color=(0.1, 0.1, 0.1, 1),
            size_hint_y=None,
            height='25dp',
            text_size=(None, None),
            halign='left',
            valign='middle'
        )
        type_layout.add_widget(type_label)
        
        self.type_spinner = Spinner(
            text='Despesa',
            values=['Receita', 'Despesa'],
            size_hint_y=None,
            height='40dp',
            background_color=(1, 1, 1, 1)
        )
        type_layout.add_widget(self.type_spinner)
        self.add_widget(type_layout)
        
        # Valor
        amount_layout = BoxLayout(orientation='vertical', size_hint_y=None, height='70dp', spacing='5dp')
        
        amount_label = Label(
            text='Valor (R$):',
            font_size='16dp',
            bold=True,
            color=(0.1, 0.1, 0.1, 1),
            size_hint_y=None,
            height='25dp',
            text_size=(None, None),
            halign='left',
            valign='middle'
        )
        amount_layout.add_widget(amount_label)
        
        self.amount_input = TextInput(
            multiline=False,
            input_filter='float',
            size_hint_y=None,
            height='40dp',
            background_color=(1, 1, 1, 1),
            foreground_color=(0.1, 0.1, 0.1, 1),
            hint_text='0.00'
        )
        amount_layout.add_widget(self.amount_input)
        self.add_widget(amount_layout)
        
        # Descrição
        desc_layout = BoxLayout(orientation='vertical', size_hint_y=None, height='70dp', spacing='5dp')
        
        desc_label = Label(
            text='Descrição:',
            font_size='16dp',
            bold=True,
            color=(0.1, 0.1, 0.1, 1),
            size_hint_y=None,
            height='25dp',
            text_size=(None, None),
            halign='left',
            valign='middle'
        )
        desc_layout.add_widget(desc_label)
        
        self.description_input = TextInput(
            multiline=False,
            size_hint_y=None,
            height='40dp',
            background_color=(1, 1, 1, 1),
            foreground_color=(0.1, 0.1, 0.1, 1),
            hint_text='Digite uma descrição...'
        )
        desc_layout.add_widget(self.description_input)
        self.add_widget(desc_layout)
        
        # Categoria
        cat_layout = BoxLayout(orientation='vertical', size_hint_y=None, height='70dp', spacing='5dp')
        
        cat_label = Label(
            text='Categoria:',
            font_size='16dp',
            bold=True,
            color=(0.1, 0.1, 0.1, 1),
            size_hint_y=None,
            height='25dp',
            text_size=(None, None),
            halign='left',
            valign='middle'
        )
        cat_layout.add_widget(cat_label)
        
        self.category_spinner = Spinner(
            text='Selecione...',
            values=[],
            size_hint_y=None,
            height='40dp',
            background_color=(1, 1, 1, 1)
        )
        cat_layout.add_widget(self.category_spinner)
        self.add_widget(cat_layout)
        print("🎛️ Category spinner criado")
        
        # Data
        date_layout = BoxLayout(orientation='vertical', size_hint_y=None, height='70dp', spacing='5dp')
        
        date_label = Label(
            text='Data:',
            font_size='16dp',
            bold=True,
            color=(0.1, 0.1, 0.1, 1),
            size_hint_y=None,
            height='25dp',
            text_size=(None, None),
            halign='left',
            valign='middle'
        )
        date_layout.add_widget(date_label)
        
        self.date_input = TextInput(
            text=date.today().strftime('%d/%m/%Y'),
            multiline=False,
            size_hint_y=None,
            height='40dp',
            background_color=(1, 1, 1, 1),
            foreground_color=(0.1, 0.1, 0.1, 1),
            hint_text='DD/MM/AAAA'
        )
        date_layout.add_widget(self.date_input)
        self.add_widget(date_layout)
        
        # Botões
        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='60dp', spacing='15dp')
        
        save_btn = Button(
            text='💾 Salvar',
            font_size='16dp',
            bold=True,
            background_color=(0.2, 0.7, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        save_btn.bind(on_press=self.save_transaction)
        
        cancel_btn = Button(
            text='❌ Cancelar',
            font_size='16dp',
            bold=True,
            background_color=(0.7, 0.2, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        cancel_btn.bind(on_press=self.cancel_form)
        
        buttons_layout.add_widget(save_btn)
        buttons_layout.add_widget(cancel_btn)
        self.add_widget(buttons_layout)
    
    def load_categories(self):
        """Carrega as categorias disponíveis"""
        print("🔄 Carregando categorias para transações...")
        try:
            self.categories = self.controller.get_categories()
            print(f"📊 Categorias carregadas para transações: {len(self.categories)}")
            
            category_names = [cat['name'] for cat in self.categories]
            
            # Atualizar diretamente sem threading
            if hasattr(self, 'category_spinner'):
                self.category_spinner.values = category_names
                print(f"✅ Spinner atualizado com {len(category_names)} categorias")
                if category_names:
                    print(f"📋 Categorias disponíveis: {', '.join(category_names)}")
                else:
                    print("⚠️ Nenhuma categoria disponível")
            else:
                print("❌ category_spinner não encontrado")
                
        except Exception as e:
            print(f"❌ Erro ao carregar categorias para transações: {e}")
            import traceback
            traceback.print_exc()
    
    def populate_form(self, transaction):
        """Preenche o formulário para edição"""
        self.type_spinner.text = 'Receita' if transaction['type'] == 'income' else 'Despesa'
        self.amount_input.text = str(transaction['amount'])
        self.description_input.text = transaction.get('description', '')
        self.date_input.text = transaction['date']
        
        # Definir categoria após carregar
        def set_category():
            if hasattr(self, 'categories') and self.categories:
                for cat in self.categories:
                    if cat['id'] == transaction['category_id']:
                        self.category_spinner.text = cat['name']
                        break
        
        # Aguardar categorias carregarem
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: set_category(), 1)
    
    def save_transaction(self, instance):
        """Salva a transação"""
        try:
            # Validar campos
            if not self.amount_input.text:
                self.show_error('Valor é obrigatório')
                return
            
            if self.category_spinner.text == 'Selecione...':
                self.show_error('Selecione uma categoria')
                return
            
            # Encontrar ID da categoria
            category_id = None
            for cat in self.categories:
                if cat['name'] == self.category_spinner.text:
                    category_id = cat['id']
                    break
            
            if not category_id:
                self.show_error('Categoria inválida')
                return
            
            # Preparar dados
            transaction_type = 'income' if self.type_spinner.text == 'Receita' else 'expense'
            amount = float(self.amount_input.text.replace(',', '.'))
            description = self.description_input.text
            
            # Converter data
            try:
                date_parts = self.date_input.text.split('/')
                transaction_date = date(int(date_parts[2]), int(date_parts[1]), int(date_parts[0]))
            except:
                transaction_date = date.today()
            
            # Salvar transação
            if self.transaction:
                # Editar transação existente
                result = self.controller.update_transaction(
                    self.transaction['id'],
                    transaction_type,
                    amount,
                    description,
                    category_id,
                    transaction_date
                )
            else:
                # Criar nova transação
                result = self.controller.add_transaction(
                    transaction_type,
                    amount,
                    description,
                    category_id,
                    transaction_date
                )
            
            if result['success']:
                self.show_success(result['message'])
                if self.callback:
                    self.callback()
            else:
                self.show_error(result['message'])
                
        except ValueError:
            self.show_error('Valor inválido')
        except Exception as e:
            self.show_error(f'Erro: {str(e)}')
    
    def cancel_form(self, instance):
        """Cancela o formulário"""
        if self.callback:
            self.callback()
    
    def show_error(self, message):
        """Mostra mensagem de erro"""
        content = BoxLayout(orientation='vertical', padding='25dp', spacing='20dp')
        
        # Fundo colorido para o popup
        with content.canvas.before:
            Color(0.98, 0.95, 0.95, 1)  # Fundo levemente avermelhado
            content.bg_rect = Rectangle(size=content.size, pos=content.pos)
        content.bind(size=lambda x, y: setattr(content.bg_rect, 'size', y))
        content.bind(pos=lambda x, y: setattr(content.bg_rect, 'pos', y))
        
        # Ícone de erro
        error_icon = Label(
            text='⚠️',
            font_size='50dp',
            size_hint_y=None,
            height='70dp'
        )
        content.add_widget(error_icon)
        
        # Título
        title_label = Label(
            text='Ops! Algo deu errado',
            font_size='18dp',
            bold=True,
            color=(0.7, 0.2, 0.2, 1),  # Vermelho escuro
            size_hint_y=None,
            height='30dp'
        )
        content.add_widget(title_label)
        
        # Mensagem
        error_label = Label(
            text=message,
            font_size='15dp',
            color=(0.1, 0.1, 0.1, 1),
            text_size=(300, None),
            halign='center',
            valign='middle'
        )
        content.add_widget(error_label)
        
        # Botão OK
        ok_btn = Button(
            text='👍 Entendi',
            font_size='16dp',
            bold=True,
            size_hint_y=None,
            height='50dp',
            background_color=(0.7, 0.2, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        content.add_widget(ok_btn)
        
        popup = Popup(
            title='',  # Remove título padrão
            content=content,
            size_hint=(0.85, 0.5),
            auto_dismiss=False,  # Usuário deve clicar no botão
            separator_height=0
        )
        
        ok_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def show_success(self, message):
        """Mostra mensagem de sucesso"""
        content = BoxLayout(orientation='vertical', padding='25dp', spacing='20dp')
        
        # Fundo colorido para o popup
        with content.canvas.before:
            Color(0.95, 0.98, 0.95, 1)  # Fundo levemente esverdeado
            content.bg_rect = Rectangle(size=content.size, pos=content.pos)
        content.bind(size=lambda x, y: setattr(content.bg_rect, 'size', y))
        content.bind(pos=lambda x, y: setattr(content.bg_rect, 'pos', y))
        
        # Ícone de sucesso
        success_icon = Label(
            text='🎉',
            font_size='50dp',
            size_hint_y=None,
            height='70dp'
        )
        content.add_widget(success_icon)
        
        # Título
        title_label = Label(
            text='Perfeito!',
            font_size='20dp',
            bold=True,
            color=(0.2, 0.7, 0.2, 1),  # Verde escuro
            size_hint_y=None,
            height='35dp'
        )
        content.add_widget(title_label)
        
        # Mensagem
        success_label = Label(
            text=message,
            font_size='15dp',
            color=(0.1, 0.1, 0.1, 1),
            text_size=(300, None),
            halign='center',
            valign='middle'
        )
        content.add_widget(success_label)
        
        # Botões
        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', spacing='10dp')
        
        # Botão Continuar
        continue_btn = Button(
            text='➕ Adicionar Mais',
            font_size='14dp',
            bold=True,
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1)
        )
        
        # Botão OK
        ok_btn = Button(
            text='✅ Pronto',
            font_size='14dp',
            bold=True,
            background_color=(0.2, 0.7, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        
        buttons_layout.add_widget(continue_btn)
        buttons_layout.add_widget(ok_btn)
        content.add_widget(buttons_layout)
        
        popup = Popup(
            title='',  # Remove título padrão
            content=content,
            size_hint=(0.85, 0.55),
            auto_dismiss=False,  # Usuário deve clicar no botão
            separator_height=0
        )
        
        # Função para continuar adicionando
        def continue_adding(instance):
            popup.dismiss()
            # Se há callback (que fecha o formulário atual), não o chama
            # para manter o formulário aberto
            
        # Função para finalizar
        def finish(instance):
            popup.dismiss()
            if self.callback:
                self.callback()
        
        continue_btn.bind(on_press=continue_adding)
        ok_btn.bind(on_press=finish)
        popup.open()
    
    def update_bg_rect(self, instance, value):
        """Atualiza o retângulo de fundo"""
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

class TransactionListItem(BoxLayout):
    """Item da lista de transações"""
    
    def __init__(self, transaction, edit_callback=None, delete_callback=None, **kwargs):
        super().__init__(orientation='horizontal', **kwargs)
        self.transaction = transaction
        self.edit_callback = edit_callback
        self.delete_callback = delete_callback
        
        self.size_hint_y = None
        self.height = '80dp'
        self.padding = '10dp'
        self.spacing = '10dp'
        
        # Cor de fundo com borda
        bg_color = (0.96, 0.96, 0.96, 1)  # Fundo quase branco mas não totalmente
        border_color = (0.75, 0.75, 0.75, 1)  # Borda mais visível
        with self.canvas.before:
            Color(*border_color)
            self.border_rect = Rectangle(size=self.size, pos=self.pos)
            Color(*bg_color)
            self.rect = Rectangle(size=(self.size[0]-2, self.size[1]-2), pos=(self.pos[0]+1, self.pos[1]+1))
        
        self.bind(size=self.update_rect, pos=self.update_rect)
        
        # Informações da transação
        info_layout = BoxLayout(orientation='vertical', size_hint_x=0.6)
        
        # Descrição
        desc_label = Label(
            text=transaction.get('description', 'Sem descrição'),
            font_size='16dp',
            bold=True,
            color=(0.15, 0.15, 0.15, 1),  # Texto bem escuro
            text_size=(None, None),
            halign='left',
            valign='middle',
            size_hint_y=0.5
        )
        
        # Detalhes
        details = f"{transaction.get('category_name', 'N/A')} • {transaction['date']}"
        details_label = Label(
            text=details,
            font_size='12dp',
            color=(0.3, 0.3, 0.3, 1),  # Cor mais escura para melhor contraste
            text_size=(None, None),
            halign='left',
            valign='middle',
            size_hint_y=0.5
        )
        
        info_layout.add_widget(desc_label)
        info_layout.add_widget(details_label)
        
        # Valor
        amount_text = f"R$ {transaction['amount']:.2f}"
        if transaction['type'] == 'expense':
            amount_text = f"-{amount_text}"
        
        amount_label = Label(
            text=amount_text,
            font_size='16dp',
            bold=True,
            color=(0.2, 0.7, 0.2, 1) if transaction['type'] == 'income' else (0.7, 0.2, 0.2, 1),
            size_hint_x=0.2
        )
        
        # Botões de ação
        actions_layout = BoxLayout(orientation='vertical', size_hint_x=0.2, spacing='5dp')
        
        edit_btn = Button(
            text='Editar',
            font_size='10dp',
            background_color=(0.2, 0.6, 1, 1)
        )
        edit_btn.bind(on_press=lambda x: self.edit_transaction())
        
        delete_btn = Button(
            text='Excluir',
            font_size='10dp',
            background_color=(0.7, 0.2, 0.2, 1)
        )
        delete_btn.bind(on_press=lambda x: self.delete_transaction())
        
        actions_layout.add_widget(edit_btn)
        actions_layout.add_widget(delete_btn)
        
        self.add_widget(info_layout)
        self.add_widget(amount_label)
        self.add_widget(actions_layout)
    
    def update_rect(self, instance, value):
        """Atualiza o retângulo de fundo"""
        self.border_rect.pos = instance.pos
        self.border_rect.size = instance.size
        self.rect.pos = (instance.pos[0]+1, instance.pos[1]+1)
        self.rect.size = (instance.size[0]-2, instance.size[1]-2)
    
    def edit_transaction(self):
        """Chama callback de edição"""
        if self.edit_callback:
            self.edit_callback(self.transaction)
    
    def delete_transaction(self):
        """Chama callback de exclusão"""
        if self.delete_callback:
            self.delete_callback(self.transaction)

class TransactionsScreen(Screen):
    """Tela de gerenciamento de transações"""
    
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.name = 'transactions'
        self.controller = controller
        self.transactions = []
        self.build_ui()
        self.load_transactions()
    
    def on_enter(self):
        """Chamado quando a tela é acessada"""
        print("🔄 Entrando na tela de transações - recarregando dados...")
        self.load_transactions()
    
    def build_ui(self):
        """Constrói a interface"""
        main_layout = BoxLayout(orientation='vertical', padding='10dp', spacing='10dp')
        
        # Cabeçalho
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
        
        title_label = Label(
            text='Transações',
            font_size='24dp',
            bold=True,
            color=(0.1, 0.1, 0.1, 1),  # Texto escuro para melhor contraste
            size_hint_x=0.7
        )
        
        add_btn = Button(
            text='+ Nova',
            size_hint_x=0.3,
            background_color=(0.2, 0.7, 0.2, 1)
        )
        add_btn.bind(on_press=self.show_add_form)
        
        header_layout.add_widget(title_label)
        header_layout.add_widget(add_btn)
        main_layout.add_widget(header_layout)
        
        # Filtros (simples)
        filters_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp', spacing='10dp')
        
        filters_layout.add_widget(Label(
            text='Filtros:', 
            size_hint_x=0.2,
            color=(0.2, 0.2, 0.2, 1)  # Texto escuro
        ))
        
        self.type_filter = Spinner(
            text='Todos',
            values=['Todos', 'Receitas', 'Despesas'],
            size_hint_x=0.4
        )
        self.type_filter.bind(text=self.filter_transactions)
        
        refresh_btn = Button(
            text='Atualizar',
            size_hint_x=0.4,
            background_color=(0.2, 0.6, 1, 1)
        )
        refresh_btn.bind(on_press=lambda x: self.load_transactions())
        
        filters_layout.add_widget(self.type_filter)
        filters_layout.add_widget(refresh_btn)
        main_layout.add_widget(filters_layout)
        
        # Lista de transações
        scroll = ScrollView()
        self.transactions_layout = BoxLayout(
            orientation='vertical', 
            spacing='5dp', 
            size_hint_y=None
        )
        self.transactions_layout.bind(minimum_height=self.transactions_layout.setter('height'))
        
        scroll.add_widget(self.transactions_layout)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def load_transactions(self):
        """Carrega as transações"""
        from kivy.clock import Clock
        
        def load_async():
            try:
                transactions = self.controller.get_transactions(limit=50)
                # Agendar atualização na thread principal
                Clock.schedule_once(lambda dt: self.update_transactions_with_data(transactions), 0)
            except Exception as e:
                print(f"❌ Erro ao carregar transações: {e}")
                Clock.schedule_once(lambda dt: self.update_transactions_with_data([]), 0)
        
        threading.Thread(target=load_async, daemon=True).start()
    
    def update_transactions_with_data(self, transactions):
        """Atualiza as transações com dados fornecidos (thread-safe)"""
        self.transactions = transactions
        self.update_transactions_list()
    
    def update_transactions_list(self):
        """Atualiza a lista de transações"""
        self.transactions_layout.clear_widgets()
        
        if not self.transactions:
            no_data_label = Label(
                text='Nenhuma transação encontrada',
                font_size='16dp',
                color=(0.4, 0.4, 0.4, 1),  # Cor escura para contraste
                size_hint_y=None,
                height='50dp'
            )
            self.transactions_layout.add_widget(no_data_label)
            return
        
        for transaction in self.transactions:
            item = TransactionListItem(
                transaction,
                edit_callback=self.edit_transaction,
                delete_callback=self.confirm_delete_transaction
            )
            self.transactions_layout.add_widget(item)
    
    def filter_transactions(self, spinner, text):
        """Filtra transações por tipo"""
        if not self.transactions:
            return
        
        self.transactions_layout.clear_widgets()
        
        # Aplicar filtro
        filtered_transactions = []
        if text == 'Todos':
            filtered_transactions = self.transactions
        elif text == 'Receitas':
            filtered_transactions = [t for t in self.transactions if t['type'] == 'income']
        elif text == 'Despesas':
            filtered_transactions = [t for t in self.transactions if t['type'] == 'expense']
        
        # Atualizar lista
        for transaction in filtered_transactions:
            item = TransactionListItem(
                transaction,
                edit_callback=self.edit_transaction,
                delete_callback=self.confirm_delete_transaction
            )
            self.transactions_layout.add_widget(item)
    
    def show_add_form(self, instance):
        """Mostra formulário de adicionar transação"""
        print("📝 Criando formulário de nova transação...")
        form = TransactionForm(
            self.controller,
            callback=self.close_form
        )
        
        # Criar popup com visual melhorado
        popup_content = BoxLayout(orientation='vertical', padding='10dp')
        
        # Cabeçalho do popup
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
        header_label = Label(
            text='📝 Nova Transação',
            font_size='20dp',
            bold=True,
            color=(0.1, 0.1, 0.1, 1)
        )
        header.add_widget(header_label)
        
        # Adicionar formulário
        popup_content.add_widget(header)
        popup_content.add_widget(form)
        
        popup = Popup(
            title='',  # Removemos o título padrão já que temos nosso próprio header
            content=popup_content,
            size_hint=(0.95, 0.85),
            auto_dismiss=False,
            separator_height=0  # Remove a linha separadora
        )
        
        self.form_popup = popup
        popup.open()
        print("✅ Formulário de transação aberto!")
    
    def edit_transaction(self, transaction):
        """Mostra formulário de editar transação"""
        form = TransactionForm(
            self.controller,
            callback=self.close_form,
            transaction=transaction
        )
        
        # Criar popup com visual melhorado
        popup_content = BoxLayout(orientation='vertical', padding='10dp')
        
        # Cabeçalho do popup
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
        header_label = Label(
            text='✏️ Editar Transação',
            font_size='20dp',
            bold=True,
            color=(0.1, 0.1, 0.1, 1)
        )
        header.add_widget(header_label)
        
        # Adicionar formulário
        popup_content.add_widget(header)
        popup_content.add_widget(form)
        
        popup = Popup(
            title='',  # Removemos o título padrão já que temos nosso próprio header
            content=popup_content,
            size_hint=(0.95, 0.85),
            auto_dismiss=False,
            separator_height=0  # Remove a linha separadora
        )
        
        self.form_popup = popup
        popup.open()
    
    def close_form(self):
        """Fecha o formulário e atualiza a lista"""
        if hasattr(self, 'form_popup'):
            self.form_popup.dismiss()
        self.load_transactions()
    
    def confirm_delete_transaction(self, transaction):
        """Confirma exclusão da transação"""
        content = BoxLayout(orientation='vertical', padding='25dp', spacing='20dp')
        
        # Fundo colorido para o popup
        with content.canvas.before:
            Color(0.98, 0.96, 0.95, 1)  # Fundo levemente alaranjado
            content.bg_rect = Rectangle(size=content.size, pos=content.pos)
        content.bind(size=lambda x, y: setattr(content.bg_rect, 'size', y))
        content.bind(pos=lambda x, y: setattr(content.bg_rect, 'pos', y))
        
        # Ícone de aviso
        warning_icon = Label(
            text='🗑️',
            font_size='50dp',
            size_hint_y=None,
            height='70dp'
        )
        content.add_widget(warning_icon)
        
        # Título
        title_label = Label(
            text='Confirmar Exclusão',
            font_size='18dp',
            bold=True,
            color=(0.7, 0.4, 0.2, 1),  # Laranja escuro
            size_hint_y=None,
            height='30dp'
        )
        content.add_widget(title_label)
        
        # Mensagem
        message_label = Label(
            text=f"Deseja realmente excluir a transação:\n\n'{transaction.get('description', 'Sem descrição')}'?\n\nEsta ação não pode ser desfeita.",
            font_size='14dp',
            color=(0.1, 0.1, 0.1, 1),
            text_size=(280, None),
            halign='center',
            valign='middle'
        )
        content.add_widget(message_label)
        
        # Botões
        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', spacing='15dp')
        
        yes_btn = Button(
            text='🗑️ Sim, Excluir',
            font_size='14dp',
            bold=True,
            background_color=(0.7, 0.2, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        
        no_btn = Button(
            text='❌ Cancelar',
            font_size='14dp',
            bold=True,
            background_color=(0.5, 0.5, 0.5, 1),
            color=(1, 1, 1, 1)
        )
        
        buttons_layout.add_widget(no_btn)
        buttons_layout.add_widget(yes_btn)
        content.add_widget(buttons_layout)
        
        popup = Popup(
            title='',  # Remove título padrão
            content=content,
            size_hint=(0.85, 0.6),
            auto_dismiss=False,
            separator_height=0
        )
        
        yes_btn.bind(on_press=lambda x: self.delete_transaction(transaction, popup))
        no_btn.bind(on_press=popup.dismiss)
        
        popup.open()
    
    def delete_transaction(self, transaction, popup):
        """Exclui a transação"""
        result = self.controller.delete_transaction(transaction['id'])
        popup.dismiss()
        
        if result['success']:
            self.load_transactions()
            # Mostrar confirmação de exclusão
            self.show_delete_success()
        else:
            self.show_delete_error(result['message'])
    
    def show_delete_success(self):
        """Mostra confirmação de exclusão bem-sucedida"""
        content = BoxLayout(orientation='vertical', padding='25dp', spacing='20dp')
        
        # Fundo colorido
        with content.canvas.before:
            Color(0.95, 0.98, 0.95, 1)  # Fundo levemente esverdeado
            content.bg_rect = Rectangle(size=content.size, pos=content.pos)
        content.bind(size=lambda x, y: setattr(content.bg_rect, 'size', y))
        content.bind(pos=lambda x, y: setattr(content.bg_rect, 'pos', y))
        
        # Ícone
        icon = Label(
            text='🗑️✅',
            font_size='45dp',
            size_hint_y=None,
            height='65dp'
        )
        content.add_widget(icon)
        
        # Título
        title_label = Label(
            text='Transação Excluída',
            font_size='18dp',
            bold=True,
            color=(0.2, 0.7, 0.2, 1),
            size_hint_y=None,
            height='30dp'
        )
        content.add_widget(title_label)
        
        # Mensagem
        message_label = Label(
            text='A transação foi removida com sucesso.',
            font_size='14dp',
            color=(0.1, 0.1, 0.1, 1),
            text_size=(280, None),
            halign='center'
        )
        content.add_widget(message_label)
        
        # Botão OK
        ok_btn = Button(
            text='👍 OK',
            font_size='16dp',
            bold=True,
            size_hint_y=None,
            height='50dp',
            background_color=(0.2, 0.7, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        content.add_widget(ok_btn)
        
        popup = Popup(
            title='',
            content=content,
            size_hint=(0.8, 0.45),
            auto_dismiss=False,
            separator_height=0
        )
        
        ok_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def show_delete_error(self, message):
        """Mostra erro na exclusão"""
        content = BoxLayout(orientation='vertical', padding='25dp', spacing='20dp')
        
        # Fundo colorido
        with content.canvas.before:
            Color(0.98, 0.95, 0.95, 1)  # Fundo levemente avermelhado
            content.bg_rect = Rectangle(size=content.size, pos=content.pos)
        content.bind(size=lambda x, y: setattr(content.bg_rect, 'size', y))
        content.bind(pos=lambda x, y: setattr(content.bg_rect, 'pos', y))
        
        # Ícone
        icon = Label(
            text='❌',
            font_size='45dp',
            size_hint_y=None,
            height='65dp'
        )
        content.add_widget(icon)
        
        # Título
        title_label = Label(
            text='Erro na Exclusão',
            font_size='18dp',
            bold=True,
            color=(0.7, 0.2, 0.2, 1),
            size_hint_y=None,
            height='30dp'
        )
        content.add_widget(title_label)
        
        # Mensagem
        message_label = Label(
            text=message,
            font_size='14dp',
            color=(0.1, 0.1, 0.1, 1),
            text_size=(280, None),
            halign='center'
        )
        content.add_widget(message_label)
        
        # Botão OK
        ok_btn = Button(
            text='👍 Entendi',
            font_size='16dp',
            bold=True,
            size_hint_y=None,
            height='50dp',
            background_color=(0.7, 0.2, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        content.add_widget(ok_btn)
        
        popup = Popup(
            title='',
            content=content,
            size_hint=(0.8, 0.45),
            auto_dismiss=False,
            separator_height=0
        )
        
        ok_btn.bind(on_press=popup.dismiss)
        popup.open()
