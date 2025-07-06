from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from supabase import create_client
from openai import OpenAI
import unicodedata

def normalizar(texto):
    """
    Transforma texto para minúsculas, remove acentos e espaços.
    """
    nfkd = unicodedata.normalize('NFKD', texto)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)]).lower().strip()


SUPA_URL = os.getenv("SUPA_URL")
SUPA_KEY = os.getenv("SUPA_KEY")
OPENAI_KEY = os.getenv("OPENAI_KEY")
if not all([SUPA_URL, SUPA_KEY, OPENAI_KEY]):
    raise RuntimeError("Set SUPA_URL SUPA_KEY OPENAI_KEY env variables")

supa = create_client(SUPA_URL, SUPA_KEY)
ai = OpenAI(api_key=OPENAI_KEY)

app = FastAPI(title="Fiore RH API", version="0.1.0")


class PDIRequest(BaseModel):
    nome: str

class PDIResponse(BaseModel):
    pdi: str


def gerar_pdi(nome: str) -> str:
    # Busca todos os colaboradores
    todos = supa.table("colaboradores").select("id, nome, perfil_pred, perfil_sec").execute().data

    # Normaliza nomes do banco
    mapeados = {normalizar(c['nome']): c for c in todos}

    # Normaliza nome recebido
    nome_normalizado = normalizar(nome)

    # Verifica se existe
    if nome_normalizado not in mapeados:
        nomes_validos = [c['nome'] for c in todos]
        raise HTTPException(
            status_code=404,
            detail=f"Colaborador não encontrado. Use um destes nomes: {', '.join(nomes_validos)}"
        )

    col = mapeados[nome_normalizado]

    # Busca os inputs recentes
    inputs = supa.table("inputs").select("texto,data") \
        .eq("colaborador_id", col["id"]) \
        .order("data", desc=True).limit(5).execute().data

    ctx = "\n".join([f"- {i['data'][:10]}: {i['texto']}" for i in inputs]) or "(sem inputs)"

    prompt = f"""Você é CHRO virtual.
Perfil DISC: {col['perfil_pred']}/{col['perfil_sec']}.
Inputs recentes:
{ctx}
Crie um PDI com 3 ações concretas e 1 alerta se necessário."""

    chat = ai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return chat.choices[0].message.content.strip()


@app.post("/pdi", response_model=PDIResponse)
def pdi(req: PDIRequest):
    texto = gerar_pdi(req.nome.strip())
    return {"pdi": texto}