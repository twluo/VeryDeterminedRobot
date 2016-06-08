from std_msgs.msg import String, Boolfrom cse_190_assi_3.msg import PolicyListimport numpy as npimport copyclass Qs(object):    def __init__(self):        self.obType = None        self.reward = None        self.qNSWE = [0.0]*4    def __repr__(self):        val, a = self.maxQ()        if a == None:            a = "_"        return "%.3f %s" % (val, a[0])    def copy(self, qold):        return copy.deepcopy(self)    def getType(self):        return self.obType    def setReward(self, reward):        self.reward = reward    def getReward(self):        return self.reward    def maxQ(self):        if self.obType != None:            return self.reward, None        assert(len(self.qNSWE) == 4)        assert(self.qNSWE[0] != None)        assert(self.qNSWE[1] != None)        assert(self.qNSWE[2] != None)        assert(self.qNSWE[3] != None)        qAndA = zip(self.qNSWE, ['N', 'S', 'W', 'E'])        q, action = max(qAndA)        return q, action    def setGridProperties(self, gridProperty):        if gridProperty == "PIT":            self.obType = "PIT"        elif gridProperty == "GOAL":            self.obType = "GOAL"        elif gridProperty == "WALL":            self.obType = "WALL"        else:            self.obType = Noneclass QLearner(object):    def __init__(self, config):        self.config = config        self.prevgrid = None        self.currstate = None        self.grid = self.gridConstructor()        self.iteration_count = 0    def northSouthWestEast(self, row, col):        """Returns the possible up down left rights"""        to_return = dict()        to_return["N"] = [row - 1, col]        to_return["S"] = [row + 1, col]        to_return["W"] = [row, col - 1]        to_return["E"] = [row, col + 1]        return dict(to_return)    def gridConstructor(self):        """Constructs the grid"""        config = self.config        height, width = config["map_size"]        grid = list()        for r in xrange(height):            column = list()            for w in xrange(width):                toAdd = Qs()                if   [r, w] in config["pits"]:                    toAdd.setGridProperties("PIT")                    toAdd.setReward(config["reward_for_falling_in_pit"])                elif [r, w] == config["goal"]:                    toAdd.setGridProperties("GOAL")                    toAdd.setReward(config["reward_for_reaching_goal"])                elif [r, w] in config["walls"]:                    toAdd.setGridProperties("WALL")                    toAdd.setReward(config["reward_for_hitting_wall"])                else:                    toAdd.setGridProperties("none")                    toAdd.setReward(config["reward_for_each_step"])                column.append(toAdd)            grid.append(column)        return grid    def renameThis(self):        """Returns boolean of whether or not it converges"""        converged = False        if self.prevgrid != None:            prevacc = 0.0            curracc = 0.0            for pr, cr in zip(self.prevgrid, self.grid):                for pc, cc in zip(pr, cr):                    prevacc += pc.maxQ()[0]                    curracc += cc.maxQ()[0]            if abs(curracc - prevacc) < self.config["threshold_difference"]:                converged = True        return self.iteration_count < self.config["max_iterations"] and not converged    def inBounds(self, r, c):        height, width = self.config["map_size"]        if   r >= height or r < 0:            return False        elif c >= width  or c < 0:            return False        return True    def getCell(self, r, c):        return self.grid[r][c]    def hitWall(self, r, c):        if not self.inBounds(r, c):            return True        elif: self.getCell(r, c).obType == 'WALL'            return True        else:            return False    def explore(self, currState, action):        """Where currstate is [row, col] and        action is 'N', 'S', 'E', or 'W' """        p_forward = self.config["prob_move_forward"]        p_backward = self.config["prob_move_backward"]        p_left = self.config["prob_move_left"]        p_right = self.config["prob_move_right"]        p_fblr = [p_foward, p_backward, p_left, p_right]        assert(sum([p_fblr]))        fblr = self.forwardBackwardLeftRight(currState, action)        newState = np.random.choice(fblr, 1, replace=True, p=p_fblr)[0]        return newState    def forwardBackwardLeftRight(self, currState, action):        assert(action is 'N' or action is 'S' or action is 'E' or action is 'W')        nswe = self.northSouthWestEast(*currState)        n = currState if self.hitWall(*nswe['N']) else nswe['N']        s = currState if self.hitWall(*nswe['S']) else nswe['S']        w = currState if self.hitWall(*nswe['W']) else nswe['W']        e = currState if self.hitWall(*nswe['E']) else nswe['E']        if action == 'N': return [n, s, w, e] if action == 'S':            return [s, n, e, w]        if action == 'W':            return [w, e, s, n]        if action == 'E':            return [e, w, n, s]    def finalState(self, r, c):        assert(self.inBounds(r, c))        obType = self.getCell(r, c).obType        return obType != None and obType != 'WALL'    def iterate(self):        self.iteration_count += 1        to_return = PolicyList()        policy_data = list()        wall_reward = self.config["reward_for_hitting_wall"]        discount = self.config["discount_factor"]        currState = None        if self.config['start'] == 'random':            pass        else:            currState = self.config['start']        while self.finalState(*currState):            """Calculate the Q's and Update"""            """Take the action with the max Q"""            """Update the currentState accordingly"""            pass