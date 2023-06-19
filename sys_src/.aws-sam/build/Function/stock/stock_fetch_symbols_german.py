import yfinance
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
    directory = 'C:/Users/Jonat/StockBird1/MySecondCsv.csv'
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

#zugriff auf csv file (wenn, erst später vonnöten)
def getCsvContent(file)   :
    with open(file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            print(', '.join(row))



#extrahieren der Ticker aus csv file in Liste
def getAbk(csv_file):
    Abk = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for i in reader:
            if i:
                Abk.append(i[0])
    return Abk

#hinzufügen der deutschen Marktendungen
def addGermEnd(listeAlt):
    liste = [] # leere Liste für die Ausgabe
    #erstes Attribut listeAlt ist "Abk" daher ersetzt
    DE = listeAlt.copy()
    DE[0] = "Deutsche Boerse XETRA"
    BM = listeAlt.copy()
    BM[0] = "Bremen Stock Exchange"
    BE = listeAlt.copy()
    BE[0] = "Berlin Stock Exchange"
    DU = listeAlt.copy()
    DU[0] = "Dusseldorf Stock Exchange"
    F = listeAlt.copy()
    F[0] = "Frankfurt Stock Exchange"
    HM = listeAlt.copy()
    HM[0] = "Hamburg Stock Exchange"
    HA = listeAlt.copy()
    HA[0] = "Hanover Stock Exchange"
    MU = listeAlt.copy()
    MU[0] = "Munic Stock Exchange"
    SG = listeAlt.copy()
    SG[0] = "Stuttgard Stock Exchange"
    DE = listeAlt.copy()
    DE[0] = "Deutsche Boerse XETRA"

    x = 1
    while x < len(listeAlt):
        DE[x] += ".DE"
        BM[x] += ".BM"
        BE[x] += ".BE"
        DU[x] += ".DU"
        F[x] += ".F"
        HM[x] += ".HM"
        HA[x] += ".HA"
        MU[x] += ".MU"
        SG[x] += ".SG"
        x += 1

    liste.extend(DE)
    liste.extend(BM)
    liste.extend(BE)
    liste.extend(DU)
    liste.extend(F)
    liste.extend(HM)
    liste.extend(HA)
    liste.extend(MU)
    liste.extend(SG)
    return liste


#Umwandeln der Abluerzungsliste in dictionary mit longname
def intoDict(Liste):
    SymbolsDE = {}
    counter = 0
    for a in Liste:
        try:
            finTest = yfinance.Ticker(Liste[counter])
            SymbolsDE[Liste[counter]] = finTest.info['longName']
            print(finTest.info['longName'])
            counter += 1
        except Exception as e:
            print(Liste[counter], "is not a combination", str(e))
            counter +=1

    return SymbolsDE

if __name__ == '__main__':
    print_csv(autoNaming(), intoDict(addGermEnd(getAbk('C:/Users/Jonat/StockBird1/MySecondCsv.csv'))))
