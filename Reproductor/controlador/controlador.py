import os
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import QStandardPaths, QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtMultimedia import QMediaPlayer
from PIL import Image

class Controlador:
    
    def __init__(self, vista, reproductor):
        self.vista = vista
        self.reproductor = reproductor
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.actualizar_slider)
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

        self.vista.mp3_slider.sliderMoved.connect(self.slider_movido)
        self.vista.mp4_slider.sliderMoved.connect(self.slider_movido)

        self.vista.mp3_volumen_slider.valueChanged.connect(self.cambiar_volumen)
        self.vista.mp4_volumen_slider.valueChanged.connect(self.cambiar_volumen)

        self.vista.galeria_botton_convertir.clicked.connect(self.convertir_jpg_a_png)
        self.vista.botton_escalar.clicked.connect(self.escalar_imagen)

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
                self.vista.mp3_slider.setValue(0)
                self.reproductor.cargar(nombre)
                self.reproductor.reproductor.mediaStatusChanged.connect(self.media_status_changed)
                self.vista.actualizar_boton_play(True)
            elif pestanya == 1:
                self.vista.mp4_slider.setValue(0)
                self.reproductor.cargar(nombre, self.vista.imagen_widget)
                self.reproductor.reproductor.mediaStatusChanged.connect(self.media_status_changed)
                self.vista.actualizar_boton_play(True)
            elif pestanya == 2:
                self.imagen_actual = nombre
                ruta = os.path.join(self.reproductor.carpeta_actual, nombre)
                self.vista.mostrar_imagen(ruta)

    def actualizar_slider(self):
        pestanya = self.vista.pestanya_actual()
        posicion = self.reproductor.posicion()
        if pestanya == 0:
            self.vista.mp3_slider.setValue(posicion)
        elif pestanya == 1:
            self.vista.mp4_slider.setValue(posicion)

    def cambiar_volumen(self, value):
        volumen = value / 100.0
        self.reproductor.cambiar_volumen(volumen)

    def slider_movido(self, posicion):
        self.reproductor.saltar_a(posicion)

    def media_status_changed(self, status):
        if status == QMediaPlayer.MediaStatus.LoadedMedia:
            self.reproductor.reproducir()
            duracion = self.reproductor.duracion()
            pestanya = self.vista.pestanya_actual()
            if pestanya == 0:
                self.vista.mp3_slider.setRange(0, duracion)
            elif pestanya == 1:
                self.vista.mp4_slider.setRange(0, duracion)
            self.timer.start()

    def mostrar_ocultar_panel_lateral(self):
        if self.vista.listar_action.isChecked():
            self.vista.dock.show()
        else:
            self.vista.dock.hide()

    def convertir_jpg_a_png(self):
        ruta = os.path.join(self.reproductor.carpeta_actual, self.imagen_actual)
        imagen = Image.open(ruta)
        nombre_imagen = os.path.splitext(self.imagen_actual)[0]
        imagen.save(os.path.join(self.reproductor.carpeta_actual, f'{nombre_imagen}.png'))
        self.vista.galeria_label_resultado_conversion.setText(f"Convertida: {nombre_imagen}.png")

    def escalar_imagen(self):
        ancho = self.vista.ancho_input.value()
        altura = self.vista.alto_input.value()
        ruta = os.path.join(self.reproductor.carpeta_actual, self.imagen_actual)
        imagen = Image.open(ruta)
        filtro = Image.Resampling.LANCZOS
        if ancho < imagen.width or altura < imagen.height:
            filtro = Image.Resampling.BICUBIC
        imagen_escalada = imagen.resize((ancho,altura), filtro)
        imagen_escalada.save("resultado.jpg")