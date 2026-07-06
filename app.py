from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
import unicodedata

app = Flask(__name__, static_folder="static")

app.secret_key = "film_diary_secret_123"

ARQUIVO_JSON = os.path.join(os.path.dirname(__file__), "database", "resenhas.json")

def normalizar(texto):
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")

def carregar_resenhas():
    if not os.path.exists(ARQUIVO_JSON):
        return []

    with open(ARQUIVO_JSON, "r", encoding="utf-8") as arquivo:
        try:
            dados = json.load(arquivo)
            return dados if isinstance(dados, list) else []
        except json.JSONDecodeError:
            return []

def salvar_resenhas(resenhas):
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
        json.dump(resenhas, arquivo, indent=4, ensure_ascii=False)

@app.route("/")
def index():

    resenhas = carregar_resenhas()

    total_filmes = len(resenhas)

    busca = request.args.get("busca", "").strip()

    if busca:
        busca_norm = normalizar(busca)

        resenhas = [
            r for r in resenhas
            if busca_norm in normalizar(r.get("nome", ""))
        ]

    nota_minima = request.args.get("nota")

    if nota_minima:
        try:
            nota = int(nota_minima)

            resenhas = [
                r for r in resenhas
                if int(r.get("nota", 0)) == nota
            ]

        except ValueError:
            pass

    for r in resenhas:
        r["is_long"] = len(r.get("resenha", "")) > 250

    return render_template(
        "index.html",
        filmes=resenhas,
        total_filmes=total_filmes,
        busca=busca,
        nota_minima=nota_minima
    )

@app.route("/adicionar", methods=["GET", "POST"])
def adicionar():

    if request.method == "POST":

        resenhas = carregar_resenhas()

        nome = request.form.get("nome", "").strip()
        ano = request.form.get("ano", "").strip()
        resenha = request.form.get("resenha", "").strip()

        nota_raw = request.form.get("nota", "").strip()

        try:
            nota = int(nota_raw)

            if nota < 0 or nota > 10:
                flash("A nota deve estar entre 0 e 10.")
                return redirect(url_for("adicionar"))

        except ValueError:
            flash("A nota deve ser um número inteiro entre 0 e 10.")
            return redirect(url_for("adicionar"))

        existe = any(
            r.get("nome", "").strip().lower() == nome.lower()
            and r.get("ano", "").strip() == ano
            and r.get("resenha", "").strip() == resenha
            and int(r.get("nota", 0)) == nota
            for r in resenhas
        )

        if existe:
            flash("Essa resenha já existe!")
            return redirect(url_for("adicionar"))

        novo_id = max([r.get("id", 0) for r in resenhas], default=0) + 1

        nova_resenha = {
            "id": novo_id,
            "nome": nome,
            "ano": ano,
            "resenha": resenha,
            "nota": nota
        }

        resenhas.append(nova_resenha)
        salvar_resenhas(resenhas)

        flash("Resenha adicionada com sucesso!")
        return redirect(url_for("index"))

    return render_template("adicionar.html")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    resenhas = carregar_resenhas()

    resenha = next((r for r in resenhas if r["id"] == id), None)

    if not resenha:
        return "Resenha não encontrada."

    if request.method == "POST":

        resenha["nome"] = request.form.get("nome", "").strip()
        resenha["ano"] = request.form.get("ano", "").strip()
        resenha["resenha"] = request.form.get("resenha", "").strip()

        nota_raw = request.form.get("nota", "").strip()

        try:
            nota = int(nota_raw)

            if nota < 0 or nota > 10:
                flash("A nota deve estar entre 0 e 10.")
                return redirect(url_for("editar", id=id))

            resenha["nota"] = nota

        except ValueError:
            flash("A nota deve ser um número inteiro entre 0 e 10.")
            return redirect(url_for("editar", id=id))

        salvar_resenhas(resenhas)

        flash("Resenha editada com sucesso!")
        return redirect(url_for("index"))

    return render_template("editar.html", filme=resenha)

@app.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):

    resenhas = carregar_resenhas()

    resenhas = [r for r in resenhas if r["id"] != id]

    salvar_resenhas(resenhas)

    flash("Resenha excluída com sucesso!")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)