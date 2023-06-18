import csv
import os
import sys
import sys_src.backend.src.stockbird_logger as stockbird_logger

logger = stockbird_logger.get_logger(LOGGER_NAME)

#falls manuelle eingabe checken ob name passt
def isReallyCsvForm(eingab):
    if eingab[-1] == "v" and eingab[-2] == "s" and eingab[-3] == "c" and eingab[-4] == ".":
        logger.info('name is ok')
        return eingab
    else:
        logger.info(f'"{eingab}" is not csv format, please end filename with .csv')
        pass

#bei automatischer namengebung -> grundname mit aufsteigender Endzahl
def autoNaming():
    #vordefinierten Pfad eingeben
    directory = 'C:/Users/Jonat/StockBird1/MyFirstCsv.csv'
    counter = 0
    while (True):
        check = os.path.exists(directory)
        if check:
            logger.info(f'"{directory}" is already used')
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
    logger.info(f'"{directory}" is the path to the domkument')
    return directory

#abspeichern der dictionary als csv Datei
def print_csv(datName, eingab):
    mydict = eingab
    filename = DatName
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Abk', 'Name'])
        for key, value in mydict.items():
            writer.writerow([key, value])
    logger.info(f'csv file created with name "{datName}"')


