# Sistema de Registo Eletrónico de Utentes

import json

FICHEIRO = "utentes.json"

UTILIZADORES = {
    "admin":    {"password": "1234", "perfil": "administrativo"},
    "dr.silva": {"password": "2345", "perfil": "medico"},
    "enf.ana":  {"password": "3456", "perfil": "enfermeiro"},
}

# O que cada perfil pode fazer
PERMISSOES = {
    "administrativo": ["registar", "pesquisar", "listar"],
    "enfermeiro":     ["pesquisar", "ver_historico"],
    "medico":         ["pesquisar", "ver_historico", "adicionar_consulta"],
}


def carregar_dados():
    try:
        f = open(FICHEIRO, "r", encoding="utf-8")
        dados = json.load(f)
        f.close()
        return dados
    except FileNotFoundError:
        return []


def guardar_dados(utentes):
    f = open(FICHEIRO, "w", encoding="utf-8")
    json.dump(utentes, f, ensure_ascii=False, indent=2)
    f.close()



def gerar_numero_registo(utentes):
    maior = 0
    for u in utentes:
        if u["numero_registo"] > maior:
            maior = u["numero_registo"]
    return maior + 1


def nif_valido(nif):
    return nif.isdigit() and len(nif) == 9


def nif_ja_existe(utentes, nif):
    for u in utentes:
        if u["nif"] == nif:
            return True
    return False


def procurar_por_numero(utentes, numero):
    for u in utentes:
        if u["numero_registo"] == numero:
            return u
    return None


def pedir_numero_registo():
    texto = input("Número de registo eletrónico: ")
    if not texto.isdigit():
        print("Número inválido.")
        return None
    return int(texto)


def login():
    print("=== Sistema de Registo Eletrónico de Utentes ===")
    for tentativa in range(3):
        nome = input("Utilizador: ")
        senha = input("Palavra-passe: ")
        if nome in UTILIZADORES and UTILIZADORES[nome]["password"] == senha:
            print("Bem-vindo,", nome)
            return nome, UTILIZADORES[nome]["perfil"]
        print("Credenciais incorretas.")
    print("Demasiadas tentativas. A sair.")
    return None, None


def registar_utente(utentes):
    print("\n--- Registar novo utente ---")
    nome = input("Nome completo: ").strip()
    if nome == "":
        print("O nome é obrigatório.")
        return
    data_nasc = input("Data de nascimento (dd/mm/aaaa): ")
    sexo = input("Sexo (M/F): ").upper()
    telefone = input("Telefone: ")
    morada = input("Morada: ")

    nif = input("NIF (deixe vazio se não aplicável): ").strip()
    if nif != "":
        if not nif_valido(nif):
            print("NIF inválido. Registo cancelado.")
            return
        if nif_ja_existe(utentes, nif):
            print("Já existe um utente com este NIF. Registo cancelado.")
            return

    utente = {
        "numero_registo": gerar_numero_registo(utentes),
        "nome": nome,
        "data_nascimento": data_nasc,
        "sexo": sexo,
        "telefone": telefone,
        "morada": morada,
        "nif": nif,
        "consultas": [],
    }
    utentes.append(utente)
    guardar_dados(utentes)
    print("Utente registado! Número de registo:", utente["numero_registo"])


def mostrar_dados_pessoais(u):
    print("\nNº registo:", u["numero_registo"])
    print("Nome:", u["nome"])
    print("Nascimento:", u["data_nascimento"])
    print("Sexo:", u["sexo"])
    print("Telefone:", u["telefone"])
    print("Morada:", u["morada"])
    if u["nif"] == "":
        print("NIF: não indicado")
    else:
        print("NIF:", u["nif"])


def pesquisar_utente(utentes):
    print("\n--- Pesquisar utente ---")
    numero = pedir_numero_registo()
    if numero is None:
        return
    u = procurar_por_numero(utentes, numero)
    if u is None:
        print("Utente não encontrado.")
    else:
        mostrar_dados_pessoais(u)


def listar_utentes(utentes):
    print("\n--- Lista de utentes ---")
    if len(utentes) == 0:
        print("Ainda não há utentes registados.")
    for u in utentes:
        print(u["numero_registo"], "-", u["nome"])


def adicionar_consulta(utentes, nome_medico):
    print("\n--- Registar consulta ---")
    numero = pedir_numero_registo()
    if numero is None:
        return
    u = procurar_por_numero(utentes, numero)
    if u is None:
        print("Utente não encontrado.")
        return

    print("Utente:", u["nome"])
    consulta = {
        "data": input("Data da consulta (dd/mm/aaaa): "),
        "profissional": nome_medico,
        "diagnostico": input("Diagnóstico: "),
        "observacoes": input("Outras informações clínicas: "),
    }
    u["consultas"].append(consulta)
    guardar_dados(utentes)
    print("Consulta registada com sucesso.")


def ver_historico(utentes):
    print("\n--- Histórico clínico ---")
    numero = pedir_numero_registo()
    if numero is None:
        return
    u = procurar_por_numero(utentes, numero)
    if u is None:
        print("Utente não encontrado.")
        return

    print("Utente:", u["nome"], "(Nº", u["numero_registo"], ")")
    if len(u["consultas"]) == 0:
        print("Sem consultas registadas.")
        return
    contador = 1
    for c in u["consultas"]:
        print("\nConsulta", contador)
        print("  Data:", c["data"])
        print("  Profissional:", c["profissional"])
        print("  Diagnóstico:", c["diagnostico"])
        print("  Observações:", c["observacoes"])
        contador = contador + 1


# ---------- Menu principal ----------
def menu(utilizador, perfil):
    utentes = carregar_dados()
    permitidas = PERMISSOES[perfil]

    while True:
        print("\n===== MENU (", perfil, ") =====")
        if "registar" in permitidas:
            print("1 - Registar utente")
        if "pesquisar" in permitidas:
            print("2 - Pesquisar utente por nº de registo")
        if "listar" in permitidas:
            print("3 - Listar utentes")
        if "adicionar_consulta" in permitidas:
            print("4 - Registar consulta")
        if "ver_historico" in permitidas:
            print("5 - Ver histórico clínico")
        print("0 - Sair")

        opcao = input("Opção: ")

        if opcao == "1" and "registar" in permitidas:
            registar_utente(utentes)
        elif opcao == "2" and "pesquisar" in permitidas:
            pesquisar_utente(utentes)
        elif opcao == "3" and "listar" in permitidas:
            listar_utentes(utentes)
        elif opcao == "4" and "adicionar_consulta" in permitidas:
            adicionar_consulta(utentes, utilizador)
        elif opcao == "5" and "ver_historico" in permitidas:
            ver_historico(utentes)
        elif opcao == "0":
            print("Sessão terminada.")
            break
        else:
            print("Opção inválida ou sem permissão.")


utilizador, perfil = login()
if utilizador is not None:
    menu(utilizador, perfil)
