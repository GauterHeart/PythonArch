"""Test."""

from yoyo import step

__depends__ = {"20230123_01_IMTPT-base"}

steps = [
    step(
        """
         create table test_c(id serial)
         """,
        "drop table test_c",
    )
]
