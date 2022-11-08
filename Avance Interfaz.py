from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLineEdit, QPushButton, QLabel, \
     QVBoxLayout, QTextEdit
from PyQt5.QtGui import QPixmap, QImage, QDesktopServices
from PyQt5.QtCore import QUrl
import requests
import threading


def custom(args):
    print(f'Thread failed: {args.exc_value}')


class windowManager(QMainWindow): #creacion de la ventana
    def __init__(self):
        self.data_movies = []
        super().__init__()
        self.setWindowTitle("Mi buscador")
        self.resize(620, 255) #definir tamaño
        self.container = QWidget()
        self.lyt_Images_Left = QVBoxLayout()
        self.lyt_Images_Center = QVBoxLayout()
        self.lyt_Images_Right = QVBoxLayout()
        self.lytPrincipal = QGridLayout()
        self.lblBusca = QLabel("words de películas a buscar: ")
        self.inlineText = QLineEdit()
        self.btnBusca = QPushButton("Filtrar")
        self.btnBusca.clicked.connect(self.divTXT)
        self.lytPrincipal.addWidget(self.lblBusca, 0, 0)
        self.lytPrincipal.addWidget(self.inlineText, 0, 1)
        self.lytPrincipal.addWidget(self.btnBusca, 0, 2)
        self.lytPrincipal.addLayout(self.lyt_Images_Left, 1, 0)
        self.lytPrincipal.addLayout(self.lyt_Images_Center, 1, 1)
        self.lytPrincipal.addLayout(self.lyt_Images_Right, 1, 2)
        self.container.setLayout(self.lytPrincipal)
        self.setCentralWidget(self.container)


    def divTXT(self): #funcion para el control de el texto
        movie = []
        words = []
        ind = 0
        threading.excepthook = custom
        list = self.inlineText.text()
        for words in list: #ciclo flor para el uso de comas
            words = list.split(",")
        thread_lst = [threading.Thread(target=self.obMovie, args=(k, ind)) for k in words]
        for i in thread_lst:
            i.start()
            ind += 3
            print("Start")
        for i in thread_lst:
            movie.append(i.join())
            print("Return")
        self.resize(750, 800) #defimir el tamaño
        print(self.data_movies)
        self.drMovies(self.data_movies, ind)

    def obMovie(self, palabra, ind):
        url_service_image = "http://clandestina-hds.com:80/movies/title?search="
        datosTotal = requests.get(url_service_image + palabra)
        datosMovie = datosTotal.json() #aqui asignamos un valor a nuestra variable
        data_short = datosMovie['results'][:3]
        for movie in data_short:
            print("Nombre de la pelicula: " + movie['title']) #mostrar el contenido de nuestro filtro
            self.data_movies.append(movie) #asignacion por metodos
            #imprimir el contenido de nuestro ind
        print(ind)

    def drMovies(self, data_movies, ind): #funcion de seguimiento para las peliculas
        ind = 0
        for movie in data_movies:
            url_service_video = "https://clandestina-hds.com/movies/"
            data_video = requests.get(url_service_video + movie['id'])
            data2_video = data_video.json()
            url_video = data2_video['trailer']['linkEmbed']
            image = Poster(movie['image'], url_video)
            txtMovie = QTextEdit("Resumen: " + movie['plot'])
            txtMovie.setReadOnly(1)
            if 0 <= ind < 3:
                self.lyt_Images_Left.addWidget(image)
                self.lyt_Images_Left.addWidget(txtMovie)
            if 3 <= ind < 6:
                self.lyt_Images_Center.addWidget(image)
                self.lyt_Images_Center.addWidget(txtMovie)
            if ind >= 6:
                self.lyt_Images_Right.addWidget(image)
                self.lyt_Images_Right.addWidget(txtMovie)
            ind += 1
        print(ind)
        self.setCentralWidget(self.container)


class Poster(QLabel):
    image_url: str
    video_url: str

    def __init__(self, image_url: str, video_url: str):
        super().__init__()
        self.image_url = image_url
        self.video_url = video_url
        image = QImage()
        image.loadFromData(requests.get(self.image_url).content)
        pixmap = QPixmap(image)
        pixmap = pixmap.scaledToWidth(100)
        self.setPixmap(pixmap)

    def mouseDoubleClickEvent(self):
        if self.video_url is not None and self.video_url is not "":
            url = QUrl(self.video_url)
            QDesktopServices.openUrl(url)


app = QApplication([])
window = windowManager()
window.show()

app.exec_()





