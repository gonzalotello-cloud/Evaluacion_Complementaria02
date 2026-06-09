"""Punto de entrada del sistema Pokédex.

Responsabilidades:
    - Inicializar el esquema de la base de datos.
    - Sembrar los datos iniciales.
    - Ejecutar y mostrar los resultados de las 8 consultas requeridas.

Este módulo no contiene lógica de negocio ni SQL. Solo orquesta llamadas
a funciones definidas en database.py, seed.py y queries.py.
"""

from database import crear_tablas, get_session
from queries import (
    campeones_por_region,
    consulta_libre,
    conteo_pokemon_por_tipo,
    estadisticas_batallas,
    pokemon_alto_nivel,
    promedio_nivel_por_entrenador,
    region_mas_insignias,
    shiny_con_apodo,
)
from seed import poblar_datos


# ---------------------------------------------------------------------------
# Helpers de presentación
# ---------------------------------------------------------------------------


def _separador(titulo: str) -> None:
    """Imprime un separador visual con el título de la consulta."""
    ancho = 60
    print()
    print("=" * ancho)
    print(f"  {titulo}")
    print("=" * ancho)


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------


def main() -> None:
    """Orquesta la inicialización, el seed y la ejecución de las 8 consultas."""
    # 1. Crear tablas si no existen
    crear_tablas()

    # 2. Abrir sesión y sembrar datos (idempotente)
    session = next(get_session())
    poblar_datos(session)

    # ------------------------------------------------------------------
    # Consulta 1 — Pokémon de alto nivel (umbral por defecto: 70)
    # ------------------------------------------------------------------
    _separador("Q1 · Pokémon con nivel >= 70")
    resultados = pokemon_alto_nivel(session)
    for p in resultados:
        apodo = f"  (apodo: {p.apodo})" if p.apodo else ""
        print(f"  {p.nombre:<15} nivel {p.nivel}{apodo}")

    # ------------------------------------------------------------------
    # Consulta 2 — Entrenadores campeones por región
    # ------------------------------------------------------------------
    _separador("Q2 · Campeones de Kanto")
    resultados = campeones_por_region(session, "Kanto")
    for e in resultados:
        print(f"  {e.nombre:<15} insignias: {e.insignias}")

    # ------------------------------------------------------------------
    # Consulta 3 — Pokémon shiny con apodo
    # ------------------------------------------------------------------
    _separador("Q3 · Pokémon shiny con apodo")
    resultados = shiny_con_apodo(session)
    if resultados:
        for nombre, apodo, nivel, entrenador in resultados:
            print(
                f"  {nombre:<15} apodo: {apodo:<15} nivel: {nivel}  entrenador: {entrenador}"
            )
    else:
        print("  (sin resultados)")

    # ------------------------------------------------------------------
    # Consulta 4 — Promedio de nivel por entrenador
    # ------------------------------------------------------------------
    _separador("Q4 · Promedio de nivel por entrenador")
    resultados = promedio_nivel_por_entrenador(session)
    for nombre, promedio in resultados:
        print(f"  {nombre:<15} promedio: {promedio}")

    # ------------------------------------------------------------------
    # Consulta 5 — Conteo de Pokémon por tipo
    # ------------------------------------------------------------------
    _separador("Q5 · Pokémon por tipo elemental")
    resultados = conteo_pokemon_por_tipo(session)
    for tipo, cantidad in resultados:
        print(f"  {tipo:<15} {cantidad} Pokémon")

    # ------------------------------------------------------------------
    # Consulta 6 — Estadísticas de batallas por entrenador
    # ------------------------------------------------------------------
    _separador("Q6 · Estadísticas de batallas")
    print(f"  {'Entrenador':<15} {'Total':>6} {'Victorias':>10} {'Derrotas':>9}")
    print(f"  {'-' * 15} {'-' * 6} {'-' * 10} {'-' * 9}")
    resultados = estadisticas_batallas(session)
    for nombre, total, victorias, derrotas in resultados:
        print(f"  {nombre:<15} {total:>6} {victorias:>10} {derrotas:>9}")

    # ------------------------------------------------------------------
    # Consulta 7 — Región con mayor promedio de insignias
    # ------------------------------------------------------------------
    _separador("Q7 · Región con mayor promedio de insignias")
    region, promedio = region_mas_insignias(session)
    print(f"  {region}  (promedio: {promedio})")

    # ------------------------------------------------------------------
    # Consulta 8 — Consulta libre con SQL crudo
    # ------------------------------------------------------------------
    _separador("Q8 · Ranking de entrenadores por nivel promedio (SQL crudo)")
    print(f"  {'Ranking':>7} {'Entrenador':<15} {'Nivel promedio':>14}")
    print(f"  {'-' * 7} {'-' * 15} {'-' * 14}")
    resultados = consulta_libre(session)
    for fila in resultados:
        print(
            f"  {fila['ranking']:>7}"
            f" {fila['entrenador']:<15}"
            f" {fila['nivel_promedio']:>14}"
        )

    session.close()


if __name__ == "__main__":
    main()