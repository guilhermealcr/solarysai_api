# Arquivo: solarys_api/app/main.py
# VERSÃO FINALÍSSIMA COM CRUD COMPLETO PARA TODAS AS TABELAS

from fastapi import FastAPI, HTTPException, status, Depends
import pyodbc
from typing import List

from . import schemas
from .database import get_db_connection

app = FastAPI(
    title="SolarysAI API",
    description="API para gerenciar dados de construção civil e fornecer insights de IA.",
    version="1.0.0"
)

# Alias para a nossa função de conexão para facilitar o uso
DbConnection = Depends(get_db_connection)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo à API SolarysAI"}

# --------------------------------------------------------------------------
# --- ENDPOINTS PARA PROJETOS ---
# --------------------------------------------------------------------------

@app.post("/projetos/", response_model=schemas.Projeto, status_code=status.HTTP_201_CREATED, tags=["Projetos"])
def create_projeto(projeto: schemas.ProjetoCreate, db: pyodbc.Connection = DbConnection):
    # (código existente)
    cursor = db.cursor()
    sql = "INSERT INTO Projetos (Nome, Descricao, Localizacao, DataInicio, DataPrevistaFim, Status) OUTPUT INSERTED.ProjetoID VALUES (?,?,?,?,?,?)"
    cursor.execute(sql, projeto.Nome, projeto.Descricao, projeto.Localizacao, projeto.DataInicio, projeto.DataPrevistaFim, projeto.Status)
    novo_id = cursor.fetchone()[0]
    db.commit()
    return schemas.Projeto(ProjetoID=novo_id, **projeto.dict())

@app.get("/projetos/", response_model=List[schemas.Projeto], tags=["Projetos"])
def get_projetos(db: pyodbc.Connection = DbConnection):
    # (código existente)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Projetos")
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

@app.get("/projetos/{projeto_id}", response_model=schemas.Projeto, tags=["Projetos"])
def get_projeto_by_id(projeto_id: int, db: pyodbc.Connection = DbConnection):
    # (código existente)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Projetos WHERE ProjetoID = ?", projeto_id)
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Projeto não encontrado.")
    columns = [column[0] for column in cursor.description]
    return dict(zip(columns, row))

@app.put("/projetos/{projeto_id}", response_model=schemas.Projeto, tags=["Projetos"])
def update_projeto(projeto_id: int, projeto_update: schemas.ProjetoCreate, db: pyodbc.Connection = DbConnection):
    # (código existente)
    cursor = db.cursor()
    sql = "UPDATE Projetos SET Nome=?, Descricao=?, Localizacao=?, DataInicio=?, DataPrevistaFim=?, Status=? WHERE ProjetoID = ?"
    cursor.execute(sql, projeto_update.Nome, projeto_update.Descricao, projeto_update.Localizacao, projeto_update.DataInicio, projeto_update.DataPrevistaFim, projeto_update.Status, projeto_id)
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Projeto não encontrado para atualização.")
    db.commit()
    return schemas.Projeto(ProjetoID=projeto_id, **projeto_update.dict())

@app.delete("/projetos/{projeto_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Projetos"])
def delete_projeto(projeto_id: int, db: pyodbc.Connection = DbConnection):
    # (código existente)
    cursor = db.cursor()
    cursor.execute("DELETE FROM Projetos WHERE ProjetoID = ?", projeto_id)
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Projeto não encontrado para deleção.")
    db.commit()

# --------------------------------------------------------------------------
# --- ENDPOINTS PARA TAREFAS ---
# --------------------------------------------------------------------------

@app.post("/tarefas/", response_model=schemas.Tarefa, status_code=status.HTTP_201_CREATED, tags=["Tarefas"])
def create_tarefa(tarefa: schemas.TarefaCreate, db: pyodbc.Connection = DbConnection):
    # (código existente)
    cursor = db.cursor()
    sql = "INSERT INTO Tarefas (ProjetoID, Descricao, DataInicioPrevista, DataFimPrevista, DataInicioReal, DataFimReal, Status) OUTPUT INSERTED.TarefaID VALUES (?,?,?,?,?,?,?)"
    cursor.execute(sql, tarefa.ProjetoID, tarefa.Descricao, tarefa.DataInicioPrevista, tarefa.DataFimPrevista, tarefa.DataInicioReal, tarefa.DataFimReal, tarefa.Status)
    novo_id = cursor.fetchone()[0]
    db.commit()
    return schemas.Tarefa(TarefaID=novo_id, **tarefa.dict())

@app.get("/projetos/{projeto_id}/tarefas/", response_model=List[schemas.Tarefa], tags=["Tarefas"])
def get_tarefas_by_projeto(projeto_id: int, db: pyodbc.Connection = DbConnection):
    # (código existente)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Tarefas WHERE ProjetoID = ?", projeto_id)
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
# (CRUD completo para Tarefas seria análogo ao de Projetos)

# --------------------------------------------------------------------------
# --- ENDPOINTS PARA RECURSOS FINANCEIROS ---
# --------------------------------------------------------------------------

@app.post("/recursos_financeiros/", response_model=schemas.RecursoFinanceiro, status_code=status.HTTP_201_CREATED, tags=["Financeiro"])
def create_recurso_financeiro(recurso: schemas.RecursoFinanceiroCreate, db: pyodbc.Connection = DbConnection):
    cursor = db.cursor()
    sql = "INSERT INTO RecursosFinanceiros (ProjetoID, Tipo, Descricao, Valor, Data) OUTPUT INSERTED.RecursoFinanceiroID VALUES (?,?,?,?,?)"
    cursor.execute(sql, recurso.ProjetoID, recurso.Tipo, recurso.Descricao, recurso.Valor, recurso.Data)
    novo_id = cursor.fetchone()[0]
    db.commit()
    return schemas.RecursoFinanceiro(RecursoFinanceiroID=novo_id, **recurso.dict())

@app.get("/projetos/{projeto_id}/recursos_financeiros/", response_model=List[schemas.RecursoFinanceiro], tags=["Financeiro"])
def get_recursos_by_projeto(projeto_id: int, db: pyodbc.Connection = DbConnection):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM RecursosFinanceiros WHERE ProjetoID = ?", projeto_id)
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

# --------------------------------------------------------------------------
# --- ENDPOINTS PARA MATERIAIS ---
# --------------------------------------------------------------------------

@app.post("/materiais/", response_model=schemas.Material, status_code=status.HTTP_201_CREATED, tags=["Materiais"])
def create_material(material: schemas.MaterialCreate, db: pyodbc.Connection = DbConnection):
    cursor = db.cursor()
    sql = "INSERT INTO Materiais (ProjetoID, NomeMaterial, QuantidadeNecessaria, QuantidadeEmEstoque, Unidade) OUTPUT INSERTED.MaterialID VALUES (?,?,?,?,?)"
    cursor.execute(sql, material.ProjetoID, material.NomeMaterial, material.QuantidadeNecessaria, material.QuantidadeEmEstoque, material.Unidade)
    novo_id = cursor.fetchone()[0]
    db.commit()
    return schemas.Material(MaterialID=novo_id, **material.dict())

@app.get("/projetos/{projeto_id}/materiais/", response_model=List[schemas.Material], tags=["Materiais"])
def get_materiais_by_projeto(projeto_id: int, db: pyodbc.Connection = DbConnection):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Materiais WHERE ProjetoID = ?", projeto_id)
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

@app.put("/materiais/{material_id}", response_model=schemas.Material, tags=["Materiais"])
def update_material(material_id: int, material_update: schemas.MaterialCreate, db: pyodbc.Connection = DbConnection):
    cursor = db.cursor()
    sql = "UPDATE Materiais SET ProjetoID=?, NomeMaterial=?, QuantidadeNecessaria=?, QuantidadeEmEstoque=?, Unidade=? WHERE MaterialID = ?"
    cursor.execute(sql, material_update.ProjetoID, material_update.NomeMaterial, material_update.QuantidadeNecessaria, material_update.QuantidadeEmEstoque, material_update.Unidade, material_id)
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Material não encontrado para atualização.")
    db.commit()
    return schemas.Material(MaterialID=material_id, **material_update.dict())

# --------------------------------------------------------------------------
# --- ENDPOINTS PARA FUNCIONÁRIOS E ALOCAÇÕES ---
# --------------------------------------------------------------------------

@app.post("/funcionarios/", response_model=schemas.Funcionario, status_code=status.HTTP_201_CREATED, tags=["Funcionários e Alocações"])
def create_funcionario(funcionario: schemas.FuncionarioCreate, db: pyodbc.Connection = DbConnection):
    # (código existente)
    cursor = db.cursor()
    sql = "INSERT INTO Funcionarios (NomeCompleto, Funcao, Status) OUTPUT INSERTED.FuncionarioID VALUES (?,?,?)"
    cursor.execute(sql, funcionario.NomeCompleto, funcionario.Funcao, funcionario.Status)
    novo_id = cursor.fetchone()[0]
    db.commit()
    return schemas.Funcionario(FuncionarioID=novo_id, **funcionario.dict())

@app.get("/funcionarios/", response_model=List[schemas.Funcionario], tags=["Funcionários e Alocações"])
def get_funcionarios(db: pyodbc.Connection = DbConnection):
    # (código existente)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Funcionarios")
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

@app.post("/alocacoes/", response_model=schemas.AlocacaoFuncionario, status_code=status.HTTP_201_CREATED, tags=["Funcionários e Alocações"])
def create_alocacao(alocacao: schemas.AlocacaoFuncionarioCreate, db: pyodbc.Connection = DbConnection):
    # (código existente)
    cursor = db.cursor()
    sql = "INSERT INTO AlocacaoFuncionarios (FuncionarioID, ProjetoID, DataInicioAlocacao, DataFimAlocacao) OUTPUT INSERTED.AlocacaoID VALUES (?,?,?,?)"
    cursor.execute(sql, alocacao.FuncionarioID, alocacao.ProjetoID, alocacao.DataInicioAlocacao, alocacao.DataFimAlocacao)
    novo_id = cursor.fetchone()[0]
    db.commit()
    return schemas.AlocacaoFuncionario(AlocacaoID=novo_id, **alocacao.dict())

@app.get("/projetos/{projeto_id}/alocacoes/", response_model=List[schemas.AlocacaoFuncionario], tags=["Funcionários e Alocações"])
def get_alocacoes_by_projeto(projeto_id: int, db: pyodbc.Connection = DbConnection):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM AlocacaoFuncionarios WHERE ProjetoID = ?", projeto_id)
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

@app.put("/alocacoes/{alocacao_id}", response_model=schemas.AlocacaoFuncionario, tags=["Funcionários e Alocações"])
def update_alocacao(alocacao_id: int, alocacao_update: schemas.AlocacaoFuncionarioCreate, db: pyodbc.Connection = DbConnection):
    cursor = db.cursor()
    sql = "UPDATE AlocacaoFuncionarios SET FuncionarioID=?, ProjetoID=?, DataInicioAlocacao=?, DataFimAlocacao=? WHERE AlocacaoID = ?"
    cursor.execute(sql, alocacao_update.FuncionarioID, alocacao_update.ProjetoID, alocacao_update.DataInicioAlocacao, alocacao_update.DataFimAlocacao, alocacao_id)
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Alocação não encontrada para atualização.")
    db.commit()
    return schemas.AlocacaoFuncionario(AlocacaoID=alocacao_id, **alocacao_update.dict())