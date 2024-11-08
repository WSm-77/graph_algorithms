import os
import time
import signal

# here you can set timeout [s]
TIMEOUT = 120

class TimeoutException(Exception):
    pass

class Test:
    def __init__(self, graphsDir, dimacs_load_function, dimacs_read_solution, graph_convert_function, function_to_test, *args):
        self.graphsDir = graphsDir
        self.dimacs_load_function = dimacs_load_function
        self.dimacs_read_solution = dimacs_read_solution
        self.graph_convert_function = graph_convert_function
        self.function_to_test = function_to_test
        self.args = args

        # testing
        self.passed = 0
        self.failed = 0

    def summarize(self):
        total = self.passed + self.failed
        print("\nsummarize:")
        print(f"passed: {self.passed}/{total}")
        print(f"failed: {self.failed}/{total}")
        self.reset_stats()

    def reset_stats(self):
        self.passed = 0
        self.failed = 0

    def timeout_handler(self, signum, frame):
        raise TimeoutException()

    def get_function_result(self, function_to_test, *args):
            signal.signal(signal.SIGALRM, self.timeout_handler)
            signal.alarm(TIMEOUT)

            mySolution = None
            functionTerminated = False

            try:
                mySolution = function_to_test(*args)
            except TimeoutException:
                print("Function was terminated...")
                functionTerminated = True

            return functionTerminated, mySolution

    def test_graph(self, fileName):
        print(f"\n\n######### {fileName} #########\n\n")

        pathToFile = os.path.join(self.graphsDir, fileName)
        V, graphEdges = self.dimacs_load_function(pathToFile)

        graph = self.graph_convert_function(graphEdges, V)

        start = time.time()
        functionTerminated, mySolution = self.get_function_result(self.function_to_test, graph, V, *(self.args))
        stop = time.time()

        solution = int(self.dimacs_read_solution(pathToFile))
        testPassed = not functionTerminated and solution == mySolution
        timeElapsed = stop - start

        testStatusMessage = "FAILED"
        if testPassed:
            self.passed += 1
            testStatusMessage = "PASSED"
        else:
            self.failed += 1

        print(f"correct solution: {solution}")
        print(f"my solution: {mySolution}")
        print(f"time: {timeElapsed:.3f} [s]")
        print()
        print(f"test status: {testStatusMessage}")

    def test_function(self):
        for fileName in os.listdir(self.graphsDir):
            self.test_graph(fileName)
        self.summarize()
