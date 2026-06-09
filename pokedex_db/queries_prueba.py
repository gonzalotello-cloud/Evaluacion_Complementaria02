"""Consultas requeridas del sistema Pokédex, implementadas como funciones tipadas.

Todas las funciones reciben una Session como único parámetro de conexión y
retornan listas o valores escalares según lo especificado en el enunciado EC2.

Reglas de este módulo:
    - Toda consulta usa select() de SQLModel, excepto la consulta 8 (SQL crudo).
    - Ninguna función referencia el engine directamente.
    - Ninguna función contiene lógica de modelos o inicialización de datos.
    - Cada función tiene un docstring de una línea que describe qué retorna.
"""

from sqlalchemy import asc, case, desc, func, text
from sqlmodel import Session, select

from models import (
    Entrenador,
    Participacion,
    Pokemon,
    PokemonTipo,
    Region,
    Tipo,
)

def pokemon_alto_nivel(session: Session, umbral: int = 70) -> list[Pokemon]:
    """Retorna los Pokémon con nivel mayor o igual al umbral, de mayor a menor."""
    query = select(Pokemon).where(Pokemon.nivel >= umbral).order_by(desc(Pokemon.nivel))
    return list(session.exec(query).all())


def campeones_por_region(
    session: Session,
    nombre_region: str,
) -> list[Entrenador]:
    """Retorna los entrenadores campeones de la región indicada."""
    stmt = (
        select(Entrenador)
        .join(Region, Entrenador.region_id == Region.id)
        .where(Region.nombre == nombre_region)
        .where(Entrenador.es_campeon == True)  # noqa: E712
    )
    return list(session.exec(stmt).all())


def shiny_con_apodo(session: Session) -> list[tuple[str, str, int, str]]:
    """Retorna (nombre_pokemon, apodo, nivel, nombre_entrenador) de Pokémon shiny con apodo."""
    stmt = (
        select(
            Pokemon.nombre,
            Pokemon.apodo,
            Pokemon.nivel,
            Entrenador.nombre,
        )
        .join(Entrenador, Pokemon.entrenador_id == Entrenador.id)
        .where(Pokemon.es_shiny == True)  # noqa: E712
        .where(Pokemon.apodo.isnot(None))
    )
    return list(session.exec(stmt).all())


def promedio_nivel_por_entrenador(session: Session) -> list[tuple[str, float]]:
    """Retorna (nombre_entrenador, promedio_nivel) ordenado de mayor a menor promedio."""
    promedio = func.round(func.avg(Pokemon.nivel), 2)
    query = (
        select(Entrenador.nombre, promedio)
        .join(Pokemon, Pokemon.entrenador_id == Entrenador.id)
        .group_by(Entrenador.id, Entrenador.nombre)
        .order_by(promedio.desc())
    )
    return list(session.exec(query).all())


def conteo_pokemon_por_tipo(session: Session) -> list[tuple[str, int]]:
    """Retorna (nombre_tipo, cantidad_pokemon) ordenado de mayor a menor cantidad."""
    cantidad = func.count(PokemonTipo.pokemon_id)
    query = (
        select(Tipo.nombre, cantidad)
        .join(PokemonTipo, PokemonTipo.tipo_id == Tipo.id)
        .group_by(Tipo.id, Tipo.nombre)
        .having(cantidad > 0)
        .order_by(cantidad.desc())
    )
    return list(session.exec(query).all())


def estadisticas_batallas(session: Session) -> list[tuple[str, int, int, int]]:
    """Retorna (nombre, total_batallas, victorias, derrotas) por entrenador, desc por total."""
    victorias = func.sum(
        case((Participacion.resultado == "victoria", 1), else_=0)
    ).label("victorias")
    derrotas = func.sum(case((Participacion.resultado == "derrota", 1), else_=0)).label(
        "derrotas"
    )
    total = func.count(Participacion.batalla_id).label("total")

    stmt = (
        select(Entrenador.nombre, total, victorias, derrotas)
        .join(Participacion, Participacion.entrenador_id == Entrenador.id)
        .group_by(Entrenador.id, Entrenador.nombre)
        .order_by(desc("total"))
    )
    return list(session.exec(stmt).all())


def region_mas_insignias(session: Session) -> tuple[str, float]:
    """Retorna (nombre_region, promedio_insignias) de la región con mayor promedio."""
    promedio = func.round(func.avg(Entrenador.insignias), 2)
    query = (
        select(Region.nombre, promedio)
        .join(Entrenador, Entrenador.region_id == Region.id)
        .group_by(Region.id, Region.nombre)
        .order_by(promedio.desc(),Region.nombre.asc())
        .limit(1)
    )
    # Solo entrega el primer resultado
    result = session.exec(query).first()
    # Retorna el nombre de la región y el promedio
    return (str(result[0]), float(result[1]))


def consulta_libre(session: Session) -> list[dict]:
    """Retorna el ranking de entrenadores según el nivel de su mejor Pokémon.

    Usa SQL crudo porque combina dos características que la API de alto nivel
    de SQLModel no puede expresar directamente:

    1. Función de ventana RANK() OVER (ORDER BY ...):
       SQLModel expone select(), where(), group_by() y order_by(), pero no
       tiene soporte directo para window functions. SQLAlchemy Core sí las
       soporta, pero requiere bajar a over() y construir expresiones de bajo
       nivel que son más verbosas y menos legibles que el SQL equivalente.

    2. Recuperar el NOMBRE del Pokémon con nivel máximo dentro de cada grupo:
       MAX(p.nivel) colapsa el grupo correctamente, pero incluir p.nombre en
       el SELECT sin agregarlo al GROUP BY viola el estándar SQL. La solución
       —una subconsulta correlacionada o FIRST_VALUE() OVER— no tiene un
       equivalente directo en la API select() de SQLModel. Expresarlo con
       select() requeriría múltiples subconsultas anidadas que oscurecerían
       la intención de la consulta. SQL crudo comunica el propósito con
       claridad en menos líneas.

    Retorna una lista de dicts con las claves:
        ranking, entrenador, mejor_pokemon, nivel_maximo, total_pokemon.
    """
    sql = text("""
        SELECT
            RANK() OVER (ORDER BY MAX(p.nivel) DESC) AS ranking,
            e.nombre                                  AS entrenador,
            p.nombre                                  AS mejor_pokemon,
            MAX(p.nivel)                              AS nivel_maximo,
            COUNT(p.id)                               AS total_pokemon
        FROM entrenador e
        JOIN pokemon p ON p.entrenador_id = e.id
        GROUP BY e.id, e.nombre
        ORDER BY ranking
    """)
    rows = session.exec(sql).all()
    return [
        {
            "ranking": row[0],
            "entrenador": row[1],
            "mejor_pokemon": row[2],
            "nivel_maximo": row[3],
            "total_pokemon": row[4],
        }
        for row in rows
    ]