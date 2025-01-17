import networkx as nx
from networkx.algorithms.components import strongly_connected_components
from networkx.algorithms.dag import topological_sort
import dimacs
from utils.test import Test

def print_evaluation(evaluation: dict):
    for key, val in sorted(evaluation.items()):
        if key < 0:
            continue

        print(f"x_{key} = {val}")

def build_graph(graphEdges: list[tuple[int, int]]) -> nx.DiGraph:
    nxGraph = nx.DiGraph()

    for vertex, neighbour in graphEdges:
        nxGraph.add_edge(-vertex, neighbour)
        nxGraph.add_edge(-neighbour, vertex)

    return nxGraph

def build_satisfiable_evaluation(nxGraph: nx.DiGraph):
    componentsGraph = nx.DiGraph()

    stronglyConnectedComponents = strongly_connected_components(nxGraph)

    vertexToComponentMap = get_vertex_to_component_map(stronglyConnectedComponents)

    for vertex, neighbour in nxGraph.edges:
        vertexComponent = vertexToComponentMap[vertex]
        neighbourComponent = vertexToComponentMap[neighbour]
        if vertexComponent != neighbourComponent:
            componentsGraph.add_edge(vertexComponent, neighbourComponent)
        else:
            componentsGraph.add_node(vertexComponent)
            componentsGraph.add_node(neighbourComponent)

    componentsGraphSorted = topological_sort(componentsGraph)

    evaluationMap = {}

    for component in componentsGraphSorted:
        for variable in component:
            if variable not in evaluationMap:
                evaluationMap[variable] = False
                evaluationMap[-variable] = True

    return evaluationMap

def get_vertex_to_component_map(stronglyConnectedComponents):
    vertexToComponentMap = {}

    for component in stronglyConnectedComponents:
        componentSet = frozenset(component)

        for vertex in component:
            vertexToComponentMap[vertex] = componentSet

    return vertexToComponentMap

def is_satisfiable(graphEdges: list[tuple[int, int]], V: int):
    nxGraph = build_graph(graphEdges)

    stronglyConnectedComponents = strongly_connected_components(nxGraph)

    for component in stronglyConnectedComponents:
        for variable in component:
            if -variable in component:
                return False

    return True

def verify_evaluation(formulaGraph, evaluationMap: dict[int, bool]):
    for variable1, variable2 in formulaGraph:
        if not (evaluationMap[variable1] or evaluationMap[variable2]):
            return False

    return True

def is_evaluation_valid(graphEdges, V):
    if not is_satisfiable(graphEdges, V):
        return False

    nxGraph = build_graph(graphEdges)
    evaluation = build_satisfiable_evaluation(nxGraph)

    if not verify_evaluation(graphEdges, evaluation):
        raise Exception("invalid evaluation!!!")

    print_evaluation(evaluation)

    return True

if __name__ == "__main__":
    graphsDir = "sat"
    graph_convert_function = lambda x, y: x
    myTest = Test(graphsDir, dimacs.loadCNFFormula, dimacs.readSolution, graph_convert_function, is_evaluation_valid)
    myTest.test_all()
