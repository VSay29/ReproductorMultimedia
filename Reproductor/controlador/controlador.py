import os
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import QStandardPaths
from PyQt6.QtGui import QIcon
from PyQt6.QtMultimedia import QMediaPlayer

class Controlador:
    
    def __init__(self, vista, reproductor):
        self.vista = vista
        self.reproductor = reproductor
        self.conectar_senyales()

    def conectar_senyales(self):

        self.vista.mp3_botton_play.clicked.connect(self.play_pausa)
        self.vista.mp4_botton_play.clicked.connect(self.play_pausa)
        
        self.vista.abrir_carpeta_action.triggered.connect(self.abrir_carpeta)
        self.vista.listar_action.triggered.connect(self.mostrar_ocultar_panel_lateral)
        self.vista.lista.itemSelectionChanged.connect(self.manejar_selector_elemento_lista)
        self.vista.tab_bar.currentChanged.connect(self.limpiar_lista)

        self.vista.mp3_botton_next.clicked.connect(self.siguiente)
        self.vista.mp4_botton_next.clicked.connect(self.siguiente)
        self.vista.botton_next.clicked.connect(self.siguiente)

        self.vista.mp3_botton_before.clicked.connect(self.anterior)
        self.vista.mp4_botton_before.clicked.connect(self.anterior)
        self.vista.botton_before.clicked.connect(self.anterior)

    def play_pausa(self):
        if self.reproductor.reproduciendo:
            self.reproductor.pausar()
        else:
            self.reproductor.reproducir()
        self.vista.actualizar_boton_play(self.reproductor.reproduciendo)

    def siguiente(self):
        total = self.vista.lista.count()
        if total == 0:
            return
        actual = self.vista.lista.currentRow()
        siguiente = (actual + 1) % total # % total hace que sea circular
        self.vista.lista.setCurrentRow(siguiente)

    def anterior(self):
        total = self.vista.lista.count()
        if total == 0:
            return
        actual = self.vista.lista.currentRow()
        anterior = (actual - 1) % total # % total hace que sea circular
        self.vista.lista.setCurrentRow(anterior)

    def abrir_carpeta(self):
        initial_dir = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.MusicLocation
        )
        ruta_carpeta = QFileDialog.getExistingDirectory(
            None, "Seleccione una carpeta", initial_dir
        )

        if ruta_carpeta:
            pestanya = self.vista.pestanya_actual()

            if pestanya == 0:
                archivos = self.reproductor.obtener_canciones(ruta_carpeta)
                icono = QIcon("Reproductor/imagenes/mp3Icon.png")
            elif pestanya == 1:
                archivos = self.reproductor.obtener_videos(ruta_carpeta)
                icono = QIcon("Reproductor/imagenes/mp4Icon.png")
            elif pestanya == 2:
                archivos = self.reproductor.obtener_imagenes(ruta_carpeta)
                icono = QIcon("Reproductor/imagenes/jpgIcon.png")

            self.vista.cargar_lista(archivos, icono)

    def limpiar_lista(self):
        self.vista.lista.clear()

    def manejar_selector_elemento_lista(self):
        elemento = self.vista.lista.currentItem()
        if elemento:
            nombre = elemento.data(0)
            pestanya = self.vista.pestanya_actual()
            if pestanya == 0:
                self.reproductor.cargar(nombre)
                self.reproductor.reproductor.mediaStatusChanged.connect(self.media_status_changed)
                self.vista.actualizar_boton_play(True)
            elif pestanya == 1:
                self.reproductor.cargar(nombre, self.vista.imagen_widget)
                self.reproductor.reproductor.mediaStatusChanged.connect(self.media_status_changed)
                self.vista.actualizar_boton_play(True)
            elif pestanya == 2:
                ruta = os.path.join(self.reproductor.carpeta_actual, nombre)
                self.vista.mostrar_imagen(ruta)

    def media_status_changed(self, status):
        if status == QMediaPlayer.MediaStatus.LoadedMedia:
            self.reproductor.reproducir()

    def mostrar_ocultar_panel_lateral(self):
        if self.vista.listar_action.isChecked():
            self.vista.dock.show()
        else:
            self.vista.dock.hide()