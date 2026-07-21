from flask import Flask, render_template, request, redirect, url_for, flash

from models.resenha_model import (
    buscar_resenhas,
    adicionar_resenha,
    buscar_resenha_por_id,
    atualizar_resenha,
    excluir_resenha,
    contar_resenhas
)

app = Flask(__name__)
  
app.secret_key = "film_diary_secret_123"

@app.route("/")
def index():

    busca = request.args.get(
        "busca",
        ""
    )

    nota_minima = request.args.get(
        "nota"
    )

    if nota_minima == "None" or nota_minima == "":

        nota_minima = None

    ordem = request.args.get(
        "ordem",
        "recentes"
    )

    resenhas = buscar_resenhas(
        busca,
        nota_minima,
        ordem
    )

    total_filmes = contar_resenhas()

    return render_template(
        "index.html",
        filmes=resenhas,
        total_filmes=total_filmes,
        busca=busca,
        nota_minima=nota_minima,
        ordem=ordem
    )

@app.route(
    "/adicionar",
    methods=["GET", "POST"]
)
def adicionar():

    if request.method == "POST":

        nome = request.form["nome"]
        ano = request.form["ano"]
        texto = request.form["resenha"]
        nota = request.form["nota"]

        resultado = adicionar_resenha(
            nome,
            ano,
            texto,
            nota
        )

        if resultado:

            flash(
                "Resenha adicionada com sucesso!",
                "sucesso"
            )

            return redirect(
                url_for("index")
            )

        else:

            flash(
                "Essa resenha já existe!",
                "erro"
            )

    return render_template(
        "adicionar.html"
    )

@app.route(
    "/editar/<int:id>",
    methods=["GET", "POST"]
)
def editar(id):

    resenha = buscar_resenha_por_id(id)

    if not resenha:

        flash(
            "Resenha não encontrada!",
            "erro"
        )

        return redirect(
            url_for("index")
        )

    if request.method == "POST":

        nome = request.form["nome"]
        ano = request.form["ano"]
        texto = request.form["resenha"]
        nota = request.form["nota"]

        atualizar_resenha(
            id,
            nome,
            ano,
            texto,
            nota
        )

        flash(
            "Resenha atualizada!",
            "sucesso"
        )

        return redirect(
            url_for("index")
        )

    return render_template(
        "editar.html",
        resenha=resenha
    )

@app.route(
    "/excluir/<int:id>",
    methods=["POST"]
)
def excluir(id):

    excluir_resenha(id)

    flash(
        "Resenha excluída!",
        "sucesso"
    )

    return redirect(
        url_for("index")
    )

if __name__ == "__main__":

    app.run(debug=True)