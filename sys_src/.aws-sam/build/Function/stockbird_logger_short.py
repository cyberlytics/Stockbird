import logging
def make_log():
    #Log bekommt automatisch Namen von Modul
    logger = logging.getLogger(__name__)

    logger.setLevel(logging.DEBUG)

    #Formatieren des Logs mit Uhrzeit, modulname und Nachricht
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

    #Abspeichern der logs in "history.log" Datei
    file_handler = logging.FileHandler('history.log')
    file_handler.setFormatter(formatter)
    #untere Zeile auskommentieren wenn in "history.log" nur Warnings rein
    #file_handler.setLevel(logging.WARNING)

    #Anzeigen der Logs auf Konsole
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    #untere Zeile auskommentieren wenn auf der Konsole nur Warnings angezeigt werden sollen
    #stream_handler.setLevel(logging.WARNING)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

