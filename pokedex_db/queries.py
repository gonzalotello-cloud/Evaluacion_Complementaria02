"""Módulo de consultas de negocio SQLModel para la base de datos Pokedex.

Este archivo contiene las 8 funciones analíticas requeridas por el enunciado,
respetando el tipado estático, los estándares de ruff/PEP 8 y el aislamiento
de la sesión de base de datos.
"""

from sqlmodel import Session, func, select, text
from sqlalchemy import case, desc

from models import (
    Batalla,
    Entrenador,
    Participacion,
    Pokemon,
    PokemonTipo,
    Region,
    Tipo,
)


def pokemon_alto_nivel(session: Session, umbral: int = 70) -> list[Pokemon]:
    """Retorna los Pokémon con nivel mayor o igual al umbral, de mayor a menor."""
    query = (select(Pokemon).where(Pokemon.nivel >= umbral).order_by(Pokemon.nivel.desc()))
    return list(session.exec(query).all())


def campeones_por_region(session: Session, nombre_region: str)-> list[Entrenador]:
    """Retorna los entrenadores campeones de una región específica."""
    query = (
        select(Entrenador)
        .join(Region, Entrenador.region_id == Region.id)
        .where(Region.nombre == nombre_region)
        .where(Entrenador.es_campeon == True)  # noqa: E712
    )
    return list(session.exec(query).all())



def shiny_con_apodo(session: Session) -> list[tuple[str, str, int, str]]:
    """Retorna (nombre_pokemon, apodo, nivel, nombre_entrenador) de Pokémon shiny con apodo."""
    query = (
        select(Pokemon.nombre, Pokemon.apodo, Pokemon.nivel, Entrenador.nombre)
        .join(Entrenador, Pokemon.entrenador_id == Entrenador.id)
        .where(Pokemon.es_shiny == True)  # noqa: E712
        .where(Pokemon.apodo.is_not(None))
    )
    # Se ejecuta y se extraen las tuplas resultantes
    return list(session.exec(query).all())


def promedio_nivel_por_entrenador(session: Session) -> list[tuple[str, float]]:
    """Retorna el promedio de nivel de Pokémon por entrenador, orden descendente."""
    promedio = func.round(func.avg(Pokemon.nivel), 2)
    query = (
        select(Entrenador.nombre, promedio)
        .join(Pokemon, Pokemon.entrenador_id == Entrenador.id)
        .group_by(Entrenador.id, Entrenador.nombre)
        .order_by(promedio.desc())
    )
    return list(session.exec(query).all())


def conteo_pokemon_por_tipo(session: Session) -> list[tuple[str, int]]:
    """Retorna la cantidad de Pokémon asociados a cada tipo elemental activo, de mayor a menor"""
    cantidad = func.count(PokemonTipo.pokemon_id)
    query = (
        select(Tipo.nombre, cantidad)
        # Esta union filtra implicitamente los casos donde cantidad = 0
        .join(PokemonTipo, Tipo.id == PokemonTipo.tipo_id)
        .group_by(Tipo.id, Tipo.nombre)
        .order_by(cantidad.desc())
    )
    return list(session.exec(query).all())


def estadisticas_batallas(session: Session) -> list[tuple[str, int, int, int]]:
    """Retorna (nombre, total_batallas, victorias, derrotas) por entrenador, desc por total batallas."""

    # Por cada fila analizada, si el campo es "victoria" se devuelve 1, 0 de lo contrario
    # Se obtiene la cantidad total de victorias con SUM
    victorias = func.sum(
        case((Participacion.resultado == "victoria", 1), else_=0)
    ).label("victorias")

    # Por cada fila analizada, si el campo es "derrota" se devuelve 1, 0 de lo contrario
    # Se obtiene la cantidad total de derrotas con SUM
    derrotas = func.sum(case((Participacion.resultado == "derrota", 1), else_=0)).label(
        "derrotas"
    )

    # Cuenta la cantidad de batallas
    total = func.count(Participacion.batalla_id).label("total")

    # Agrupa los datos por entrenador y entrega
    # Nombre entrenador, total batallas, victorias y derrotas por entrenador
    # en orden descendente
    stmt = (
        select(Entrenador.nombre, total, victorias, derrotas)
        .join(Participacion, Participacion.entrenador_id == Entrenador.id)
        .group_by(Entrenador.id, Entrenador.nombre)
        .order_by(desc("total"))
    )
    return list(session.exec(stmt).all())


def region_mas_insignias(session: Session) -> tuple[str, float]:
    """Retorna el nombre y el promedio más alto de insignias registrado por región."""
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
    """Retorna el ranking de puestos de los entrenadores según el nivel promedio de sus Pokémon."""

    query = text("""
               SELECT 
                RANK() OVER (ORDER BY AVG(pokemon.nivel) DESC) AS ranking,
                entrenador.nombre AS entrenador,
                ROUND(AVG(pokemon.nivel), 2) AS nivel_promedio
               FROM entrenador
               JOIN pokemon ON pokemon.entrenador_id = entrenador.id
               GROUP BY entrenador.id, entrenador.nombre
               ORDER BY ranking;
               """)

    resultado = session.exec(query)
    return [dict(fila._mapping) for fila in resultado]