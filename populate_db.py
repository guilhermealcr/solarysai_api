# Arquivo: solarys_api/populate_db.py
# VERSÃO 2 - Agora criando projetos e suas respectivas tarefas

import requests
import random
from faker import Faker
from datetime import datetime, timedelta

# URL base da nossa API que está rodando localmente
API_URL = "http://127.0.0.1:8000"

# Inicializa o Faker para gerar dados em português brasileiro
fake = Faker('pt_BR')

def criar_projeto():
    """Cria um dicionário com dados de um projeto fictício."""
    data_inicio = fake.date_between(start_date='-2y', end_date='-1y')
    duracao_dias = random.randint(180, 730)
    data_fim = data_inicio + timedelta(days=duracao_dias)

    projeto_data = {
        "Nome": f"Obra {fake.bs().title()}",
        "Descricao": fake.text(max_nb_chars=200),
        "Localizacao": fake.address(),
        "DataInicio": data_inicio.strftime("%Y-%m-%d"),
        "DataPrevistaFim": data_fim.strftime("%Y-%m-%d"),
        "Status": "Em Andamento" # Vamos focar em projetos em andamento
    }
    return projeto_data

def criar_tarefas_para_projeto(projeto_id: int):
    """Cria um número aleatório de tarefas para um dado projeto_id."""
    num_tarefas = random.randint(5, 20) # Cada projeto terá de 5 a 20 tarefas
    print(f"    - Criando {num_tarefas} tarefas...")

    for _ in range(num_tarefas):
        dias_inicio = random.randint(1, 180)
        duracao_prevista_dias = random.randint(3, 30)

        data_inicio_prevista = datetime.now() + timedelta(days=dias_inicio)
        data_fim_prevista = data_inicio_prevista + timedelta(days=duracao_prevista_dias)

        # LÓGICA PARA SIMULAR ATRASOS (Ouro para a IA)
        chance_de_atraso = random.random() # Gera um número entre 0.0 e 1.0
        status_final = "Concluída no Prazo"
        data_inicio_real = data_inicio_prevista + timedelta(days=random.randint(0, 3)) # Pode começar um pouco depois
        data_fim_real = data_fim_prevista

        # Se a tarefa tiver um prazo curto, aumentamos a chance de atraso
        if duracao_prevista_dias < 10 and chance_de_atraso > 0.4: # 60% de chance de atrasar
            status_final = "Atrasada"
            data_fim_real += timedelta(days=random.randint(1, 10)) # Adiciona dias de atraso
        elif chance_de_atraso > 0.8: # 20% de chance de atrasar mesmo em tarefas normais
            status_final = "Atrasada"
            data_fim_real += timedelta(days=random.randint(1, 5))

        tarefa_data = {
            "ProjetoID": projeto_id,
            "Descricao": fake.sentence(nb_words=6),
            "DataInicioPrevista": data_inicio_prevista.isoformat(),
            "DataFimPrevista": data_fim_prevista.isoformat(),
            "DataInicioReal": data_inicio_real.isoformat(),
            "DataFimReal": data_fim_real.isoformat(),
            "Status": status_final
        }
        
        # Faz a requisição POST para o endpoint de tarefas da nossa API
        response = requests.post(f"{API_URL}/tarefas/", json=tarefa_data)
        if response.status_code != 201:
            print(f"      ! Erro ao criar tarefa. Status: {response.status_code}, Resposta: {response.text}")


def popular_banco(num_projetos=10):
    """Função principal que cria projetos e suas tarefas via API."""
    print(f"Iniciando a criação de {num_projetos} projetos e suas tarefas...")

    for i in range(num_projetos):
        novo_projeto = criar_projeto()
        
        try:
            response = requests.post(f"{API_URL}/projetos/", json=novo_projeto)
            
            if response.status_code == 201:
                projeto_criado = response.json()
                print(f"  > Projeto '{projeto_criado['Nome']}' (ID: {projeto_criado['ProjetoID']}) criado.")
                
                # CHAMA A FUNÇÃO PARA CRIAR TAREFAS PARA O PROJETO RECÉM-CRIADO
                criar_tarefas_para_projeto(projeto_criado['ProjetoID'])
            else:
                print(f"  ! Erro ao criar projeto. Status: {response.status_code}, Resposta: {response.text}")

        except requests.exceptions.ConnectionError as e:
            print("\nERRO DE CONEXÃO: A API não parece estar rodando.")
            print("Por favor, inicie o servidor com: uvicorn app.main:app --reload")
            break

    print("\nCriação de dados concluída.")

# --- Ponto de Entrada do Script ---
if __name__ == "__main__":
    # Agora podemos definir um número maior de uma vez!
    # Vamos começar com 50 projetos para gerar um bom volume de tarefas.
    popular_banco(num_projetos=700)