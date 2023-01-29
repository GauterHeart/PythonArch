class ProgramException(Exception):
    def __init__(self) -> None:
        self.msg = "Program not found"

    def __str__(self) -> str:
        return "{}".format(self.msg)
