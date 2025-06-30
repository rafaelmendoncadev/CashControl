"""
Tela de relatórios financeiros
Exibe gráficos e análises das transações
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line
from datetime import datetime, date
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io
import threading
import os

class ChartWidget(Widget):
    """Widget base para gráficos"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chart_data = None
        self.chart_type = 'bar'
        self.bind(size=self.update_chart, pos=self.update_chart)
    
    def set_data(self, data, chart_type='bar'):
        """Define os dados do gráfico"""
        self.chart_data = data
        self.chart_type = chart_type
        self.update_chart()
    
    def update_chart(self, *args):
        """Atualiza o gráfico"""
        if self.chart_data:
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self._draw_chart(), 0.1)
    
    def _draw_chart(self):
        """Desenha o gráfico"""
        if not self.chart_data:
            return
        
        try:
            # Limpar widgets antigos
            self.clear_widgets()
            
            # Criar figura matplotlib
            fig, ax = plt.subplots(figsize=(8, 6), facecolor='white')
            
            if self.chart_type == 'bar':
                self._draw_bar_chart(ax)
            elif self.chart_type == 'line':
                self._draw_line_chart(ax)
            elif self.chart_type == 'pie':
                self._draw_pie_chart(ax)
            
            # Salvar como imagem temporária
            temp_file = 'temp_report_chart.png'
            fig.savefig(temp_file, dpi=100, bbox_inches='tight', facecolor='white')
            plt.close(fig)
            
            # Adicionar imagem ao widget
            img = Image(source=temp_file)
            self.add_widget(img)
            
        except Exception as e:
            print(f"Erro ao criar gráfico: {e}")
    
    def _draw_bar_chart(self, ax):
        """Desenha gráfico de barras"""
        if 'categories' in self.chart_data:
            # Gráfico de barras por categoria
            categories = [item['category'] for item in self.chart_data['categories']]
            values = [item['amount'] for item in self.chart_data['categories']]
            colors = [item.get('color', '#2196F3') for item in self.chart_data['categories']]
            
            bars = ax.bar(categories, values, color=colors)
            ax.set_title('Gastos por Categoria', fontsize=14)
            ax.set_ylabel('Valor (R$)', fontsize=12)
            
            # Rotacionar labels se necessário
            if len(categories) > 5:
                ax.tick_params(axis='x', rotation=45)
            
            # Adicionar valores nas barras
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'R$ {value:.0f}', ha='center', va='bottom', fontsize=10)
        
        elif 'monthly' in self.chart_data:
            # Gráfico de receitas vs despesas por mês
            months = self.chart_data['monthly']['months']
            income = self.chart_data['monthly']['income']
            expenses = self.chart_data['monthly']['expenses']
            
            x = range(len(months))
            width = 0.35
            
            ax.bar([i - width/2 for i in x], income, width, label='Receitas', color='#4CAF50')
            ax.bar([i + width/2 for i in x], expenses, width, label='Despesas', color='#F44336')
            
            ax.set_title('Receitas vs Despesas por Mês', fontsize=14)
            ax.set_ylabel('Valor (R$)', fontsize=12)
            ax.set_xticks(x)
            ax.set_xticklabels(months)
            ax.legend()
    
    def _draw_line_chart(self, ax):
        """Desenha gráfico de linha"""
        if 'evolution' in self.chart_data:
            dates = self.chart_data['evolution']['dates']
            balances = self.chart_data['evolution']['balances']
            
            ax.plot(dates, balances, marker='o', linewidth=2, color='#2196F3')
            ax.set_title('Evolução do Saldo', fontsize=14)
            ax.set_ylabel('Saldo (R$)', fontsize=12)
            ax.grid(True, alpha=0.3)
            
            # Colorir área positiva/negativa
            ax.fill_between(dates, balances, 0, 
                           where=[b >= 0 for b in balances], 
                           color='green', alpha=0.3, interpolate=True)
            ax.fill_between(dates, balances, 0, 
                           where=[b < 0 for b in balances], 
                           color='red', alpha=0.3, interpolate=True)
    
    def _draw_pie_chart(self, ax):
        """Desenha gráfico de pizza"""
        if 'categories' in self.chart_data:
            categories = [item['category'] for item in self.chart_data['categories'][:6]]
            values = [item['amount'] for item in self.chart_data['categories'][:6]]
            colors = [item.get('color', '#2196F3') for item in self.chart_data['categories'][:6]]
            
            wedges, texts, autotexts = ax.pie(
                values, 
                labels=categories, 
                colors=colors,
                autopct='%1.1f%%',
                startangle=90
            )
            
            ax.set_title('Distribuição de Gastos', fontsize=14)

class ReportCard(BoxLayout):
    """Card para exibir métricas dos relatórios"""
    
    def __init__(self, title, value, subtitle="", color=(0.2, 0.6, 1, 1), **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.size_hint_y = None
        self.height = '100dp'
        self.padding = '15dp'
        
        # Fundo do card
        with self.canvas.before:
            Color(*color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        self.bind(size=self.update_rect, pos=self.update_rect)
        
        # Título
        title_label = Label(
            text=title,
            font_size='14dp',
            color=(1, 1, 1, 1),
            size_hint_y=0.3
        )
        
        # Valor principal
        value_label = Label(
            text=str(value),
            font_size='22dp',
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=0.5
        )
        
        # Subtítulo
        if subtitle:
            subtitle_label = Label(
                text=subtitle,
                font_size='12dp',
                color=(0.9, 0.9, 0.9, 1),
                size_hint_y=0.2
            )
            self.add_widget(subtitle_label)
        
        self.add_widget(title_label)
        self.add_widget(value_label)
    
    def update_rect(self, instance, value):
        """Atualiza o retângulo de fundo"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class ReportsScreen(Screen):
    """Tela de relatórios"""
    
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.name = 'reports'
        self.controller = controller
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year
        self.build_ui()
        self.load_report_data()
    
    def build_ui(self):
        """Constrói a interface"""
        main_layout = BoxLayout(orientation='vertical', padding='10dp', spacing='10dp')
        
        # Cabeçalho
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
        
        title_label = Label(
            text='Relatórios',
            font_size='24dp',
            bold=True,
            size_hint_x=0.5
        )
        
        # Seletores de período
        period_layout = BoxLayout(orientation='horizontal', size_hint_x=0.5, spacing='10dp')
        
        self.month_spinner = Spinner(
            text=str(self.current_month),
            values=[str(i) for i in range(1, 13)],
            size_hint_x=0.3
        )
        self.month_spinner.bind(text=self.on_period_change)
        
        self.year_spinner = Spinner(
            text=str(self.current_year),
            values=[str(i) for i in range(2020, 2030)],
            size_hint_x=0.3
        )
        self.year_spinner.bind(text=self.on_period_change)
        
        update_btn = Button(
            text='Atualizar',
            size_hint_x=0.4,
            background_color=(0.2, 0.6, 1, 1)
        )
        update_btn.bind(on_press=self.update_reports)
        
        period_layout.add_widget(self.month_spinner)
        period_layout.add_widget(self.year_spinner)
        period_layout.add_widget(update_btn)
        
        header_layout.add_widget(title_label)
        header_layout.add_widget(period_layout)
        main_layout.add_widget(header_layout)
        
        # ScrollView para o conteúdo
        scroll = ScrollView()
        content_layout = BoxLayout(orientation='vertical', spacing='20dp', size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # Cards de resumo
        self.summary_layout = GridLayout(
            cols=3, 
            spacing='10dp', 
            size_hint_y=None, 
            height='120dp'
        )
        content_layout.add_widget(self.summary_layout)
        
        # Gráfico principal
        chart_title = Label(
            text='Gastos por Categoria',
            font_size='18dp',
            bold=True,
            size_hint_y=None,
            height='30dp'
        )
        content_layout.add_widget(chart_title)
        
        self.main_chart = ChartWidget(size_hint_y=None, height='400dp')
        content_layout.add_widget(self.main_chart)
        
        # Botões de ação
        actions_layout = BoxLayout(
            orientation='horizontal', 
            size_hint_y=None, 
            height='50dp',
            spacing='10dp'
        )
        
        export_btn = Button(
            text='Exportar CSV',
            background_color=(0.2, 0.7, 0.2, 1)
        )
        export_btn.bind(on_press=self.export_csv)
        
        chart_type_btn = Button(
            text='Tipo Gráfico',
            background_color=(0.6, 0.2, 0.8, 1)
        )
        chart_type_btn.bind(on_press=self.change_chart_type)
        
        actions_layout.add_widget(export_btn)
        actions_layout.add_widget(chart_type_btn)
        content_layout.add_widget(actions_layout)
        
        scroll.add_widget(content_layout)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def on_period_change(self, spinner, text):
        """Chamado quando o período é alterado"""
        try:
            self.current_month = int(self.month_spinner.text)
            self.current_year = int(self.year_spinner.text)
        except ValueError:
            pass
    
    def update_reports(self, instance):
        """Atualiza os relatórios"""
        self.load_report_data()
    
    def load_report_data(self):
        """Carrega os dados dos relatórios"""
        def load():
            try:
                # Obter relatório mensal
                report = self.controller.get_monthly_report(self.current_month, self.current_year)
                
                if report:
                    # Atualizar UI na thread principal
                    from kivy.clock import Clock
                    Clock.schedule_once(lambda dt: self.update_ui(report), 0)
                
            except Exception as e:
                print(f"Erro ao carregar relatórios: {e}")
        
        threading.Thread(target=load, daemon=True).start()
    
    def update_ui(self, report):
        """Atualiza a interface com os dados do relatório"""
        # Atualizar cards de resumo
        self.update_summary_cards(report['summary'])
        
        # Atualizar gráfico principal
        if report['category_expenses']:
            chart_data = {'categories': report['category_expenses']}
            self.main_chart.set_data(chart_data, 'bar')
    
    def update_summary_cards(self, summary):
        """Atualiza os cards de resumo"""
        self.summary_layout.clear_widgets()
        
        # Card de receitas
        income_card = ReportCard(
            'Receitas do Mês',
            f"R$ {summary['income']:.2f}",
            color=(0.2, 0.7, 0.2, 1)
        )
        
        # Card de despesas
        expense_card = ReportCard(
            'Despesas do Mês',
            f"R$ {summary['expense']:.2f}",
            color=(0.7, 0.2, 0.2, 1)
        )
        
        # Card de saldo
        balance_color = (0.2, 0.7, 0.2, 1) if summary['balance'] >= 0 else (0.7, 0.2, 0.2, 1)
        balance_card = ReportCard(
            'Saldo do Mês',
            f"R$ {summary['balance']:.2f}",
            subtitle='Receitas - Despesas',
            color=balance_color
        )
        
        self.summary_layout.add_widget(income_card)
        self.summary_layout.add_widget(expense_card)
        self.summary_layout.add_widget(balance_card)
    
    def change_chart_type(self, instance):
        """Permite alterar o tipo de gráfico"""
        content = BoxLayout(orientation='vertical', spacing='20dp')
        
        content.add_widget(Label(
            text='Selecione o tipo de gráfico:',
            size_hint_y=None,
            height='30dp'
        ))
        
        buttons_layout = BoxLayout(orientation='vertical', spacing='10dp')
        
        bar_btn = Button(text='Gráfico de Barras', background_color=(0.2, 0.6, 1, 1))
        pie_btn = Button(text='Gráfico de Pizza', background_color=(0.6, 0.2, 0.8, 1))
        
        buttons_layout.add_widget(bar_btn)
        buttons_layout.add_widget(pie_btn)
        content.add_widget(buttons_layout)
        
        popup = Popup(
            title='Tipo de Gráfico',
            content=content,
            size_hint=(0.8, 0.4),
            auto_dismiss=True
        )
        
        bar_btn.bind(on_press=lambda x: self.set_chart_type('bar', popup))
        pie_btn.bind(on_press=lambda x: self.set_chart_type('pie', popup))
        
        popup.open()
    
    def set_chart_type(self, chart_type, popup):
        """Define o tipo de gráfico"""
        popup.dismiss()
        
        # Recarregar gráfico com novo tipo
        if hasattr(self.main_chart, 'chart_data') and self.main_chart.chart_data:
            self.main_chart.set_data(self.main_chart.chart_data, chart_type)
    
    def export_csv(self, instance):
        """Exporta relatório para CSV"""
        try:
            # Definir período
            start_date = date(self.current_year, self.current_month, 1)
            if self.current_month == 12:
                end_date = date(self.current_year + 1, 1, 1)
            else:
                end_date = date(self.current_year, self.current_month + 1, 1)
            
            # Nome do arquivo
            filename = f"relatorio_{self.current_month:02d}_{self.current_year}.csv"
            filepath = os.path.join(os.getcwd(), filename)
            
            # Exportar
            result = self.controller.export_to_csv(start_date, end_date, filepath)
            
            # Mostrar resultado
            popup = Popup(
                title='Exportação',
                content=Label(text=result['message']),
                size_hint=(0.8, 0.3),
                auto_dismiss=True
            )
            popup.open()
            
        except Exception as e:
            popup = Popup(
                title='Erro',
                content=Label(text=f'Erro ao exportar: {str(e)}'),
                size_hint=(0.8, 0.3),
                auto_dismiss=True
            )
            popup.open()
