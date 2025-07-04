"""
Dashboard principal da aplicação
Mostra resumo financeiro, gráficos e transações recentes
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.uix.widget import Widget
from kivy.clock import Clock
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from kivy.uix.image import Image
import io
import threading

class PieChartWidget(Widget):
    """Widget personalizado para gráfico de pizza"""
    
    def __init__(self, data=None, **kwargs):
        super().__init__(**kwargs)
        self.data = data or []
        self.bind(size=self.update_chart, pos=self.update_chart)
    
    def update_chart(self, *args):
        """Atualiza o gráfico quando o tamanho muda"""
        if self.data:
            Clock.schedule_once(lambda dt: self._draw_chart(), 0.1)
    
    def _draw_chart(self):
        """Desenha o gráfico de pizza"""
        if not self.data:
            return
        
        try:
            # Criar figura matplotlib
            fig, ax = plt.subplots(figsize=(4, 4), facecolor='none')
            
            # Preparar dados
            categories = [item['category'] for item in self.data[:6]]  # Top 6
            values = [item['amount'] for item in self.data[:6]]
            colors = [item['color'] for item in self.data[:6]]
            
            # Criar gráfico de pizza
            wedges, texts, autotexts = ax.pie(
                values, 
                labels=categories, 
                colors=colors,
                autopct='%1.1f%%',
                startangle=90,
                textprops={'fontsize': 8}
            )
            
            ax.set_title('Gastos por Categoria', fontsize=10, pad=20)
            
            # Converter para imagem
            canvas = FigureCanvasAgg(fig)
            canvas.draw()
            buf = io.BytesIO()
            canvas.print_png(buf)
            buf.seek(0)
            
            # Limpar widgets antigos
            self.clear_widgets()
            
            # Adicionar imagem
            img = Image()
            img.texture = Image(source='').texture  # Placeholder
            
            # Salvar temporariamente
            with open('temp_chart.png', 'wb') as f:
                f.write(buf.getvalue())
            
            img.source = 'temp_chart.png'
            self.add_widget(img)
            
            plt.close(fig)
            
        except Exception as e:
            print(f"Erro ao criar gráfico: {e}")

class DashboardCard(BoxLayout):
    """Card personalizado para métricas do dashboard"""
    
    def __init__(self, title, value, color=(0.2, 0.6, 1, 1), **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.size_hint_y = None
        self.height = '80dp'
        self.padding = '10dp'
        self.spacing = '5dp'
        
        # Desenhar fundo
        with self.canvas.before:
            Color(*color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        self.bind(size=self.update_rect, pos=self.update_rect)
        
        # Título
        title_label = Label(
            text=title,
            font_size='14dp',
            color=(1, 1, 1, 1),
            size_hint_y=0.4
        )
        
        # Valor
        value_label = Label(
            text=str(value),
            font_size='20dp',
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=0.6
        )
        
        self.add_widget(title_label)
        self.add_widget(value_label)
    
    def update_rect(self, instance, value):
        """Atualiza o retângulo de fundo"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class TransactionItem(BoxLayout):
    """Item de transação para lista"""
    
    def __init__(self, transaction, **kwargs):
        super().__init__(orientation='horizontal', **kwargs)
        self.size_hint_y = None
        self.height = '60dp'
        self.padding = '10dp'
        self.spacing = '10dp'
        
        # Cor de fundo baseada no tipo
        bg_color = (0.2, 0.7, 0.2, 0.3) if transaction['type'] == 'income' else (0.7, 0.2, 0.2, 0.3)
        
        with self.canvas.before:
            Color(*bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        self.bind(size=self.update_rect, pos=self.update_rect)
        
        # Informações da transação
        info_layout = BoxLayout(orientation='vertical', size_hint_x=0.7)
        
        # Descrição
        desc_label = Label(
            text=transaction.get('description', 'Sem descrição'),
            font_size='16dp',
            text_size=(None, None),
            halign='left',
            size_hint_y=0.6
        )
        
        # Categoria e data
        details = f"{transaction.get('category_name', 'N/A')} • {transaction['date']}"
        details_label = Label(
            text=details,
            font_size='12dp',
            color=(0.7, 0.7, 0.7, 1),
            text_size=(None, None),
            halign='left',
            size_hint_y=0.4
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
            size_hint_x=0.3
        )
        
        self.add_widget(info_layout)
        self.add_widget(amount_label)
    
    def update_rect(self, instance, value):
        """Atualiza o retângulo de fundo"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class DashboardScreen(Screen):
    """Tela principal do dashboard"""
    
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.name = 'dashboard'
        self.controller = controller
        self.build_ui()
        self.refresh_data()
    
    def build_ui(self):
        """Constrói a interface do dashboard"""
        main_layout = BoxLayout(orientation='vertical', padding='10dp', spacing='10dp')
        
        # Título
        title_label = Label(
            text='Dashboard Financeiro',
            font_size='24dp',
            bold=True,
            size_hint_y=None,
            height='40dp'
        )
        main_layout.add_widget(title_label)
        
        # ScrollView para o conteúdo
        scroll = ScrollView()
        content_layout = BoxLayout(orientation='vertical', spacing='15dp', size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # Cards de resumo
        self.cards_layout = GridLayout(cols=3, spacing='10dp', size_hint_y=None, height='100dp')
        content_layout.add_widget(self.cards_layout)
        
        # Gráfico de gastos por categoria
        chart_title = Label(
            text='Gastos por Categoria (Mês Atual)',
            font_size='18dp',
            bold=True,
            size_hint_y=None,
            height='30dp'
        )
        content_layout.add_widget(chart_title)
        
        self.chart_widget = PieChartWidget(size_hint_y=None, height='300dp')
        content_layout.add_widget(self.chart_widget)
        
        # Transações recentes
        transactions_title = Label(
            text='Transações Recentes',
            font_size='18dp',
            bold=True,
            size_hint_y=None,
            height='30dp'
        )
        content_layout.add_widget(transactions_title)
        
        self.transactions_layout = BoxLayout(orientation='vertical', spacing='5dp', size_hint_y=None)
        self.transactions_layout.bind(minimum_height=self.transactions_layout.setter('height'))
        content_layout.add_widget(self.transactions_layout)
        
        # Botão de atualizar
        refresh_btn = Button(
            text='Atualizar Dashboard',
            size_hint_y=None,
            height='40dp',
            background_color=(0.2, 0.6, 1, 1)
        )
        refresh_btn.bind(on_press=lambda x: self.refresh_data())
        content_layout.add_widget(refresh_btn)
        
        scroll.add_widget(content_layout)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def refresh_data(self):
        """Atualiza os dados do dashboard"""
        def update_ui(dt=None):
            try:
                # Obter dados do controlador
                data = self.controller.get_dashboard_data()
                
                # Atualizar cards de resumo
                self.update_summary_cards(data['monthly_summary'])
                
                # Atualizar gráfico
                self.update_chart(data['category_expenses'])
                
                # Atualizar transações recentes
                self.update_recent_transactions(data['recent_transactions'])
                
            except Exception as e:
                print(f"Erro ao atualizar dashboard: {e}")
        
        # Executar na thread principal usando Clock
        Clock.schedule_once(update_ui, 0.1)
    
    def update_summary_cards(self, summary):
        """Atualiza os cards de resumo"""
        self.cards_layout.clear_widgets()
        
        # Card de receitas
        income_card = DashboardCard(
            'Receitas',
            f"R$ {summary['income']:.2f}",
            color=(0.2, 0.7, 0.2, 1)
        )
        
        # Card de despesas
        expense_card = DashboardCard(
            'Despesas',
            f"R$ {summary['expense']:.2f}",
            color=(0.7, 0.2, 0.2, 1)
        )
        
        # Card de saldo
        balance_color = (0.2, 0.7, 0.2, 1) if summary['balance'] >= 0 else (0.7, 0.2, 0.2, 1)
        balance_card = DashboardCard(
            'Saldo',
            f"R$ {summary['balance']:.2f}",
            color=balance_color
        )
        
        self.cards_layout.add_widget(income_card)
        self.cards_layout.add_widget(expense_card)
        self.cards_layout.add_widget(balance_card)
    
    def update_chart(self, category_expenses):
        """Atualiza o gráfico de pizza"""
        if category_expenses:
            self.chart_widget.data = category_expenses
            self.chart_widget.update_chart()
    
    def update_recent_transactions(self, transactions):
        """Atualiza a lista de transações recentes"""
        self.transactions_layout.clear_widgets()
        
        if not transactions:
            no_data_label = Label(
                text='Nenhuma transação encontrada',
                font_size='14dp',
                color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None,
                height='40dp'
            )
            self.transactions_layout.add_widget(no_data_label)
            return
        
        for transaction in transactions[:5]:  # Mostrar apenas as 5 mais recentes
            item = TransactionItem(transaction)
            self.transactions_layout.add_widget(item)
