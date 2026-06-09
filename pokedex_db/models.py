from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


# Tablas Asociativas

class PokemonTipo(SQLModel, table=True):
    """Tabla asociativa que relaciona Pokemon con Tipo (Relación N:M).

    La clave primaria es compuesta: (pokemon_id, tipo_id). Esto garantiza
    que un mismo par Pokémon-Tipo no pueda registrarse dos veces.
    Un Pokémon puede tener hasta dos tipos distintos.
    """

    pokemon_id: int = Field(foreign_key="pokemon.id", primary_key=True)
    tipo_id: int = Field(foreign_key="tipo.id", primary_key=True)


class Participacion(SQLModel, table=True):
    """Tabla asociativa que relaciona Entrenador con Batalla (Relación N:M).

    La clave primaria es compuesta: (entrenador_id, batalla_id).
    Registra la participación de exactamente dos entrenadores por batalla,
    junto con el resultado obtenido ("victoria", "derrota" o "empate").
    """

    entrenador_id: int = Field(foreign_key="entrenador.id", primary_key=True)
    batalla_id: int = Field(foreign_key="batalla.id", primary_key=True)
    resultado: str = Field(
        description="Resultado obtenido: 'victoria', 'derrota' o 'empate'"
    )


# Entidades Principales

class Region(SQLModel, table=True):
    """Representa una región del mundo Pokémon.

    Una región puede tener muchos entrenadores registrados (1-a-N).
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True, nullable=False)
    generacion: int = Field(
        ge=1,
        le=9,
    )
    descripcion: Optional[str] = Field(default=None, nullable=True)

    # Relaciones: entrenadores que pertenecen a cada región
    entrenadores: List["Entrenador"] = Relationship(back_populates="region")


class Entrenador(SQLModel, table=True):
    """Representa un entrenador Pokémon registrado en el sistema.

    Pertenece a una Region (N-a-1) y puede tener muchos Pokemon (1-a-N).
    Participa en muchas Batalla a través de Participacion (N-a-M).
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(nullable=False)
    edad: int = Field(ge=10)
    insignias: int = Field(
        ge=0,
        le=8,
    )
    es_campeon: Optional[bool] = Field(default=None, nullable=True)

    # Clave foránea hacia Región
    region_id: int = Field(foreign_key="region.id")

    # Relaciones
    # Relación N-a-1: región a la que pertenece el entrenador.
    region: Region = Relationship(back_populates="entrenadores")

    # Relación 1-a-N: Pokemon capturados por este entrenador.
    pokemons: List["Pokemon"] = Relationship(back_populates="entrenador")

    # Relación N-a-M: batallas en las que participó.
    batallas_participadas: List["Batalla"] = Relationship(
        back_populates="entrenadores", link_model=Participacion
    )


class Pokemon(SQLModel, table=True):
    """Representa un Pokemon capturado perteneciente a un entrenador.

    Tiene una relación N-a-M con Tipo a través de PokemonTipo
    (un Pokémon puede tener hasta dos tipos distintos).
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(nullable=False)
    nivel: int = Field(
        ge=1,
        le=100,
    )
    puntos_vida: int = Field(gt=0)
    es_shiny: Optional[bool] = Field(default=False, nullable=True)
    apodo: Optional[str] = Field(default=None, nullable=True)

    # Clave foránea hacia entrenador
    entrenador_id: int = Field(foreign_key="entrenador.id")

    # Relaciones
    # Relación N-a-1: entrenador propietario del Pokémon.
    entrenador: Entrenador = Relationship(back_populates="pokemons")

    # Relación N-a-M: tipos asignados a cada Pokémon.
    tipos: List["Tipo"] = Relationship(
        back_populates="pokemons",
        link_model=PokemonTipo
    )


class Tipo(SQLModel, table=True):
    """Representa un tipo de Pokemon.

    Un tipo puede asignarse a muchos Pokémon (N-a-M via PokemonTipo).
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True, nullable=False)
    color_hex: Optional[str] = Field(default=None, nullable=True)


    # Relación N-a-M: Pokemon asociado a cada tipo
    pokemons: List[Pokemon] = Relationship(
        back_populates="tipos",
        link_model=PokemonTipo
    )


class Batalla(SQLModel, table=True):
    """Representa un combate entre dos entrenadores.

    Los participantes se vinculan a través de la tabla Participacion.
    El campo ganador_id es opcional: es None cuando el combate termina
    en empate.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    fecha: str = Field(nullable=False)
    lugar: str = Field(nullable=False)
    rondas: int = Field(gt=0)
    ganador_id: Optional[int] = Field(default=None, foreign_key="entrenador.id", nullable=True)

    # Relación N-a-M: entrenadores que participaron en cada batalla.
    entrenadores: List[Entrenador] = Relationship(
        back_populates="batallas_participadas",
        link_model=Participacion
    )