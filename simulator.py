from random import uniform, random, expovariate
from pathlib import Path

dateSimulation = 0
timeSimulation = 160
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
averageWaitingTimeRepair = 0
rateUseRepair = 0
billBook = []

#Variables pour l'export
fileName = "SimulatorRepairCenter.txt"
billBookExport = []

class arrivalBus:
    def execute():
        global numberBuses
        billBook.append((arrivalBus, dateSimulation + expovariate(1/2)))
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
        global numberBuses, numberBusesRepaired, areaNumberBusesQueueC, areaNumberBusesQueueR, areaPositionsRepairCentre, numberBusesQueueC, numberBusesQueueR, statusControlCentre, positionsRepairCentre
        numberBuses = 0
        numberBusesRepaired = 0
        areaNumberBusesQueueC = 0
        areaNumberBusesQueueR = 0
        areaPositionsRepairCentre = 0
        numberBusesQueueC = 0
        numberBusesQueueR = 0
        statusControlCentre = False
        positionsRepairCentre = 0
        billBook.append((arrivalBus, dateSimulation + expovariate(1/2)))
        billBook.append((end, timeSimulation))
		
    def __str__(self):
        return "Debut"

class end:
    def execute():
        global averageWaitingTimeControl, averageWaitingTimeRepair, rateUseRepair
        billBook.clear()
        averageWaitingTimeControl = areaNumberBusesQueueC / numberBuses
        averageWaitingTimeRepair = areaNumberBusesQueueR / numberBusesRepaired
        rateUseRepair = areaPositionsRepairCentre / (2 * timeSimulation)
	
    def __str__(self):
        return 'Fin'

def export_result_to_txt():
	global fileName, timeSimulation, numberBuses, numberBusesRepaired, numberBusesQueueC, numberBusesQueueR, averageWaitingTimeControl, averageWaitingTimeRepair, rateUseRepair, billBookExport
	with open(fileName,"a+") as fic :
		fic.write('Durée de la simulation : {}\n'.format(timeSimulation))
		fic.write('Nombre de bus entrées : {}\n'.format(numberBuses))
		fic.write('Nombre de bus réparés : {}\n'.format(numberBusesRepaired))
		fic.write('Nombre de bus file controle : {}\n'.format(numberBusesQueueC))
		fic.write('Nombre de bus file réparation : {}\n'.format(numberBusesQueueR))
		fic.write('Temps moyen attente file controle : {}\n'.format(averageWaitingTimeControl))
		fic.write('Temps moyen attente file réparation : {}\n'.format(averageWaitingTimeRepair))
		fic.write('Taux d\'utilisation du centre de réparation : {}\n'.format(rateUseRepair))
		fic.write('Echéancier de la simulation : {}\n\n'.format(billBookExport))
 

def updating_areas(date1, date2):
    global areaNumberBusesQueueC, areaNumberBusesQueueR, areaPositionsRepairCentre
    areaNumberBusesQueueC += (date2 - date1) * numberBusesQueueC
    areaNumberBusesQueueR += (date2 - date1) * numberBusesQueueR
    areaPositionsRepairCentre += (date2 - date1) * positionsRepairCentre

dateSimulation = 0
billBook.append((start, dateSimulation))
while billBook:
    billBook.sort(key = lambda date: date[1]) 
    eventDate = billBook[0]	
    billBookExport.append(billBook[0])
    del billBook[0]
    updating_areas(dateSimulation, eventDate[1])
    dateSimulation = eventDate[1]
    eventDate[0].execute()
export_result_to_txt()
