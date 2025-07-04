"""
Tela de gerenciamento de categorias - Layout Moderno
Permite visualizar, criar, editar e remover categorias com interface aprimorada
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
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp
import threading

class ModernCard(BoxLayout):
    """Card moderno com bordas arredondadas e sombra"""
    
    def __init__(self, bg_color=(1, 1, 1, 1), border_color=(0.9, 0.9, 0.9, 1), **kwargs):
        super().__init__(**kwargs)
        self.bg_color = bg_color
        self.border_color = border_color
        
        with self.canvas.before:
            # Sombra
            Color(0.8, 0.8, 0.8, 0.3)
            self.shadow = RoundedRectangle(
                size=(self.width + dp(4), self.height + dp(4)),
                pos=(self.x - dp(2), self.y - dp(2)),
                radius=[dp(8)]
            )
            # Borda
            Color(*border_color)
            self.border = RoundedRectangle(
                size=self.size,
                pos=self.pos,
                radius=[dp(6)]
            )
            # Fundo
            Color(*bg_color)
            self.bg = RoundedRectangle(
                size=(self.width - dp(2), self.height - dp(2)),
                pos=(self.x + dp(1), self.y + dp(1)),
                radius=[dp(5)]
            )
        
        self.bind(size=self.update_graphics, pos=self.update_graphics)
    
    def update_graphics(self, *args):
        """Atualiza os gráficos quando o tamanho/posição muda"""
        self.shadow.size = (self.width + dp(4), self.height + dp(4))
        self.shadow.pos = (self.x - dp(2), self.y - dp(2))
        self.border.size = self.size
        self.border.pos = self.pos
        self.bg.size = (self.width - dp(2), self.height - dp(2))
        self.bg.pos = (self.x + dp(1), self.y + dp(1))

class ModernButton(Button):
    """Botão moderno com estilo aprimorado"""
    
    def __init__(self, button_type='primary', **kwargs):
        super().__init__(**kwargs)
        
        # Definir cores baseadas no tipo
        if button_type == 'primary':
            self.background_color = (0.13, 0.59, 0.95, 1)  # Azul moderno
        elif button_type == 'success':
            self.background_color = (0.20, 0.73, 0.29, 1)  # Verde moderno
        elif button_type == 'danger':
            self.background_color = (0.96, 0.26, 0.21, 1)  # Vermelho moderno
        elif button_type == 'warning':
            self.background_color = (1.0, 0.60, 0.0, 1)    # Laranja moderno
        elif button_type == 'secondary':
            self.background_color = (0.40, 0.40, 0.40, 1)  # Cinza moderno
        
        self.font_size = dp(14)
        self.bold = True

class ModernColorPicker(BoxLayout):
    """Seletor de cores visual moderno"""
    
    def __init__(self, selected_color='#2196F3', callback=None, **kwargs):
        super().__init__(orientation='horizontal', **kwargs)
        self.selected_color = selected_color
        self.callback = callback
        self.size_hint_y = None
        self.height = dp(50)
        self.spacing = dp(5)
        
        # Adicionar atributo color para evitar conflitos
        self.color = (1, 1, 1, 1)
        
        self.colors = [
            '#2196F3', '#4CAF50', '#FF5722', '#FF9800',
            '#9C27B0', '#795548', '#E91E63', '#00BCD4',
            '#607D8B', '#9E9E9E', '#F44336', '#8BC34A'
        ]
        
        for color in self.colors:
            color_btn = Button(
                text='●' if color == selected_color else '',
                size_hint_x=None,
                width=dp(40),
                font_size=dp(20)
            )
            
            # Converter hex para RGB
            try:
                hex_color = color.lstrip('#')
                r = int(hex_color[0:2], 16) / 255.0
                g = int(hex_color[2:4], 16) / 255.0
                b = int(hex_color[4:6], 16) / 255.0
                color_btn.background_color = (r, g, b, 1)
            except:
                color_btn.background_color = (0.5, 0.5, 0.5, 1)
            
            color_btn.bind(on_press=lambda x, c=color: self.select_color(c))
            self.add_widget(color_btn)
    
    def select_color(self, color):
        """Seleciona uma cor"""
        self.selected_color = color
        # Atualizar indicador visual
        for i, child in enumerate(self.children):
            if self.colors[len(self.children) - 1 - i] == color:
                child.text = '●'
                child.color = (1, 1, 1, 1)
            else:
                child.text = ''
                child.color = (0, 0, 0, 1)
        
        if self.callback:
            self.callback(color)

class CategoryForm(ModernCard):
    """Formulário moderno para criar/editar categorias"""
    
    def __init__(self, controller, callback=None, category=None, **kwargs):
        super().__init__(
            orientation='vertical',
            bg_color=(1, 1, 1, 1),
            border_color=(0.85, 0.85, 0.85, 1),
            **kwargs
        )
        self.controller = controller
        self.callback = callback
        self.category = category
        self.selected_color = '#2196F3'
        self.selected_icon = 'folder'
        
        self.padding = dp(20)
        self.spacing = dp(15)
        
        self.build_form()
        
        if category:
            self.populate_form(category)
    
    def build_form(self):
        """Constrói o formulário moderno"""
        
        # Título com estilo
        title_layout = BoxLayout(size_hint_y=None, height=dp(40))
        title = 'Editar Categoria' if self.category else 'Nova Categoria'
        title_label = Label(
            text=title,
            font_size=dp(24),
            bold=True,
            color=(0.2, 0.2, 0.2, 1)
        )
        title_layout.add_widget(title_label)
        self.add_widget(title_layout)
        
        # Seção Nome
        name_section = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(80), spacing=dp(5))
        
        name_label = Label(
            text='Nome da Categoria',
            font_size=dp(16),
            bold=True,
            color=(0.3, 0.3, 0.3, 1),
            size_hint_y=None,
            height=dp(25),
            halign='left'
        )
        name_label.bind(size=name_label.setter('text_size'))
        
        self.name_input = TextInput(
            multiline=False,
            size_hint_y=None,
            height=dp(45),
            font_size=dp(16),
            background_color=(0.98, 0.98, 0.98, 1),
            foreground_color=(0.2, 0.2, 0.2, 1),
            cursor_color=(0.13, 0.59, 0.95, 1),
            hint_text='Ex: Alimentação, Transporte...'
        )
        
        name_section.add_widget(name_label)
        name_section.add_widget(self.name_input)
        self.add_widget(name_section)
        
        # Seção Cor
        color_section = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(90), spacing=dp(5))
        
        color_label = Label(
            text='Cor da Categoria',
            font_size=dp(16),
            bold=True,
            color=(0.3, 0.3, 0.3, 1),
            size_hint_y=None,
            height=dp(25),
            halign='left'
        )
        color_label.bind(size=color_label.setter('text_size'))
        
        self.color_picker = ModernColorPicker(
            selected_color=self.selected_color,
            callback=self.on_color_selected
        )
        
        color_section.add_widget(color_label)
        color_section.add_widget(self.color_picker)
        self.add_widget(color_section)
        
        # Seção Ícone
        icon_section = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(80), spacing=dp(5))
        
        icon_label = Label(
            text='Ícone da Categoria',
            font_size=dp(16),
            bold=True,
            color=(0.3, 0.3, 0.3, 1),
            size_hint_y=None,
            height=dp(25),
            halign='left'
        )
        icon_label.bind(size=icon_label.setter('text_size'))
        
        self.icon_spinner = Spinner(
            text='📁 folder',
            values=[
                '📁 folder', '🍽️ restaurant', '🚗 car', '🎬 movie',
                '🏥 medical-bag', '🏫 school', '🏠 home', '👕 tshirt-crew',
                '💰 cash', '💻 laptop', '📈 trending-up', '❓ help-circle',
                '🛒 shopping-cart', '❤️ heart', '✈️ airplane', '🎮 gamepad',
                '🎵 music', '⚽ sports', '🔧 tools', '🎨 art'
            ],
            size_hint_y=None,
            height=dp(45),
            font_size=dp(16),
            background_color=(0.98, 0.98, 0.98, 1)
        )
        
        icon_section.add_widget(icon_label)
        icon_section.add_widget(self.icon_spinner)
        self.add_widget(icon_section)
        
        # Preview
        preview_section = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(80), spacing=dp(5))
        
        preview_label = Label(
            text='Preview',
            font_size=dp(16),
            bold=True,
            color=(0.3, 0.3, 0.3, 1),
            size_hint_y=None,
            height=dp(25),
            halign='left'
        )
        preview_label.bind(size=preview_label.setter('text_size'))
        
        self.preview_layout = BoxLayout(size_hint_y=None, height=dp(50))
        self.update_preview()
        
        preview_section.add_widget(preview_label)
        preview_section.add_widget(self.preview_layout)
        self.add_widget(preview_section)
        
        # Vincular eventos
        self.name_input.bind(text=lambda x, y: self.update_preview())
        self.icon_spinner.bind(text=lambda x, y: self.update_preview())
        
        # Espaçador
        self.add_widget(Widget(size_hint_y=0.5))
        
        # Botões
        buttons_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(15)
        )
        
        cancel_btn = ModernButton(
            text='Cancelar',
            button_type='secondary'
        )
        cancel_btn.bind(on_press=self.cancel_form)
        
        save_btn = ModernButton(
            text='Salvar Categoria',
            button_type='success'
        )
        save_btn.bind(on_press=self.save_category)
        
        buttons_layout.add_widget(cancel_btn)
        buttons_layout.add_widget(save_btn)
        self.add_widget(buttons_layout)
    
    def on_color_selected(self, color):
        """Callback quando cor é selecionada"""
        self.selected_color = color
        self.update_preview()
    
    def populate_form(self, category):
        """Preenche o formulário para edição"""
        self.name_input.text = category['name']
        self.selected_color = category['color']
        self.color_picker.selected_color = category['color']
        self.color_picker.select_color(category['color'])
        
        # Encontrar ícone correspondente
        icon_name = category['icon']
        for value in self.icon_spinner.values:
            if icon_name in value:
                self.icon_spinner.text = value
                break
        
        self.update_preview()
    
    def update_preview(self):
        """Atualiza o preview da categoria"""
        self.preview_layout.clear_widgets()
        
        # Converter cor hex para RGB
        try:
            color_hex = self.selected_color.lstrip('#')
            r = int(color_hex[0:2], 16) / 255.0
            g = int(color_hex[2:4], 16) / 255.0
            b = int(color_hex[4:6], 16) / 255.0
            color = (r, g, b, 1)
        except:
            color = (0.2, 0.6, 1, 1)
        
        # Preview card
        preview_card = ModernCard(
            orientation='horizontal',
            bg_color=(*color[:3], 0.1),
            border_color=color,
            size_hint_y=None,
            height=dp(45),
            padding=dp(10),
            spacing=dp(10)
        )
        
        # Ícone
        icon_emoji = self.icon_spinner.text.split(' ')[0] if self.icon_spinner.text else '📁'
        icon_label = Label(
            text=icon_emoji,
            font_size=dp(20),
            size_hint_x=None,
            width=dp(30)
        )
        
        # Nome
        name_label = Label(
            text=self.name_input.text or 'Nova Categoria',
            font_size=dp(16),
            bold=True,
            color=color,
            halign='left'
        )
        name_label.bind(size=name_label.setter('text_size'))
        
        preview_card.add_widget(icon_label)
        preview_card.add_widget(name_label)
        self.preview_layout.add_widget(preview_card)
    
    def save_category(self, instance):
        """Salva a categoria"""
        name = self.name_input.text.strip()
        
        if not name:
            self.show_error('O nome da categoria é obrigatório!')
            return
        
        # Extrair nome do ícone
        icon_text = self.icon_spinner.text
        icon_name = icon_text.split(' ')[1] if ' ' in icon_text else 'folder'
        
        try:
            if self.category:
                # Editar categoria existente
                result = self.controller.update_category(
                    self.category['id'],
                    name,
                    icon_name,
                    self.selected_color
                )
            else:
                # Criar nova categoria
                result = self.controller.add_category(
                    name,
                    icon_name,
                    self.selected_color
                )
            
            if result['success']:
                self.show_success(result['message'])
                if self.callback:
                    self.callback()
            else:
                self.show_error(result['message'])
                
        except Exception as e:
            self.show_error(f'Erro ao salvar categoria: {str(e)}')
    
    def cancel_form(self, instance):
        """Cancela o formulário"""
        if self.callback:
            self.callback()
    
    def show_error(self, message):
        """Mostra mensagem de erro"""
        popup = Popup(
            title='Erro',
            content=Label(
                text=message,
                text_size=(dp(250), None),
                halign='center',
                valign='middle'
            ),
            size_hint=(0.8, 0.3),
            auto_dismiss=True
        )
        popup.open()
    
    def show_success(self, message):
        """Mostra mensagem de sucesso"""
        popup = Popup(
            title='Sucesso',
            content=Label(
                text=message,
                text_size=(dp(250), None),
                halign='center',
                valign='middle'
            ),
            size_hint=(0.8, 0.3),
            auto_dismiss=True
        )
        popup.open()

class CategoryCard(ModernCard):
    """Card moderno para exibir categoria"""
    
    def __init__(self, category, edit_callback=None, delete_callback=None, **kwargs):
        super().__init__(
            orientation='horizontal',
            bg_color=(1, 1, 1, 1),
            border_color=(0.9, 0.9, 0.9, 1),
            **kwargs
        )
        self.category = category
        self.edit_callback = edit_callback
        self.delete_callback = delete_callback
        
        self.size_hint_y = None
        self.height = dp(80)
        self.padding = dp(15)
        self.spacing = dp(15)
        
        self.build_card()
    
    def build_card(self):
        """Constrói o card da categoria"""
        
        # Converter cor hex para RGB
        try:
            color_hex = self.category['color'].lstrip('#')
            r = int(color_hex[0:2], 16) / 255.0
            g = int(color_hex[2:4], 16) / 255.0
            b = int(color_hex[4:6], 16) / 255.0
            color = (r, g, b, 1)
        except:
            color = (0.2, 0.6, 1, 1)
        
        # Seção do ícone
        icon_section = BoxLayout(
            orientation='vertical',
            size_hint_x=None,
            width=dp(60)
        )
        
        # Círculo colorido com ícone
        icon_bg = Widget(size_hint_y=None, height=dp(50))
        with icon_bg.canvas:
            Color(*color)
            self.icon_circle = RoundedRectangle(
                size=(dp(50), dp(50)),
                pos=icon_bg.pos,
                radius=[dp(25)]
            )
        
        icon_bg.bind(pos=self.update_icon_pos)
        
        icon_label = Label(
            text='●',
            font_size=dp(24),
            color=(1, 1, 1, 1),
            bold=True
        )
        
        icon_bg.add_widget(icon_label)
        icon_section.add_widget(icon_bg)
        
        # Seção de informações
        info_section = BoxLayout(
            orientation='vertical',
            size_hint_x=0.6
        )
        
        # Nome da categoria
        name_label = Label(
            text=self.category['name'],
            font_size=dp(18),
            bold=True,
            color=(0.2, 0.2, 0.2, 1),
            halign='left',
            valign='middle'
        )
        name_label.bind(size=name_label.setter('text_size'))
        
        # Detalhes
        details_text = f"🎨 {self.category['color']} • 📁 {self.category['icon']}"
        details_label = Label(
            text=details_text,
            font_size=dp(12),
            color=(0.6, 0.6, 0.6, 1),
            halign='left',
            valign='middle'
        )
        details_label.bind(size=details_label.setter('text_size'))
        
        info_section.add_widget(name_label)
        info_section.add_widget(details_label)
        
        # Seção de ações
        actions_section = BoxLayout(
            orientation='vertical',
            size_hint_x=None,
            width=dp(80),
            spacing=dp(5)
        )
        
        edit_btn = ModernButton(
            text='Editar',
            button_type='primary',
            size_hint_y=None,
            height=dp(30),
            font_size=dp(12)
        )
        edit_btn.bind(on_press=lambda x: self.edit_category())
        
        delete_btn = ModernButton(
            text='Excluir',
            button_type='danger',
            size_hint_y=None,
            height=dp(30),
            font_size=dp(12)
        )
        delete_btn.bind(on_press=lambda x: self.delete_category())
        
        actions_section.add_widget(edit_btn)
        actions_section.add_widget(delete_btn)
        
        # Adicionar seções ao card
        self.add_widget(icon_section)
        self.add_widget(info_section)
        self.add_widget(actions_section)
    
    def update_icon_pos(self, instance, pos):
        """Atualiza posição do ícone"""
        self.icon_circle.pos = (pos[0] + dp(5), pos[1])
    
    def edit_category(self):
        """Chama callback de edição"""
        if self.edit_callback:
            self.edit_callback(self.category)
    
    def delete_category(self):
        """Chama callback de exclusão"""
        if self.delete_callback:
            self.delete_callback(self.category)

class CategoriesScreen(Screen):
    """Tela moderna de gerenciamento de categorias"""
    
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.name = 'categories'
        self.controller = controller
        self.categories = []
        
        # Definir cor de fundo
        with self.canvas.before:
            Color(0.96, 0.96, 0.96, 1)  # Fundo cinza claro
            self.bg = Rectangle(size=self.size, pos=self.pos)
        
        self.bind(size=self.update_bg, pos=self.update_bg)
        
        self.build_ui()
        self.load_categories()
    
    def update_bg(self, *args):
        """Atualiza o fundo"""
        self.bg.size = self.size
        self.bg.pos = self.pos
    
    def build_ui(self):
        """Constrói a interface moderna"""
        main_layout = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20)
        )
        
        # Cabeçalho moderno
        header = ModernCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            bg_color=(0.13, 0.59, 0.95, 1),
            border_color=(0.13, 0.59, 0.95, 1),
            padding=dp(20),
            spacing=dp(10)
        )
        
        title_label = Label(
            text='Gerenciar Categorias',
            font_size=dp(28),
            bold=True,
            color=(1, 1, 1, 1)
        )
        
        subtitle_label = Label(
            text='Organize suas transações com categorias personalizadas',
            font_size=dp(14),
            color=(0.9, 0.9, 1, 1)
        )
        
        header.add_widget(title_label)
        header.add_widget(subtitle_label)
        main_layout.add_widget(header)
        
        # Barra de ações
        actions_bar = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(15)
        )
        
        add_btn = ModernButton(
            text='+ Nova Categoria',
            button_type='success',
            size_hint_x=0.6
        )
        add_btn.bind(on_press=self.show_add_form)
        
        refresh_btn = ModernButton(
            text='🔄 Atualizar',
            button_type='primary',
            size_hint_x=0.4
        )
        refresh_btn.bind(on_press=lambda x: self.load_categories())
        
        actions_bar.add_widget(add_btn)
        actions_bar.add_widget(refresh_btn)
        main_layout.add_widget(actions_bar)
        
        # Lista de categorias
        self.scroll_view = ScrollView()
        self.categories_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None,
            padding=[0, dp(10), 0, dp(10)]
        )
        self.categories_layout.bind(minimum_height=self.categories_layout.setter('height'))
        
        self.scroll_view.add_widget(self.categories_layout)
        main_layout.add_widget(self.scroll_view)
        
        self.add_widget(main_layout)
    
    def load_categories(self):
        """Carrega as categorias"""
        try:
            categories = self.controller.get_categories()
            self.categories = categories
            self.update_categories_list()
        except Exception as e:
            print(f"Erro ao carregar categorias: {e}")
            self.show_error('Erro ao carregar categorias')
    
    def update_categories_list(self):
        """Atualiza a lista de categorias"""
        self.categories_layout.clear_widgets()
        
        if not self.categories:
            # Mensagem quando não há categorias
            empty_card = ModernCard(
                orientation='vertical',
                size_hint_y=None,
                height=dp(150),
                bg_color=(1, 1, 1, 1),
                border_color=(0.9, 0.9, 0.9, 1),
                padding=dp(30)
            )
            
            empty_icon = Label(
                text='📁',
                font_size=dp(48),
                size_hint_y=None,
                height=dp(60)
            )
            
            empty_text = Label(
                text='Nenhuma categoria encontrada\nClique em "Nova Categoria" para começar',
                font_size=dp(16),
                color=(0.6, 0.6, 0.6, 1),
                halign='center'
            )
            empty_text.bind(size=empty_text.setter('text_size'))
            
            empty_card.add_widget(empty_icon)
            empty_card.add_widget(empty_text)
            self.categories_layout.add_widget(empty_card)
            return
        
        # Adicionar cards das categorias
        for category in self.categories:
            card = CategoryCard(
                category,
                edit_callback=self.edit_category,
                delete_callback=self.confirm_delete_category
            )
            self.categories_layout.add_widget(card)
    
    def show_add_form(self, instance):
        """Mostra formulário de adicionar categoria"""
        form = CategoryForm(
            self.controller,
            callback=self.close_form
        )
        
        popup = Popup(
            title='',
            content=form,
            size_hint=(0.9, 0.9),
            auto_dismiss=False,
            separator_height=0
        )
        
        self.form_popup = popup
        popup.open()
    
    def edit_category(self, category):
        """Mostra formulário de editar categoria"""
        form = CategoryForm(
            self.controller,
            callback=self.close_form,
            category=category
        )
        
        popup = Popup(
            title='',
            content=form,
            size_hint=(0.9, 0.9),
            auto_dismiss=False,
            separator_height=0
        )
        
        self.form_popup = popup
        popup.open()
    
    def close_form(self):
        """Fecha o formulário e atualiza a lista"""
        if hasattr(self, 'form_popup'):
            self.form_popup.dismiss()
        self.load_categories()
    
    def confirm_delete_category(self, category):
        """Confirma exclusão da categoria"""
        content = ModernCard(
            orientation='vertical',
            bg_color=(1, 1, 1, 1),
            border_color=(0.96, 0.26, 0.21, 1),
            padding=dp(20),
            spacing=dp(20)
        )
        
        # Ícone de aviso
        warning_icon = Label(
            text='⚠️',
            font_size=dp(48),
            size_hint_y=None,
            height=dp(60)
        )
        
        # Texto de confirmação
        confirm_text = Label(
            text=f'Deseja realmente excluir a categoria:\n\n"{category["name"]}"?\n\nEsta ação não pode ser desfeita!',
            font_size=dp(16),
            color=(0.3, 0.3, 0.3, 1),
            halign='center'
        )
        confirm_text.bind(size=confirm_text.setter('text_size'))
        
        # Botões
        buttons_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(15)
        )
        
        cancel_btn = ModernButton(
            text='Cancelar',
            button_type='secondary'
        )
        
        confirm_btn = ModernButton(
            text='Sim, Excluir',
            button_type='danger'
        )
        
        buttons_layout.add_widget(cancel_btn)
        buttons_layout.add_widget(confirm_btn)
        
        content.add_widget(warning_icon)
        content.add_widget(confirm_text)
        content.add_widget(buttons_layout)
        
        popup = Popup(
            title='',
            content=content,
            size_hint=(0.8, 0.5),
            auto_dismiss=False,
            separator_height=0
        )
        
        cancel_btn.bind(on_press=popup.dismiss)
        confirm_btn.bind(on_press=lambda x: self.delete_category(category, popup))
        
        popup.open()
    
    def delete_category(self, category, popup):
        """Exclui a categoria"""
        popup.dismiss()
        
        # Implementar exclusão futuramente
        info_content = ModernCard(
            orientation='vertical',
            bg_color=(1, 1, 1, 1),
            border_color=(0.13, 0.59, 0.95, 1),
            padding=dp(20),
            spacing=dp(15)
        )
        
        info_icon = Label(
            text='ℹ️',
            font_size=dp(36),
            size_hint_y=None,
            height=dp(50)
        )
        
        info_text = Label(
            text='Exclusão de categorias será implementada em breve.\n\nPor segurança, categorias com transações\nassociadas não podem ser removidas.',
            font_size=dp(14),
            color=(0.4, 0.4, 0.4, 1),
            halign='center'
        )
        info_text.bind(size=info_text.setter('text_size'))
        
        ok_btn = ModernButton(
            text='Entendi',
            button_type='primary',
            size_hint_y=None,
            height=dp(40)
        )
        
        info_content.add_widget(info_icon)
        info_content.add_widget(info_text)
        info_content.add_widget(ok_btn)
        
        info_popup = Popup(
            title='',
            content=info_content,
            size_hint=(0.8, 0.4),
            auto_dismiss=False,
            separator_height=0
        )
        
        ok_btn.bind(on_press=info_popup.dismiss)
        info_popup.open()
    
    def show_error(self, message):
        """Mostra mensagem de erro"""
        popup = Popup(
            title='Erro',
            content=Label(text=message),
            size_hint=(0.8, 0.3),
            auto_dismiss=True
        )
        popup.open()
