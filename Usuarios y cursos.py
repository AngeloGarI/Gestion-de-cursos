class Usuario:
    def __init__(self, id, nombre, email):
        self.id=id
        self.nombre=nombre
        self.email=email
        self.tipo="usuario"

    def iniciar_sesion(self, email):
        return self.email==email
    
class Estudiante(Usuario):
    def __init__(self, id, nombre, email, carnet):
        super().__init__(id, nombre, email)
        self.carnet=carnet
        self.tipo="estudiante"
        self.cursos_inscritos=[]
        self.calificaciones={} #{curso_id: calificacion}

    def asignar_cursos(self, curso):
        if curso not in self.cursos_inscritos:
            self.cursos_inscritos.append(curso)
            return True
        return False
    
    def obtener_promedio(self,curso_id=None):
        if curso_id:
            if curso_id in self.calificaciones and self.calificaciones[curso_id]:
                califs=self.calificaciones[curso_id].values()
                return sum(califs)/len(califs)
            return 0
        else:
            # CALCULAMOS EL PROMEDIO GENERAL
            promedios=[]
            for curso_id, evaluaciones in self.calificaciones.items():
                if evaluaciones:
                    promedios.append(sum(evaluaciones.values())/len(evaluaciones))
            return sum(promedios)/len(promedios) 
        
class Profesor(Usuario):
    def __init__(self, id, nombre, email, profesion):
        super().__init__(id, nombre, email, profesion)
        self.profesion=profesion
        self.tipo="Profesor"
        self.cursos=[]

    def crear_curso(self, codigo, nombre):
        curso = Curso(codigo, nombre, self)
        self.cursos.append(curso)
        return curso
    
    def crear_evaluacion(self, curso, tipo, nombre, puntaje_maximo):
        return Evaluacion.crear_evaluacion(tipo, nombre, curso, puntaje_maximo)