"""SmartBin AI - Simulación didáctica del basurero inteligente (POO).
No usa un modelo real de IA: simula la decisión para explicar el funcionamiento."""
import random
from pyscript import document


class Residuo:
    def __init__(self, nombre, reciclable):
        self.nombre = nombre
        self.reciclable = reciclable


class CamaraIA:
    """Simula la visión artificial: devuelve la categoría o None si hay poca certeza."""
    UMBRAL = 70  # % mínimo de certeza para actuar

    def analizar(self, residuo, certeza):
        if certeza < self.UMBRAL:
            return None
        return residuo.reciclable


class Compuerta:
    """Simula un servomotor controlado por el Arduino."""
    def __init__(self, id_html):
        self.id_html = id_html
        self.angulo = 0

    def mover(self, abrir):
        self.angulo = 90 if abrir else 0
        cont = document.getElementById(self.id_html)
        if abrir:
            cont.classList.add("abierta")
        else:
            cont.classList.remove("abierta")


class SmartBin:
    def __init__(self):
        self.camara = CamaraIA()
        self.verde = Compuerta("bin-rec")
        self.gris = Compuerta("bin-no")
        self.conteo = {"rec": 0, "no": 0, "dudas": 0}

    def procesar(self, residuo, certeza):
        tiempo = round(0.3 + (100 - certeza) / 100 + random.random() * 0.3, 2)  # simulado
        categoria = self.camara.analizar(residuo, certeza)
        self.verde.mover(categoria is True)
        self.gris.mover(categoria is False)
        if categoria is None:
            self.conteo["dudas"] += 1
            return f"❓ Certeza {certeza}% (menor a {self.camara.UMBRAL}%): no se abre ninguna compuerta. Se pide revisión manual. Tiempo simulado: {tiempo} s."
        clave = "rec" if categoria else "no"
        self.conteo[clave] += 1
        destino = "RECICLABLE (compuerta verde, servo a 90°)" if categoria else "NO RECICLABLE (compuerta gris, servo a 90°)"
        return f"✅ {residuo.nombre}: {destino}. Certeza {certeza}%. Tiempo simulado: {tiempo} s."


bin_ia = SmartBin()


def simular(event=None):
    nombre, rec = document.getElementById("residuo").value.split("|")
    certeza = int(document.getElementById("certeza").value)
    texto = bin_ia.procesar(Residuo(nombre, rec == "1"), certeza)
    document.getElementById("resultado").innerText = texto
    document.getElementById("c-rec").innerText = str(bin_ia.conteo["rec"])
    document.getElementById("c-no").innerText = str(bin_ia.conteo["no"])
    document.getElementById("c-dudas").innerText = str(bin_ia.conteo["dudas"])
