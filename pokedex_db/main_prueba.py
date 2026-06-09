from database import crear_tablas, get_session
from queries import (
    campeones_por_region,
    conteo_pokemon_por_tipo,
    consulta_libre,
    estadisticas_batallas,
    pokemon_alto_nivel,
    promedio_nivel_por_entrenador,
    region_mas_insignias,
    shiny_con_apodo,
)
from seed import poblar_datos


def imprimir_separador(titulo: str) -> None:
    """Imprime un separador visual formateado para mejorar la legibilidad en consola."""
    print("\n" + "=" * 80)
    print(f" {titulo.upper()} ".center(80, "="))
    print("=" * 80)


def mostrar_reportes() -> None:
    """Ejecuta y muestra en consola los resultados de todas las consultas requeridas.

    Utiliza el generador de contexto get_session() para inyectar una Session limpia
    a cada una de las funciones analíticas del módulo de consultas.
    """
    # Consumimos el generador de sesión de forma segura usando un bloque context manager
    with next(get_session()) as session:

        # ----------------------------------------------------------------------
        # CONSULTAS CON FILTROS (WHERE)
        # ----------------------------------------------------------------------
        imprimir_separador("Consulta 1: Pokémon de Alto Nivel (>= 70)")
        pokemons_alto = pokemon_alto_nivel(session, umbral=70)
        for p in pokemons_alto:
            apodo_str = f" ('{p.apodo}')" if p.apodo else ""
            print(f"• Pokémon: {p.nombre}{apodo_str} | Nivel: {p.nivel}")

        imprimir_separador("Consulta 2: Entrenadores Campeones en Kanto")
        campeones_kanto = campeones_por_region(session, nombre_region="Kanto")
        for c in campeones_kanto:
            print(f"• Entrenador: {c.nombre} | Insignias: {c.insignias} | Campeón: {c.es_campeon}")

        imprimir_separador("Consulta 3: Pokémon Shiny con Apodo")
        shinies = shiny_con_apodo(session)
        for nombre_pk, apodo, nivel, nombre_ent in shinies:
            print(f"• {nombre_pk} nicknamed '{apodo}' (Lv. {nivel}) -> Trainer: {nombre_ent}")

        # ----------------------------------------------------------------------
        # CONSULTAS CON AGREGACIONES
        # ----------------------------------------------------------------------
        imprimir_separador("Consulta 4: Promedio de Nivel por Entrenador")
        promedios = promedio_nivel_por_entrenador(session)
        for entrenador, prom in promedios:
            print(f"• Entrenador: {entrenador:<15} | Promedio de Nivel: {prom:.2f}")

        imprimir_separador("Consulta 5: Conteo de Pokémon por Tipo Elemental")
        conteos_tipo = conteo_pokemon_por_tipo(session)
        for tipo, cantidad in conteos_tipo:
            print(f"• Tipo: {tipo:<12} | Cantidad de Pokémon: {cantidad}")

        imprimir_separador("Consulta 6: Estadísticas de Batallas por Entrenador")
        stats = estadisticas_batallas(session)
        for name, total, wins, losses in stats:
            print(
                f"• Entrenador: {name:<15} | Total: {total:<2} "
                f"| Victorias: {wins:<2} | Derrotas: {losses:<2}"
            )

        imprimir_separador("Consulta 7: Región con Mayor Promedio de Insignias")
        reg_nombre, reg_prom = region_mas_insignias(session)
        print(f"• La región líder es: {reg_nombre} con un promedio de {reg_prom:.2f} insignias.")

        # ----------------------------------------------------------------------
        # CONSULTA LIBRE CON SQL CRUDO
        # ----------------------------------------------------------------------
        imprimir_separador("Consulta 8: Reporte Libre (Ranking de Competitividad)")
        ranking = consulta_libre(session)
        for row in ranking:
            print(
                f"Rank #{row['ranking']} | Entrenador: {row['entrenador']:<10} "
                f"| Mejor Pokémon: {row['mejor_pokemon']:<10} "
                f"(Lv. {row['nivel_maximo']}) | Total Equipo: {row['total_pokemon']}"
            )


def main() -> None:
    """Función principal que coordina el ciclo de vida de la ejecución del proyecto."""
    print("Iniciando el Sistema de Gestión Pokedex DB...")

    # Fase 1: Creación de la estructura física de la base de datos (pokedex.db)
    crear_tablas()
    print("• Infraestructura de tablas verificada/creada con éxito.")

    # Fase 2: Ejecución del script de siembra de datos iniciales de forma idempotente
    poblar_datos()
    print("• Poblado de datos iniciales ejecutado exitosamente.")

    # Fase 3: Procesamiento y despliegue visual de los reportes analíticos
    print("• Extrayendo reportes desde la base de datos...")
    mostrar_reportes()

    print("\n" + "=" * 80)
    print(" Ejecución del Proyecto Finalizada Exitosamente ".center(80, "■"))
    print("=" * 80)


if __name__ == "__main__":
    main()