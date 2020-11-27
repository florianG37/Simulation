from random import uniform, random, expovariate


class arrivalBus:
    def execute():
        global numberBuses
        billBook.append((arrivalBus, dateSimulation + expovariate(1 / 2)))
        numberBuses += 1
        billBook.append((arrivalQueueC, dateSimulation))

    def __str__(self):
        return "Arrivée Bus"


class arrivalQueueC:
    def execute():
        global numberBusesQueueC
        numberBusesQueueC += 1
        if not statusControlCentre:
            billBook.append((accessControl, dateSimulation))

    def __str__(self):
        return "Arrivée File Contrôle"


class accessControl:
    def execute():
        global numberBusesQueueC, statusControlCentre
        numberBusesQueueC -= 1
        statusControlCentre = True
        billBook.append((departureControl, dateSimulation + uniform(1 / 4, 13 / 12)))

    def __str__(self):
        return "Accès Contrôle"


class departureControl:
    def execute():
        global statusControlCentre
        statusControlCentre = False
        if numberBusesQueueC > 0:
            billBook.append((accessControl, dateSimulation))
        if random() < 0.3:
            billBook.append((arrivalQueueR, dateSimulation))

    def __str__(self):
        return "Départ Contrôle"


class arrivalQueueR:
    def execute():
        global numberBusesQueueR, numberBusesRepaired
        numberBusesQueueR += 1
        numberBusesRepaired += 1
        if positionsRepairCentre < 2:
            billBook.append((accessRepair, dateSimulation))

    def __str__(self):
        return "Arrivée File Réparation"


class accessRepair:
    def execute():
        global numberBusesQueueR, positionsRepairCentre
        numberBusesQueueR -= 1
        positionsRepairCentre += 1
        billBook.append((departureRepair, dateSimulation + uniform(2.1, 4.5)))

    def __str__(self):
        return "Accès Réparation"


class departureRepair:
    def execute():
        global positionsRepairCentre
        positionsRepairCentre -= 1
        if numberBusesQueueR > 0:
            billBook.append((accessRepair, dateSimulation))

    def __str__(self):
        return "Depart Réparation"


class start:
    def execute():
        global numberBuses, numberBusesRepaired, areaNumberBusesQueueC, areaNumberBusesQueueR, areaPositionsRepairCentre, numberBusesQueueC, numberBusesQueueR, statusControlCentre, positionsRepairCentre, maximumWaitingTimeControl, maximumWaitingTimeRepair
        numberBuses = 0
        numberBusesRepaired = 0
        areaNumberBusesQueueC = 0
        areaNumberBusesQueueR = 0
        areaPositionsRepairCentre = 0
        numberBusesQueueC = 0
        numberBusesQueueR = 0
        statusControlCentre = False
        positionsRepairCentre = 0
        maximumWaitingTimeControl = 0
        maximumWaitingTimeRepair = 0
        billBook.append((arrivalBus, dateSimulation + expovariate(1 / 2)))
        billBook.append((end, timeSimulation))

    def to_string():
        return "Debut"


class end:
    def execute():
        global averageWaitingTimeControl, averageWaitingTimeRepair, rateUseRepair, averageSizeControlQueue, averageSizeRepairQueue
        billBook.clear()
        try:
            averageWaitingTimeControl = areaNumberBusesQueueC / numberBuses
        except ZeroDivisionError:
            averageWaitingTimeControl = 0
        averageSizeControlQueue = areaNumberBusesQueueC / timeSimulation
        try:
            averageWaitingTimeRepair = areaNumberBusesQueueR / numberBusesRepaired
        except ZeroDivisionError:
            averageWaitingTimeRepair = 0
        averageSizeRepairQueue = areaNumberBusesQueueR / timeSimulation
        rateUseRepair = areaPositionsRepairCentre / (2 * timeSimulation)

    def __str__(self):
        return "Fin"


def updating_areas(date1, date2):
    global areaNumberBusesQueueC, areaNumberBusesQueueR, areaPositionsRepairCentre, maximumWaitingTimeControl, maximumWaitingTimeRepair
    areaNumberBusesQueueC += (date2 - date1) * numberBusesQueueC
    areaNumberBusesQueueR += (date2 - date1) * numberBusesQueueR
    areaPositionsRepairCentre += (date2 - date1) * positionsRepairCentre

    if (date2 - date1) * numberBusesQueueC > maximumWaitingTimeControl:
        maximumWaitingTimeControl = (date2 - date1) * numberBusesQueueC
    if (date2 - date1) * numberBusesQueueR > maximumWaitingTimeRepair:
        maximumWaitingTimeRepair = (date2 - date1) * numberBusesQueueR


def export_result_to_txt():
    global i, fileName, timeSimulation, numberBuses, numberBusesRepaired, numberBusesQueueC, numberBusesQueueR, averageWaitingTimeControl, averageWaitingTimeRepair, rateUseRepair, billBookExport
    with open(fileName, "a+") as fic:
        fic.write('Simulation n° : {}\n'.format(i))
        fic.write('Durée de la simulation : {}\n'.format(timeSimulation))
        fic.write('Nombre de bus entrées : {}\n'.format(numberBuses))
        fic.write('Nombre de bus réparés : {}\n'.format(numberBusesRepaired))
        fic.write('Temps moyen attente file controle : {}\n'.format(averageWaitingTimeControl))
        fic.write('Taille moyenne file controle : {}\n'.format(averageSizeControlQueue))
        fic.write('Temps moyen attente file réparation : {}\n'.format(averageWaitingTimeRepair))
        fic.write('Taille moyenne file réparation : {}\n'.format(averageSizeRepairQueue))
        fic.write('Taux d\'utilisation du centre de réparation : {}\n'.format(rateUseRepair))
        fic.write('Echéancier de la simulation : {}\n\n'.format(billBookExport))


def export_final_result_to_txt():
    global fileName, timeSimulation, repeatSimulation, listNumberBuses, listNumberBusesRepaired, listNumberBusesQueueC, listNumberBusesQueueR, listAverageWaitingTimeControl, listAverageWaitingTimeRepair, listRateUserRepair, listMaximumWaitingTimeControl, listMaximumWaitingTimeRepair
    with open(fileName, "a+") as fic:
        fic.write('Nombre de répétition de la simulation : {}\n'.format(repeatSimulation))
        fic.write('Temps de simulation : {}\n'.format(timeSimulation))

        fic.write('Nombre de bus entrées pour chaque simulation : {}\n'.format(listNumberBuses))
        fic.write('Nombre de bus réparés pour chaque simulation : {}\n'.format(listNumberBusesRepaired))
        fic.write(
            'Temps moyen attente file controle pour chaque simulation : {}\n'.format(listAverageWaitingTimeControl))
        fic.write('Taille moyenne file controle pour chaque simulation : {}\n'.format(listAverageSizeControlQueue))
        fic.write(
            'Temps moyen attente file réparation pour chaque simulation : {}\n'.format(listAverageWaitingTimeRepair))
        fic.write('Taille moyenne file réparation pour chaque simulation : {}\n'.format(listAverageSizeRepairQueue))
        fic.write(
            'Taux d\'utilisation du centre de réparation pour chaque simulation : {}\n\n'.format(listRateUserRepair))

        fic.write('Moyenne du nombre de bus entrées : {} \n'.format(sum(listNumberBuses) / len(listNumberBuses)))
        fic.write('Moyenne du nombre de bus réparés : {} \n'.format(
            sum(listNumberBusesRepaired) / len(listNumberBusesRepaired)))
        fic.write('Moyenne du temps moyen attente file controle : {} \n'.format(
            sum(listAverageWaitingTimeControl) / len(listAverageWaitingTimeControl)))
        fic.write('Moyenne de la taille moyenne file controle : {}\n'.format(
            sum(listAverageSizeControlQueue) / len(listAverageSizeControlQueue)))
        fic.write('Moyenne du temps moyen attente file réparation : {} \n'.format(
            sum(listAverageWaitingTimeRepair) / len(listAverageWaitingTimeRepair)))
        fic.write('Moyenne de la taille moyenne file réparation : {}\n'.format(
            sum(listAverageSizeRepairQueue) / len(listAverageSizeRepairQueue)))
        fic.write('Moyenne du taux d\'utilisation du centre de réparation : {}\n'.format(
            sum(listRateUserRepair) / len(listRateUserRepair)))
        fic.write('Moyenne du temps maximum attente file contrôle : {}\n'.format(
            sum(listMaximumWaitingTimeControl) / len(listMaximumWaitingTimeControl)))
        fic.write('Moyenne du temps maximum attente file réparation : {}\n\n'.format(
            sum(listMaximumWaitingTimeRepair) / len(listMaximumWaitingTimeRepair)))


def add_result_to_lists():
    global numberBuses, numberBusesRepaired, numberBusesQueueC, numberBusesQueueR, averageWaitingTimeControl, averageWaitingTimeRepair, rateUseRepair, maximumWaitingTimeControl, maximumWaitingTimeRepair, listNumberBuses, listNumberBusesRepaired, listNumberBusesQueueC, listNumberBusesQueueR, listAverageWaitingTimeControl, listAverageWaitingTimeRepair, listRateUserRepair, listMaximumWaitingTimeControl, listMaximumWaitingTimeRepair
    listNumberBuses.append(numberBuses)
    listNumberBusesRepaired.append(numberBusesRepaired)
    listNumberBusesQueueC.append(numberBusesQueueC)
    listNumberBusesQueueR.append(numberBusesQueueR)
    listAverageWaitingTimeControl.append(averageWaitingTimeControl)
    listAverageSizeControlQueue.append(averageSizeControlQueue)
    listAverageWaitingTimeRepair.append(averageWaitingTimeRepair)
    listAverageSizeRepairQueue.append(averageSizeRepairQueue)
    listRateUserRepair.append(rateUseRepair)
    listMaximumWaitingTimeControl.append(maximumWaitingTimeControl)
    listMaximumWaitingTimeRepair.append(maximumWaitingTimeRepair)


# Paramètres de la simulation
repeatSimulation = 500
timeSimulation = 40

# initialisation des variables de la simulation
dateSimulation = 0
numberBuses = 0
numberBusesRepaired = 0
areaNumberBusesQueueC = 0
areaNumberBusesQueueR = 0
areaPositionsRepairCentre = 0
numberBusesQueueC = 0
numberBusesQueueR = 0
statusControlCentre = False
positionsRepairCentre = 0
averageWaitingTimeControl = 0
averageSizeRepairQueue = 0
averageWaitingTimeRepair = 0
averageSizeRepairQueue = 0
rateUseRepair = 0
maximumWaitingTimeControl = 0
maximumWaitingTimeRepair = 0
billBook = []

listNumberBuses = []
listNumberBusesRepaired = []
listNumberBusesQueueC = []
listNumberBusesQueueR = []
listAverageWaitingTimeControl = []
listAverageSizeControlQueue = []
listAverageWaitingTimeRepair = []
listAverageSizeRepairQueue = []
listRateUserRepair = []
listMaximumWaitingTimeControl = []
listMaximumWaitingTimeRepair = []

# Variables pour l'export
fileName = "SimulatorRepairCenter.txt"
billBookExport = []

for i in range(0, repeatSimulation):
    dateSimulation = 0
    billBook.append((start, dateSimulation))
    while billBook:
        billBook.sort(key=lambda date: date[1])
        eventDate = billBook[0]
        billBookExport.append(billBook[0])
        del billBook[0]
        updating_areas(dateSimulation, eventDate[1])
        dateSimulation = eventDate[1]
        eventDate[0].execute()
    # export_result_to_txt()
    add_result_to_lists()
    print("Simulation n°{}".format(i))
export_final_result_to_txt()
