
class SingleRoute:
   def __init__(self, start, end, distance):
      self.start = start
      self.end = end
      self.distance = distance


class RailMap:
    def __init__(self, numberOfSingleRoutes, numberOfTowns, listOfSingleRoutes):
        self.numberOfSingleRoutes = numberOfSingleRoutes
        self.numberOfTowns = numberOfTowns
        self.listOfSingleRoutes = listOfSingleRoutes


class SearchJourney:
    def __init__(self, listOfStops, FullRailMap):
        self.listOfStops = listOfStops
        self.FullRailMap = FullRailMap
        self.numberOfStops = len(listOfStops)
        
    def checkIfPossible(self):
        isItPossible = True
        numberOfSubroutes = self.numberOfStops-1
        for subrouteIndex in range(0,numberOfSubroutes):
            if not self.checkSubRouteExists(self.listOfStops[subrouteIndex], self.listOfStops[subrouteIndex+1]):
                isItPossible = False
                
        return isItPossible

    def checkSubRouteExists(self, start, end):
        doesSubRouteExist = False
        for SingleRoute in self.FullRailMap.listOfSingleRoutes:
            if SingleRoute.start in start and SingleRoute.end in end:
                doesSubRouteExist = True

        return doesSubRouteExist

    
class Journey:
    def __init__(self, AllowedJourney):
        self.AllowedJourney = AllowedJourney
        self.numberOfSubroutes = AllowedJourney.numberOfStops-1

    def getTotalDistance(self):
        totalDistance = 0
        for stopIndex in range(0, self.numberOfSubroutes):
            totalDistance += self.getSubrouteDistance(self.AllowedJourney.listOfStops[stopIndex], self.AllowedJourney.listOfStops[stopIndex+1])
            
        return totalDistance

    def getSubrouteDistance(self, start, end):
        distance = 0
        for SingleRoute in self.AllowedJourney.FullRailMap.listOfSingleRoutes:
            if SingleRoute.start in start and SingleRoute.end in end:
                distance += int(SingleRoute.distance)
        return distance         


class RouteMatrix:
    def __init__(self, FullRailMap):
        self.FullRailMap = FullRailMap
        self.mapInMatrixForm = self.initialiseSquareMatrixOfZeros(self.FullRailMap.numberOfTowns) 
        self.townLetterToIndexConversion = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}

        for SingleRoute in FullRailMap.listOfSingleRoutes:
            i = self.townLetterToIndexConversion[SingleRoute.start]
            j = self.townLetterToIndexConversion[SingleRoute.end]
            self.mapInMatrixForm[i][j] = 1

    def getNumberOfTripsBetween(self,startPoint,endPoint,inThisManyStops):
        matrixTool = self.matrixToThePowerOf(self.mapInMatrixForm, inThisManyStops)
        NumberOfTrips = matrixTool[ self.townLetterToIndexConversion[startPoint] ] [ self.townLetterToIndexConversion[endPoint] ]
        return NumberOfTrips

    def matrixToThePowerOf(self, matrix, power):
        dimension = len(matrix)
        finalMatrix = matrix
        secondMatrix = matrix
        for n in range(1,power):
            finalMatrix = self.multiplyTwoSquareMatrices(matrix,secondMatrix)
            secondMatrix = finalMatrix

        return finalMatrix
        
    def multiplyTwoSquareMatrices(self, firstMatrix, secondMatrix):
        dimension = len(firstMatrix)
        finalMatrix = self.initialiseSquareMatrixOfZeros(dimension)
        for i in range(0,dimension):
            for j in range(0,dimension):
                for k in range(0,dimension):
                    finalMatrix[i][j] += firstMatrix[i][k]*secondMatrix[k][j]
            
        return finalMatrix

    def initialiseSquareMatrixOfZeros(self,dimension):
        zeroVector = [0 for x in xrange(dimension)]
        initialisedMatrix = [zeroVector[:] for x in xrange(dimension)]
        return initialisedMatrix


class DijkstraAlgorithm:
    def __init__(self, FullRailMap,):
        self.FullRailMap = FullRailMap
        self.townLetterToIndexConversion = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
        self.effectivelyInfinity = 1e12
        self.distance = [self.effectivelyInfinity for x in xrange(self.FullRailMap.numberOfTowns)] 
        self.unvisited = [True for x in xrange(self.FullRailMap.numberOfTowns)]
    
    def runDijkstra(self, start, end):
        self.distance[self.townLetterToIndexConversion[start]] = 0
        currentNode = start
        while True:
           self.visitUnvisitedNeighbours(currentNode)
           self.markAsVisited(currentNode)

           if self.isAlgorithmFinished(end):
               break
           else:
               currentNode = self.moveToNextNode()
               
        return self.distance[self.townLetterToIndexConversion[end]]

    def visitUnvisitedNeighbours(self, node):
        for route in self.FullRailMap.listOfSingleRoutes:
                if node in route.start and self.unvisited[self.townLetterToIndexConversion[route.end]]:
                    self.updateDistance(node, route.end, route.distance)
                    
    def updateDistance(self, node, endNode, distanceToAdd):
        if self.distance[self.townLetterToIndexConversion[endNode]] > self.distance[self.townLetterToIndexConversion[node]] + int(distanceToAdd):
             self.distance[self.townLetterToIndexConversion[endNode]] =  self.distance[self.townLetterToIndexConversion[node]] + int(distanceToAdd)

    def markAsVisited(self, node):
        self.unvisited[self.townLetterToIndexConversion[node]] = False

    def isAlgorithmFinished(self,end):
        return not self.unvisited[self.townLetterToIndexConversion[end]]
           
    def moveToNextNode(self):
        indexOfNextNode = self.findShortestDistance()
        return self.resetCurrentNode(indexOfNextNode)
    
    def findShortestDistance(self):
        minimiseThis = self.effectivelyInfinity
        indexOfNextNode=0
        for town in range(0, self.FullRailMap.numberOfTowns):
            if self.distance[town] < minimiseThis and self.unvisited[town]:
                minimiseThis = self.distance[town]
                indexOfNextNode=town
                
        return indexOfNextNode        

    def resetCurrentNode(self,nodeIndex):
        townIndexToLetterConversion = invert_dictionary(self.townLetterToIndexConversion)
        nextNode=townIndexToLetterConversion[nodeIndex]
        return nextNode


class LoopJourney:
    def __init__(self, FullRailMap, loopTown):
        self.FullRailMap = FullRailMap
        self.loopTown = loopTown
        self.townLetterToIndexConversion = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}

    def getMinimumDistanceOfLoopJourney(self):
        routesEndingAtDesiredLocation = self.getRoutesEndingHere(self.loopTown)
        if not routesEndingAtDesiredLocation:
            return 'NO SUCH ROUTE'
        else:
            possibleJourneyTotalDistances = self.getPossibleJourneyTotalDistances(routesEndingAtDesiredLocation)
            return self.findJourneyWithMinimumDistance(possibleJourneyTotalDistances)

    def getRoutesEndingHere(self, town):
        routesEndingHere = []
        for Route in self.FullRailMap.listOfSingleRoutes:
            if town in Route.end:
                routesEndingHere.extend([Route])
                
        return  routesEndingHere        
        
    def getPossibleJourneyTotalDistances(self, routesEndingAtDesiredLocation):
        totalDistances = []
        for Route in routesEndingAtDesiredLocation:
            dijkstraDistance = DijkstraAlgorithm(self.FullRailMap).runDijkstra(self.loopTown,Route.start)
            totalDistances.extend([dijkstraDistance + int(Route.distance)])
            
        return totalDistances

    def findJourneyWithMinimumDistance(self, possibleJourneyTotalDistances):
        minimiseThis = possibleJourneyTotalDistances[0]
        for distance in possibleJourneyTotalDistances:
            if distance < minimiseThis:
                minimiseThis = distance
                     
        return minimiseThis


class JourneysShorterThan:
    def __init__(self, FullRailMap):
        self.FullRailMap = FullRailMap
        self.queue = []
        self.distance = []
        self.continueBranch = []
        self.maxDistance = 0

    def initialiseSearch(self, start, maxDistance):
        self.queue.append(start)
        self.distance.append(0)
        self.continueBranch.append(True)
        self.maxDistance = maxDistance
        currentNode = start

        self.findRoutesFromHere(currentNode,0)

    def runSearch(self, end):
        index=0
        while True:
            if self.isSearchFinished(index):
                break
            index += 1
            currentNode = self.queue[index]
            if self.continueBranch[index]:
                self.findRoutesFromHere(currentNode, index)
        return self.countPossibleRoutes(end)

    def isSearchFinished(self,index):
        return index > len(self.queue) - 2
          
    def findRoutesFromHere(self, currentNode, index):
        for singleRoute in self.FullRailMap.listOfSingleRoutes: 
            if currentNode in singleRoute.start:
                self.updateLists(singleRoute, index)

    def updateLists(self, singleRoute, index):               
        self.queue.append(singleRoute.end)
        newTotalDistance = int(singleRoute.distance) + self.distance[index]
        self.distance.append(newTotalDistance)
        if newTotalDistance < self.maxDistance:
            self.continueBranch.append(True)
        else:
            self.continueBranch.append(False)

    def countPossibleRoutes(self, end):
        count=0
        for index in range(0, len(self.queue)):
            if end in self.queue[index] and  0 < self.distance[index] < self.maxDistance:
                count += 1
               
        return count



def invert_dictionary(dictionary):
    return dict([ (v, k) for k, v in dictionary.iteritems( ) ])

