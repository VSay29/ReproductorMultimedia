import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow,
                             QLabel, QPushButton, QDockWidget,
                             QStatusBar, QTabWidget, QWidget,
                             QHBoxLayout, QVBoxLayout, QListWidget,
                             QFileDialog, QListWidgetItem)

from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

from PyQt6.QtGui import QPixmap, QAction, QKeySequence, QIcon
from PyQt6.QtCore import Qt, QStandardPaths, QUrl

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initialize_ui()
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.current_music_folder = ""
        with open('Reproductor mp3/estilos.css', 'r') as file:
            style = file.read()
        self.setStyleSheet(style)
        self.player = None
        self.playing_reproductor = False

    def initialize_ui(self):
        self.setGeometry(100,100,800,500) #X,Y,Ancho,Alto -> En ese orden
        self.setWindowTitle("Reproductor MP3")
        self.generate_main_window()
        self.create_dock()
        self.create_action()
        self.create_menu()
        self.show()

    def generate_main_window(self):
        tab_bar = QTabWidget(self)
        self.reproductor_container = QWidget()
        self.settings_container = QWidget()
        tab_bar.addTab(self.reproductor_container, "Reproductor")
        tab_bar.addTab(self.settings_container, "Ajustes")

        self.generate_reproductor_tab()

        tab_h_box = QHBoxLayout()
        tab_h_box.addWidget(tab_bar)

        main_container = QWidget()
        main_container.setLayout(tab_h_box)
        self.setCentralWidget(main_container)

    def generate_reproductor_tab(self):
        main_v_box = QVBoxLayout() # Contenedor vertical
        buttons_h_box = QHBoxLayout() # Contenedor horizontal

        song_image = QLabel()
        pixmap = QPixmap("Reproductor mp3/images/fondo2.png").scaled(512, 300)
        song_image.setPixmap(pixmap)
        song_image.setScaledContents(True)

        self.botton_repeat = QPushButton()
        self.botton_repeat.setObjectName("botonRepeat")
        self.botton_before = QPushButton()
        self.botton_before.setObjectName("botonBefore")
        self.botton_play = QPushButton()
        self.botton_play.setObjectName("botonPlay")
        self.botton_play.clicked.connect(self.play_pause_song)
        self.botton_next = QPushButton()
        self.botton_next.setObjectName("botonNext")
        self.botton_random = QPushButton()
        self.botton_random.setObjectName("botonRandom")

        self.botton_repeat.setFixedSize(40,40)
        self.botton_before.setFixedSize(40,40)
        self.botton_play.setFixedSize(50,50)
        self.botton_next.setFixedSize(40,40)
        self.botton_random.setFixedSize(40,40)

        buttons_h_box.addWidget(self.botton_repeat)
        buttons_h_box.addWidget(self.botton_before)
        buttons_h_box.addWidget(self.botton_play)
        buttons_h_box.addWidget(self.botton_next)
        buttons_h_box.addWidget(self.botton_random)

        buttons_container = QWidget()
        buttons_container.setLayout(buttons_h_box)

        main_v_box.addWidget(song_image)
        main_v_box.addWidget(buttons_container)

        self.reproductor_container.setLayout(main_v_box)


    def create_action(self):
        self.listar_musica_action = QAction('Listar música', self, checkable = True)
        self.listar_musica_action.setShortcut(QKeySequence("Ctrl+L"))
        self.listar_musica_action.setStatusTip("Selecciona una lista de canciones a reproducir")
        self.listar_musica_action.triggered.connect(self.list_music)
        self.listar_musica_action.setChecked(True)

        self.open_folder_musica_action = QAction('Abrir carpeta', self)
        self.open_folder_musica_action.setShortcut(QKeySequence("Ctrl+O"))
        self.open_folder_musica_action.setStatusTip("Abrir carpeta de música")
        self.open_folder_musica_action.triggered.connect(self.open_folder_music)

    def create_menu(self):
        self.menuBar()
        menu_file = self.menuBar().addMenu("File")
        menu_view = self.menuBar().addMenu("View")
        menu_file.addAction(self.open_folder_musica_action)
        menu_view.addAction(self.listar_musica_action)

    def create_dock(self):
        self.songs_list = QListWidget()
        self.dock = QDockWidget()
        self.dock.setWindowTitle("Lista de canciones")
        self.dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea |
            Qt.DockWidgetArea.RightDockWidgetArea
        )
        self.songs_list.itemSelectionChanged.connect(self.handle_song_selection)
        self.dock.setWidget(self.songs_list)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)

    def list_music(self):
        if self.listar_musica_action.isChecked():
            self.dock.show()
        else:
            self.dock.hide()

    def open_folder_music(self):
        self.songs_list.clear()
        initial_dir = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.MusicLocation
        )
        self.current_music_folder = QFileDialog.getExistingDirectory(None, "Seleccione una carpeta", initial_dir)
        icon = QIcon("Reproductor mp3/images/mp3Icon.png")
        for archivo in os.listdir(self.current_music_folder):
            ruta_archivo = os.path.join(self.current_music_folder, archivo)
            if ruta_archivo.endswith(".mp3"):
                item = QListWidgetItem(archivo)
                item.setIcon(icon)
                self.songs_list.addItem(item)

    
    def create_player(self):
        if self.player:
            self.player.deleteLater()
        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.player.setAudioOutput(self.audioOutput)
        self.player.mediaStatusChanged.connect(self.media_status_changed)
        self.audioOutput.setVolume(1.0)

    #SLOT HANDLING

    def play_pause_song(self):
        if self.playing_reproductor:
            self.botton_play.setStyleSheet("image: url('Reproductor mp3/images/pause.png');")
            self.player.pause()
            self.playing_reproductor = False
        else:
            self.botton_play.setStyleSheet("image: url('Reproductor mp3/images/play.png');")
            self.player.play()
            self.playing_reproductor = True

    def media_status_changed(self, status):
        if status == QMediaPlayer.MediaStatus.LoadedMedia:
            self.player.play()

    def handle_song_selection(self):
        selected_item = self.songs_list.currentItem()
        if selected_item:
            self.botton_play.setStyleSheet("image: url('Reproductor mp3/images/play.png');")
            song_name = selected_item.data(0)
            song_folder_path = os.path.join(self.current_music_folder, song_name)
            self.create_player()
            source = QUrl.fromLocalFile(song_folder_path)
            self.player.setSource(source)
            self.playing_reproductor = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())