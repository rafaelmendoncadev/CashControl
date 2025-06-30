# GUIA DE USO - CashControl

## 🚀 Como Executar o Aplicativo

### Método 1: Usando o arquivo batch (Windows)
1. Clique duas vezes em `run_app.bat`
2. O aplicativo será iniciado automaticamente

### Método 2: Via linha de comando
```bash
# Ativar ambiente virtual
.venv\Scripts\activate

# Executar aplicativo
python main.py
```

## 📋 Funcionalidades Principais

### 1. Dashboard
- **Saldo Atual**: Mostra receitas - despesas
- **Resumo Mensal**: Estatísticas do mês atual
- **Gráfico de Categorias**: Pizza com principais gastos
- **Transações Recentes**: Últimas 5 transações

### 2. Transações
- **Adicionar Nova**: Botão "+ Nova" no topo
- **Tipos Disponíveis**: Receita ou Despesa
- **Campos Obrigatórios**: Valor, Categoria
- **Editar/Excluir**: Botões em cada transação
- **Filtros**: Por tipo (Todos, Receitas, Despesas)

### 3. Relatórios
- **Período**: Selecione mês/ano
- **Gráficos**: Barras e pizza
- **Exportação**: CSV com todas as transações
- **Análises**: Resumos por categoria

### 4. Configurações
- **Backup**: Criar cópia de segurança
- **Restauração**: Recuperar dados
- **Sobre**: Informações do aplicativo

## 🏷️ Categorias Padrão

O sistema vem com as seguintes categorias pré-configuradas:

**Despesas:**
- 🍕 Alimentação
- 🚗 Transporte  
- 🎬 Lazer
- 🏥 Saúde
- 📚 Educação
- 🏠 Casa
- 👕 Roupas

**Receitas:**
- 💰 Salário
- 💻 Freelance
- 📈 Investimentos
- ❓ Outros

## 💡 Dicas de Uso

### Para Iniciantes
1. **Primeiro Uso**: Execute o aplicativo e siga a tela de boas-vindas
2. **Adicione Transações**: Comece com suas transações mais recentes
3. **Use Categorias**: Mantenha uma organização consistente
4. **Verifique o Dashboard**: Acompanhe seu saldo regularmente

### Para Usuários Avançados
1. **Backup Regular**: Faça backups semanais dos dados
2. **Análise Mensal**: Use relatórios para análise de gastos
3. **Categorias Personalizadas**: Crie categorias específicas para suas necessidades
4. **Exportação CSV**: Use para análises externas ou backup

## 🔧 Utilitários Auxiliares

### setup_util.py
Ferramenta de configuração e testes:

```bash
python setup_util.py
```

**Opções disponíveis:**
1. **Criar dados de exemplo** - Popula o banco com transações teste
2. **Mostrar informações** - Exibe estatísticas do banco
3. **Criar backup** - Gera arquivo de backup
4. **Resetar banco** - ⚠️ APAGA TODOS OS DADOS
5. **Executar testes** - Verifica funcionamento do sistema

### Exemplos de Uso

**Criar dados de demonstração:**
```bash
python setup_util.py
# Escolha opção 1
```

**Verificar funcionamento:**
```bash
python setup_util.py  
# Escolha opção 5 (testes)
```

## 📊 Interpretando os Dados

### Dashboard
- **Verde**: Valores positivos (receitas, saldo positivo)
- **Vermelho**: Valores negativos (despesas, saldo negativo)
- **Azul**: Informações neutras

### Gráficos
- **Pizza**: Distribuição percentual de gastos
- **Barras**: Comparação entre valores
- **Cores**: Cada categoria tem cor única

### Transações
- **Fundo Verde**: Receitas
- **Fundo Vermelho**: Despesas
- **Data**: Formato DD/MM/AAAA

## 🔒 Backup e Segurança

### Backup Automático
- Local: Pasta do aplicativo
- Formato: arquivo .db
- Nome: `backup_finance_AAAAMMDD_HHMMSS.db`

### Backup Manual
1. Vá em Configurações
2. Clique "Criar Backup"
3. Arquivo será salvo na pasta do app

### Restauração
1. Coloque arquivo de backup na pasta
2. Use "Restaurar Backup" nas configurações
3. ⚠️ Sobrescreverá dados atuais

## ❌ Solução de Problemas

### Aplicativo não inicia
1. Verifique se Python 3.7+ está instalado
2. Reinstale dependências: `pip install -r requirements.txt`
3. Execute testes: `python setup_util.py` (opção 5)

### Erro de banco de dados
1. Execute setup_util.py
2. Escolha opção 4 para resetar banco
3. Restaure backup se necessário

### Gráficos não aparecem
1. Verifique instalação matplotlib: `pip install matplotlib`
2. Adicione algumas transações primeiro
3. Reforce as categorias têm cores definidas

### Performance lenta
1. Faça backup dos dados
2. Limite transações antigas
3. Reinicie o aplicativo

## 📞 Suporte

Para dúvidas ou problemas:
1. Consulte este guia primeiro
2. Execute testes básicos (`setup_util.py`)
3. Verifique logs de erro no terminal
4. Crie backup antes de tentar correções

---

**CashControl v1.0** - Controle suas finanças com simplicidade! 💰✨
