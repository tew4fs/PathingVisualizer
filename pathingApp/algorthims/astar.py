class AStar:
    def reconstructPath(self, cameFrom, current):
        totalPath = [current]
        while current in cameFrom.keys():
            current = cameFrom[current]
            totalPath.append(current)
        return totalPath

    def h(self, a, b):
        return abs(b[0] - a[0]) + abs(b[1] - a[1])

    def lowestFScore(self, openSet, fScore):
        node = openSet[0]
        minFScore = fScore[node]
        for n in openSet:
            if fScore[n] < minFScore:
                minFScore = fScore[n]
                node = n
        return node

    def getNeighbors(self, current, blocks, gridHeight, gridWidth):
        neighbors = []
        c = current[0]
        r = current[1]
        if (c - 1) >= 0 and blocks.count((c - 1, r)) == 0:
            neighbors.append(((c - 1), r))
        if (c + 1) < gridWidth and blocks.count((c + 1, r)) == 0:
            neighbors.append(((c + 1), r))
        if (r - 1) >= 0 and blocks.count((c, r - 1)) == 0:
            neighbors.append((c, (r - 1)))
        if (r + 1) < gridHeight and blocks.count((c, r + 1)) == 0:
            neighbors.append((c, (r + 1)))
        return neighbors

    def A_Star(self, start, goal, blocks, gridHeight, gridWidth):
        pointsObserved = []
        openSet = [start]

        cameFrom = dict()

        gScore = dict()
        gScore[start] = 0

        fScore = dict()
        fScore[start] = self.h(start, goal)

        while len(openSet) > 0:
            current = self.lowestFScore(openSet, fScore)
            pointsObserved.append(current)
            if current == goal:
                return self.reconstructPath(cameFrom, current), pointsObserved

            openSet.remove(current)

            neighbors = self.getNeighbors(current, blocks, gridHeight, gridWidth)
            for neighbor in neighbors:
                tenativeGScore = gScore[current] + 1
                try:
                    if tenativeGScore < gScore[neighbor]:
                        cameFrom[neighbor] = current
                        gScore[neighbor] = tenativeGScore
                        fScore[neighbor] = tenativeGScore + self.h(neighbor, goal)
                        if openSet.count(neighbor) == 0:
                            openSet.append(neighbor)
                except KeyError:
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tenativeGScore
                    fScore[neighbor] = tenativeGScore + self.h(neighbor, goal)
                    if openSet.count(neighbor) == 0:
                        openSet.append(neighbor)
        return [], pointsObserved
