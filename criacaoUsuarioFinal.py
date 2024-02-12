import re
import pyodbc

#TABELA CRIADA NO SQL Server
#CREATE TABLE Usuarios(
#ID INT PRIMARY KEY IDENTITY(1,1)
#Nome NVARCHAR(50) NOT NULL,
#Senha NVARCHAR(255) NOT NULL
#);

#variavel responsavel pela conexão com o BD
dados_conexão = (
    "Driver={SQL Server};"
    "Server=DESKTOP-7DKI1JR\\SQLEXPRESS;"
    "Database=acessos;"
)

conexao = pyodbc.connect(dados_conexão)
print("CONEXÃO BEM SUCEDIDA")

print("-----------------------------")
print("SISTEMA DE CONTROLE DE ACESSO")
print("-----------------------------")

print("O que deseja fazer? [1- Cadastrar Usuario 2- Deletar Usuario 3- Atualizar Usuario 4- Exibir Usuario]")
RespostaAcao = int(input("Resposta: "))

def get_last_id(cursor):
    cursor.execute("SELECT MAX(ID) AS LastID FROM Usuarios")
    row = cursor.fetchone()
    return 0 if row.LastID is None else int(row.LastID)

#VERICAÇÕES DO CAMPO USUARIO
credenciaisUsuario = False
credenciaisSenha = False

if RespostaAcao == 1:
    usuario = False

    while not usuario:

        print("CADASTRE SEU NOME DE USUARIO [somente letras minusculas]")
        nomeUsuario = input("Usuario: ")

        #re.match entra no if para que o nome de usuario seja apenas minusculo, se for maiusculo o nome de usurio é invalido.
    
        if re.match(r'^[a-z]{3,15}$', nomeUsuario):
            usuario = True
        else:
            print("Nome de usuario inválido!")
            usuario = False

    if usuario:
        credenciaisUsuario = True
              
    #VERIFICAÇÕES DO CAMPO SENHA        

    senha =  False
    while not senha:
        print("CADASTRE A SUA SENHA [É necessário ter uma letra maiuscula, minuscula e um numero]")        
        senhaUsuario = input("Senha: ")

        #re.match entra no if para que a senha de usuario cumpra os requisitos, caso não cumpra entra com false e faz o loop novamente
    
        if re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$', senhaUsuario):
            senha = True
        else:
            print("A senha não está cumprindo os requisitos! Digite novamente!")      
            senha = False
        
    if senha == True:
        credenciaisSenha = True
            
contID = get_last_id(conexao.cursor()) + 1

#VALIDAÇÃO PARA INSERIR NO BD
#SE A RESPOSTA FOR 1 E AS CREDENCIAIS VERDADEIRAS, TRABALHAMOS O LOOP
#O TRY E EXCEPT SERVE PARA DAR TRATAMENTO EM ERROS CASO OCORRA
#O try é uma "tentativa de execução" e nessa tentativa caso ocorra algum erro inesperado, o código entra no except.
#É uma boa pratica no momento de chamar a conexao de um BD, abrir essa conexão, executar algo e encerrar essa conexão.
if RespostaAcao == 1 and credenciaisUsuario and credenciaisSenha:
    
        try:
            conn = conexao
            cursor = conn.cursor()
        
            cursor.execute("INSERT INTO Usuarios (Nome, Senha) VALUES (?, ?)", nomeUsuario, senhaUsuario)
            conn.commit()

            # Recupera o último ID cadastrado
            contID = get_last_id(cursor)

            print("BOAS VINDAS!")
            print(f"ID {contID} cadastrado.")
        
        except Exception as e:
            print(f"Erro ao inserir no banco de dados: {e}")
        
#DELETAR NO BD 
if RespostaAcao == 2:
    try:
        conn = conexao
        cursor = conn.cursor()        
        print("DELETAR USUARIO [S/N]")
        respotaExcluir = input("Resposta: ")

        if respotaExcluir.upper() == "S":
            
            opcao = False
            while not opcao:
                apagarPorIDouNome = (input("Escolha por qual opção você deseja deletar [ID / Nome] lembrando que é Nome de usuario: "))
                if apagarPorIDouNome == "Nome":
                    nomeParaApagar = input("Digite o nome de usuario que deseja apagar: ")
                    cursor.execute("DELETE FROM Usuarios WHERE Nome=?", nomeParaApagar)
                    conn.commit()
                    print("Usuario deletado do banco de dados!")
                    conn.close()
                    opcao = True
                elif apagarPorIDouNome == "ID":
                    idParaApagar = int(input("Digite o numero do ID que deseja apagar: "))
                    cursor.execute("DELETE FROM Usuarios WHERE id=?", idParaApagar)
                    conn.commit()
                    print("Usuario deletado do banco de dados!")
                    conn.close()
                    opcao = True
                else:
                    print("Digite ou a palavra 'ID' ou 'Nome'")
                    opcao = False

        else:
            print("PROGRAMA FINALIZADO!")
    except Exception as e:
            print(f"Erro ao deletar usuario no banco de dados: {e}")    
            
#ATUALIZAR USUARIO NO BD
if RespostaAcao == 3:
    try:
        conn = conexao
        cursor = conn.cursor()
        print("Deseja atualizar algum usuario cadastrado? [S/N]")
        respotaAtualizar = input("Resposta: ")       
        
        if respotaAtualizar.upper() == "S":
            usuario = False
            while not usuario:
                idParaAtualizar = int(input("Digite o numero do ID que deseja atualizar: "))
                nomeParaAtualizar = input("Digite o novo nome para atualizar: ")
                if re.match(r'^[a-z]{3,15}$', nomeParaAtualizar):
                    usuario = True
                else:
                    print("Nome de usuario inválido!")
                    usuario = False
            senha = False
            while not senha:        
                senhaParaAtualizar = input("Digite a nova senha para atualizar:")
                if re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$', senhaParaAtualizar):
                    senha = True
                else:
                    print("A senha não está cumprindo os requisitos! Digite novamente!")      
                    senha = False
           #cursor.execute("UPDATE Usuarios SET Nome=?, Senha=? WHERE ID=?", (novoNome, novaSenha, idParaAtualizar))         
            cursor.execute("UPDATE Usuarios SET Nome=?, Senha=? WHERE ID=?", (nomeParaAtualizar, senhaParaAtualizar, idParaAtualizar))
            conn.commit()
            print("ID atualizado com sucesso!")
            conn.close()
        else:
            print("PROGRAMA FINALIZADO")    
    except Exception as e:
            print(f"Erro ao atualizar usuario no banco de dados: {e}")
            
#EXIBIR USUARIO            
if RespostaAcao == 4:
    try:    
        conn = conexao
        cursor = conn.cursor()
        print("Qual usuario deseja exibir? escolha por [' ID ' ou ' Nome '] lembre-se de digitar as palavras conforme está dentro do colchets.")
        respostaExibirUsuario = input("Resposta: ")
        idErrado = False
        while not idErrado:  
            if respostaExibirUsuario == "ID":
                respostaExibirID = int(input("Digite o ID que deseja exibir: "))
                cursor.execute("SELECT * FROM Usuarios WHERE ID=?", respostaExibirID)
                resultadoID = cursor.fetchone()
        
                if resultadoID:
                    print("----DADOS DO USUARIO----")
                    print(f"ID: {resultadoID.ID}")
                    print(f"Nome de usuario: {resultadoID.Nome}")
                    print(f"Senha: {resultadoID.Senha}")
                    idErrado = True
                else:
                    print("Usuario não encontrado no banco de dados")
                    idErrado = False
            elif respostaExibirUsuario == "Nome":
                conn= conexao
                cursor = conn.cursor()
                respostaExibirNome = input("Digite o Nome de usuario que deseja exibir: ")
                cursor.execute("SELECT * FROM Usuarios WHERE Nome=?", respostaExibirNome)
                resultadoNome = cursor.fetchone()
        
                if resultadoNome:
                    print("----DADOS DO USUARIO----")
                    print(f"ID: {resultadoNome.ID}")
                    print(f"Nome de usuario: {resultadoNome.Nome}")
                    print(f"Senha: {resultadoNome.Senha}")
                    idErrado = True
                else:
                    print("Usuario não encontrado no banco de dados.")
                    idErrado = False
    except Exception as e:
        print(f"Erro ao atualizar usuario no banco de dados: {e}")

        
    
    
  

