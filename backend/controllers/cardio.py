from flask import request, render_template, Blueprint, session
from datetime import date
from models import Cardio, Atividades
from database import db

bp_cardio = Blueprint("cardio", __name__)


# ADD EXERCICIO

@bp_cardio.route("/cardio", methods=["GET", "POST"])
def add_cardio():

    lista_atividades = Atividades.query.all()

    if request.method == "POST":

        data = data = date.fromisoformat(request.form["data"])
        hora = request.form["hora"]
        atividade = request.form["atividade"]
        duracao = request.form["duracao"]
        distancia = float(request.form["distancia"])
        calorias = float(request.form["calorias"])
        frequencia_media = float(request.form["frequencia_media"])
        frequencia_maxima = float(request.form["frequencia_maxima"])
        observacoes = request.form["observacoes"]

        novo_cardio = Cardio(
            usuario_id=session["usuario_id"],
            data=data,
            hora=hora,
            atividade = atividade,
            duracao = duracao,
            distancia = distancia,
            calorias = calorias,
            frequencia_media = frequencia_media,
            frequencia_maxima = frequencia_maxima,
            observacoes = observacoes,
        )

        db.session.add(novo_cardio)

        db.session.commit()

    lista = Cardio.query.filter_by(usuario_id=session["usuario_id"]).order_by(
        Cardio.atividade.desc()
    ).all()

    return render_template(
        "site/forms/exercicios/registrar-cardio.html",
        atividades= lista_atividades,
        lista=lista
    )


# EDITAR EXERCICIO

@bp_cardio.route("/editar-cardio/<int:id>", methods=["GET", "POST"])
def editar_cardio(id):
    
    lista_atividades = Atividades.query.all()
    
    cardio = Cardio.query.filter_by(id=id, usuario_id=session["usuario_id"]).first()

    if not cardio:
        return render_template(
            "mensagem.html",
            mensagem="Cardio não encontrado.",
            link="/cardio"
        )

    lista_atividades = Atividades.query.all()

    if request.method == "POST":

        cardio.data = date.fromisoformat(request.form["data"])
        cardio.hora = str(request.form["hora"])
        atividade = request.form["atividade"]
        duracao = request.form["duracao"]
        distancia = float(request.form["distancia"])
        calorias = float(request.form["calorias"])
        frequencia_media = float(request.form["frequencia_media"])
        frequencia_maxima = float(request.form["frequencia_maxima"])
        observacoes = request.form["observacoes"]

        db.session.commit()

        return render_template(
            "mensagem.html",
            mensagem="Exercício cardiovasculas atualizado com sucesso!",
            link="/cardio"
        )

    return render_template(
        "site/forms/exercicios/cardio-edicao.html",
        cardio=cardio,
        atividades= lista_atividades
    )


# EXCLUIR EXERCÍCIO

@bp_cardio.route("/excluir-cardio/<int:id>")
def excluir_cardio(id):

    cardio = Cardio.query.filter_by(id=id, usuario_id=session["usuario_id"]).first()

    if not cardio:
        return render_template(
            "mensagem.html",
            mensagem="Exercício cardiovascular não encontrado.",
            link="/cardio"
        )

    db.session.delete(cardio)

    db.session.commit()

    return render_template(
        "mensagem.html",
        mensagem="Exercício cardiovascular excluído com sucesso!",
        link="/cardio"
    )


#######################################################################
# LISTA DE ATIVIDADES
#######################################################################

# ADICIONAR NOVA ATIVIDADE

@bp_cardio.route("/nova-atividade", methods=["GET", "POST"])
def add_atividade():

    if request.method == "POST":

        atividade = request.form["atividade"]


        nova_atividade = Atividades(
            atividade=atividade,
        )

        db.session.add(nova_atividade)

        db.session.commit()

    atividades = Atividades.query.order_by(
        Atividades.exercicio.asc()
    ).all()

    return render_template(
        "/site/forms/exercicios/add-atividade.html",
        atividades = atividades
    )


# EDITAR EXERCICIO DA LISTA

@bp_cardio.route(
    "/editar-atividade/<int:id>",
    methods=["GET", "POST"]
)
def editar_exercicio_lista(id):

    item = Atividades.query.get(id)

    if not item:
        return render_template(
            "mensagem.html",
            mensagem="Atividade não encontrada!",
            link="/nova-atividade"
        )

    if request.method == "POST":

        item.exercicio = request.form["exercicio"]

        item.repeticoes = int(
            request.form["meta_repeticoes"]
        )

        db.session.commit()

        return render_template(
            "mensagem.html",
            mensagem="Atividade atualizada com sucesso!",
            link="/nova-atividade"
        )

    return render_template(
        "site/forms/exercicios/editar-atividade.html",
        atividade=item
    )


# EXCLUIR EXERCICIO DA LISTA

@bp_cardio.route("/excluir-atividade/<int:id>")
def excluir_exercicio_lista(id):

    item = Atividades.query.get(id)

    if not item:
        return render_template(
            "mensagem.html",
            mensagem="Exercício não encontrado.",
            link="/nova-atividade"
        )

    db.session.delete(item)

    db.session.commit()

    return render_template(
        "mensagem.html",
        mensagem="Atividade Excluída com Sucesso.",
        link="/nova-atividade"
    )