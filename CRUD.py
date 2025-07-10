import json
from datetime import date
import math

# Arquivo para armazenar informações
registros = "registros.json"
produtos = "produtos.json"

# Função para carregar dados do arquivo
def carregar_dados(type):
    if type == "clientes":
        try:
            with open(registros, "r") as arquivo: #Faz a leitura do arquivo .json
                return json.load(arquivo)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    elif type == "produtos":
        try:
            with open(produtos, "r") as arquivo: #Faz a leitura do arquivo .json
                return json.load(arquivo)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

# Função para salvar dados no arquivo
def salvar_dados(cadastros, type):
    if(type == "clientes"):
        with open(registros, "w") as arquivo: #Escreve o arquivo ou sobrescreve um arquivo .json
            json.dump(cadastros, arquivo, indent=4)  #Descarrega as informações para cadastros
    elif(type == "produtos"):
        with open(produtos, "w") as arquivo: #Escreve o arquivo ou sobrescreve um arquivo .json
            json.dump(cadastros, arquivo, indent=4)  #Descarrega as informações para cadastros

# Função para adicionar um novo cadastro
def adicionar_cadastro():
    cadastros = carregar_dados("clientes")
    nome_cliente = input("Digite o nome do cliente: ")
    if nome_cliente.strip() == "":
        print("Nome não pode estar vazio.")
        return
    
    try:
        nascimento = input("Digite sua data de nascimento (Exemplo: 06/09/2000): ")
        if len(nascimento) != 10:
            print("Use o formato de xx/xx/xxxx para a data. Exemplo: 06/09/2000")
            return
        else:
            dataNascimento = date(int(nascimento[6:]),int(nascimento[3:5]),int(nascimento[:2]))
    except ValueError:
        print("Use o formato de xx/xx/xxxx para a data. Exemplo: 06/09/2000")
        return

    email = input("Digite o email: ")
    if "@" not in email:
        print("E-mail inválido.")
        return

    cpf = input("Digite o CPF: (use apenas números) ")
    if len(cpf) != 11 or not cpf.isdigit():
        print("Cpf inválido.")
        return

    telefone = input("Digite um número para contato: (use apenas números) ")
    if not telefone.isdigit():
        print("Número de Telefone inválido")
        return

    cadastros.append({"nome": nome_cliente, "nascimento": nascimento, "email": email, "cpf": cpf, "telefone": telefone}) #Adiciona as informações nos vetores
    salvar_dados(cadastros, "clientes")
    print("\nCliente cadastrado com sucesso!")

# Função para verificar os cadastros existentes
def verificar_cadastros():
    cadastros = carregar_dados("clientes")
    if cadastros:
        # Cabeçalho da tabela
        print(f"\n{'Nome':<20} {'Nascimento':<15} {'Idade':<6} {'Email':<30} {'CPF':<15} {'Telefone':<15}") #Formatação do cabeçalho
        print("-" * 100)  # Linha divisória

        # Exibição dos dados dos clientes
        for cliente in cadastros:
            cpfFormatado = f"{cliente['cpf'][:3]}.{cliente['cpf'][3:6]}.{cliente['cpf'][6:9]}-{cliente['cpf'][9:]}" # Formatação do cpf para o formato com . e - 
            dataNascimento = date(int(cliente['nascimento'][6:]),int(cliente['nascimento'][3:5]),int(cliente['nascimento'][:2])) # Transforma a data de nascimento em um formato xx-xx-xxxx
            idade = (date.today() - dataNascimento).days//365 # Diminui o dia de hoje pela data de nascimento e converte para anos

            print(f"\n{cliente['nome']:<20} {cliente['nascimento']:<15} {idade:<6} {cliente['email']:<30} {cpfFormatado:<15} {cliente['telefone']:<15}")#Formatação das váriaveis
    else:
        print("\nNenhum cadastro encontrado")

# Função para atualizar um cadastro existente
def atualizar_cadastros():
    cadastros = carregar_dados("clientes")
    verificar_cadastros() #Chama a função de verificação já formatada para a exibição dos cadastros
    cpf = input("\nDigite o CPF do cliente que deseja atualizar (ou 'cancelar' para voltar): ")
    if cpf.lower() == 'cancelar': #Utilização do lower para o uso da palavra em maiuscula como input.
        print("\nOperação de atualização cancelada.")
        return #Encerra o comando e retorna para o menu de escolha
    for cliente in cadastros: #Verifica cada variavel dentro da lista
        if cliente["cpf"] == cpf:
                opcao = input("Digite a opção que deseja alterar: ")

                if(opcao.lower() not in cliente): # Caso a opção escolhida não exista.
                    print("Opção Inválida!") # Ele envia essa mensagem
                    return
                else: # Caso a opcao exista
                    cliente[opcao.lower()] = input(F"Novo {opcao}: ") # Ele pede para atualizá-la               
                    salvar_dados(cadastros, "clientes") # E Envia para o JSON
                    print("\nCadastro atualizado com sucesso!")
                return 
    print("\nCadastro não localizado") # Caso não encontre o CPF, essa mensagem será enviada.

# Função para excluir um cadastro
def excluir_cadastro():
    cadastros = carregar_dados("clientes")
    verificar_cadastros()
    cpf = input("\nDigite o CPF do cliente a ser excluído (ou 'cancelar' para voltar): ")
    
    if cpf.lower() == 'cancelar':
        print("\nOperação de exclusão cancelada.")
        return 
    if not any(cliente["cpf"] == cpf for cliente in cadastros): #verifica se os valores são verdades, caso não, então não sera localizado
        print("\nCadastro não localizado.")
        return
    cadastros = [cliente for cliente in cadastros if cliente["cpf"] != cpf] #Faz a verificação de cada cliente para fazer a exclusão criando uma lista sobre a outra (list comprehension)
    salvar_dados(cadastros, "clientes")
    print("\nCadastro excluído com sucesso!")

# Função para exibir o menu e processar as escolhas do usuário
def menu():
    while True:
        print("\n---BANCO DE DADOS DE CLIENTES---")
        print("1. Fazer cadastro")
        print("2. Consultar cadastro")
        print("3. Atualizar cadastro")
        print("4. Excluir cadastro")
        print("5. Sair")

        escolha = input("\nEscolha uma das opções: ") 
        #Permite a escolha do menu
        if escolha == "1":
            adicionar_cadastro()
        elif escolha == "2":
            verificar_cadastros()
        elif escolha == "3":
            atualizar_cadastros()
        elif escolha == "4":
            excluir_cadastro()
        elif escolha == "5":
            print("\nFinalizando o programa...")
            break
        else:
            print("\nEscolha inválida, por favor escolha uma opção disponível.")
menu() #Chama o menu para exibição
