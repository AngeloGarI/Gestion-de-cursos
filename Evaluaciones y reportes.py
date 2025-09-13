from abc import ABC, abstractmethod
class Evaluacion(ABC):
    def __init__(self, nombre, curso, puntaje_maximo):
        self.nombre = nombre
        self.curso = curso
        self.puntaje_maximo = puntaje_maximo
        self.notas = {}

    @abstractmethod
    def tipo(self):
        pass

    def registrar_nota(self, estudiante, nota):
        if estudiante not in self.curso.estudiantes:
            raise ValueError (f"Estudiante {estudiante.nombre} no inscrito "
                              f"en el curso {self.curso.nombre}")
        if nota < 0 or nota > self.puntaje_maximo:
            raise ValueError(f"Nota invalida: {nota}")
        self.notas[estudiante] = nota
        if self.curso.codigo not in estudiante.calificaciones:
            estudiante.calificaciones[self.curso.codigo] = {}
        estudiante.calificaciones[self.curso.codigo][self.nombre] = nota

    def obtener_promedio_curso(self):
        if self.notas:
            return sum(self.notas.values())/len(self.notas)
        return 0
