import json
from datetime import date

# Arquivo para armazenar informações
registros = "registros.json"

# Função para carregar dados do arquivo
def carregar_dados():
    try:
        with open(registros, "r") as arquivo: #Faz a leitura do arquivo .json
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Função para salvar dados no arquivo
def salvar_dados(cadastros):
    with open(registros, "w") as arquivo: #Escreve o arquivo ou sobrescreve um arquivo .json
        json.dump(cadastros, arquivo, indent=4)  #Descarrega as informações para cadastros

def opcoes_cadastro(opcao): # Função de pegar o resultado de cada item separadamente
    if(opcao == "nome"):
        nome_cliente = input("Digite o nome do cliente: ")
        if nome_cliente.strip() == "": # Se o nome for vazio a função irá encerrar
            print("Nome não pode estar vazio.")
            return 
        else: return nome_cliente

    if(opcao == "nascimento"):
        try:
            nascimento = input("Digite sua data de nascimento (Exemplo: 06/09/2000): ")
            if len(nascimento) != 10: # Se o tamanho da data de nascimento for menor que 10 caracteres, a função irá encerrar
                print("Use o formato de xx/xx/xxxx para a data. Exemplo: 06/09/2000")
                return
            else:
                dataNascimento = date(int(nascimento[6:]),int(nascimento[3:5]),int(nascimento[:2])) # Transforma a data de nascimento em um formato xx-xx-xxxx
                idade = (date.today() - dataNascimento).days//365 # Diminui o dia de hoje pela data de nascimento e converte para anos
                if idade < 0: # Caso a idade seja negativa o código irá encerrar 
                    print("Data inválida!")
                    return
                return nascimento
        except ValueError: # Caso não seja usado números 
            print("Use o formato de xx/xx/xxxx para a data. Exemplo: 06/09/2000")
            return
    
    if(opcao == "email"): 
        email = input("Digite o email: ")
        if "@" not in email: # Caso o e-mail não contenha @ o código irá encerrar
            print("E-mail inválido.")
            return
        else: return email
    
    if(opcao == "cpf"):
        cpf = input("Digite o CPF: (use apenas números) ")
        if len(cpf) != 11 or not cpf.isdigit(): # Caso o tamanho do cpf seja diferente de 11 dígitos, o código irá encerrar
            print("Cpf inválido.")
            return
        else: return cpf

    if(opcao == "cep"):
        cep = input("Digite o CEP: (use apenas números) ")
        if len(cep) != 8 or not cep.isdigit(): # Caso o tamanho do cep seja diferente de 8 dígitos, o código irá encerrar
            print("CEP inválido.")
            return
        else: return cep
    
    if(opcao == "telefone"):
        telefone = input("Digite um número para contato: (use apenas números) ")
        if not telefone.isdigit(): # Caso o telefone tenha letras, o código irá encerrar
            print("Número de Telefone inválido")
            return
        else: return telefone
    
# Função para adicionar um novo cadastro
def adicionar_cadastro():
    cadastros = carregar_dados()
    opcoes = ["nome", "nascimento", "email", "cpf", "cep","telefone"] # Lista das opções
    novo_cliente = {} # Cria um objeto vazio

    for item in opcoes: # Envia a validação de cada uma das opções na lista
        novo_cliente[item] = opcoes_cadastro(item) # Envia as opções para o objeto
        if novo_cliente[item] is None: # Caso ocorra algum erro, o código irá encerrar
            return

    cadastros.append(novo_cliente) #Adiciona as informações nos vetores
    salvar_dados(cadastros)
    print("\nCliente cadastrado com sucesso!")

# Função para verificar os cadastros existentes
def verificar_cadastros():
    cadastros = carregar_dados()
    if cadastros:
        # Cabeçalho da tabela
        print(f"\n{'Nome':<20} {'Nascimento':<15} {'Idade':<6} {'Email':<30} {'CPF':<15} {'CEP':<15} {'Telefone':<15}") #Formatação do cabeçalho
        print("-" * 120)  # Linha divisória

        # Exibição dos dados dos clientes
        for cliente in cadastros:
            cpfFormatado = f"{cliente['cpf'][:3]}.{cliente['cpf'][3:6]}.{cliente['cpf'][6:9]}-{cliente['cpf'][9:]}" # Formatação do cpf para o formato com . e - 
            cepFormatado = f"{cliente['cep'][:5]}-{cliente['cep'][5:]}" # Formatação do cep para formato com -

            dataNascimento = date(int(cliente['nascimento'][6:]),int(cliente['nascimento'][3:5]),int(cliente['nascimento'][:2])) # Transforma a data de nascimento em um formato xx-xx-xxxx
            idade = (date.today() - dataNascimento).days//365 # Diminui o dia de hoje pela data de nascimento e converte para anos

            print(f"\n{cliente['nome']:<20} {cliente['nascimento']:<15} {idade:<6} {cliente['email']:<30} {cpfFormatado:<15} {cepFormatado:<15} {cliente['telefone']:<15}") # Formatação das váriaveis
    else:
        print("\nNenhum cadastro encontrado")

# Função para atualizar um cadastro existente
def atualizar_cadastros():
    cadastros = carregar_dados()
    verificar_cadastros() #Chama a função de verificação já formatada para a exibição dos cadastros
    cpf = input("\nDigite o CPF do cliente que deseja atualizar, usando apenas números (ou 'cancelar' para voltar): ")
    if cpf.lower() == 'cancelar': #Utilização do lower para o uso da palavra em maiuscula como input.
        print("\nOperação de atualização cancelada.")
        return #Encerra o comando e retorna para o menu de escolha
    for cliente in cadastros: #Verifica cada variavel dentro da lista
        if cliente["cpf"] == cpf:
                opcao = input("Digite a opção que deseja alterar: ")

                if(opcao.lower() in cliente or opcao.lower() == "idade"): # Caso a opção escolhida exista.
                    if(opcao.lower() == "idade"):
                        opcao = "nascimento"

                    novaInfo = opcoes_cadastro(opcao.lower()) # Ele pede para atualizá-la
                    if novaInfo is None: # Caso algum erro ocorra 
                        return
                    else:
                        cliente[opcao.lower()] = novaInfo
                        salvar_dados(cadastros) # E Envia para o JSON
                        print("\nCadastro atualizado com sucesso!")
                        return 
                else: # Caso a não opcao exista
                    print("Opção Inválida!") # Ele envia essa mensagem
                    return
    print("\nCadastro não localizado") # Caso não encontre o CPF, essa mensagem será enviada.

# Função para excluir um cadastro
def excluir_cadastro():
    cadastros = carregar_dados()
    verificar_cadastros()
    cpf = input("\nDigite o CPF do cliente a ser excluído, usando apenas os números (ou 'cancelar' para voltar): ")
    
    if cpf.lower() == 'cancelar':
        print("\nOperação de exclusão cancelada.")
        return 
    if not any(cliente["cpf"] == cpf for cliente in cadastros): #verifica se os valores são verdades, caso não, então não sera localizado
        print("\nCadastro não localizado.")
        return
    cadastros = [cliente for cliente in cadastros if cliente["cpf"] != cpf] #Faz a verificação de cada cliente para fazer a exclusão criando uma lista sobre a outra (list comprehension)
    salvar_dados(cadastros)
    print("\nCadastro excluído com sucesso!")

# Função para exibir o menu e processar as escolhas do usuário
def menu():
    while True:
        print("\n---BANCO DE DADOS DE CLIENTES TECHNOVA---")
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