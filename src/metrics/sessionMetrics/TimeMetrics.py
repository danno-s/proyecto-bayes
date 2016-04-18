"""
Definición de distintas Distance (implementacicones de SessionMetric) que utilizan la información
del tiempo y fecha de las sesiones.
"""
from datetime import timedelta

from src.metrics.Metric import SessionMetric


class DurationDistance(SessionMetric):
    """
    Clase que implementa la métrica como una diferencia entre las duraciones de las sesiones.
    """

    def __init__(self):
        SessionMetric.__init__(self)

    def distance(self, s1, s2):
        """Distancia de las sesiones s1 y s2 definida como el valor absoluto de la diferencia entre
         las duraciones de las sesiones.

        Parameters
        ----------
        s1 : Session
            una sesión.
        s2 : Session
            una sesión.
        Returns
        -------
        float
            distancia calculada.
        """
        return float(abs(self.getDuration(s1) - self.getDuration(s2)))

    def getDuration(self, session):
        """Retorna la duración de la sesión en segundos.

        Parameters
        ----------
        session : Session
            una sesión

        Returns
        -------
        int
            la duración de la sesión en segundos..
        """
        td = session.endTime - session.initTime
        return td / timedelta(seconds=1)


class HourOfDayDistance(SessionMetric):
    """
    Clase que implementa la métrica como una diferencia entre la hora relativa del día en que se dió
    inicio a las sesiones.

    Notes
        Hora relativa del día se refiere a de las 24 horas, a qué fracción del día corresponde la hora de inicio.
        Por ejemplo, a medio día (12:00) la hora relativa del día sería 0.5, mientras que a las 18:00, la hora relativa
        del día sería 0.75.

        La idea de esto es evaluar si existe una tendencia en el momento del día en que se realizan las sesiones.
    """

    def __init__(self):
        SessionMetric.__init__(self)

    def distance(self, s1, s2):
        """Distancia de las sesiones s1 y s2 definida como la diferencia entre las duraciones de las sesiones.

        Parameters
        ----------
        s1 : Session
            una sesión.
        s2 : Session
            una sesión.
        Returns
        -------
        float
            distancia calculada.
        """
        return float(abs(self.getHourOfDay(s1) - self.getHourOfDay(s2)))

    def getHourOfDay(self, session):
        """Retorna la hora relativa del día de inicio de la sesión.

        Parameters
        ----------
        session : Session
            una sesión

        Returns
        -------
        float
            hora relativa del día de la sesión.
        """
        relative_hour = session.initTime.hour + session.initTime.minute / 60.
        print(relative_hour)
        return relative_hour / 24.0
