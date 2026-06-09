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
    """Imprime un separador visual con el título de la consulta.
    Permite una visualización más estética de los resultados
    """
    ancho = 60
    print()
    print("=" * ancho)
    print(f"  {titulo}")
    print("=" * ancho)

def main() -> None:
    """Orquesta la ejecución del pipeline completo
    Utiliza solamente las funciones definidas previamente en los archivos anteriores
    """

    crear_tablas()

    # Abre sesión y pobla la base de datos
    session = next(get_session())
    poblar_datos(session)

    # Consulta 1
    _separador("Consulta 1: Pokemon de alto nivel")
    resultados = pokemon_alto_nivel(session)
    # Imprime los resultados del query
    for pokemon in resultados:
        apodo = f"  (apodo: {pokemon.apodo})" if pokemon.apodo else ""
        print(f"  {pokemon.nombre:<15} nivel {pokemon.nivel}{apodo}")

    # Consulta 2
    _separador("Consulta 2: Campeones de Kanto")
    resultados = campeones_por_region(session, "Kanto")
    # Imprime los resultados
    for entrenador in resultados:
        print(f"  {entrenador.nombre:<15} insignias: {entrenador.insignias}")

    # Consulta 3
    _separador("Consulta 3: Pokemon shiny con apodo")
    resultados = shiny_con_apodo(session)
    if resultados:
        for nombre, apodo, nivel, entrenador in resultados:
            print(
                f"  {nombre:<15} apodo: {apodo:<15} nivel: {nivel}  entrenador: {entrenador}"
            )
    else:
        print("  (sin resultados)")

    # Consulta 4
    _separador("Consulta 4: Promedio de nivel por entrenador")
    resultados = promedio_nivel_por_entrenador(session)
    for nombre, promedio in resultados:
        print(f"  {nombre:<15} promedio: {promedio}")

    # Consulta 5
    _separador("Consulta 5: Conteo de Pokemon por tipo")
    resultados = conteo_pokemon_por_tipo(session)
    for tipo, cantidad in resultados:
        print(f"  {tipo:<15} {cantidad} Pokémon")

    # Consulta 6
    _separador("Consulta 6: Estadísticas de batallas")
    print(f"  {'Entrenador':<15} {'Total':>6} {'Victorias':>10} {'Derrotas':>9}")
    print(f"  {'-' * 15} {'-' * 6} {'-' * 10} {'-' * 9}")
    resultados = estadisticas_batallas(session)
    for nombre, total, victorias, derrotas in resultados:
        print(f"  {nombre:<15} {total:>6} {victorias:>10} {derrotas:>9}")

    # Consulta 7
    _separador("Consulta 7: Región con mayor promedio de insignias")
    region, promedio = region_mas_insignias(session)
    print(f"  {region}  (promedio: {promedio})")

    # Consulta 8
    _separador("Consulta 8: Ranking de entrenadores por nivel promedio (SQL crudo)")
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