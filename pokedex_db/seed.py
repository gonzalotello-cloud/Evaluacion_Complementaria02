from sqlmodel import Session, select

from models import (
    Batalla,
    Entrenador,
    Participacion,
    Pokemon,
    PokemonTipo,
    Region,
    Tipo,
)

def poblar_datos(session: Session) -> None:
    """Inserta los datos en la base de datos."""

    # Es idempotente: Si se ejecuta dos veces sobre la misma base de datos
    # (si ya existen regiones), retorna sin modificar nada.
    if session.exec(select(Region)).first() is not None:
        print("Datos ya existentes")
        return

    """
    REGIONES
    """
    kanto = Region(nombre="Kanto", generacion=1, descripcion="Es una de las regiones con menos cuevas y montañas.")
    johto = Region(nombre="Johto", generacion=2, descripcion="Región casi llana con una meseta al este y un sistema montañoso al noreste.")
    hoenn = Region(nombre="Hoenn", generacion=3, descripcion="Está basado en Kyūshū, la isla más al sur de las cuatro islas principales de Japón. ")
    sinnoh = Region(nombre="Sinnoh", generacion=4, descripcion="Presenta una cantidad de climas muy variados pero predominan los fríos.")
    session.add_all([kanto, johto, hoenn, sinnoh])
    session.commit()  #

    """
    TIPOS POKEMON
    """
    t_electrico = Tipo(nombre="Eléctrico", color_hex="#E5C531")
    t_fuego = Tipo(nombre="Fuego", color_hex="#EA7A3C")
    t_agua = Tipo(nombre="Agua", color_hex="#539AE2")
    t_planta = Tipo(nombre="Planta", color_hex="#71C558")
    t_volador = Tipo(nombre="Volador", color_hex="#7DA6DE")
    t_dragon = Tipo(nombre="Dragón", color_hex="#6A7BAF")
    t_hielo = Tipo(nombre="Hielo", color_hex="#70CBD4")
    t_tierra = Tipo(nombre="Tierra", color_hex="#CC9F4F")
    session.add_all([t_electrico, t_fuego, t_agua, t_planta, t_volador, t_dragon, t_hielo, t_tierra])
    session.commit()

    """
    ENTRENADORES
    """
    ash = Entrenador(nombre="Ash", edad=10, insignias=8, es_campeon=True, region_id=kanto.id)
    gary = Entrenador(nombre="Gary", edad=11, insignias=8, es_campeon=False, region_id=kanto.id)
    ethan = Entrenador(nombre="Ethan", edad=12, insignias=8, es_campeon=True, region_id=johto.id)
    lira = Entrenador(nombre="Lira", edad=12, insignias=5, es_campeon=False, region_id=johto.id)
    brendan = Entrenador(nombre="Brendan", edad=13, insignias=7, es_campeon=False, region_id=hoenn.id)
    may = Entrenador(nombre="May", edad=13, insignias=6, es_campeon=False, region_id=hoenn.id)
    lucas = Entrenador(nombre="Lucas", edad=14, insignias=4, es_campeon=False, region_id=sinnoh.id)
    dawn = Entrenador(nombre="Dawn", edad=14, insignias=8, es_campeon=False, region_id=sinnoh.id)
    session.add_all([ash, gary, ethan, lira, brendan, may, lucas, dawn])
    session.commit()

    """
    POKEMON
    """
    pokemons = [
        # Pokémon de Ash
        Pokemon(nombre="Pikachu", nivel=88, puntos_vida=220, es_shiny=False, apodo=None, entrenador_id=ash.id),
        Pokemon(nombre="Charizard", nivel=78, puntos_vida=260, es_shiny=True, apodo=None, entrenador_id=ash.id),   # Shiny 1
        Pokemon(nombre="Bulbasaur", nivel=15, puntos_vida=90, es_shiny=False, apodo=None, entrenador_id=ash.id),   # Nivel <20
        # Pokémon de Gary
        Pokemon(nombre="Blastoise", nivel=75, puntos_vida=280, es_shiny=False, apodo=None, entrenador_id=gary.id),
        Pokemon(nombre="Arcanine", nivel=68, puntos_vida=240, es_shiny=False, apodo="Perron", entrenador_id=gary.id), # Apodo 1
        Pokemon(nombre="Pidgeot", nivel=62, puntos_vida=210, es_shiny=False, apodo="Pajaron", entrenador_id=gary.id), # Apodo 2
        # Pokémon de Ethan
        Pokemon(nombre="Typhlosion", nivel=82, puntos_vida=270, es_shiny=False, apodo=None, entrenador_id=ethan.id), # Nivel >80
        Pokemon(nombre="Gyarados", nivel=45, puntos_vida=310, es_shiny=True, apodo="Pez", entrenador_id=ethan.id), # Shiny 2, Apodo 3
        Pokemon(nombre="Ampharos", nivel=50, puntos_vida=200, es_shiny=False, apodo=None, entrenador_id=ethan.id),
        # Pokémon de Lyra
        Pokemon(nombre="Meganium", nivel=48, puntos_vida=250, es_shiny=False, apodo=None, entrenador_id=lira.id),
        Pokemon(nombre="Marill", nivel=12, puntos_vida=85, es_shiny=False, apodo=None, entrenador_id=lira.id), # Nivel <20
        # Pokémon de Brendan
        Pokemon(nombre="Sceptile", nivel=70, puntos_vida=230, es_shiny=False, apodo=None, entrenador_id=brendan.id),
        Pokemon(nombre="Swellow", nivel=45, puntos_vida=180, es_shiny=False, apodo=None, entrenador_id=brendan.id),
        Pokemon(nombre="Piplup", nivel=5, puntos_vida=20, es_shiny=True, apodo=None, entrenador_id=brendan.id), # Nivel <20, Shiny 3
        # Pokémon de May
        Pokemon(nombre="Blaziken", nivel=72, puntos_vida=245, es_shiny=False, apodo=None, entrenador_id=may.id),
        Pokemon(nombre="Beautifly", nivel=38, puntos_vida=150, es_shiny=True, apodo=None, entrenador_id=may.id),    # Shiny 4
        # Pokémon de Lucas
        Pokemon(nombre="Torterra", nivel=66, puntos_vida=300, es_shiny=False, apodo=None, entrenador_id=lucas.id),
        Pokemon(nombre="Staraptor", nivel=58, puntos_vida=215, es_shiny=False, apodo=None, entrenador_id=lucas.id),
        # Pokémon de Dawn
        Pokemon(nombre="Empoleon", nivel=71, puntos_vida=265, es_shiny=False, apodo=None, entrenador_id=dawn.id),
        Pokemon(nombre="Mamoswine", nivel=64, puntos_vida=320, es_shiny=False, apodo=None, entrenador_id=dawn.id),
    ]
    session.add_all(pokemons)
    session.commit()

    """
    ASIGNACIÓN DE TIPOS A CADA POKEMON
    """
    asignacion_tipos = [
        PokemonTipo(pokemon_id=pokemons[0].id, tipo_id=t_electrico.id),  # Pikachu (Eléctrico)
        PokemonTipo(pokemon_id=pokemons[1].id, tipo_id=t_fuego.id),      # Charizard (Fuego / Volador)
        PokemonTipo(pokemon_id=pokemons[1].id, tipo_id=t_volador.id),
        PokemonTipo(pokemon_id=pokemons[2].id, tipo_id=t_planta.id),     # Bulbasaur (Planta)
        PokemonTipo(pokemon_id=pokemons[3].id, tipo_id=t_agua.id),       # Blastoise (Agua)
        PokemonTipo(pokemon_id=pokemons[4].id, tipo_id=t_fuego.id),      # Arcanine (Fuego)
        PokemonTipo(pokemon_id=pokemons[5].id, tipo_id=t_volador.id),    # Pidgeot (Volador)
        PokemonTipo(pokemon_id=pokemons[6].id, tipo_id=t_fuego.id),      # Typhlosion (Fuego)
        PokemonTipo(pokemon_id=pokemons[7].id, tipo_id=t_agua.id),       # Gyarados (Agua / Volador)
        PokemonTipo(pokemon_id=pokemons[7].id, tipo_id=t_volador.id),
        PokemonTipo(pokemon_id=pokemons[8].id, tipo_id=t_electrico.id),  # Ampharos (Eléctrico)
        PokemonTipo(pokemon_id=pokemons[9].id, tipo_id=t_planta.id),     # Meganium (Planta)
        PokemonTipo(pokemon_id=pokemons[10].id, tipo_id=t_agua.id),      # Marill (Agua)
        PokemonTipo(pokemon_id=pokemons[11].id, tipo_id=t_planta.id),    # Sceptile (Planta)
        PokemonTipo(pokemon_id=pokemons[12].id, tipo_id=t_volador.id),   # Swellow (Volador)
        PokemonTipo(pokemon_id=pokemons[13].id, tipo_id=t_agua.id),      # Piplup (Agua)
        PokemonTipo(pokemon_id=pokemons[14].id, tipo_id=t_fuego.id),     # Blaziken (Fuego / Volador)
        PokemonTipo(pokemon_id=pokemons[14].id, tipo_id=t_volador.id),
        PokemonTipo(pokemon_id=pokemons[15].id, tipo_id=t_volador.id),   # Beautifly (Volador)
        PokemonTipo(pokemon_id=pokemons[16].id, tipo_id=t_planta.id),    # Torterra (Planta / Tierra)
        PokemonTipo(pokemon_id=pokemons[16].id, tipo_id=t_tierra.id),
        PokemonTipo(pokemon_id=pokemons[17].id, tipo_id=t_volador.id),   # Staraptor (Volador)
        PokemonTipo(pokemon_id=pokemons[18].id, tipo_id=t_agua.id),      # Empoleon (Agua / Hielo)
        PokemonTipo(pokemon_id=pokemons[18].id, tipo_id=t_hielo.id),
        PokemonTipo(pokemon_id=pokemons[19].id, tipo_id=t_tierra.id),    # Mamoswine (Tierra / Hielo)
        PokemonTipo(pokemon_id=pokemons[19].id, tipo_id=t_hielo.id),
    ]
    session.add_all(asignacion_tipos)
    session.commit()

    """
    BATALLAS Y ENTRENADORES PARTICIPANTES
    """
    # Batalla 1: Victoria de Ash sobre Gary
    b1 = Batalla(fecha="2026-05-10", lugar="Estación Central", rondas=5, ganador_id=ash.id)
    session.add(b1)
    session.commit()
    session.add_all([
        Participacion(entrenador_id=ash.id, batalla_id=b1.id, resultado="victoria"),
        Participacion(entrenador_id=gary.id, batalla_id=b1.id, resultado="derrota"),
    ])

    # Batalla 2: Victoria de Ethan sobre Lira
    b2 = Batalla(fecha="2026-05-12", lugar="Plaza Colón", rondas=3, ganador_id=ethan.id)
    session.add(b2)
    session.commit()
    session.add_all([
        Participacion(entrenador_id=ethan.id, batalla_id=b2.id, resultado="victoria"),
        Participacion(entrenador_id=lira.id, batalla_id=b2.id, resultado="derrota"),
    ])

    # Batalla 3: Empate entre Brendan y May
    b3 = Batalla(fecha="2026-05-15", lugar="Pastos UCN", rondas=4, ganador_id=None)  # Empate
    session.add(b3)
    session.commit()
    session.add_all([
        Participacion(entrenador_id=brendan.id, batalla_id=b3.id, resultado="empate"),
        Participacion(entrenador_id=may.id, batalla_id=b3.id, resultado="empate"),
    ])

    # Batalla 4: Victoria de Dawn sobre Lucas
    b4 = Batalla(fecha="2026-05-18", lugar="Calama", rondas=6, ganador_id=dawn.id)
    session.add(b4)
    session.commit()
    session.add_all([
        Participacion(entrenador_id=dawn.id, batalla_id=b4.id, resultado="victoria"),
        Participacion(entrenador_id=lucas.id, batalla_id=b4.id, resultado="derrota"),
    ])

    # Batalla 5: Victoria de Ash sobre Brendan
    b5 = Batalla(fecha="2026-05-20", lugar="Coviefi", rondas=3, ganador_id=ash.id)
    session.add(b5)
    session.commit()
    session.add_all([
        Participacion(entrenador_id=ash.id, batalla_id=b5.id, resultado="victoria"),
        Participacion(entrenador_id=brendan.id, batalla_id=b5.id, resultado="derrota"),
    ])

    # Batalla 6: Victoria de Gary sobre Ethan
    b6 = Batalla(fecha="2026-05-22", lugar="Sala R-15 UCN", rondas=5, ganador_id=gary.id)
    session.add(b6)
    session.commit()
    session.add_all([
        Participacion(entrenador_id=gary.id, batalla_id=b6.id, resultado="victoria"),
        Participacion(entrenador_id=ethan.id, batalla_id=b6.id, resultado="derrota"),
    ])
    session.commit()
