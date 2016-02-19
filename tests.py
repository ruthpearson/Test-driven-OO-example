import main as code
import unittest


def setUpForAllTestClasses(self):
        inputFile = 'testinput.txt'
        with open(inputFile) as inputGraph:
            graphContent=[line.strip('\n') for line in inputGraph.readlines()]
      
        listOfSingleRoutes = [code.SingleRoute(graphContent[i][0],graphContent[i][1],graphContent[i][2]) for i in range(0,len(graphContent))]
        numberOfSingleRoutes = len(listOfSingleRoutes)
        numberOfTowns=5
        self.KiwilandMap = code.RailMap(numberOfSingleRoutes, numberOfTowns, listOfSingleRoutes)


class TestsForSingleRouteAndRailMapClasses(unittest.TestCase):
    def setUp(self):
        setUpForAllTestClasses(self)

    def test_SingleRoute_returns_correctInstance(self):
	self.assertIsInstance(self.KiwilandMap.listOfSingleRoutes[0],code.SingleRoute)

    def test_RailMap_returns_correctInstance(self):
	self.assertIsInstance(self.KiwilandMap,code.RailMap) 


class TestsForSearchJourneyAndJourneyClasses(unittest.TestCase):
    def setUp(self):
        setUpForAllTestClasses(self)
	self.PossibleJourneySearch = code.SearchJourney(['A','B','C'], self.KiwilandMap)
	self.JourneyToTest = code.Journey(self.PossibleJourneySearch)

    def test_SearchJourney__init__returns_3(self):
	self.assertEqual(code.SearchJourney(['A','B','C'], self.KiwilandMap).numberOfStops, 3)	

    def test_checkSubRouteExists_returns_True(self):
        self.assertTrue(self.PossibleJourneySearch.checkSubRouteExists('B', 'C') )

    def test_checkSubRouteExists_returns_False(self):
        self.assertFalse(self.PossibleJourneySearch.checkSubRouteExists('C', 'A') )

    def test_checkIfPossible_returns_True(self):
        self.assertTrue(self.PossibleJourneySearch.checkIfPossible())

    def test_checkIfPossible_returns_False(self):
        ImpossibleJourneySearch =  code.SearchJourney(['A','C','B'], self.KiwilandMap)
        self.assertFalse(ImpossibleJourneySearch.checkIfPossible())

    def test_Journey__init__returns_2(self):
	self.assertEqual(self.JourneyToTest.numberOfSubroutes, 2)    

    def test_getSubrouteDistance_returns_8(self):
        self.assertEqual(self.JourneyToTest.getSubrouteDistance('D','C'),8)

    def test_getTotalDistance_returns_9(self):
        self.assertEqual(self.JourneyToTest.getTotalDistance(),9)

    def test_getTotalDistance_returns_21(self):
        JourneyToTest = code.Journey(code.SearchJourney(['E','B','C','D','E'], self.KiwilandMap))
        self.assertEqual(JourneyToTest.getTotalDistance(),21)

   
class TestsForRouteMatrixClass(unittest.TestCase):
    def setUp(self):
        setUpForAllTestClasses(self)

    def test_RouteMatrix__init__returns_1(self):
        self.assertEqual(code.RouteMatrix(self.KiwilandMap).mapInMatrixForm[0][1], 1)
	
    def test_initialiseSquareMatrixOfZeros_returns_0(self):
	zeroMatrix = code.RouteMatrix(self.KiwilandMap).initialiseSquareMatrixOfZeros(8)    
	self.assertEqual(zeroMatrix[7][7],0)
	
    def test_multiplyTwoSquareMatrices_returns_3(self):
        matrixOne = [ [1, 2], [3, 4] ]
        matrixTwo = [ [1, 1], [1, 1] ]
        product = code.RouteMatrix(self.KiwilandMap).multiplyTwoSquareMatrices(matrixOne,matrixTwo)
        self.assertEqual(product[0][0], 3)

    def test_matrixToThePowerOf_returns_4(self):
        matrix = [ [1, 1], [1, 1] ]
        matrixCubed = code.RouteMatrix(self.KiwilandMap).matrixToThePowerOf(matrix, 3)
        self.assertEqual(matrixCubed[0][0],4)

    def test_getNumberOfTripsBetween_returns_3(self):
        self.assertEqual( code.RouteMatrix(self.KiwilandMap).getNumberOfTripsBetween('A','C',4), 3)

class TestsForDijkstraAlgorithmClass(unittest.TestCase):
    def setUp(self):
        setUpForAllTestClasses(self)

    def test_DijkstraAlgorithm__init__returns_True(self):
	self.assertTrue(code.DijkstraAlgorithm(self.KiwilandMap).unvisited[4])

    def test_visitUnvisitedNeighbours_returns_5(self):
        DijkstraToTest = code.DijkstraAlgorithm(self.KiwilandMap)
	DijkstraToTest.distance[0] = 0
        DijkstraToTest.visitUnvisitedNeighbours('A')
        self.assertEqual(DijkstraToTest.distance[1], 5)

    def test_updateDistance_returns_7(self):
        DijkstraToTest = code.DijkstraAlgorithm(self.KiwilandMap)
	DijkstraToTest.distance[0] = 0
	DijkstraToTest.updateDistance('A', 'E', 7)
	self.assertEqual(DijkstraToTest.distance[4], 7)

    def test_markAsVisited_returns_True(self):
        DijkstraToTest = code.DijkstraAlgorithm(self.KiwilandMap)
	DijkstraToTest.markAsVisited('C')
	self.assertFalse(DijkstraToTest.unvisited[2])

    def test_isAlgorithmFinished_returns_False(self):
        self.assertFalse(code.DijkstraAlgorithm(self.KiwilandMap).isAlgorithmFinished('C'))

    def test_isAlgorithmFinished_returns_True(self):
        DijkstraToTest=code.DijkstraAlgorithm(self.KiwilandMap)
	DijkstraToTest.unvisited[1] = False
        self.assertTrue(DijkstraToTest.isAlgorithmFinished('B'))

    def test_findShortestDistance_returns_4(self):    
        DijkstraToTest = code.DijkstraAlgorithm(self.KiwilandMap)
        DijkstraToTest.distance[2] = 4
        self.assertEqual(DijkstraToTest.findShortestDistance(), 2)

    def test_resetCurrentNode_returns_C(self):
        self.assertEqual(code.DijkstraAlgorithm(self.KiwilandMap).resetCurrentNode(2), 'C')

    def test_moveToNextNode_returns_C(self):
        DijkstraToTest = code.DijkstraAlgorithm(self.KiwilandMap)
        DijkstraToTest.distance[2]=4
        self.assertEqual(DijkstraToTest.moveToNextNode(), 'C')

    def test_runDijkstra_returns_5(self):
        self.assertEqual(code.DijkstraAlgorithm(self.KiwilandMap).runDijkstra('A','B'), 5)

    def test_runDijkstra_returns_9(self):
        DijkstraToTest = code.DijkstraAlgorithm(self.KiwilandMap)
        self.assertEqual(DijkstraToTest.runDijkstra('D','B'), 9)


class TestsForLoopJourneyClass(unittest.TestCase):
    def setUp(self):
        setUpForAllTestClasses(self)

    def test_getRoutesEndingHere_returns_2(self):
        routesEndingAtC = code.LoopJourney(self.KiwilandMap, 'C').getRoutesEndingHere('C')
        self.assertEqual(len(routesEndingAtC), 2)

    def test_getPossibleJourneyTotalDistances_returns_9(self):
        routeBtoC = self.KiwilandMap.listOfSingleRoutes[1]
	routeDtoC = self.KiwilandMap.listOfSingleRoutes[3]
        TotalDistances = code.LoopJourney(self.KiwilandMap, 'C').getPossibleJourneyTotalDistances([routeBtoC,routeDtoC])
        self.assertEqual(TotalDistances[0],9)

    def test_findJourneyWithMinimumDistance_returns_2(self):
        minimumDistance = code.LoopJourney(self.KiwilandMap, 'C').findJourneyWithMinimumDistance([2, 6, 8])
        self.assertEqual(minimumDistance, 2)

    def test_getMinimumDistanceOfLoopJourney_returns_16(self):
        self.assertEqual(code.LoopJourney(self.KiwilandMap, 'D').getMinimumDistanceOfLoopJourney(), 16)
        
    def test_getMinimumDistanceOfLoopJourney_returns_NOSUCHROUTE(self):
        self.assertEqual(code.LoopJourney(self.KiwilandMap, 'A').getMinimumDistanceOfLoopJourney(), 'NO SUCH ROUTE')

class TestsForJourneyShorterThanClass(unittest.TestCase):
    def setUp(self):
        setUpForAllTestClasses(self)

    def test_JourneysShorterThan__init__returns_0(self):
	self.assertEqual(code.JourneysShorterThan(self.KiwilandMap).maxDistance, 0)

    def test_initialiseSearch_returns_5(self):
        JourneyFromA = code.JourneysShorterThan(self.KiwilandMap)
        JourneyFromA.initialiseSearch('A', 10)
        self.assertEqual(JourneyFromA.distance[1], 5)

    def test_isSearchFinished_returns_True(self):
        JourneyFromA = code.JourneysShorterThan(self.KiwilandMap)
        JourneyFromA.queue=['A','B','D','E']
        self.assertTrue(JourneyFromA.isSearchFinished(3))

    def test_isSearchFinished_returns_False(self):
        JourneyFromA = code.JourneysShorterThan(self.KiwilandMap)
        JourneyFromA.queue=['A','B','D','E']
        self.assertFalse(JourneyFromA.isSearchFinished(2))

    def test_updateLists_returns_9(self):
        JourneyFromA = code.JourneysShorterThan(self.KiwilandMap)
        JourneyFromA.initialiseSearch('A', 10)
        JourneyFromA.updateLists(JourneyFromA.FullRailMap.listOfSingleRoutes[1], 1)
        self.assertEqual(JourneyFromA.distance[4], 9)

    def test_findRoutesFromHere_returns_C(self):
        JourneyFromE = code.JourneysShorterThan(self.KiwilandMap)
        JourneyFromE.initialiseSearch('E', 10)
        JourneyFromE.findRoutesFromHere('B', 1)
        self.assertEqual(JourneyFromE.queue[2],'C')

    def test_runSearch_returns_C(self):
        JourneyFromA = code.JourneysShorterThan(self.KiwilandMap)
        JourneyFromA.initialiseSearch('A', 20)
        JourneyFromA.runSearch('C')
        self.assertEqual(JourneyFromA.queue[4],'C')

    def test_runSearch_returns_1(self):
        JourneyFromE = code.JourneysShorterThan(self.KiwilandMap)
        JourneyFromE.initialiseSearch('E', 10)
        self.assertEqual(JourneyFromE.runSearch('C'),1)     

    def test_countPossibleRoutes_returns_1(self):
        JourneyFromA = code.JourneysShorterThan(self.KiwilandMap)
        JourneyFromA.initialiseSearch('A', 10)
        self.assertEqual(JourneyFromA.countPossibleRoutes('B'),1)


if __name__ == '__main__':
    unittest.main()


