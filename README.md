# CashControl - Aplicativo de Finanças Pessoais

Um aplicativo completo de controle de finanças pessoais desenvolvido em Python usando Kivy.

## Funcionalidades

### 📊 Dashboard Principal
- Saldo atual (receitas - despesas)
- Resumo do mês atual
- Gráfico de pizza das principais categorias de gastos
- Últimas 5 transações

### 💰 Gestão de Transações
- Adicionar receitas e despesas
- Editar e excluir transações
- Filtros por tipo e categoria
- Categorização automática

### 📈 Categorias
- Categorias pré-definidas (Alimentação, Transporte, Lazer, etc.)
- **🆕 Interface para gerenciar categorias** - Crie, visualize e organize suas categorias personalizadas
- **🆕 Acesso via menu principal** - Botão dedicado na barra de navegação
- Ícones e cores para cada categoria
- Integração automática com transações e relatórios

### 📊 Relatórios
- Gráficos de barras e pizza
- Relatórios por categoria e período
- Exportação para CSV
- Análise de tendências

### ⚙️ Recursos Adicionais
- Backup e restauração de dados
- Interface responsiva
- Tema moderno e intuitivo
- Configurações personalizáveis
- **🆕 Gerenciamento completo de categorias personalizadas**

## 📋 Documentação Adicional

- **[CATEGORIAS.md](CATEGORIAS.md)** - Guia completo para gerenciar categorias personalizadas
- **[FUNCIONALIDADES.md](FUNCIONALIDADES.md)** - Lista detalhada de todas as funcionalidades
- **[GUIA_USO.md](GUIA_USO.md)** - Manual de uso do aplicativo

## Tecnologias Utilizadas

- **Python 3.7+**
- **Kivy** - Framework para interface gráfica
- **SQLite** - Banco de dados local
- **Matplotlib** - Geração de gráficos
- **KivyMD** - Componentes Material Design

## Estrutura do Projeto

```
CashControl/
├── main.py                    # Aplicação principal
├── models/                    # Modelos de dados
│   ├── __init__.py
│   ├── database.py           # Gerenciamento do banco SQLite
│   └── transaction.py        # Modelo de transações e categorias
├── views/                     # Interface do usuário
│   ├── __init__.py
│   ├── dashboard.py          # Tela do dashboard
│   ├── transactions.py       # Tela de transações
│   └── reports.py            # Tela de relatórios
├── controllers/               # Lógica de negócio
│   ├── __init__.py
│   └── finance_controller.py # Controlador principal
└── assets/                   # Recursos (ícones, imagens)
    └── icons/
```

## Instalação

1. **Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd CashControl
```

2. **Crie um ambiente virtual:**
```bash
python -m venv .venv
```

3. **Ative o ambiente virtual:**

Windows:
```bash
.venv\Scripts\activate
```

Linux/Mac:
```bash
source .venv/bin/activate
```

4. **Instale as dependências:**
```bash
pip install kivy matplotlib kivymd pillow
```

## Executando o Aplicativo

```bash
python main.py
```

## Como Usar

### Primeiro Uso
1. Execute o aplicativo
2. Uma tela de boas-vindas será exibida
3. Comece adicionando suas primeiras transações

### Adicionando Transações
1. Vá para a aba "Transações"
2. Clique em "+ Nova"
3. Preencha os dados da transação
4. Selecione o tipo (Receita/Despesa)
5. Escolha uma categoria
6. Salve a transação

### Visualizando Relatórios
1. Acesse a aba "Relatórios"
2. Selecione o mês/ano desejado
3. Visualize gráficos e análises
4. Exporte dados para CSV se necessário

### Gerenciando Categorias
- As categorias padrão são criadas automaticamente
- Você pode criar novas categorias conforme necessário
- Cada categoria tem ícone e cor personalizáveis

## Funcionalidades Técnicas

### Banco de Dados
- SQLite para armazenamento local
- Tabelas: transactions, categories, budgets, goals, settings
- Backup automático disponível

### Interface
- Design responsivo
- Navegação por abas
- Gráficos interativos
- Formulários de validação

### Segurança
- Validação de dados de entrada
- Tratamento de erros
- Backup de segurança

## Backup e Restauração

### Criar Backup
1. Vá em Configurações
2. Clique em "Criar Backup"
3. Um arquivo .db será gerado

### Restaurar Backup
1. Coloque o arquivo de backup na pasta do app
2. Use a função "Restaurar Backup"

## Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Roadmap

- [ ] Sincronização em nuvem
- [ ] Notificações push
- [ ] Metas de economia
- [ ] Controle de orçamento
- [ ] Relatórios avançados
- [ ] Tema escuro
- [ ] Multi-idiomas

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Suporte

Para reportar bugs ou solicitar funcionalidades, abra uma issue no GitHub.

---

**CashControl** - Controle suas finanças de forma simples e eficiente! 💰📊
