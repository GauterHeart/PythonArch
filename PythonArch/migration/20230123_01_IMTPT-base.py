"""Base."""

from yoyo import step

__depends__: dict = {}

steps = [
    step(
        """
         create table client(
            id serial primary key unique,
            name name not null,
            public_key varchar(256) not null,
            private_key varchar(512) not null,
            date_create timestamp default now())
         """,
        "drop table client",
    ),
]
