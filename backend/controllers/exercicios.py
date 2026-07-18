from flask import request, render_template, Blueprint, session, redirect
from datetime import datetime, date
from models import Exercicio, ListaExercicio, Usuario
from database import db
from cache import EXERCICIOS_CACHE

bp_exercicios = Blueprint("exercicios", __name__)


# ADD EXERCICIO

@bp_exercicios.route("/exercicio", methods=["GET", "POST"])
def add_exercicio():
    
    data_exercicios_inicio = None
    data_exercicios_final = None
    data_inicio = None
    data_final = None
    
    lista_exercicios = EXERCICIOS_CACHE.values()
    usuario = Usuario.query.get(session["usuario_id"])

    if request.method == "POST":
        
        acao = request.form.get("acao")
        
        if acao == "salvar":

            exercicio = request.form["exercicio"]
            exercicio_info = ListaExercicio.query.filter_by(exercicio=exercicio).first()
            grupo_muscular = exercicio_info.grupo_muscular
            serie = str(request.form["serie"])
            repeticoes = int(request.form["repeticoes"])
            kg_tempo = float(request.form["kg_tempo"].replace(",", "."))
            
            if usuario.peso is None:
                return render_template("mensagem.html",mensagem="Cadastre seu peso antes de registrar exercícios.",link="/corpo")
    
            calorias = round(repeticoes * kg_tempo * exercicio_info.fator_calorias * usuario.peso/1000,2)
            agora = datetime.now()
            data = agora
            hora = agora.strftime("%H:%M:%S")
            
            novo_exercicio = Exercicio(
                usuario_id=session["usuario_id"],
                data=data,
                hora=hora,
                exercicio=exercicio,
                grupo_muscular = grupo_muscular,
                calorias = calorias,
                serie=serie,
                repeticoes=repeticoes,
                kg_tempo=kg_tempo
            )
    
            db.session.add(novo_exercicio)
    
            db.session.commit()
            return redirect("/exercicio")
            
        elif acao == "filtrar":
            data_inicio = request.form.get("data_inicio")
            data_final = request.form.get("data_final")
            
        if data_inicio:
            data_exercicios_inicio = datetime.strptime(data_inicio,"%Y-%m-%d").date()

        if data_final:
            data_exercicios_final = datetime.strptime(data_final,"%Y-%m-%d").date()
            
    query = Exercicio.query.filter_by(usuario_id=session["usuario_id"])

    if data_exercicios_inicio == None and data_exercicios_final == None:
        query = query.filter(Exercicio.data == date.today())
    
    elif data_exercicios_inicio and not data_exercicios_final:
        query = query.filter(Exercicio.data >= data_exercicios_inicio)
        
    elif data_exercicios_final and not data_exercicios_inicio:
        query = query.filter(Exercicio.data <= data_exercicios_final)
        
    else:
        query = query.filter(Exercicio.data.between(data_exercicios_inicio,data_exercicios_final))
        
    lista = query.order_by(Exercicio.data.desc(),Exercicio.id.desc()).all()

    return render_template(
        "site/forms/exercicios/exercicio.html",
        exercicios=lista_exercicios,
        lista=lista
    )


# EDITAR EXERCICIO

@bp_exercicios.route("/editar-exercicio/<int:id>", methods=["GET", "POST"])
def editar_exercicio(id):

    exercicio = Exercicio.query.filter_by(id=id, usuario_id=session["usuario_id"]).first()
    usuario = Usuario.query.get(session["usuario_id"])

    if not exercicio:
        return render_template(
            "mensagem.html",
            mensagem="Exercício não encontrado.",
            link="/exercicio"
        )

    lista_exercicios = EXERCICIOS_CACHE.values()

    if request.method == "POST":

        exercicio.exercicio = request.form["exercicio"]
        exercicio_info = ListaExercicio.query.filter_by(exercicio=exercicio.exercicio).first()
        exercicio.grupo_muscular = exercicio_info.grupo_muscular
    
        if not exercicio_info:
            return render_template("mensagem.html",mensagem="Exercício não encontrado na base de dados.",link="/exercicio")
    
        exercicio.serie = str(request.form["serie"])
        exercicio.repeticoes = int(request.form["repeticoes"])
        exercicio.kg_tempo = float(request.form["kg_tempo"].replace(",", "."))
        
        if usuario.peso is None:
            return render_template("mensagem.html",mensagem="Cadastre seu peso antes de registrar exercícios.",link="/corpo")        

        exercicio.calorias = round(exercicio.repeticoes * exercicio.kg_tempo * exercicio_info.fator_calorias * usuario.peso/1000,2)

        db.session.commit()

        return render_template(
            "mensagem.html",
            mensagem="Exercício atualizado com sucesso!",
            link="/exercicio"
        )

    return render_template(
        "site/forms/exercicios/exercicio-edicao.html",
        exercicio=exercicio,
        exercicios=lista_exercicios
    )


# EXCLUIR EXERCÍCIO

@bp_exercicios.route("/excluir-exercicio/<int:id>")
def excluir_exercicio(id):

    exercicio = Exercicio.query.filter_by(id=id, usuario_id=session["usuario_id"]).first()

    if not exercicio:
        return render_template(
            "mensagem.html",
            mensagem="Exercício não encontrado.",
            link="/exercicio"
        )

    db.session.delete(exercicio)

    db.session.commit()

    return render_template(
        "mensagem.html",
        mensagem="Exercício excluído com sucesso!",
        link="/exercicio"
    )


#######################################################################
# LISTA DE EXERCICIOS
#######################################################################

# ADICIONAR NOVO EXERCICIO

# @bp_exercicios.route("/novo-exercicio", methods=["GET", "POST"])
# def add_exercicio_lista():

#     if request.method == "POST":

#         exercicio = request.form["exercicio"]

#         grupo_muscular = request.form["grupo_muscular"]

#         novo_exercicio = ListaExercicio(
#             exercicio=exercicio,
#             grupo_muscular=grupo_muscular
#         )

#         db.session.add(novo_exercicio)

#         db.session.commit()

#     exercicios = ListaExercicio.query.order_by(
#         ListaExercicio.exercicio.asc()
#     ).all()

#     return render_template(
#         "/site/forms/exercicios/add-exercicio.html",
#         exercicios=exercicios
#     )


# EDITAR EXERCICIO DA LISTA

# @bp_exercicios.route(
#     "/editar-exercicio-lista/<int:id>",
#     methods=["GET", "POST"]
# )
# def editar_exercicio_lista(id):

#     item = ListaExercicio.query.get(id)

#     if not item:
#         return render_template(
#             "mensagem.html",
#             mensagem="Exercício não encontrado!",
#             link="/novo-exercicio"
#         )

#     if request.method == "POST":

#         item.exercicio = request.form["exercicio"]
#         item.grupo_muscular = int(request.form["grupo_muscular"])

#         db.session.commit()

#         return render_template(
#             "mensagem.html",
#             mensagem="Exercício atualizado com sucesso!",
#             link="/novo-exercicio"
#         )

#     return render_template(
#         "site/forms/exercicios/editar-exercicio.html",
#         exercicio=item
#     )


# # EXCLUIR EXERCICIO DA LISTA

# @bp_exercicios.route("/excluir-exercicio-lista/<int:id>")
# def excluir_exercicio_lista(id):

#     item = ListaExercicio.query.filter_by(id=id, usuario_id=session["usuario_id"]).first()

#     if not item:
#         return render_template(
#             "mensagem.html",
#             mensagem="Exercício não encontrado.",
#             link="/novo-exercicio"
#         )

#     db.session.delete(item)

#     db.session.commit()

#     return render_template(
#         "mensagem.html",
#         mensagem="Exercício Excluído com Sucesso.",
#         link="/novo-exercicio"
#     )