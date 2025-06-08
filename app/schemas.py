# Arquivo: solarys_api/app/schemas.py
from pydantic import BaseModel
import datetime

# --- PROJETOS ---
class ProjetoBase(BaseModel):
    Nome: str
    Descricao: str | None = None
    Localizacao: str | None = None
    DataInicio: datetime.date
    DataPrevistaFim: datetime.date
    Status: str

class ProjetoCreate(ProjetoBase):
    pass

class Projeto(ProjetoBase):
    ProjetoID: int
    class Config: from_attributes = True

# --- TAREFAS ---
class TarefaBase(BaseModel):
    ProjetoID: int
    Descricao: str
    DataInicioPrevista: datetime.datetime
    DataFimPrevista: datetime.datetime
    DataInicioReal: datetime.datetime | None = None
    DataFimReal: datetime.datetime | None = None
    Status: str

class TarefaCreate(TarefaBase):
    pass

class Tarefa(TarefaBase):
    TarefaID: int
    class Config: from_attributes = True

# --- RECURSOS FINANCEIROS ---
class RecursoFinanceiroBase(BaseModel):
    ProjetoID: int
    Tipo: str
    Descricao: str
    Valor: float
    Data: datetime.date

class RecursoFinanceiroCreate(RecursoFinanceiroBase):
    pass

class RecursoFinanceiro(RecursoFinanceiroBase):
    RecursoFinanceiroID: int
    class Config: from_attributes = True

# --- MATERIAIS ---
class MaterialBase(BaseModel):
    ProjetoID: int
    NomeMaterial: str
    QuantidadeNecessaria: float
    QuantidadeEmEstoque: float = 0
    Unidade: str

class MaterialCreate(MaterialBase):
    pass

class Material(MaterialBase):
    MaterialID: int
    class Config: from_attributes = True

# --- FUNCIONÁRIOS ---
class FuncionarioBase(BaseModel):
    NomeCompleto: str
    Funcao: str
    Status: str

class FuncionarioCreate(FuncionarioBase):
    pass

class Funcionario(FuncionarioBase):
    FuncionarioID: int
    class Config: from_attributes = True

# --- ALOCAÇÃO DE FUNCIONÁRIOS ---
class AlocacaoFuncionarioBase(BaseModel):
    FuncionarioID: int
    ProjetoID: int
    DataInicioAlocacao: datetime.date
    DataFimAlocacao: datetime.date | None = None

class AlocacaoFuncionarioCreate(AlocacaoFuncionarioBase):
    pass

class AlocacaoFuncionario(AlocacaoFuncionarioBase):
    AlocacaoID: int
    class Config: from_attributes = True

# --- ALERTAS AI ---
class AlertaAIBase(BaseModel):
    ProjetoID: int
    TipoAlerta: str
    DescricaoAlerta: str
    NivelSeveridade: str
    Status: str

class AlertaAICreate(AlertaAIBase):
    pass

class AlertaAI(AlertaAIBase):
    AlertaID: int
    DataGeracao: datetime.datetime
    class Config: from_attributes = True

# --- SUGESTÕES AI ---
class SugestaoAIBase(BaseModel):
    AlertaID: int
    DescricaoSugestao: str
    ImpactoEstimado: str | None = None
    StatusAprovacao: str = "Pendente"

class SugestaoAICreate(SugestaoAIBase):
    pass

class SugestaoAI(SugestaoAIBase):
    SugestaoID: int
    class Config: from_attributes = True