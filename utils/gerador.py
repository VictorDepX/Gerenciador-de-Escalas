from datetime import datetime, timedelta
import calendar
import json
import os

DADOS_PATH = "data/funcionarios.json"

def carregar_funcionarios():
    if os.path.exists(DADOS_PATH):
        with open(DADOS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_escala_json(nome_arquivo, escala):
    path = os.path.join("data", nome_arquivo)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(escala, f, indent=4, ensure_ascii=False)

def carregar_escala_json(nome_arquivo):
    path = os.path.join("data", nome_arquivo)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def gerar_escala(mes, ano):
    funcionarios = carregar_funcionarios()
    if not funcionarios:
        return {}

    calendario = calendar.Calendar()
    dias_do_mes = [dia for dia in calendario.itermonthdates(ano, mes) if dia.month == mes]

    escala = {}
    total_funcionarios = len(funcionarios)
    idx = 0

    for dia in dias_do_mes:
        dia_str = dia.strftime("%Y-%m-%d")
        funcionario = funcionarios[idx % total_funcionarios]
        escala[dia_str] = funcionario
        idx += 1

    return escala

def calcular_pagamento(escala):
    funcionarios = carregar_funcionarios()
    nomes = [f for f in funcionarios]
    salario_base = 1418.00
    horas_mensal = 220
    valor_hora = salario_base / horas_mensal

    contagem = {f: 0 for f in nomes}

    for dia, funcionario in escala.items():
        contagem[funcionario] += 1

    resultado = {}
    for nome, dias_trabalhados in contagem.items():
        horas_trabalhadas = dias_trabalhados * 6
        salario = horas_trabalhadas * valor_hora
        resultado[nome] = {
            "dias": dias_trabalhados,
            "horas": horas_trabalhadas,
            "salario": round(salario, 2)
        }

    return resultado
