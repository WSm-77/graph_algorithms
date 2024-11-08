# import dimacs
import os
import time

class Test:
    def __init__(self, graphsDir, dimacs_load_function, dimacs_read_solution, graph_convert_function, function_to_test, *args):
        self.graphsDir = graphsDir
        self.dimacs_load_function = dimacs_load_function
        self.dimacs_read_solution = dimacs_read_solution
        self.graph_convert_function = graph_convert_function
        self.function_to_test = function_to_test
        self.args = args

    def test_graph(self, graphName: str):
        pathToFile = os.path.join(self.graphsDir, graphName)
        V, graphEdges = self.dimacs_load_function(pathToFile)
        print(sorted(graphEdges))

        graph = self.graph_convert_function(graphEdges, V)

        print(*graph, sep="\n")

        solution = int(self.dimacs_read_solution(pathToFile))

        print(solution)

        mySolution = self.function_to_test(graph, V, *(self.args))

        print(mySolution)

    def test_function(self):
        passed = 0
        failed = 0
        total = 0

        for fileName in os.listdir(self.graphsDir):
            print(f"\n\n######### {fileName} #########\n\n")

            pathToFile = os.path.join(self.graphsDir, fileName)
            V, graphEdges = self.dimacs_load_function(pathToFile)


            graph = self.graph_convert_function(graphEdges, V)

            # test function
            start = time.time()
            mySolution = self.function_to_test(graph, V, *(self.args))
            stop = time.time()
            timeElapsedBfs = stop - start

            solution = int(self.dimacs_read_solution(pathToFile))

            testStatusMessage = "PASSED"
            if solution == mySolution:
                passed += 1
            else:
                testStatusMessage = "FAILED"
                failed += 1

            print(f"correct solution: {solution}")
            print(f"my solution: {mySolution}")
            print(f"time: {timeElapsedBfs:.3f} [s]")
            print()
            print(f"test status: {testStatusMessage}")

            total += 1

            # break       # remove

        print("\nsummarize:")
        print(f"passed: {passed}/{total}")
        print(f"failed: {failed}/{total}")
