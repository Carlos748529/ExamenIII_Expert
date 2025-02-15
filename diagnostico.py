# diagnostico.py

from experta import Fact, KnowledgeEngine, Rule, MATCH

class Sintoma(Fact):
    """Hecho para declarar la presencia (True) o ausencia (False) de un síntoma."""
    pass

class DiagnosticoEngine(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.resultado = None

    # Regla para diagnosticar Influenza: fiebre, tos y dolor de garganta.
    @Rule(Sintoma(fiebre=True), Sintoma(tos=True), Sintoma(dolor_garganta=True))
    def diagnostico_influenza(self):
        self.declare(Fact(diagnostico="Influenza"))

    # Regla para diagnosticar Gastroenteritis: dolor abdominal, náuseas y vómitos.
    @Rule(Sintoma(dolor_abdominal=True), Sintoma(nauseas=True), Sintoma(vomito=True))
    def diagnostico_gastroenteritis(self):
        self.declare(Fact(diagnostico="Gastroenteritis"))

    # Regla para diagnosticar Escarlatina: fiebre y erupción.
    @Rule(Sintoma(fiebre=True), Sintoma(erupcion=True))
    def diagnostico_escarlatina(self):
        self.declare(Fact(diagnostico="Escarlatina"))    
    
    # Regla para capturar y almacenar el diagnóstico encontrado.
    @Rule(Fact(diagnostico=MATCH.diag))
    def capturar_diagnostico(self, diag):
        self.resultado = diag
