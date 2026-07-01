from flask import request, render_template, Blueprint, session, redirect
from datetime import date, datetime
from models import Agua
from database import db

bp_agua = Blueprint("agua", __name__)


# ADICIONAR CONSUMO DE ÁGUA

@bp_agua.route("/agua", methods=["GET", "POST"])
def add_agua():

    data_agua_inicio = None
    data_agua_final = None
    data_inicio = None
    data_final = None

    if request.method == "POST":

        acao = request.form.get("acao")

        if acao == "salvar":

            data = date.fromisoformat(request.form["data"])
            hora = request.form["hora"]
            quantidade = float(request.form["quantidade"])
            observacoes = request.form["observacoes"]

            novo_registro = Agua(
                usuario_id=session["usuario_id"],
                data=data,
                hora=hora,
                quantidade=quantidade,
                observacoes=observacoes
            )

            db.session.add(novo_registro)
            db.session.commit()

            return redirect("/agua")

        elif acao == "filtrar":

            data_inicio = request.form.get("data_inicio")
            data_final = request.form.get("data_final")

        if data_inicio:
            data_agua_inicio = datetime.strptime(
                data_inicio,
                "%Y-%m-%d"
            ).date()

        if data_final:
            data_agua_final = datetime.strptime(
                data_final,
                "%Y-%m-%d"
            ).date()

    query = Agua.query.filter_by(usuario_id=session["usuario_id"])

    if data_agua_inicio is None and data_agua_final is None:
        query = query.filter(Agua.data == date.today())

    elif data_agua_inicio and not data_agua_final:
        query = query.filter(Agua.data >= data_agua_inicio)

    elif data_agua_final and not data_agua_inicio:
        query = query.filter(Agua.data <= data_agua_final)

    else:
        query = query.filter(
            Agua.data.between(data_agua_inicio, data_agua_final)
        )

    lista = query.order_by(
        Agua.data.desc(),
        Agua.id.desc()
    ).all()

    return render_template(
        "site/forms/agua/registrar-agua.html",
        lista=lista
    )


# EDITAR CONSUMO DE ÁGUA

@bp_agua.route("/editar-agua/<int:id>", methods=["GET", "POST"])
def editar_agua(id):

    agua = Agua.query.filter_by(
        id=id,
        usuario_id=session["usuario_id"]
    ).first()

    if not agua:
        return render_template(
            "mensagem.html",
            mensagem="Registro de consumo de água não encontrado.",
            link="/agua"
        )

    if request.method == "POST":

        agua.data = date.fromisoformat(request.form["data"])
        agua.hora = request.form["hora"]
        agua.quantidade = float(request.form["quantidade"])
        agua.observacoes = request.form["observacoes"]

        db.session.commit()

        return render_template(
            "mensagem.html",
            mensagem="Registro de consumo de água atualizado com sucesso!",
            link="/agua"
        )

    return render_template(
        "site/forms/agua/agua-edicao.html",
        agua=agua
    )


# EXCLUIR CONSUMO DE ÁGUA

@bp_agua.route("/excluir-agua/<int:id>")
def excluir_agua(id):

    agua = Agua.query.filter_by(
        id=id,
        usuario_id=session["usuario_id"]
    ).first()

    if not agua:
        return render_template(
            "mensagem.html",
            mensagem="Registro de consumo de água não encontrado.",
            link="/agua"
        )

    db.session.delete(agua)
    db.session.commit()

    return render_template(
        "mensagem.html",
        mensagem="Registro de consumo de água excluído com sucesso!",
        link="/agua"
    )