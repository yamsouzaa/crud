Sistema de Controle de Acesso em Python utilizando SQL Server
Este é um simples sistema de controle de acesso em Python, utilizando o banco de dados SQL Server para armazenar informações de usuários. O sistema oferece funcionalidades básicas, como cadastrar, deletar, atualizar e exibir usuários.

Pré-requisitos:
Certifique-se de ter o Python instalado em sua máquina. Além disso, é necessário instalar a biblioteca pyodbc, que é utilizada para a conexão com o banco de dados. Você pode instalá-la executando o seguinte comando:

pip install pyodbc
Configuração do Banco de Dados
Antes de executar o programa, certifique-se de ter um banco de dados chamado acessos criado no SQL Server. Utilize o script SQL fornecido no código para criar a tabela necessária (Usuarios).

Configuração da Conexão com o Banco de Dados
No código, a variável dados_conexão contém as informações necessárias para a conexão com o banco de dados. Certifique-se de ajustar esses valores de acordo com as configurações do seu ambiente.

python
dados_conexão = (
    "Driver={SQL Server};"
    "Server=SEU_SERVIDOR_SQL;"
    "Database=acessos;"
)

Executando o Programa
Execute o script Python e siga as instruções apresentadas no console. O sistema oferece as seguintes opções:

1- Cadastrar Usuário
2- Deletar Usuário
3- Atualizar Usuário
4- Exibir Usuário

Ao selecionar cada opção, siga as instruções fornecidas para realizar a ação desejada.
Lembre-se de sempre ajustar as credenciais e configurações do banco de dados conforme necessário.

Observação: Este projeto é um exemplo simples e pode ser expandido para incluir mais funcionalidades e melhorias.
