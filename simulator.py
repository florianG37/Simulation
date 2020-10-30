from random import uniform, random, expovariate

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
billBook = []


class arrivalBus:
    def execute():
        global numberBuses
        billBook.append((arrivalBus, dateSimulation + expovariate(1/2)))
        numberBuses += 1
        billBook.append((arrivalQueueC, dateSimulation))


class arrivalQueueC:
    def execute():
        global numberBusesQueueC
        numberBusesQueueC += 1
        if not statusControlCentre:
            billBook.append((accessControl, dateSimulation))


class accessControl:
    def execute():
        global numberBusesQueueC, statusControlCentre
        numberBusesQueueC -= 1
        statusControlCentre = True
        billBook.append((departureControl, dateSimulation + uniform(1 / 4, 13 / 12)))


class departureControl:
    def execute():
        global statusControlCentre
        statusControlCentre = False
        if numberBusesQueueC > 0:
            billBook.append((accessControl, dateSimulation))
        if random() < 0.3:
            billBook.append((arrivalQueueR, dateSimulation))


class arrivalQueueR:
    def execute():
        global numberBusesQueueR, numberBusesRepaired
        numberBusesQueueR += 1
        numberBusesRepaired += 1
        if positionsRepairCentre < 2:
            billBook.append((accessRepair, dateSimulation))


class accessRepair:
    def execute():
        global numberBusesQueueR, positionsRepairCentre
        numberBusesQueueR -= 1
        positionsRepairCentre += 1
        billBook.append((departureRepair, dateSimulation + uniform(2.1, 4.5)))


class departureRepair:
    def execute():
        global positionsRepairCentre
        positionsRepairCentre -= 1
        if numberBusesQueueR > 0:
            billBook.append((accessRepair, dateSimulation))


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
        billBook.append((end, 160))


class end:
    def execute():
        billBook.clear()
        averageWaitingTimeControl = areaNumberBusesQueueC / numberBuses
        averageWaitingTimeRepair = areaNumberBusesQueueR / numberBusesRepaired
        rateUseRepair = areaPositionsRepairCentre / (2 * 160)


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
    del billBook[0]
    updating_areas(dateSimulation, eventDate[1])
    dateSimulation = eventDate[1]
    eventDate[0].execute()
