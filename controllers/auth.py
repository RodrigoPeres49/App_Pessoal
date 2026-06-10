from flask import (Blueprint,render_template,request,redirect,session)
from datetime import date
from models import db, Usuario

bp_auth = Blueprint("auth", __name__)

# CADASTRO

@bp_auth.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form["email"]
        data_nasc = date.fromisoformat(request.form["data_nasc"])
        idade = Usuario.definir_idade(data_nasc)
        sexo = request.form["sexo"]
        senha = request.form["senha"]

        usuario_existente = Usuario.query.filter_by(
            email=email
        ).first()

        if usuario_existente:

            return render_template(
                "mensagem.html",
                mensagem="Email já cadastrado.",
                link="/cadastro"
            )

        usuario = Usuario(
            nome=nome,
            email=email,
            data_nasc = data_nasc,
            idade = idade,
            sexo = sexo
        )

        usuario.set_senha(senha)

        db.session.add(usuario)
        db.session.commit()

        return render_template(
            "mensagem.html",
            mensagem="Cadastro realizado com sucesso!",
            link="/login"
        )

    return render_template(
        "login/cadastro.html"
    )
    
# LOGIN

@bp_auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        senha = request.form["senha"]

        usuario = Usuario.query.filter_by(
            email=email
        ).first()

        if not usuario:

            return render_template(
                "mensagem.html",
                mensagem="Usuário não encontrado.",
                link="/login"
            )

        if not usuario.verificar_senha(senha):

            return render_template(
                "mensagem.html",
                mensagem="Senha incorreta.",
                link="/login"
            )

        session["usuario_id"] = usuario.id
        session["usuario_nome"] = usuario.nome

        return redirect("/")

    return render_template("login/login.html")
    
# LOGOUT

@bp_auth.route("/logout")
def logout():

    session.clear()

    return redirect("/login")