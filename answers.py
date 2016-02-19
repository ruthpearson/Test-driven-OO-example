import main as code

#setup
inputFile = 'testinput.txt'
with open(inputFile) as inputGraph:
    graphContent=[line.strip('\n') for line in inputGraph.readlines()]
    
listOfSingleRoutes = [code.SingleRoute(graphContent[i][0],graphContent[i][1],graphContent[i][2]) for i in range(0,len(graphContent))]
numberOfSingleRoutes = len(listOfSingleRoutes)
numberOfTowns=5

KiwilandMap = code.RailMap(numberOfSingleRoutes, numberOfTowns, listOfSingleRoutes)


#Q1-5
Q1 = ['A','B','C']
Q2 = ['A','D']
Q3 = ['A','D','C']
Q4 = ['A','E', 'B','C','D']
Q5 = ['A','E','D']

QuestionOneToFive = [Q1, Q2, Q3, Q4, Q5]

for question in QuestionOneToFive:
    JourneySearch = code.SearchJourney(question, KiwilandMap)
    if JourneySearch.checkIfPossible():
        print  code.Journey(JourneySearch).getTotalDistance()
    else:
        print 'NO SUCH ROUTE'

#Q6
numberOfTrips=0
for stops in [1, 2, 3]:
    numberOfTrips += code.RouteMatrix(KiwilandMap).getNumberOfTripsBetween('C','C',stops)
print numberOfTrips

#Q7
print code.RouteMatrix(KiwilandMap).getNumberOfTripsBetween('A','C',4)

#Q8
DijkstraToUse=code.DijkstraAlgorithm(KiwilandMap)
print DijkstraToUse.runDijkstra('A','C')

#Q9
print code.LoopJourney(KiwilandMap, 'B').getMinimumDistanceOfLoopJourney()

#Q10
JourneyFromC = code.JourneysShorterThan(KiwilandMap)
JourneyFromC.initialiseSearch('C', 30)
print JourneyFromC.runSearch('C')


