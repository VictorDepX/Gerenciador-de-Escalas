import json
from collections import defaultdict
import os

SALARIO_MINIMO = 1418.00
CARGA_MENSAL = 220

def calcular_salarios(path_json):
    with open(path_json, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    ano = dados['ano']
    mes = dados['mes']
    calendario = dados['calendario']
    
    funcionarios = {}

    # Percorrer cada semana do calendário
    for semana in calendario:
        for dia in semana:
            if dia is None:
                continue  # Ignora os dias com valor None
            if 'funcionarios' not in dia or not dia['funcionarios']:
                continue  # Ignora dias sem funcionários

            # Percorre os funcionários do dia
            for nome in dia['funcionarios']:
                nome = nome.strip()
                if not nome:
                    continue
                if nome not in funcionarios:
                    funcionarios[nome] = {'dias': 0}
                funcionarios[nome]['dias'] += 1
    
    # Monta o relatório com o cálculo de salários
    relatorio = []
    for nome, info in funcionarios.items():
        dias = info['dias']
        horas = dias * 6  # Cada dia tem 6 horas de trabalho
        salario = horas * 10  # Cada hora vale 10 reais
        relatorio.append({
            'nome': nome,
            'dias_trabalhados': dias,
            'horas': horas,
            'salario': salario
        })
    
    # Cria a pasta data/relatorios se não existir
    os.makedirs('data/relatorios', exist_ok=True)
    relatorio_path = f"data/relatorios/relatorio_{ano}_{mes}.json"
    
    # Salva o relatório em formato JSON
    with open(relatorio_path, 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, indent=4, ensure_ascii=False)
    
    return relatorio_path