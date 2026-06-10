from flask import request, render_template, Blueprint, session
from datetime import datetime
from models import db, Refeicao, Alimento

bp_refeicoes = Blueprint("refeicoes", __name__)

# ADD REFEIÇÃO

@bp_refeicoes.route("/alimentacao", methods=["GET", "POST"])
def add_refeicao():

    alimentos = Alimento.query.all()

    if request.method == "POST":

        alimento_nome = request.form["alimento"]
        quantidade = float(request.form["quantidade"].replace(",", "."))

        alimento = Alimento.query.filter_by(
            alimento=alimento_nome
        ).first()

        if alimento:

            calorias = round(alimento.calorias * quantidade, 2)
            proteinas = round(alimento.proteinas * quantidade, 2)
            fibras = round(alimento.fibras * quantidade, 2)
            carboidratos = round(alimento.carboidratos * quantidade, 2)
            gorduras = round(alimento.gorduras * quantidade, 2)

        else:

            calorias = 0
            proteinas = 0
            fibras = 0
            carboidratos = 0
            gorduras = 0

        agora = datetime.now()

        nova_refeicao = Refeicao(
            usuario_id=session["usuario_id"],
            data=agora,
            hora=agora.strftime("%H:%M:%S"),
            alimento=alimento_nome,
            calorias=calorias,
            proteinas=proteinas,
            carboidratos = carboidratos,
            quantidade=quantidade,
            fibras=fibras,
            gorduras=gorduras
        )

        db.session.add(nova_refeicao)
        db.session.commit()

    lista = Refeicao.query.filter_by(usuario_id=session["usuario_id"]).order_by(Refeicao.data.desc(),Refeicao.hora.desc()).all()

    return render_template(
        "site/forms/refeicoes/refeicao.html",
        refeicoes=alimentos,
        lista=lista
    )


# EDITAR REFEIÇÃO

@bp_refeicoes.route("/editar-refeicao/<int:id>", methods=["GET", "POST"])
def editar_refeicao(id):

    refeicao = Refeicao.query.filter_by(id=id, usuario_id=session["usuario_id"]).first()

    if not refeicao:
        return render_template(
            "mensagem.html",
            mensagem="Refeição não encontrada!",
            link="/alimentacao"
        )

    alimentos = Alimento.query.all()

    if request.method == "POST":

        alimento_nome = request.form["alimento"]
        quantidade = float(request.form["quantidade"].replace(",", "."))

        alimento = Alimento.query.filter_by(
            alimento=alimento_nome
        ).first()

        if alimento:

            refeicao.calorias = round(alimento.calorias * quantidade, 2)
            refeicao.proteinas = round(alimento.proteinas * quantidade, 2)
            refeicao.carboidratos = round(alimento.carboidratos * quantidade, 2)
            refeicao.fibras = round(alimento.fibras * quantidade, 2)
            refeicao.gorduras = round(alimento.gorduras * quantidade, 2)

        else:

            refeicao.calorias = 0
            refeicao.proteinas = 0
            refeicao.carboidratos = 0
            refeicao.fibras = 0
            refeicao.gorduras = 0

        refeicao.alimento = alimento_nome
        refeicao.quantidade = quantidade

        db.session.commit()

        return render_template(
            "mensagem.html",
            mensagem="Refeição atualizada com sucesso!",
            link="/alimentacao"
        )

    return render_template(
        "site/forms/refeicoes/refeicao-edicao.html",
        refeicao=refeicao,
        refeicoes=alimentos
    )


# EXCLUIR REFEIÇÃO

@bp_refeicoes.route("/excluir-refeicao/<int:id>")
def excluir_refeicao(id):

    refeicao = Refeicao.query.filter_by(id=id, usuario_id=session["usuario_id"]).first()

    if not refeicao:

        return render_template(
            "mensagem.html",
            mensagem="Refeição não encontrada.",
            link="/alimentacao"
        )

    db.session.delete(refeicao)
    db.session.commit()

    return render_template(
        "mensagem.html",
        mensagem="Refeição excluída com sucesso!",
        link="/alimentacao"
    )


####################################################################
# TABELA DE ALIMENTOS
####################################################################

# ADICIONAR ALIMENTO

@bp_refeicoes.route("/novo-alimento", methods=["GET", "POST"])
def add_alimento():

    if request.method == "POST":

        alimento = request.form["alimento"]
        calorias = float(request.form["calorias"].replace(",", "."))
        proteinas = float(request.form["proteinas"].replace(",", "."))
        carboidratos = float(request.form["carboidratos"].replace(",", "."))
        fibras = float(request.form["fibras"].replace(",", "."))
        gorduras = float(request.form["gorduras"].replace(",", "."))

        novo_alimento = Alimento(
            alimento=alimento,
            calorias=calorias,
            proteinas=proteinas,
            carboidratos = carboidratos,
            fibras=fibras,
            gorduras=gorduras
        )

        db.session.add(novo_alimento)
        db.session.commit()

    alimentos = Alimento.query.all()

    return render_template(
        "site/forms/refeicoes/add-alimento.html",
        alimentos=alimentos
    )


# EDITAR ALIMENTO

@bp_refeicoes.route("/editar-alimento/<int:id>", methods=["GET", "POST"])
def editar_alimento(id):

    alimento = Alimento.query.get(id)

    if not alimento:

        return render_template(
            "mensagem.html",
            mensagem="Alimento não encontrado!",
            link="/novo-alimento"
        )

    if request.method == "POST":

        alimento.alimento = request.form["alimento"]
        alimento.calorias = float(request.form["calorias"].replace(",", "."))
        alimento.proteinas = float(request.form["proteinas"].replace(",", "."))
        alimento.carboidratos = float(request.form["carboidratos"].replace(",","."))
        alimento.fibras = float(request.form["fibras"].replace(",", "."))
        alimento.gorduras = float(request.form["gorduras"].replace(",", "."))

        db.session.commit()

        return render_template(
            "mensagem.html",
            mensagem="Alimento atualizado com sucesso!",
            link="/novo-alimento"
        )

    return render_template(
        "site/forms/refeicoes/editar-alimento.html",
        alimento=alimento
    )


# EXCLUIR ALIMENTO

@bp_refeicoes.route("/excluir-alimento/<int:id>")
def excluir_alimento(id):

    alimento = Alimento.query.get(id)

    if not alimento:

        return render_template(
            "mensagem.html",
            mensagem="Alimento não encontrado.",
            link="/novo-alimento"
        )

    db.session.delete(alimento)
    db.session.commit()

    return render_template(
        "mensagem.html",
        mensagem="Alimento excluído com sucesso.",
        link="/novo-alimento"
    )
    