import yfinance

def getSymb():
    Symbols = {}
    list1 = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
     "V", "W", "X", "Y", "Z"]
    list2 = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
             "V", "W", "X", "Y", "Z"]
    list3 = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
             "V", "W", "X", "Y", "Z"]
    list4 = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
             "V", "W", "X", "Y", "Z"]

    for a in list1:
        s_try = a

        try:
            finTest = yfinance.Ticker(s_try)
            Symbols[a] = finTest.info['longName']
            print(finTest.info['longName'])
        except Exception as e:
            print(s_try, "is not a combination", str(e))
        for b in list2:
            s_try = a + b
           # s_try += b
            try:
                finTest = yfinance.Ticker(s_try)
                Symbols[s_try] = finTest.info['longName']
                print(finTest.info['longName'])
            except Exception as e:
                print(s_try, "is not a combination", str(e))
            for c in list3:
                s_try = a + b +c
                try:
                    finTest = yfinance.Ticker(s_try)
                    Symbols[s_try] = finTest.info['longName']
                    print(finTest.info['longName'])
                except Exception as e:
                    print(s_try, "is not a combination", str(e))

                for d in list4:
                    s_try = a + b + c +
                    try:
                        finTest = yfinance.Ticker(s_try)
                        Symbols[s_try] = finTest.info['longName']
                        print(finTest.info['longName'])
                    except Exception as e:
                        print(s_try, "is not a combination", str(e))
    return Symbols


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




if __name__ == '__main__':
    print_csv(autoNaming(),getSymb())

