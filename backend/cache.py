ALIMENTOS_CACHE = {}
EXERCICIOS_CACHE = {}

def carregar_cache():
    from models import Alimento, ListaExercicio

    ALIMENTOS_CACHE.clear()
    EXERCICIOS_CACHE.clear()

    ALIMENTOS_CACHE.update({
        alimento.alimento: alimento
        for alimento in Alimento.query.all()
    })

    EXERCICIOS_CACHE.update({
        exercicio.exercicio: exercicio
        for exercicio in ListaExercicio.query.all()
    })