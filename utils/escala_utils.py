from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas

from utils.pagamento import calcular_salarios  # certifique-se de importar corretamente

import json
import os



CAMINHO_ESCALAS = "data/escalas"
os.makedirs(CAMINHO_ESCALAS, exist_ok=True)

def listar_escalas():
    escalas = []
    if not os.path.exists(CAMINHO_ESCALAS):
        return escalas

    for nome_arquivo in os.listdir(CAMINHO_ESCALAS):
        if nome_arquivo.endswith(".json"):
            caminho = os.path.join(CAMINHO_ESCALAS, nome_arquivo)
            with open(caminho, 'r', encoding='utf-8') as f:
                try:
                    escala = json.load(f)
                    escalas.append(escala)
                except json.JSONDecodeError:
                    print(f"Erro ao carregar: {nome_arquivo}")
    return escalas


def salvar_escala(mes, ano, dados):
    nome_arquivo = f"escala_{ano}_{mes}.json"
    caminho = os.path.join(CAMINHO_ESCALAS, nome_arquivo)

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

    # Gera o relatório automaticamente ao salvar a escala
    calcular_salarios(caminho)

def carregar_escala(ano, mes):
    caminho = os.path.join(CAMINHO_ESCALAS, f"escala_{ano}_{mes}.json")
    if not os.path.exists(caminho):
        return "Não foi possível encontrar a escala."
    with open(caminho, "r", encoding="utf-8") as f:
        escala = json.load(f)
    escala.setdefault("ano", ano)
    escala.setdefault("mes", mes)
    return escala


def listar_escalas_salvas():
    os.makedirs(CAMINHO_ESCALAS, exist_ok=True)
    arquivos = [f for f in os.listdir(CAMINHO_ESCALAS) if f.endswith(".json")]
    escalas = []
    for arq in arquivos:
        partes = arq.replace("escala_", "").replace(".json", "").split("_")
        if len(partes) == 2:
            ano, mes = partes
            escalas.append((int(mes), int(ano)))
    escalas.sort(key=lambda x: (x[1], x[0]), reverse=True)
    return escalas

def exportar_pdf(mes, ano):
    # Carrega a escala do mês e ano usando a função carregar_escala
    escala = carregar_escala(ano, mes)
    
    # Verifica se a escala foi carregada corretamente
    if escala is None:
        raise ValueError(f"Escala para {mes}/{ano} não encontrada.")
    
    # Criação do canvas para o PDF em memória (sem salvar em arquivo)
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(letter))
    c.setFont("Helvetica-Bold", 14)
    
    # Cabeçalho centralizado
    largura_pagina, altura_pagina = landscape(letter)  # Obtendo as dimensões da página
    texto_cabecalho = f"Escala de Trabalho - {mes}/{ano}"
    texto_x = (largura_pagina - c.stringWidth(texto_cabecalho, "Helvetica-Bold", 14)) / 2  # Centralizando o texto
    c.drawString(texto_x, 550, texto_cabecalho)
    
    # Cabeçalho da tabela
    dados_tabela = [["Data", "Funcionário", "Tipo"]]
    
    # Processando o calendário
    for semana in escala.get("calendario", []):
        if semana:
            for dia_info in semana:
                if dia_info is None:
                    # Adiciona linha com campos em branco
                    dados_tabela.append(["", "", ""])
                elif isinstance(dia_info, dict):
                    dia = dia_info.get("dia")
                    funcionarios = dia_info.get("funcionarios", [])
                    tipo = dia_info.get("tipo", "")
                    for funcionario in funcionarios:
                        data_str = f"{dia}/{mes}/{ano}" if dia else ""
                        dados_tabela.append([data_str, funcionario, tipo])

    # Criação da tabela
    tabela = Table(dados_tabela, colWidths=[120, 200, 150])
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    # Ajustando a posição da tabela para ficar abaixo do cabeçalho
    tabela.wrapOn(c, largura_pagina - 60, altura_pagina - 150)  # Ajustando largura e altura para ficar na posição correta
    tabela.drawOn(c, 30, 100)  # Desenhando a tabela a partir da posição 30x100
    
    # Salva o conteúdo em memória ao invés de um arquivo físico
    c.save()

    # Retorna o buffer com o conteúdo PDF gerado
    buffer.seek(0)
    return buffer