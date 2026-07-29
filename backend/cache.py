ALIMENTOS_CACHE = {}
EXERCICIOS_CACHE = {}

def carregar_cache():
    from models import Alimento, ListaExercicio

    print("Carregando alimentos...")

    alimentos = Alimento.query.all()

    print(f"{len(alimentos)} alimentos carregados")

    ALIMENTOS_CACHE.clear()
    ALIMENTOS_CACHE.update({
        alimento.alimento: alimento
        for alimento in alimentos
    })

    print("Carregando exercícios...")

    exercicios = ListaExercicio.query.all()

    print(f"{len(exercicios)} exercícios carregados")

    EXERCICIOS_CACHE.clear()
    EXERCICIOS_CACHE.update({
        exercicio.exercicio: exercicio
        for exercicio in exercicios
    })

    print("Cache carregado")