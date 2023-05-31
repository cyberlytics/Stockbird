import csv
import os

#falls manuelle eingabe checken ob name passt
def isReallyCsvForm(Eingab):
    if Eingab[-1] == "v" and Eingab[-2] == "s" and Eingab[-3] == "c" and Eingab[-4] == ".":
        return Eingab
    else:
        print("CSV Format nicht eingehalten, bitte Dateinamen mit .csv enden lassen")

#bei automatischer namengebung -> grundname mit aufsteigender Endzahl
def autoNaming():
    #vordefinierten Pfad eingeben
    directory = 'C:/Users/Jonat/StockBird1/MyFirstCsv.csv'
    counter = 0
    while (True):
        check = os.path.exists(directory)
        if check:
            counter += 1
            if counter > 1:
                directory = directory[::-1]
                directory = directory.replace(str(counter - 1)[::-1], str(counter)[::-1], 1)
                directory = directory[::-1]
            if counter <= 1:
                s_pos = directory.find('.csv')
                directory = directory[:s_pos] + "1" + directory[s_pos:]
            else:
                continue
        else:
            break
    return directory

#abspeichern der dictionary als csv Datei
def print_csv(DatName, Eingab):
    mydict = Eingab
    filename = DatName
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Abk', 'Name'])
        for key, value in mydict.items():
            writer.writerow([key, value])


if __name__ == '__main__':
    print_csv(autoNaming(),{"a": "aachens auflauf galerie", "b": "bertholds buch brochüren", "c": "chammaleon can clim", "d": "durst durch daniel", "e": "emil eignet emma"} )

