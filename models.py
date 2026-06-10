from database import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# USUARIO

class Usuario(db.Model):
    __tablename__ = "usuarios"
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    data_nasc = db.Column(db.Date, nullable=False)
    sexo = db.Column(db.String(20), nullable=False)
    peso = db.Column(db.Float, nullable=True)
    altura = db.Column(db.Float, nullable=True)
    calorias_diarias = db.Column(db.Float, nullable=True)
    carboidratos_diarios = db.Column(db.Float, nullable=True)
    proteinas_diarias = db.Column(db.Float, nullable=True)
    fibras_diarias = db.Column(db.Float, nullable=True)
    gorduras_diarias = db.Column(db.Float, nullable=True)
    ultima_pressao = db.Column(db.String(20), nullable=True)
    percentual_gordura = db.Column(db.Float, nullable=True)
    massa_magra = db.Column(db.Float, nullable=True)
    massa_gorda = db.Column(db.Float, nullable=True)
    meta_peso = db.Column(db.Float, nullable=True)
    meta_massa_magra = db.Column(db.Float, nullable=True)
    meta_massa_gorda = db.Column(db.Float, nullable=True)
    imc = db.Column(db.Float, nullable=True)
    
    # IDADE
    
    idade = db.Column(db.Integer, nullable=False)
    
    def definir_idade(data_nasc):
        hoje = datetime.date.today()

        idade = hoje.year - data_nasc.year

        if (hoje.month, hoje.day) < (data_nasc.month, data_nasc.day):
            idade -= 1

        return idade
    
    # SENHA
    
    senha = db.Column(db.String(255), nullable=False)
    
    def set_senha(self, senha):
        self.senha = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha, senha)
    
    
# REGISTRO DOS EXERCÍCIOS FEITOS

class Exercicio(db.Model):
    __tablename__ = "exercicios"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer,db.ForeignKey("usuarios.id"),nullable=False)
    data = db.Column(db.Date, nullable=False)
    hora = db.Column(db.String(20), nullable=False)
    exercicio = db.Column(db.String(100), nullable=False)
    grupo_muscular = db.Column(db.String(50), nullable=False)
    calorias = db.Column(db.Float, nullable=False)
    serie = db.Column(db.String(50), nullable=False)
    repeticoes = db.Column(db.Integer, nullable=False)
    kg_tempo = db.Column(db.Float, nullable=False)


# LISTA DE EXERCÍCIOS DISPONÍVEIS

class ListaExercicio(db.Model):
    __tablename__ = "lista_exercicios"
    id = db.Column(db.Integer, primary_key=True)
    exercicio = db.Column(db.String(100), nullable=False)
    grupo_muscular = db.Column(db.String(50), nullable=False)
    fator_calorias = db.Column(db.Float, nullable=True)
    
# REGISTRO DAS REFEIÇÕES

class Refeicao(db.Model):
    __tablename__ = "refeicoes"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer,db.ForeignKey("usuarios.id"),nullable=False)
    data = db.Column(db.Date, nullable=False)
    hora = db.Column(db.String(20), nullable=False)
    alimento = db.Column(db.String(100), nullable=False)
    calorias = db.Column(db.Float, nullable=True)
    proteinas = db.Column(db.Float, nullable=True)
    carboidratos = db.Column(db.Float, nullable=True)
    fibras = db.Column(db.Float, nullable=True)
    gorduras = db.Column(db.Float, nullable=True)
    quantidade = db.Column(db.Float, nullable=True)


# LISTA DE ALIMENTOS

class Alimento(db.Model):
    __tablename__ = "alimentos"

    id = db.Column(db.Integer, primary_key=True)
    alimento = db.Column(db.String(100), nullable=True)
    calorias = db.Column(db.Float, nullable=True)
    proteinas = db.Column(db.Float, nullable=True)
    carboidratos = db.Column(db.Float, nullable=True)
    fibras = db.Column(db.Float, nullable=True)
    gorduras = db.Column(db.Float, nullable=True)
    
# REGISTRO DE CARDIO

class Cardio(db.Model):
    __tablename__ = "cardios"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer,db.ForeignKey("usuarios.id"),nullable=False)
    data = db.Column(db.Date, nullable=False)
    hora = db.Column(db.String(20), nullable=False)
    atividade = db.Column(db.String(100), nullable=False)
    duracao = db.Column(db.Float, nullable=False)
    distancia = db.Column(db.Float, nullable=True)
    calorias = db.Column(db.Float, nullable=True)
    frequencia_media = db.Column(db.Integer, nullable=True)
    frequencia_maxima = db.Column(db.Integer, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)    
    
class Atividades(db.Model):
    __tablename__ = "atividades"
    
    id = db.Column(db.Integer, primary_key=True)
    atividade = db.Column(db.String(20), nullable=False)



# AVALIAÇÃO FÍSICA

class AvaliacaoFisica(db.Model):
    __tablename__ = "avaliacoes_fisicas"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer,db.ForeignKey("usuarios.id"),nullable=False)
    data = db.Column(db.Date, nullable=False)
    peso = db.Column(db.Float, nullable=False)
    altura = db.Column(db.Float, nullable=False)
    idade = db.Column(db.Integer, nullable= False)
    imc = db.Column(db.Float, nullable=True)
    percentual_gordura = db.Column(db.Float, nullable=True)
    massa_magra = db.Column(db.Float, nullable=True)
    massa_gorda = db.Column(db.Float, nullable=True)
    meta_percentual_gordura = db.Column(db.Float, nullable=True)
    meta_massa_magra = db.Column(db.Float, nullable=True)
    meta_massa_gorda = db.Column(db.Float, nullable=True)
    meta_peso = db.Column(db.Float, nullable=True)


# DOBRAS CUTÂNEAS

class DobrasCutaneas(db.Model):
    __tablename__ = "dobras_cutaneas"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer,db.ForeignKey("usuarios.id"),nullable=False)
    avaliacao_id = db.Column(db.Integer,db.ForeignKey("avaliacoes_fisicas.id"),nullable=False)
    subescapular = db.Column(db.Float, nullable=True)
    bicipital = db.Column(db.Float, nullable=True)
    tricipital = db.Column(db.Float, nullable=True)
    axilar_media = db.Column(db.Float, nullable=True)
    supra_iliaca = db.Column(db.Float, nullable=True)
    supra_espinhal = db.Column(db.Float, nullable=True)
    peitoral = db.Column(db.Float, nullable=True)
    abdominal = db.Column(db.Float, nullable=True)
    coxa = db.Column(db.Float, nullable=True)
    panturrilha = db.Column(db.Float, nullable=True)

# PERÍMETROS CORPORAIS

class PerimetrosCorporais(db.Model):
    __tablename__ = "perimetros_corporais"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer,db.ForeignKey("usuarios.id"),nullable=False)
    avaliacao_id = db.Column(db.Integer,db.ForeignKey("avaliacoes_fisicas.id"),nullable=False)
    ombro = db.Column(db.Float, nullable=True)
    torax_inspirado = db.Column(db.Float, nullable=True)
    cintura = db.Column(db.Float, nullable=True)
    abdomen = db.Column(db.Float, nullable=True)
    quadril = db.Column(db.Float, nullable=True)
    antebraco_direito = db.Column(db.Float, nullable=True)
    antebraco_esquerdo = db.Column(db.Float, nullable=True)
    braco_contraido_direito = db.Column(db.Float, nullable=True)
    braco_contraido_esquerdo = db.Column(db.Float, nullable=True)
    coxa_direita = db.Column(db.Float, nullable=True)
    coxa_esquerda = db.Column(db.Float, nullable=True)
    panturrilha_direita = db.Column(db.Float, nullable=True)
    panturrilha_esquerda = db.Column(db.Float, nullable=True)
    

class Pressao(db.Model):
    __tablename__ = "pressao"

    id = db.Column(db.Integer,primary_key=True)
    usuario_id = db.Column(db.Integer,db.ForeignKey("usuarios.id"),nullable=False)
    sistolica = db.Column(db.Integer,nullable=False)
    diastolica = db.Column(db.Integer,nullable=False)
    frequencia_cardiaca = db.Column(db.Integer,nullable=True)
    observacoes = db.Column(db.Text,nullable=True)
    data = db.Column(db.Date,nullable=False)
    hora = db.Column(db.String(8),nullable=False)

    def __repr__(self):
        return f"<Pressao {self.sistolica}/{self.diastolica}>"