from collections import defaultdict


class Graph:

    def __init__(self, vertices, distance_metric=30.0):
        """
        Creates directed graph using adjacency list representation

        :param vertices: No. of points that will be represented as nodes in graph;
        :param distance_metric: Metric to create edge between two nodes.
        """
        self.V = vertices  # No. of vertices
        self.distance_metric = distance_metric
        self.graph = defaultdict(list)

    def add_edge(self, u, v):
        """
        Adds edge u->v to the graph;

        :param u: Head node;
        :param v: Tail node;
        """
        self.graph[u].append(v)

    def DFSUtil(self, v, visited):
        """
        Implementation of DFS Algorithm. O(V + E) complexity

        :param v: Current visiting node;
        :param visited: list of booleans visited or not, nodes as indexes.
        :return: List of accessible nodes.
        """
        # Mark the current node as visited and print it
        visited[v] = True

        # Create SCC
        result = [v]

        # Recur for all the vertices adjacent to this vertex
        for i in self.graph[v]:
            if not visited[i]:
                result = result + self.DFSUtil(i, visited)
        return result

    def fill_order(self, v, visited, stack):
        """
        Fill vertices in stack recursively.

        :param v: Head vertex;
        :param visited: List of visited vertexes in the graph;
        :param stack: stack to fill in vertexes by the visiting order/
        """
        # Mark the current node as visited
        visited[v] = True
        # Recur for all the vertices adjacent to this vertex
        for i in self.graph[v]:
            if not visited[i]:
                self.fill_order(i, visited, stack)
        stack = stack.append(v)

    def get_transpose(self):
        """
        Reverses graph direction.

        :return: reversed graph
        """
        graph = Graph(self.V)

        # Recur for all the vertices adjacent to this vertex
        for i in self.graph:
            for j in self.graph[i]:
                graph.add_edge(j, i)
        return graph

    def get_sccs(self):
        """
        Gets SCCs of the graph

        :return: List of SCCs of the graph. Each SCC contains id`s of Nodes
        """
        stack = []
        # Mark all the vertices as not visited (For first DFS)
        visited = [False] * self.V

        # Fill vertices in stack according to their finishing times
        for i in range(self.V):
            if not visited[i]:
                self.fill_order(i, visited, stack)

        # Create a reversed graph
        gr = self.get_transpose()

        # Mark all the vertices as not visited (For second DFS)
        visited = [False] * self.V

        # Now process all vertices in order defined by Stack
        SCC = []
        while stack:
            i = stack.pop()
            if not visited[i]:
                SCC.append(self.DFSUtil(i, visited))
                print("")

        return SCC

