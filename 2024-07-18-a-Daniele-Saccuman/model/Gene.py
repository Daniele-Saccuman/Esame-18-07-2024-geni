from dataclasses import dataclass

@dataclass
class Genes:

    GeneID: str
    Function: str
    Essential:str
    Chromosome: int

    def __hash__(self):
        return hash(self.GeneID)

    def __str__(self):
        return f"{self.GeneID} - {self.Function} - {self.Essential} - {self.Chromosome}"