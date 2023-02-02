"""Logger."""

from yoyo import step

__depends__ = {"20230123_01_IMTPT-auth"}

steps = [
    step(
        """
         create table status(
            id serial primary key,
            name name unique)
         """,
        "drop table status",
    ),
    step(
        """
         create table type(
            id serial primary key,
            name name unique)
         """,
        "drop table type",
    ),
    step(
        """
         create table service(
            id serial primary key,
            name name unique)
         """,
        "drop table service",
    ),
    step(
        """
         create table logger(
            id bigserial primary key,
            status_id integer not null,
            type_id ineger not null,
            service_id ineger nou null,
            msg varchar(2056) not null,
            date_create timestamp not null default now(),
            constraint logger_status_fk
              foreign key(status_id)
              references status(id),
            constraint logger_type_fk
              foreign key(type_id)
              references type(id),
            constraint logger_service_fk
              foreign key(service_id)
              references service(id)
            )
         """,
        "drop table logger",
    ),
]
