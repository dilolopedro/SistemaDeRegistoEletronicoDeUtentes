# Sistema de Registo Eletrónico de Utentes

Aplicação de consola em Python para modernizar o registo, a identificação e o acompanhamento de pacientes em unidades de saúde. Projeto académico desenvolvido para o 3º ano de Engenharia Informática, usando apenas conceitos básicos de programação.

## Objetivos

- Registar os dados pessoais dos utentes.
- Atribuir a cada utente um **número único de registo eletrónico**.
- Associar o registo ao **NIF**, quando aplicável.
- Guardar e consultar o **histórico clínico** (consultas, datas, diagnósticos e outras informações relevantes).
- Localizar utentes pelo número de registo.
- Controlar o acesso à informação segundo o **perfil do utilizador**.

## Requisitos

- Python 3.6 ou superior
- Nenhuma biblioteca externa (só se usa o módulo `json`, que já vem com o Python)

## Como executar

```bash
python registo_utentes.py
```

Os dados são guardados automaticamente no ficheiro `utentes.json`, criado na primeira vez que se regista um utente.

## Utilizadores de teste

| Utilizador | Palavra-passe | Perfil |
|---|---|---|
| `admin` | `1234` | administrativo |
| `dr.silva` | `2345` | médico |
| `enf.ana` | `3456` | enfermeiro |

## Níveis de acesso

| Funcionalidade | Administrativo | Enfermeiro | Médico |
|---|:---:|:---:|:---:|
| Registar utente | ✅ | ❌ | ❌ |
| Pesquisar utente | ✅ | ✅ | ✅ |
| Listar utentes | ✅ | ❌ | ❌ |
| Ver histórico clínico | ❌ | ✅ | ✅ |
| Registar consulta | ❌ | ❌ | ✅ |

## Funcionalidades

### Registar utente
Pede nome, data de nascimento, sexo, telefone, morada e NIF (opcional). O número de registo é gerado automaticamente. O NIF, se indicado, tem de ter 9 dígitos e não pode estar repetido.

### Pesquisar utente
Localiza o utente pelo número de registo e mostra os seus dados pessoais.

### Listar utentes
Mostra o número de registo e o nome de todos os utentes.

### Registar consulta
O médico indica o número de registo do utente e preenche data, diagnóstico e observações. O nome do profissional é associado automaticamente à consulta.

### Ver histórico clínico
Apresenta, de forma organizada, todas as consultas do utente.

## Estrutura dos dados

Cada utente é um dicionário guardado numa lista:

```json
{
  "numero_registo": 1,
  "nome": "João Manuel",
  "data_nascimento": "12/05/1990",
  "sexo": "M",
  "telefone": "923000000",
  "morada": "Rua A, Luanda",
  "nif": "123456789",
  "consultas": [
    {
      "data": "10/11/2026",
      "profissional": "dr.silva",
      "diagnostico": "Gripe",
      "observacoes": "Repouso e hidratação"
    }
  ]
}
```

## Organização do código

| Função | Descrição |
|---|---|
| `carregar_dados` / `guardar_dados` | Lêem e gravam o ficheiro JSON |
| `gerar_numero_registo` | Cria o número único de registo |
| `nif_valido` / `nif_ja_existe` | Validam o NIF |
| `procurar_por_numero` | Localiza um utente pelo número de registo |
| `login` | Autentica o utilizador (3 tentativas) |
| `registar_utente` | Regista um novo utente |
| `pesquisar_utente` / `listar_utentes` | Consulta de utentes |
| `adicionar_consulta` | Acrescenta uma consulta ao histórico |
| `ver_historico` | Mostra o histórico clínico |
| `menu` | Menu principal, adaptado ao perfil |

## Limitações

- As palavras-passe estão no código e não estão protegidas por hash.
- O ficheiro `utentes.json` não está cifrado.
- As datas não são validadas quanto ao formato.
- Não é possível editar nem eliminar utentes ou consultas.
- Não existe registo (log) de quem consultou cada histórico.

## Melhorias futuras

- Utilizar uma base de dados (SQLite) em vez de JSON.
- Guardar palavras-passe com hash e cifrar os dados clínicos.
- Pesquisar utentes por nome ou NIF.
- Editar dados do utente.
- Registar alergias, medicação e exames.
- Validar datas.
- Criar um log de auditoria dos acessos.
- Desenvolver uma interface gráfica ou web.

## Nota sobre proteção de dados

Os dados de saúde são informação sensível. Num sistema real, o tratamento destes dados deve respeitar a legislação de proteção de dados aplicável, garantindo confidencialidade, controlo de acessos e rastreabilidade.

## Autor

*(Dilolo Eauial Pedro, 3º Ano, turma: TL101 Período: Manhã)*
