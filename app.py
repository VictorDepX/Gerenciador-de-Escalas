from flask import Flask, render_template, request, redirect, url_for, Response
from datetime import date, timedelta

from utils.escala_utils import *
from utils.pagamento import *

import json
import os
import calendar
import random

app = Flask(__name__)

def pegar_ultima_escala():
    path = "data/escalas"
    arquivos = os.listdir(path)
    arquivos_json = [f for f in arquivos if f.endswith(".json")]
    if not arquivos_json:
        return None, None, {}
    
    arquivos_json.sort(reverse=True)
    nome_arquivo = arquivos_json[0]
    ano, mes = map(int, nome_arquivo.replace("escala_", "").replace(".json", "").split("_"))
    escala = carregar_escala(ano, mes)
    return ano, mes, escala

def carregar_funcionarios():
    caminho = os.path.join("data", "funcionarios.json")
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

@app.route('/')
def index():
    ano = request.args.get('ano', type=int)
    mes = request.args.get('mes', type=int)
    
    escala = None
    if ano and mes:
        escala = carregar_escala(ano, mes)
    
    # Lista de escalas já salvas
    escalas = listar_escalas()
    
    return render_template('index.html', escala=escala, escalas=escalas)


@app.route("/gerar", methods=["GET", "POST"])
def gerar():
    if request.method == "POST":
        # Extrair ano e mês do campo 'mes_ano'
        mes_ano = request.form.get("mes_ano")  # Formato: '2025-04'
        ano, mes = map(int, mes_ano.split("-"))

        # Carrega os nomes dos funcionários
        caminho = os.path.join("data", "funcionarios.json")
        with open(caminho, "r", encoding="utf-8") as f:
            funcionarios = json.load(f)

        # Geração da escala complexa
        _, ultimo_dia = calendar.monthrange(ano, mes)
        calendario = []
        semana = []

        data_atual = date(ano, mes, 1)
        primeiro_dia_semana = data_atual.weekday()  # segunda = 0, domingo = 6
        dia_semana_indexado = (primeiro_dia_semana + 1) % 7  # domingo = 0

        # Preenche os dias em branco da primeira semana
        for _ in range(dia_semana_indexado):
            semana.append(None)

        for dia in range(1, ultimo_dia + 1):
            tipo = "fim-de-semana" if data_atual.weekday() >= 5 else "dia-util"
            # Lógica para não escalar ninguém aos domingos
            if data_atual.weekday() == 6:
                semana.append({
                    "dia": dia,
                    "tipo": "domingo",
                    "funcionarios": []
                })
            else:
                escolhidos = random.sample(funcionarios, 2)
                semana.append({
                    "dia": dia,
                    "tipo": tipo,
                    "funcionarios": escolhidos
                })

            if len(semana) == 7:
                calendario.append(semana)
                semana = []

            data_atual += timedelta(days=1)

        if semana:
            while len(semana) < 7:
                semana.append(None)
            calendario.append(semana)

        escala = {
            "ano": ano,
            "mes": mes,
            "calendario": calendario
        }

        salvar_escala(mes, ano, escala)
        return redirect(url_for("index", ano=ano, mes=mes))

    return render_template("gerar.html")


@app.route("/editar/<int:ano>/<int:mes>", methods=["GET", "POST"])
def editar(ano, mes):
    escala = carregar_escala(ano, mes)
    if not escala:
        return "Escala não encontrada."

    funcionarios = carregar_funcionarios()

    if request.method == "POST":
        dia = int(request.form["dia"])
        alvo = int(request.form["alvo"])  # 0 ou 1
        novo_func = request.form["funcionario"]

        for semana in escala['calendario']:
            for dia_semana in semana:
                if dia_semana and dia_semana["dia"] == dia:
                    escala_funcionarios = dia_semana["funcionarios"]
                    escala_funcionarios[alvo] = novo_func
                    break

        salvar_escala(mes, ano, escala)
        return redirect(url_for("editar", ano=ano, mes=mes))

    return render_template("editar.html", escala=escala, ano=ano, mes=mes, funcionarios=funcionarios)

@app.route("/exportar/<int:mes>/<int:ano>")
def exportar(ano, mes):
    # Gera o PDF para o mês e ano solicitados
    pdf_buffer = exportar_pdf(mes, ano)

    # Envia o PDF gerado como resposta para o usuário
    return Response(
        pdf_buffer,
        mimetype='application/pdf',
        headers={"Content-Disposition": f"attachment;filename=escala_{mes}_{ano}.pdf"}
    )

@app.route('/relatorio/<int:ano>/<int:mes>')
def relatorio(ano, mes):
    escala_path = f"data/escalas/escala_{ano}_{mes}.json"
    relatorio_path = calcular_salarios(escala_path)

    with open(relatorio_path, 'r', encoding='utf-8') as f:
        resultados = json.load(f)

    return render_template('relatorio.html', resultados=resultados)



if __name__ == "__main__":
    app.run(debug=True)

