from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl
import os

class Reproductor:

    def __init__(self):
        self.reproduciendo = False
        self.carpeta_actual = ""
        self.reproductor = None
        self.audioOutput = None

    def crear_reproductor(self, video_widget=None):
        if self.reproductor:
            self.reproductor.deleteLater()
        self.reproductor = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.reproductor.setAudioOutput(self.audioOutput)
        self.audioOutput.setVolume(1.0)
        if video_widget:
            self.reproductor.setVideoOutput(video_widget)

    def cargar(self, nombre, video_widget=None):
        ruta = os.path.join(self.carpeta_actual, nombre)
        self.crear_reproductor(video_widget)
        origen = QUrl.fromLocalFile(ruta)
        self.reproductor.setSource(origen)
        self.reproduciendo = True

    def reproducir(self):
        if self.reproductor:
            self.reproductor.play()
            self.reproduciendo = True

    def pausar(self):
        if self.reproductor:
            self.reproductor.pause()
            self.reproduciendo = False

    def detener(self):
        if self.reproductor:
            self.reproductor.stop()
            self.reproductor.deleteLater()
            self.reproductor = None
            self.reproduciendo = False

    def obtener_canciones(self, ruta_carpeta):
        self.carpeta_actual = ruta_carpeta
        canciones = []
        for archivo in os.listdir(ruta_carpeta):
            ruta = os.path.join(ruta_carpeta, archivo)
            if ruta.endswith(".mp3"):
                canciones.append(archivo)
        return canciones

    def obtener_videos(self, ruta_carpeta):
        self.carpeta_actual = ruta_carpeta
        videos = []
        for archivo in os.listdir(ruta_carpeta):
            ruta = os.path.join(ruta_carpeta, archivo)
            if ruta.endswith(".mp4"):
                videos.append(archivo)
        return videos
    
    def obtener_imagenes(self, ruta_carpeta):
        self.carpeta_actual = ruta_carpeta
        imagenes = []
        for archivo in os.listdir(ruta_carpeta):
            ruta = os.path.join(ruta_carpeta, archivo)
            if ruta.endswith(".jpg"):
                imagenes.append(archivo)
        return imagenes
    
    def duracion(self):
        return self.reproductor.duration()
    
    def posicion(self):
        return self.reproductor.position()
    
    def saltar_a(self, posicion):
        self.reproductor.setPosition(posicion)

    def cambiar_volumen(self, volumen):
        if self.audioOutput:
            self.audioOutput.setVolume(volumen)