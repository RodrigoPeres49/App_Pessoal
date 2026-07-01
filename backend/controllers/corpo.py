from flask import Blueprint, render_template, request, session
from math import log10
from models import Usuario
from datetime import date, datetime

from models import (
    db,
    AvaliacaoFisica,
    DobrasCutaneas,
    PerimetrosCorporais,
    Pressao
)

bp_corpo = Blueprint("corpo", __name__)



# FUNÇÃO AUXILIAR


def valor_float(campo):

    valor = request.form.get(campo)

    if valor == "" or valor is None:
        return 0

    return float(valor.replace(",", "."))



# AVALIAÇÃO FÍSICA


@bp_corpo.route("/avaliacao-fisica", methods=["GET", "POST"])
def avaliacao_fisica():

    if request.method == "POST":
        
        usuario = Usuario.query.get(session["usuario_id"])

        # DADOS GERAIS

        data = date.fromisoformat(request.form["data"])
        peso = valor_float("peso")
        altura = valor_float("altura")
        idade = usuario.idade


        # DOBRAS CUTÂNEAS


        subescapular = valor_float("subescapular")
        bicipital = valor_float("bicipital")
        tricipital = valor_float("tricipital")
        axilar_media = valor_float("axilar_media")
        supra_iliaca = valor_float("supra_iliaca")
        supra_espinhal = valor_float("supra_espinhal")
        peitoral = valor_float("peitoral")
        abdominal = valor_float("abdominal")
        coxa = valor_float("coxa")
        panturrilha = valor_float("panturrilha")


        # SOMA DAS DOBRAS


        soma_dobras = (peitoral + abdominal + coxa)


        # DENSIDADE CORPORAL
        # JACKSON & POLLOCK 3 DOBRAS


        if usuario.sexo == "masculino":
        
            densidade_corporal = (
                1.112
                - (0.00043499 * soma_dobras)
                + (0.00000055 * (soma_dobras ** 2))
                - (0.00028826 * idade)
            )
        
        else:  # feminino
        
            densidade_corporal = (
                1.0970
                - (0.00046971 * soma_dobras)
                + (0.00000056 * (soma_dobras ** 2))
                - (0.00012828 * idade)
            )
        

        # PERCENTUAL DE GORDURA
        # FÓRMULA DE SIRI

        percentual_gordura = round(((4.95 / densidade_corporal) - 4.50) * 100,2)

        # IMC

        imc = round(peso / (altura * altura),2)

        # MASSAS


        massa_gorda = round(peso * (percentual_gordura / 100),2)
        massa_magra = round(peso - massa_gorda,2)

        # METAS SAUDÁVEIS

        if idade < 30:
            meta_percentual_gordura = 12
        elif idade < 40:
            meta_percentual_gordura = 14
        elif idade < 50:
            meta_percentual_gordura = 16
        else:
            meta_percentual_gordura = 18
        
        meta_massa_gorda = round(peso * (meta_percentual_gordura / 100),2)
        
        if imc < 22:
           meta_massa_magra = massa_magra + 2
        else:
            meta_massa_magra = massa_magra
        
        
        meta_peso = round(meta_massa_magra /(1 - (meta_percentual_gordura / 100)),2)
        

        
        # USUARIO RECEBENDO O PESO E MASSA EM GERAL
        
        usuario.peso = peso
        usuario.altura = altura
        usuario.meta_peso = meta_peso
        usuario.massa_magra = massa_magra
        usuario.massa_gorda = massa_gorda
        usuario.meta_massa_magra = meta_massa_magra
        usuario.meta_massa_gorda = meta_massa_gorda
        usuario.pecentual_gordura = percentual_gordura
        usuario.imc = imc
        
        # USUARIO RECEBENDO QUANTIDADES DIÁRIAS
        
        # CALORIAS
        
        tmb = 370 + (21.6 * massa_magra)
        fator_atividade = 1.55
        calorias_manutencao = round(tmb * fator_atividade,0)
        calorias_diarias = round(calorias_manutencao * 0.90, 0)
        
        # PROTEINAS, GORDURAS, FIBRAS
        
        proteinas_diarias = round(peso*2,0)
        gorduras_diarias = round(peso*0.8,0)
        fibras_diarias = round(calorias_diarias/1000*14,0)
        
        # CARBOIDRATOS
        
        calorias_proteina = proteinas_diarias * 4
        calorias_gordura = gorduras_diarias * 9
        
        carboidratos_diarios = round((calorias_diarias - calorias_proteina - calorias_gordura)/4,0)
        
        # AGUA
        
        meta_agua_diaria = round((peso * 35) + 750, 0)
        
        
        
        usuario.calorias_diarias = calorias_diarias
        usuario.proteinas_diarias = proteinas_diarias
        usuario.carboidratos_diarios = carboidratos_diarios
        usuario.fibras_diarias = fibras_diarias
        usuario.gorduras_diarias = gorduras_diarias
        usuario.meta_agua_diaria = meta_agua_diaria
        
        

        # AVALIAÇÃO

        avaliacao = AvaliacaoFisica(
            usuario_id=session["usuario_id"],
            data=data,
            peso=peso,
            altura=altura,
            idade=idade,
            imc=imc,
            percentual_gordura=percentual_gordura,
            massa_magra=massa_magra,
            massa_gorda=massa_gorda,
            meta_percentual_gordura=meta_percentual_gordura,
            meta_massa_magra=meta_massa_magra,
            meta_massa_gorda=meta_massa_gorda,
            meta_peso=meta_peso
        )

        db.session.add(avaliacao)
        db.session.commit()


        # DOBRAS CUTÂNEAS

        dobras = DobrasCutaneas(

            avaliacao_id=avaliacao.id,
            usuario_id=session["usuario_id"],
            subescapular=subescapular,
            bicipital=bicipital,
            tricipital=tricipital,
            axilar_media=axilar_media,
            supra_iliaca=supra_iliaca,
            supra_espinhal=supra_espinhal,
            peitoral=peitoral,
            abdominal=abdominal,
            coxa=coxa,
            panturrilha=panturrilha
        )

        db.session.add(dobras)

        # PERÍMETROS CORPORAIS

        perimetros = PerimetrosCorporais(

            avaliacao_id=avaliacao.id,
            usuario_id=session["usuario_id"],
            ombro=valor_float("ombro"),
            torax_inspirado=valor_float("torax_inspirado"),
            cintura=valor_float("cintura"),
            abdomen=valor_float("abdomen"),
            quadril=valor_float("quadril"),
            antebraco_direito=valor_float("antebraco_direito"),
            antebraco_esquerdo=valor_float("antebraco_esquerdo"),
            braco_contraido_direito=valor_float("braco_contraido_direito"),
            braco_contraido_esquerdo=valor_float("braco_contraido_esquerdo"),
            coxa_direita=valor_float("coxa_direita"),
            coxa_esquerda=valor_float("coxa_esquerda"),
            panturrilha_direita=valor_float("panturrilha_direita"),
            panturrilha_esquerda=valor_float("panturrilha_esquerda")
        )

        db.session.add(perimetros)

        db.session.commit()

        return render_template(
            "mensagem.html",
            mensagem="Avaliação física salva com sucesso!",
            link="/avaliacao-fisica"
        )

    avaliacoes = AvaliacaoFisica.query.order_by(
        AvaliacaoFisica.id.desc()
    ).all()

    return render_template(
        "site/forms/corpo/avaliacao-fisica.html",
        avaliacoes=avaliacoes
    )

# EDITAR AVALIAÇÃO

@bp_corpo.route("/editar-avaliacao/<int:id>", methods=["GET", "POST"])
def editar_avalicao(id):
    avaliacao = AvaliacaoFisica.query.filter_by(id=id, usuario_id=session["usuario_id"]).first()
    perimetros = PerimetrosCorporais.query.filter_by(avaliacao_id=id).first()
    dobras_cutaneas = DobrasCutaneas.query.filter_by(avaliacao_id=id).first()
    usuario = Usuario.query.get(session["usuario_id"])
    
    if not avaliacao:

        return render_template("mensagem.html",mensagem="Avaliação não encontrada.",link="/avaliacao-fisica")
        
    if request.method == "POST":

        # DADOS GERAIS

        avaliacao.data = date.fromisoformat(request.form["data"])
        avaliacao.peso = valor_float("peso")
        avaliacao.altura = valor_float("altura")
        avaliacao.idade = int(request.form["idade"])

        # DOBRAS

        dobras_cutaneas.subescapular = valor_float("subescapular")
        dobras_cutaneas.bicipital = valor_float("bicipital")
        dobras_cutaneas.tricipital = valor_float("tricipital")
        dobras_cutaneas.axilar_media = valor_float("axilar_media")
        dobras_cutaneas.supra_iliaca = valor_float("supra_iliaca")
        dobras_cutaneas.supra_espinhal = valor_float("supra_espinhal")
        dobras_cutaneas.peitoral = valor_float("peitoral")
        dobras_cutaneas.abdominal = valor_float("abdominal")
        dobras_cutaneas.coxa = valor_float("coxa")
        dobras_cutaneas.panturrilha = valor_float("panturrilha")

        # SOMA DOBRAS

        soma_dobras = (
            dobras_cutaneas.peitoral
            + dobras_cutaneas.abdominal
            + dobras_cutaneas.coxa
        )

        # DENSIDADE CORPORAL

        if usuario.sexo == "masculino":
        
            densidade_corporal = (
                1.112
                - (0.00043499 * soma_dobras)
                + (0.00000055 * (soma_dobras ** 2))
                - (0.00028826 * avaliacao.idade)
            )
        
        else:  # feminino
        
            densidade_corporal = (
                1.0970
                - (0.00046971 * soma_dobras)
                + (0.00000056 * (soma_dobras ** 2))
                - (0.00012828 * avaliacao.idade)
            )

        # PERCENTUAL GORDURA

        percentual_gordura = round(((4.95 / densidade_corporal) - 4.50) * 100,2)

        # IMC

        avaliacao.imc = round(avaliacao.peso / (avaliacao.altura * avaliacao.altura),2)
        avaliacao.percentual_gordura = percentual_gordura

        # MASSAS

        avaliacao.massa_gorda = round(avaliacao.peso *(percentual_gordura / 100),2)
        avaliacao.massa_magra = round(avaliacao.peso -avaliacao.massa_gorda,2)

        # METAS

        avaliacao.meta_percentual_gordura = 15
        avaliacao.meta_massa_gorda = round(avaliacao.peso * 0.15,2)
        avaliacao.meta_massa_magra = (avaliacao.massa_magra)
        avaliacao.meta_peso = round(avaliacao.meta_massa_magra / 0.85,2)

        # PERÍMETROS

        perimetros.ombro = valor_float("ombro")
        perimetros.torax_inspirado = valor_float("torax_inspirado")
        perimetros.cintura = valor_float("cintura")
        perimetros.abdomen = valor_float("abdomen")
        perimetros.quadril = valor_float("quadril")
        perimetros.antebraco_direito = valor_float("antebraco_direito")
        perimetros.antebraco_esquerdo = valor_float("antebraco_esquerdo")
        perimetros.braco_contraido_direito = valor_float("braco_contraido_direito")
        perimetros.braco_contraido_esquerdo = valor_float("braco_contraido_esquerdo")
        perimetros.coxa_direita = valor_float("coxa_direita")
        perimetros.coxa_esquerda = valor_float("coxa_esquerda")
        perimetros.panturrilha_direita = valor_float("panturrilha_direita")
        perimetros.panturrilha_esquerda = valor_float("panturrilha_esquerda")
        
        
        # USUARIO RECEBENDO O PESO E MASSA EM GERAL
        
        usuario.peso = avaliacao.peso
        usuario.altura = avaliacao.altura
        usuario.meta_peso = avaliacao.meta_peso
        usuario.massa_magra = avaliacao.massa_magra
        usuario.massa_gorda = avaliacao.massa_gorda
        usuario.meta_massa_magra = avaliacao.meta_massa_magra
        usuario.meta_massa_gorda = avaliacao.meta_massa_gorda
        usuario.percentual_gordura = avaliacao.percentual_gordura
        usuario.imc = avaliacao.imc
        
        # USUARIO RECEBENDO QUANTIDADES DIÁRIAS
        
        # CALORIAS
        
        if usuario.sexo == "masculino":
            tmb = (10 * usuario.peso) + (6.25 * (usuario.altura * 100)) - (5 * usuario.idade) + 5
        else:
            tmb = (10 * usuario.peso) + (6.25 * (usuario.altura * 100)) - (5 * usuario.idade) - 161
        
        fator_atividade = 1.55
        calorias_manutencao = round(tmb * fator_atividade,0)
        calorias_diarias = round(calorias_manutencao * 0.90, 0)
        
        # PROTEINAS, GORDURAS, FIBRAS
        
        proteinas_diarias = round(avaliacao.peso*2.2,0)
        gorduras_diarias = round(avaliacao.peso,0)
        fibras_diarias = round(calorias_diarias/1000*14,0)
        
        # CARBOIDRATOS
        
        calorias_proteina = proteinas_diarias * 4
        calorias_gordura = gorduras_diarias * 9
        
        carboidratos_diarios = round((calorias_diarias - calorias_proteina - calorias_gordura)/4,0)
        
        # AGUA
        
        meta_agua_diaria = round((peso * 35) + 750, 0)
        
        usuario.calorias_diarias = calorias_diarias
        usuario.proteinas_diarias = proteinas_diarias
        usuario.carboidratos_diarios = carboidratos_diarios
        usuario.fibras_diarias = fibras_diarias
        usuario.gorduras_diarias = gorduras_diarias
        usuario.meta_agua_diaria = meta_agua_diaria

        db.session.commit()

        return render_template(
            "mensagem.html",
            mensagem="Avaliação atualizada com sucesso!",
            link="/avaliacao-fisica"
        )

    return render_template(
        "site/forms/corpo/editar-avaliacao.html",
        avaliacao=avaliacao,
        perimetros=perimetros,
        dobras=dobras_cutaneas
    )

# EXCLUIR AVALIAÇÃO

@bp_corpo.route("/excluir-avaliacao/<int:id>")
def excluir_avaliacao(id):

    avaliacao = AvaliacaoFisica.query.filter_by(id=id, usuario_id=session["usuario_id"]).first()
    perimetros = PerimetrosCorporais.query.filter_by(avaliacao_id=id).first()
    dobras_cutaneas = DobrasCutaneas.query.filter_by(avaliacao_id=id).first()
    usuario = Usuario.query.get(session["usuario_id"])

    if not avaliacao:

        return render_template(
            "mensagem.html",
            mensagem="Avaliação não encontrada.",
            link="/avaliacao-fisica"
        )


    if perimetros:
        db.session.delete(perimetros)

    if dobras_cutaneas:
        db.session.delete(dobras_cutaneas)

    db.session.delete(avaliacao)
    db.session.commit()
    
    ultima_avaliacao = AvaliacaoFisica.query.filter_by(usuario_id= session["usuario_id"]).order_by(AvaliacaoFisica.id.desc()).first()
    
    if ultima_avaliacao:

        usuario.peso = ultima_avaliacao.peso 
        usuario.altura = ultima_avaliacao.altura
        usuario.meta_peso = ultima_avaliacao.meta_peso
    
        usuario.massa_magra = ultima_avaliacao.massa_magra
        usuario.massa_gorda = ultima_avaliacao.massa_gorda
    
        usuario.meta_massa_magra = ultima_avaliacao.meta_massa_magra
        usuario.meta_massa_gorda = ultima_avaliacao.meta_massa_gorda
    
        usuario.percentual_gordura = ultima_avaliacao.percentual_gordura
        usuario.imc = ultima_avaliacao.imc
    
        # REFAZER CÁLCULOS DIÁRIOS
        
        # CALORIAS
    
        tmb = 370 + (21.6 * ultima_avaliacao.massa_magra)
        fator_atividade = 1.55
        calorias_manutencao = round(tmb * fator_atividade,0)
        calorias_diarias = round(calorias_manutencao * 0.90, 0)
        
        # PROTEINAS, GORDURAS, FIBRAS
    
        proteinas_diarias = round(ultima_avaliacao.peso * 2,0)
        gorduras_diarias = round(ultima_avaliacao.peso * 0.8,0)
        fibras_diarias = round(calorias_diarias / 1000 * 14,0)
        
        # CARBOIDRATOS
    
        calorias_proteina = proteinas_diarias * 4
        calorias_gordura = gorduras_diarias * 9
    
        carboidratos_diarios = round(
            (
                calorias_diarias
                - calorias_proteina
                - calorias_gordura
            ) / 4,
            0
        )
        
        # AGUA
        
        meta_agua_diaria = round((usuario.peso * 35) + 750, 0)
    
        usuario.calorias_diarias = calorias_diarias
        usuario.proteinas_diarias = proteinas_diarias
        usuario.gorduras_diarias = gorduras_diarias
        usuario.fibras_diarias = fibras_diarias
        usuario.carboidratos_diarios = carboidratos_diarios
        usuario.meta_agua_diaria = meta_agua_diaria
        
        db.session.commit()
        
    else:
        usuario.calorias_diarias = None
        usuario.proteinas_diarias = None
        usuario.gorduras_diarias = None
        usuario.fibras_diarias = None
        usuario.carboidratos_diarios = None
        usuario.meta_agua_diaria = None
        
        db.session.commit()

    return render_template(
        "mensagem.html",
        mensagem="Avaliação excluída com sucesso!",
        link="/avaliacao-fisica"
    )


# PRESSÃO ARTERIAL

# ADD PRESSÃO

@bp_corpo.route("/pressao", methods=["GET", "POST"])
def registrar_pressao():
    
    data_pressao_inicio = None
    data_pressao_final = None
    data_inicio = None
    data_final = None

    if request.method == "POST":
        
        acao = request.form.get("acao")
        
        if acao == "salvar":

            nova_pressao = Pressao(
                usuario_id=session["usuario_id"],
                data = request.form["data"],
                hora = request.form["hora"],
                sistolica=int(request.form["sistolica"]),
                diastolica=int(request.form["diastolica"]),
                frequencia_cardiaca=int(request.form["frequencia_cardiaca"]),
                observacoes=request.form["observacoes"]
            )
    
            db.session.add(nova_pressao)
            db.session.commit()
    
            return render_template(
                "mensagem.html",
                mensagem="Pressão registrada com sucesso!",
                link="/pressao"
            )
            
        elif acao == "filtrar":
            data_inicio = request.form.get("data_inicio")
            data_final = request.form.get("data_final")
            
        if data_inicio:
            data_pressao_inicio = datetime.strptime(data_inicio,"%Y-%m-%d").date()

        if data_final:
            data_pressao_final = datetime.strptime(data_final,"%Y-%m-%d").date()

    query = Pressao.query.filter_by(usuario_id=session["usuario_id"])

    if data_pressao_inicio == None and data_pressao_final == None:
        query = query.filter(Pressao.data == date.today())
    
    elif data_pressao_inicio and not data_pressao_final:
        query = query.filter(Pressao.data >= data_pressao_inicio)
        
    elif data_pressao_final and not data_pressao_inicio:
        query = query.filter(Pressao.data <= data_pressao_final)
        
    else:
        query = query.filter(Pressao.data.between(data_pressao_inicio,data_pressao_final))
        
    pressoes = query.order_by(Pressao.data.desc(),Pressao.id.desc()).all()


    return render_template(
        "site/forms/corpo/pressao.html",
        pressoes=pressoes
    )
    
# EDITAR PRESSÃO
@bp_corpo.route("/editar-pressao/<int:id>", methods=["GET", "POST"])
def editar_pressao(id):
    
    pressao = Pressao.query.filter_by(id=id, usuario_id=session["usuario_id"]).first()
    
    if not pressao:
        return render_template(
            "mensagem.html",
            mensagem="Registro não encontrado!",
            link = "/pressao"
        )
    
    if request.method == "POST":
        pressao.data = request.form["data"]
        pressao.hora = request.form["hora"]
        pressao.sistolica=int(request.form["sistolica"])
        pressao.diastolica=int(request.form["diastolica"])
        pressao.frequencia_cardiaca=int(request.form["frequencia_cardiaca"])
        pressao.observacoes=request.form["observacoes"]
        
        db.session.commit()
        
        return render_template(
            "mensagem.html",
            mensagem = "Registro de pressão atualizada com sucesso!",
            link = "/pressao"
        )
    
    return render_template(
        "site/forms/corpo/editar-pressao.html",
        pressao = pressao
    )

# EXCLUIR PRESSÃO

@bp_corpo.route("/excluir-pressao/<int:id>")
def excluir_pressao(id):
    
    pressao = Pressao.query.filter_by(id=id, usuario_id=session["usuario_id"]).first()
    
    if not pressao:
        return render_template(
            "mensagem.html",
            mensagem="Registro não encontrado!",
            link = "/pressao"
        )
    
    db.session.delete(pressao)
    db.session.commit()
    
    return render_template(
    "mensagem.html",
    mensagem = "Registro de pressão excluída com sucesso!",
    link = "/pressao"
    )