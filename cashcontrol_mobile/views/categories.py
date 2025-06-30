"""
Tela de gerenciamento de categorias
Permite visualizar, criar, editar e remover categorias
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, Rectangle
import threading

class CategoryForm(BoxLayout):
    """Formulário para criar/editar categorias"""
    
    def __init__(self, controller, callback=None, category=None, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.controller = controller
        self.callback = callback
        self.category = category  # Para edição
        self.build_form()
        
        if category:
            self.populate_form(category)
    
    def build_form(self):
        """Constrói o formulário"""
        self.padding = '20dp'
        self.spacing = '15dp'
        
        # Título
        title = 'Editar Categoria' if self.category else 'Nova Categoria'
        title_label = Label(
            text=title,
            font_size='20dp',
            bold=True,
            color=(0.1, 0.1, 0.1, 1),  # Texto escuro
            size_hint_y=None,
            height='40dp'
        )
        self.add_widget(title_label)
        
        # Nome da categoria
        name_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp')
        name_layout.add_widget(Label(
            text='Nome:', 
            size_hint_x=0.3,
            color=(0.2, 0.2, 0.2, 1)  # Texto escuro
        ))
        
        self.name_input = TextInput(
            multiline=False,
            size_hint_x=0.7
        )
        name_layout.add_widget(self.name_input)
        self.add_widget(name_layout)
        
        # Cor da categoria
        color_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp')
        color_layout.add_widget(Label(
            text='Cor:', 
            size_hint_x=0.3,
            color=(0.2, 0.2, 0.2, 1)  # Texto escuro
        ))
        
        self.color_spinner = Spinner(
            text='#2196F3',
            values=[
                '#2196F3',  # Azul
                '#4CAF50',  # Verde
                '#FF5722',  # Vermelho
                '#FF9800',  # Laranja
                '#9C27B0',  # Roxo
                '#795548',  # Marrom
                '#E91E63',  # Rosa
                '#00BCD4',  # Ciano
                '#607D8B',  # Azul Acinzentado
                '#9E9E9E'   # Cinza
            ],
            size_hint_x=0.7
        )
        color_layout.add_widget(self.color_spinner)
        self.add_widget(color_layout)
        
        # Ícone da categoria
        icon_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp')
        icon_layout.add_widget(Label(
            text='Ícone:', 
            size_hint_x=0.3,
            color=(0.2, 0.2, 0.2, 1)  # Texto escuro
        ))
        
        self.icon_spinner = Spinner(
            text='folder',
            values=[
                'folder',
                'restaurant',
                'car',
                'movie',
                'medical-bag',
                'school',
                'home',
                'tshirt-crew',
                'cash',
                'laptop',
                'trending-up',
                'help-circle',
                'shopping-cart',
                'heart',
                'airplane',
                'gamepad',
                'music'
            ],
            size_hint_x=0.7
        )
        icon_layout.add_widget(self.icon_spinner)
        self.add_widget(icon_layout)
        
        # Preview da categoria
        preview_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='60dp')
        preview_layout.add_widget(Label(
            text='Preview:', 
            size_hint_x=0.3,
            color=(0.2, 0.2, 0.2, 1)  # Texto escuro
        ))
        
        self.preview_widget = BoxLayout(orientation='horizontal', size_hint_x=0.7)
        self.update_preview()
        preview_layout.add_widget(self.preview_widget)
        self.add_widget(preview_layout)
        
        # Atualizar preview quando valores mudarem
        self.name_input.bind(text=lambda x, y: self.update_preview())
        self.color_spinner.bind(text=lambda x, y: self.update_preview())
        self.icon_spinner.bind(text=lambda x, y: self.update_preview())
        
        # Botões
        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', spacing='10dp')
        
        save_btn = Button(
            text='Salvar',
            background_color=(0.2, 0.7, 0.2, 1)
        )
        save_btn.bind(on_press=self.save_category)
        
        cancel_btn = Button(
            text='Cancelar',
            background_color=(0.7, 0.2, 0.2, 1)
        )
        cancel_btn.bind(on_press=self.cancel_form)
        
        buttons_layout.add_widget(save_btn)
        buttons_layout.add_widget(cancel_btn)
        self.add_widget(buttons_layout)
    
    def populate_form(self, category):
        """Preenche o formulário para edição"""
        self.name_input.text = category['name']
        self.color_spinner.text = category['color']
        self.icon_spinner.text = category['icon']
        self.update_preview()
    
    def update_preview(self):
        """Atualiza o preview da categoria"""
        self.preview_widget.clear_widgets()
        
        # Criar widget de preview
        preview = BoxLayout(orientation='horizontal', spacing='10dp')
        
        # Converter cor hex para RGB
        try:
            color_hex = self.color_spinner.text.lstrip('#')
            if len(color_hex) == 6:
                r = int(color_hex[0:2], 16) / 255.0
                g = int(color_hex[2:4], 16) / 255.0
                b = int(color_hex[4:6], 16) / 255.0
                color = (r, g, b, 1)
            else:
                color = (0.2, 0.6, 1, 1)
        except:
            color = (0.2, 0.6, 1, 1)
        
        # Círculo colorido (simulando ícone)
        icon_widget = Label(
            text='●',
            font_size='24dp',
            color=color,
            size_hint_x=None,
            width='40dp'
        )
        
        # Nome da categoria
        name_label = Label(
            text=self.name_input.text or 'Nova Categoria',
            font_size='16dp',
            color=(0.2, 0.2, 0.2, 1)  # Texto escuro para preview
        )
        
        preview.add_widget(icon_widget)
        preview.add_widget(name_label)
        self.preview_widget.add_widget(preview)
    
    def save_category(self, instance):
        """Salva a categoria"""
        try:
            name = self.name_input.text.strip()
            print(f"🔍 Tentando salvar categoria: '{name}'")
            
            if not name:
                print("❌ Nome vazio!")
                self.show_error('Nome da categoria é obrigatório')
                return
            
            color = self.color_spinner.text
            icon = self.icon_spinner.text
            print(f"🎨 Cor: {color}, Ícone: {icon}")
            
            if self.category:
                # Editar categoria existente (se implementado no controller)
                print("ℹ️ Modo edição (não implementado)")
                self.show_info('Edição de categorias será implementada em breve')
            else:
                # Criar nova categoria
                print("➕ Criando nova categoria...")
                result = self.controller.add_category(name, icon, color)
                print(f"📝 Resultado do controller: {result}")
                
                if result.get('success'):
                    print("✅ Categoria salva com sucesso!")
                    self.show_success(result['message'])
                    # Chamar callback imediatamente após sucesso
                    if self.callback:
                        print("🔄 Chamando callback...")
                        # Usar Clock para garantir que seja executado na thread principal
                        from kivy.clock import Clock
                        Clock.schedule_once(lambda dt: self.callback(), 0.1)
                else:
                    print("❌ Erro ao salvar categoria")
                    self.show_error(result.get('message', 'Erro desconhecido'))
                    
        except Exception as e:
            print(f"💥 Exceção ao salvar categoria: {e}")
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
        title_text = 'Nome já existe' if 'Já existe uma categoria' in message else 'Ops! Algo deu errado'
        title_label = Label(
            text=title_text,
            font_size='18dp',
            bold=True,
            color=(0.7, 0.2, 0.2, 1),
            size_hint_y=None,
            height='30dp'
        )
        content.add_widget(title_label)
        
        # Mensagem principal
        main_message = Label(
            text=message,
            font_size='15dp',
            color=(0.1, 0.1, 0.1, 1),
            text_size=(300, None),
            halign='center'
        )
        content.add_widget(main_message)
        
        # Se for erro de nome duplicado, adicionar sugestões
        if 'Já existe uma categoria' in message:
            suggestions_text = "💡 Sugestões:\n• Adicione um número (ex: 'Categoria 2')\n• Seja mais específico (ex: 'Alimentação Casa')\n• Use nome diferente (ex: 'Comida', 'Refeições')"
            suggestions_label = Label(
                text=suggestions_text,
                font_size='13dp',
                color=(0.4, 0.4, 0.4, 1),
                text_size=(300, None),
                halign='left'
            )
            content.add_widget(suggestions_label)
        
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
        
        popup_height = 0.6 if 'Já existe uma categoria' in message else 0.5
        popup = Popup(
            title='',
            content=content,
            size_hint=(0.9, popup_height),
            auto_dismiss=False,
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
            text='Categoria Criada!',
            font_size='20dp',
            bold=True,
            color=(0.2, 0.7, 0.2, 1),
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
            halign='center'
        )
        content.add_widget(success_label)
        
        # Botões
        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', spacing='10dp')
        
        # Botão Continuar
        continue_btn = Button(
            text='➕ Criar Mais',
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
            title='',
            content=content,
            size_hint=(0.85, 0.55),
            auto_dismiss=False,
            separator_height=0
        )
        
        # Função para continuar criando
        def continue_creating(instance):
            popup.dismiss()
            # Limpa o formulário para nova categoria
            self.name_input.text = ''
            self.color_spinner.text = '#2196F3'
            self.icon_spinner.text = 'folder'
            self.update_preview()
            
        # Função para finalizar
        def finish(instance):
            popup.dismiss()
            if self.callback:
                self.callback()
        
        continue_btn.bind(on_press=continue_creating)
        ok_btn.bind(on_press=finish)
        popup.open()
    
    def show_info(self, message):
        """Mostra mensagem informativa"""
        content = BoxLayout(orientation='vertical', padding='25dp', spacing='20dp')
        
        # Fundo colorido para o popup
        with content.canvas.before:
            Color(0.95, 0.97, 0.98, 1)  # Fundo levemente azulado
            content.bg_rect = Rectangle(size=content.size, pos=content.pos)
        content.bind(size=lambda x, y: setattr(content.bg_rect, 'size', y))
        content.bind(pos=lambda x, y: setattr(content.bg_rect, 'pos', y))
        
        # Ícone informativo
        info_icon = Label(
            text='ℹ️',
            font_size='50dp',
            size_hint_y=None,
            height='70dp'
        )
        content.add_widget(info_icon)
        
        # Título
        title_label = Label(
            text='Informação',
            font_size='18dp',
            bold=True,
            color=(0.2, 0.6, 1, 1),
            size_hint_y=None,
            height='30dp'
        )
        content.add_widget(title_label)
        
        # Mensagem
        info_label = Label(
            text=message,
            font_size='15dp',
            color=(0.1, 0.1, 0.1, 1),
            text_size=(300, None),
            halign='center'
        )
        content.add_widget(info_label)
        
        # Botão OK
        ok_btn = Button(
            text='👍 OK',
            font_size='16dp',
            bold=True,
            size_hint_y=None,
            height='50dp',
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1)
        )
        content.add_widget(ok_btn)
        
        popup = Popup(
            title='',
            content=content,
            size_hint=(0.85, 0.5),
            auto_dismiss=False,
            separator_height=0
        )
        
        ok_btn.bind(on_press=popup.dismiss)
        popup.open()
        popup.open()

class CategoryItem(BoxLayout):
    """Item da lista de categorias"""
    
    def __init__(self, category, edit_callback=None, delete_callback=None, **kwargs):
        super().__init__(orientation='horizontal', **kwargs)
        self.category = category
        self.edit_callback = edit_callback
        self.delete_callback = delete_callback
        
        self.size_hint_y = None
        self.height = '70dp'
        self.padding = '10dp'
        self.spacing = '10dp'
        
        # Cor de fundo mais clara com melhor contraste
        with self.canvas.before:
            Color(0.92, 0.92, 0.92, 1)  # Fundo ligeiramente mais escuro para melhor contraste
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        self.bind(size=self.update_rect, pos=self.update_rect)
        
        # Ícone da categoria (círculo colorido)
        try:
            color_hex = category['color'].lstrip('#')
            if len(color_hex) == 6:
                r = int(color_hex[0:2], 16) / 255.0
                g = int(color_hex[2:4], 16) / 255.0
                b = int(color_hex[4:6], 16) / 255.0
                color = (r, g, b, 1)
            else:
                color = (0.2, 0.6, 1, 1)
        except:
            color = (0.2, 0.6, 1, 1)
        
        icon_label = Label(
            text='●',
            font_size='32dp',
            color=color,
            size_hint_x=None,
            width='60dp'
        )
        
        # Informações da categoria
        info_layout = BoxLayout(orientation='vertical', size_hint_x=0.6)
        
        # Nome
        name_label = Label(
            text=category['name'],
            font_size='18dp',
            bold=True,
            color=(0.1, 0.1, 0.1, 1),  # Texto bem escuro
            text_size=(None, None),
            halign='left',
            valign='middle',
            size_hint_y=0.6
        )
        
        # Detalhes
        details = f"Ícone: {category['icon']} • Cor: {category['color']}"
        details_label = Label(
            text=details,
            font_size='12dp',
            color=(0.4, 0.4, 0.4, 1),  # Cor escura mas não totalmente preta
            text_size=(None, None),
            halign='left',
            valign='middle',
            size_hint_y=0.4
        )
        
        info_layout.add_widget(name_label)
        info_layout.add_widget(details_label)
        
        # Botões de ação
        actions_layout = BoxLayout(orientation='vertical', size_hint_x=0.2, spacing='5dp')
        
        edit_btn = Button(
            text='Editar',
            font_size='10dp',
            background_color=(0.2, 0.6, 1, 1)
        )
        edit_btn.bind(on_press=lambda x: self.edit_category())
        
        delete_btn = Button(
            text='Excluir',
            font_size='10dp',
            background_color=(0.7, 0.2, 0.2, 1)
        )
        delete_btn.bind(on_press=lambda x: self.delete_category())
        
        actions_layout.add_widget(edit_btn)
        actions_layout.add_widget(delete_btn)
        
        self.add_widget(icon_label)
        self.add_widget(info_layout)
        self.add_widget(actions_layout)
    
    def update_rect(self, instance, value):
        """Atualiza o retângulo de fundo"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def edit_category(self):
        """Chama callback de edição"""
        if self.edit_callback:
            self.edit_callback(self.category)
    
    def delete_category(self):
        """Chama callback de exclusão"""
        if self.delete_callback:
            self.delete_callback(self.category)

class CategoriesScreen(Screen):
    """Tela de gerenciamento de categorias"""
    
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.name = 'categories'
        self.controller = controller
        self.categories = []
        print("🏗️ Inicializando tela de categorias...")
        self.build_ui()
        print("🔄 Carregando categorias iniciais...")
        self.load_categories()
        print("✅ Tela de categorias inicializada!")
    
    def build_ui(self):
        """Constrói a interface"""
        main_layout = BoxLayout(orientation='vertical', padding='10dp', spacing='10dp')
        
        # Cabeçalho
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
        
        title_label = Label(
            text='Categorias',
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
        print("🔘 Botão '+ Nova' criado e vinculado")
        
        header_layout.add_widget(title_label)
        header_layout.add_widget(add_btn)
        main_layout.add_widget(header_layout)
        
        # Informações
        info_label = Label(
            text='Gerencie suas categorias de receitas e despesas.\nNomes de categorias devem ser únicos.',
            font_size='14dp',
            color=(0.4, 0.4, 0.4, 1),  # Cor mais escura para melhor contraste
            size_hint_y=None,
            height='40dp',
            text_size=(None, None),
            halign='center'
        )
        main_layout.add_widget(info_label)
        
        # Lista de categorias
        scroll = ScrollView()
        self.categories_layout = BoxLayout(
            orientation='vertical', 
            spacing='5dp', 
            size_hint_y=None
        )
        self.categories_layout.bind(minimum_height=self.categories_layout.setter('height'))
        
        scroll.add_widget(self.categories_layout)
        main_layout.add_widget(scroll)
        
        # Botão de atualizar
        refresh_btn = Button(
            text='Atualizar Lista',
            size_hint_y=None,
            height='40dp',
            background_color=(0.2, 0.6, 1, 1)
        )
        refresh_btn.bind(on_press=lambda x: self.load_categories())
        main_layout.add_widget(refresh_btn)
        
        self.add_widget(main_layout)
    
    def load_categories(self):
        """Carrega as categorias"""
        print("🔄 Carregando categorias...")
        try:
            categories = self.controller.get_categories()
            print(f"📊 Categorias carregadas: {len(categories)}")
            # Mostrar algumas para debug
            for i, cat in enumerate(categories[-3:]):
                print(f"  📁 {cat['name']} (ID: {cat['id']})")
            
            # Atualizar diretamente sem threading
            self.update_categories_list_with_data(categories)
        except Exception as e:
            print(f"💥 Erro ao carregar categorias: {e}")
            import traceback
            traceback.print_exc()
    
    def update_categories_list_with_data(self, categories):
        """Atualiza a lista de categorias com dados fornecidos"""
        print(f"🎯 Atualizando UI com {len(categories)} categorias")
        self.categories = categories
        self.update_categories_list()
    
    def update_categories_list(self):
        """Atualiza a lista de categorias"""
        print(f"🖼️ Atualizando lista visual com {len(self.categories)} categorias")
        self.categories_layout.clear_widgets()
        
        if not self.categories:
            print("ℹ️ Nenhuma categoria para mostrar")
            no_data_label = Label(
                text='Nenhuma categoria encontrada',
                font_size='16dp',
                color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None,
                height='50dp'
            )
            self.categories_layout.add_widget(no_data_label)
            return
        
        for i, category in enumerate(self.categories):
            print(f"  📁 Adicionando categoria {i+1}: {category['name']}")
            item = CategoryItem(
                category,
                edit_callback=self.edit_category,
                delete_callback=self.confirm_delete_category
            )
            self.categories_layout.add_widget(item)
        
        print("✅ Lista visual atualizada!")
    
    def show_add_form(self, instance):
        """Mostra formulário de adicionar categoria"""
        print("📝 Abrindo formulário de nova categoria...")
        form = CategoryForm(
            self.controller,
            callback=self.close_form
        )
        
        popup = Popup(
            title='Nova Categoria',
            content=form,
            size_hint=(0.9, 0.8),
            auto_dismiss=False
        )
        
        self.form_popup = popup
        popup.open()
        print("✅ Formulário de categoria aberto!")
    
    def edit_category(self, category):
        """Mostra formulário de editar categoria"""
        form = CategoryForm(
            self.controller,
            callback=self.close_form,
            category=category
        )
        
        popup = Popup(
            title='Editar Categoria',
            content=form,
            size_hint=(0.9, 0.8),
            auto_dismiss=False
        )
        
        self.form_popup = popup
        popup.open()
    
    def close_form(self):
        """Fecha o formulário e atualiza a lista"""
        print("🔒 Fechando formulário e atualizando lista...")
        if hasattr(self, 'form_popup'):
            self.form_popup.dismiss()
        self.load_categories()
    
    def confirm_delete_category(self, category):
        """Confirma exclusão da categoria"""
        content = BoxLayout(orientation='vertical', spacing='20dp')
        content.add_widget(Label(
            text=f"Deseja realmente excluir a categoria:\n{category['name']}?\n\nAtenção: Esta ação não pode ser desfeita!",
            text_size=(None, None),
            halign='center'
        ))
        
        buttons_layout = BoxLayout(orientation='horizontal', spacing='10dp')
        
        yes_btn = Button(
            text='Sim, Excluir',
            background_color=(0.7, 0.2, 0.2, 1)
        )
        
        no_btn = Button(
            text='Cancelar',
            background_color=(0.5, 0.5, 0.5, 1)
        )
        
        buttons_layout.add_widget(yes_btn)
        buttons_layout.add_widget(no_btn)
        content.add_widget(buttons_layout)
        
        popup = Popup(
            title='Confirmar Exclusão',
            content=content,
            size_hint=(0.8, 0.4),
            auto_dismiss=False
        )
        
        yes_btn.bind(on_press=lambda x: self.delete_category(category, popup))
        no_btn.bind(on_press=popup.dismiss)
        
        popup.open()
    
    def delete_category(self, category, popup):
        """Exclui a categoria"""
        popup.dismiss()
        
        # Por enquanto, apenas mostra mensagem
        info_popup = Popup(
            title='Informação',
            content=Label(text='Exclusão de categorias será implementada em breve.\nPor segurança, categorias com transações não podem ser removidas.'),
            size_hint=(0.8, 0.3),
            auto_dismiss=True
        )
        info_popup.open()
