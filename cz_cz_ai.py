from commitizen.cz.base import BaseCommitizen


class Cz_aiCz(BaseCommitizen):
    def questions(self) -> list:
        print("Questions method not implemented yet")
        raise NotImplementedError("Not Implemented yet")

    def message(self, answers: dict) -> str:
        raise NotImplementedError("Not Implemented yet")
