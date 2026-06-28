from flask import Flask, render_template, redirect, session
import secrets
from sqlalchemy import func
from controllers.exercicios import bp_exercicios
from controllers.refeicoes import bp_refeicoes
from controllers.cardio import bp_cardio
from controllers.corpo import bp_corpo
from controllers.auth import bp_auth
from database import db
from models import Alimento, ListaExercicio, Refeicao, Cardio, Exercicio, Usuario
import pandas as pd
from datetime import datetime
import os
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)


uri = os.environ.get("DATABASE_URL")

if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
    
if not uri:
    uri = "sqlite:///database.db"

app.config["SQLALCHEMY_DATABASE_URI"] = uri

db.init_app(app)

with app.app_context():

    migrate = Migrate(app, db)

    # IMPORTAR ALIMENTOS

    if Alimento.query.count() == 0:

        df_alimentos = pd.read_excel(
            "Tabelas.xlsx",
            sheet_name="Alimentos"
        )

        for _, row in df_alimentos.iterrows():

            novo_alimento = Alimento(
                alimento=row["Alimento"],
                calorias=float(row["Calorias"]),
                proteinas=float(row["Proteinas"]),
                carboidratos=float(row["Carboidratos"]),
                fibras=float(row["Fibras"]),
                gorduras=float(row["Gorduras"])
            )

            db.session.add(novo_alimento)

        print("Alimentos importados!")

    # IMPORTAR EXERCÍCIOS

    if ListaExercicio.query.count() == 0:

        df_exercicios = pd.read_excel(
            "Tabelas.xlsx",
            sheet_name="Exercicios"
        )
        
        for _, row in df_exercicios.iterrows():

            novo_exercicio = ListaExercicio(
                exercicio=row["Exercicio"],
                grupo_muscular=row["Grupo Muscular"],
                fator_calorias = float(row["Fator_Calorias"])
            )

            db.session.add(novo_exercicio)

        print("Exercícios importados!")

    db.session.commit()

@app.route("/")
def index():

    if "usuario_id" not in session: 
        return redirect("/login")
    
    usuario = Usuario.query.get(session["usuario_id"])

    hoje = datetime.now().date()

    calorias_refeicoes = db.session.query(
        func.sum(Refeicao.calorias)
    ).filter(
        Refeicao.usuario_id == usuario.id,
        Refeicao.data == hoje
    ).scalar() or 0
    
    calorias_cardio = db.session.query(
        func.sum(Cardio.calorias)
    ).filter(
        Cardio.usuario_id == usuario.id,
        Cardio.data == hoje
    ).scalar() or 0

    calorias_exercicios = db.session.query(
        func.sum(Exercicio.calorias)
    ).filter(
        Exercicio.usuario_id == usuario.id,
        Exercicio.data == hoje
    ).scalar() or 0   
    
    calorias_consumidas = (calorias_refeicoes - calorias_cardio - calorias_exercicios)
    
    proteinas_consumidas = db.session.query(
        func.sum(Refeicao.proteinas)
    ).filter(
        Refeicao.usuario_id == usuario.id,
        Refeicao.data == hoje
    ).scalar() or 0
    
    carboidratos_consumidos = db.session.query(
        func.sum(Refeicao.carboidratos)
    ).filter(
        Refeicao.usuario_id == usuario.id,
        Refeicao.data == hoje
    ).scalar() or 0
    
    fibras_consumidas = db.session.query(
        func.sum(Refeicao.fibras)
    ).filter(
        Refeicao.usuario_id == usuario.id,
        Refeicao.data == hoje
    ).scalar() or 0
    
    gorduras_consumidas = db.session.query(
        func.sum(Refeicao.gorduras)
    ).filter(
        Refeicao.usuario_id == usuario.id,
        Refeicao.data == hoje
    ).scalar() or 0
    

    return render_template(
        "site/body.html",
        usuario=usuario,
        calorias_consumidas=round(calorias_consumidas,2),
        proteinas_consumidas=round(proteinas_consumidas,2),
        carboidratos_consumidos=round(carboidratos_consumidos,2),
        fibras_consumidas=round(fibras_consumidas,2),
        gorduras_consumidas=round(gorduras_consumidas,2),
        calorias_cardio = calorias_cardio,
        hoje = hoje
    )
@app.route("/inativo")
def index():
    return render_template("mensagem.html", mensagem="Modo inativo no momento", link = "/")

app.register_blueprint(bp_exercicios)
app.register_blueprint(bp_refeicoes)
app.register_blueprint(bp_corpo)
app.register_blueprint(bp_cardio)
app.register_blueprint(bp_auth)

if __name__ == "__main__":
    app.run()