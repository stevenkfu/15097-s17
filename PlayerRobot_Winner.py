# Latest submit by Ananya

from robot import Robot
from constants import Actions, TileType
import random
import time
import math

##########################################################################
# One of your team members, Chris Hung, has made a starter bot for you.  #
# Unfortunately, he is busy on vacation so he is unable to aid you with  #
# the development of this bot.                                           #
#                                                                        #
# Make sure to read the README for the documentation he left you         #
#                                                                        #
# @authors: christoh, [TEAM_MEMBER_1], [TEAM_MEMBER_2], [TEAM_MEMBER_3]  #
# @version: 2/4/17                                                       #
#                                                                        #
# README - Introduction                                                  #
#                                                                        #
# Search the README with these titles to see the descriptions.           #
##########################################################################

# !!!!! Make your changes within here !!!!!
class player_robot(Robot):

    visited = []
    global_map = []
    stage = None
    EXPLORATION_STAGE = 1
    FORAGING_STAGE = 2
    SATISFIED_STAGE = 3
    SAD_STAGE = 4
    WAITFORMINE_STAGE = 5
    MININGMINE_STAGE = 6
    RUSHHOME_STAGE = 7

    def __init__(self, args):
        super(self.__class__, self).__init__(args)
        ##############################################
        # A couple of variables - read what they do! # 
        #                                            #
        # README - My_Robot                          #
        ##############################################
        self.toHome = []             
        self.numturns = 0            
        self.goinghome = False;      
        self.targetPath = None
        self.targetDest = (0,0)
        self.rad = -1
        self.stdx = 0
        self.stdy = 0
        self.prevMove = 0
        
    def findUnblocked2(self, view, x, y, count):
        if(count > 7):
            return (-2, -2)
        newx = -2
        newy = -2
        if(x == 1 and y == 1):
            newx = 1
            newy = 0
        elif(x == 1 and y == 0):
            newx = 1
            newy = -1
        elif(x == 1 and y == -1):
            newx = 0
            newy = -1
        elif(x == 0 and y == 1):
            newx = 1
            newy = 1
        elif(x == 0 and y == -1):
            newx = -1
            newy = -1
        elif(x == -1 and y == 1):
            newx = 0
            newy = 1
        elif(x == -1 and y == 0):
            newx = -1
            newy = 1
        elif(x == -1 and y == -1):
            newx = -1
            newy = 0
        if(self.possible(view, newx, newy)):
            return (newx, newy)
        return self.findUnblocked2(view, newx, newy, count+1);
        
    def findUnblocked(self, view, x, y, count):
        if(count > 7):
            return (-2, -2)
        newx = -2
        newy = -2
        if(x == 1 and y == 1):
            newx = 0
            newy = 1
        elif(x == 1 and y == 0):
            newx = 1
            newy = 1
        elif(x == 1 and y == -1):
            newx = 1
            newy = 0
        elif(x == 0 and y == 1):
            newx = -1
            newy = 1
        elif(x == 0 and y == -1):
            newx = 1
            newy = -1
        elif(x == -1 and y == 1):
            newx = -1
            newy = 0
        elif(x == -1 and y == 0):
            newx = -1
            newy = -1
        elif(x == -1 and y == -1):
            newx = 0
            newy = -1
        if(self.possible(view, newx, newy)):
            return (newx, newy)
        return self.findUnblocked(view, newx, newy, count+1);
        
    def findPath(self, view):
        xmov = self.stdx
        ymov = self.stdy
        self.xpos = self.x - 101
        self.ypos = self.y - 101
        if(self.possible(view, xmov, ymov)):
            self.xpos += xmov
            self.ypos += ymov
            angle = math.atan2(self.ypos, self.xpos) - self.rad
            mag = math.cos(angle) * math.sqrt(self.xpos * self.xpos + self.ypos * self.ypos)
            xorg = mag * math.cos(self.rad)
            yorg = mag * math.sin(self.rad)
            xdiff = -yorg
            ydiff = xorg
            # if(xdiff > 1):
            #     print(str(self.index) + " " + str(xdiff) + " " + str(self.get_turn()))
            if(xdiff > 2 and self.possible(view, xmov+2, ymov)):
                xmov = xmov + 2
            elif(xdiff < -2 and self.possible(view, xmov-2, ymov)):
                xmov = xmov - 2
            elif(xdiff > 1 and self.possible(view, xmov+1, ymov)):
                xmov = xmov + 1
            elif(xdiff < -1 and self.possible(view, xmov-1, ymov)):
                xmov = xmov - 1
                
            if(ydiff > 2 and self.possible(view, xmov, ymov+2)):
                ymov = ymov + 2
            elif(ydiff < -2 and self.possible(view, xmov, ymov-2)):
                ymov = ymov - 2
            elif(ydiff > 1 and self.possible(view, xmov, ymov+1)):
                ymov = ymov + 1
            elif(ydiff < -1 and self.possible(view, xmov, ymov-1)):
                ymov = ymov - 1
            self.xpos -= self.stdx
            self.ypos -= self.stdy
            self.xpos += xmov
            self.ypos += ymov
            return self.computeMove(xmov, ymov);
        else:
            (movex, movey) = (0,0)
            if(self.index % 2 == 0):
                (movex, movey) = self.findUnblocked2(view, xmov, ymov, 0)
            else:
                (movex, movey) = self.findUnblocked(view, xmov, ymov, 0)
            if (movex == -2):
                return None
            if(self.get_turn() < 15):
                print(str(self.index) + " " + str(xmov) + " " + str(ymov) + " " + str(movex) + " " + str(movey) + " " + str(self.xpos) + " " + str(self.ypos) + " " + str(self.get_turn()) + " " + str(self.possible(view, movex, movey)))
            self.xpos += movex
            self.ypos += movey
            return self.computeMove(movex, movey)


    def getIndex(self, view):
        self.rad = math.pi*self.index/50*2
        xm = math.cos(self.rad)
        ym = math.sin(self.rad)
        if(xm > math.sin(math.pi/8)):
            self.stdx = 1
        elif(xm < -math.sin(math.pi/8)):
            self.stdx = -1
        if(ym > math.sin(math.pi/8)):
            self.stdy = 1
        elif(ym < -math.sin(math.pi/8)):
            self.stdy = -1
        print(str(self.index) + " " + str(self.rad) + " " + str(self.stdx) + " " + str(self.stdy))
        return 

    # A couple of helper functions (Implemented at the bottom)
    def OppositeDir(self, direction):
        return # See below

    def ViewScan(self, view):
        return # See below

    def FindRandomPath(self, view):
        return # See below

    def UpdateTargetPath(self):
        return # See below
    
    def get_dx_dy(self, direction):
        dx = 0
        dy = 0
        if(direction == Actions.MOVE_N):
            dx = 0
            dy = 1
        elif(direction == Actions.MOVE_NE):
            dx = 1
            dy = 1
        elif(direction == Actions.MOVE_E):
            dx = 1
            dy = 0
        elif(direction == Actions.MOVE_SE):
            dy = -1
            dx = 1
        elif(direction == Actions.MOVE_S):
            dx = 0
            dy = -1
        elif(direction == Actions.MOVE_SW):
            dx = -1
            dy = -1
        elif(direction == Actions.MOVE_W):
            dx = -1
            dy = 0
        elif(direction == Actions.MOVE_NW):
            dx = -1
            dy = 1
        return (dx, dy)
    
    def _process_move(self, move):
        (direction, _) = move
        self.prevDirection = direction
        (dx, dy) = self.get_dx_dy(direction)
        self.x += dx
        self.y += dy

    def _update_map(self, view):
        for i in range(5):
            for j in range(5):
                dx = j - 2
                dy = 2 - i
                self.global_map[self.x + dx][self.y + dy] = view[i][j]
        self.visited[self.x][self.y] = True

    def get_move(self, view):
        move = self._get_move(view)
        self._process_move(move)
        self._update_map(view)
        return move

    def set_init_map(self):
        self.global_map = [[None for i in range(205)] for i in range(205)]
        self.visited = [[False for i in range(205)] for i in range(205)]
        self.visited[101][101] = True

    def exploration_stage(self, view):
        markerDrop = Actions.DROP_NONE
        actionToTake = self.findPath(view)
        # Probably need this because of bug.
        if(self.get_turn() == 0 and actionToTake == None):
            actionToTake = Actions.MOVE_S
        self.prevMove = actionToTake            
        return (actionToTake, markerDrop)

    def computeMove(self, x, y):
        if(x == 1 and y == 1):
            return Actions.MOVE_NE
        elif(x == 1 and y == 0):
            return Actions.MOVE_E
        elif(x == 1 and y == -1):
            return Actions.MOVE_SE
        elif(x == 0 and y == 1):
            return Actions.MOVE_N
        elif(x == 0 and y == -1):
            return Actions.MOVE_S
        elif(x == -1 and y == 1):
            return Actions.MOVE_NW
        elif(x == -1 and y == 0):
            return Actions.MOVE_W
        elif(x == -1 and y == -1):
            return Actions.MOVE_SW
        assert(False);

    def possible(self, view, x, y):
        if(math.fabs(x) > 1 or math.fabs(y) > 1):
            return False
        if(x == 0 and y == 0):
            return False
        if(self.computeMove(x, y) == self.OppositeDir(self.prevMove)):
            return False
        return view[2-y][2+x][0].CanMove()



    ###########################################################################################
    # This function is called every iteration. This method receives the current robot's view  #
    # and returns a tuple of (move_action, marker_action).                                    #
    #                                                                                         #
    # README - Get_Move                                                                       #
    ###########################################################################################
    def _get_move(self, view):

        MAX_TURNS = 1000

        # All robots back by last turn
        if (self.get_turn() == 999):
            assert(self.x == 101)
            assert(self.y == 101)

        if (self.get_turn() == 0):
            self.index = view[2][2][1] - 1
            self.getIndex(view)
            self.stage = self.EXPLORATION_STAGE
            self.exploration_start = 0
            self.set_init_map()
            self.x = 101
            self.y = 101

        turns_left = MAX_TURNS - self.get_turn()

        if turns_left <= len(self.toHome) + 2 or self.storage_remaining() == 0:
            self.stage = self.RUSHHOME_STAGE

        if self.stage == self.EXPLORATION_STAGE:
            self.exploration_start += 1
            move = self.exploration_stage(view)
            (direction, _) = move
            if self.exploration_start == 100 or direction is None:
                self.exploration_start = 0
                self.stage = self.FORAGING_STAGE
            else:
                self.toHome.append(direction)
                return move

        if self.stage == self.FORAGING_STAGE:
            # Run BFS to find closest resource
            # Search for resources
            # Updates self.targetPath, sefl.targetDest
            self.ViewScan(view)
            # If you can't find any resources...go in a random direction!
            actionToTake = None
            if(self.targetPath == None):
                actionToTake = self.FindRandomPath(view)

            # Congrats! You have found a resource
            elif(self.targetPath == []):
                self.targetPath = None
                return (Actions.MINE, Actions.DROP_NONE)
            else:
                # Use the first coordinate on the path as the destination , and action to move
                actionToTake = self.UpdateTargetPath()
            self.toHome.append(actionToTake)
            return (actionToTake, Actions.DROP_NONE)

        # How to navigate back home
        if(self.stage == self.RUSHHOME_STAGE):
            # You are at home
            if(self.toHome == []):
                self.stage = self.EXPLORATION_STAGE
                return (Actions.DROPOFF, Actions.DROP_NONE)
            # Trace your steps back home
            prevAction = self.toHome.pop()
            revAction = self.OppositeDir(prevAction)
            assert(isinstance(revAction, int))
            return (revAction, Actions.DROP_NONE)

    # Returns opposite direction
    def OppositeDir(self, prevAction):
        if(prevAction == Actions.MOVE_N):
            return Actions.MOVE_S
        elif(prevAction == Actions.MOVE_NE):
            return Actions.MOVE_SW
        elif(prevAction == Actions.MOVE_E):
            return Actions.MOVE_W
        elif(prevAction == Actions.MOVE_SE):
            return Actions.MOVE_NW
        elif(prevAction == Actions.MOVE_S):
            return Actions.MOVE_N
        elif(prevAction == Actions.MOVE_SW):
            return Actions.MOVE_NE
        elif(prevAction == Actions.MOVE_W):
            return Actions.MOVE_E
        elif(prevAction == Actions.MOVE_NW):
            return Actions.MOVE_SE
        else:
            return Actions.MOVE_S

    # Scans the entire view for resource searching
    # REQUIRES: view (see call location)
    def ViewScan(self, view):
        viewLen = len(view)
        queue = [[(0,0)]]
        deltas = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]
        visited = set()
        visited.add((0,0))

        targetDepleted = (view[self.targetDest[0]][self.targetDest[1]][0].GetType() == TileType.Resource and
                         view[self.targetDest[0]][self.targetDest[1]][0].AmountRemaining() <= 0)

        # BFS TO find the next resource within your view
        if(self.targetPath == None or targetDepleted):
            while(len(queue)>0):
                path = queue[0]
                loc = path[0]
                queue = queue[1:]
                viewIndex = (loc[0] + viewLen//2,loc[1]+viewLen//2)
                if (view[viewIndex[0]][viewIndex[1]][0].GetType() == TileType.Resource and
                    view[viewIndex[0]][viewIndex[1]][0].AmountRemaining() > 0):
                    # print(path)
                    self.targetPath = path[1:]
                    self.targetDest = path[0]
                    return
                elif(view[viewIndex[0]][viewIndex[1]][0].CanMove()):
                    for i in range(8):
                        x = loc[0] + deltas[i][0]
                        y = loc[1] + deltas[i][1]
                        if(abs(x) <= viewLen//2 and abs(y) <= viewLen//2):
                            if((x,y) not in visited):
                                queue.append([(x,y)] + path[1:] + [deltas[i]])
                                visited.add((x,y))

        return

    def get_valid_moves(self, view):
        viewLen = len(view)
        moves = []
        if (view[viewLen//2-1][viewLen//2][0].CanMove()):
            moves.append(Actions.MOVE_N)
        if (view[viewLen//2+1][viewLen//2][0].CanMove()):
            moves.append(Actions.MOVE_S)
        if (view[viewLen//2][viewLen//2+1][0].CanMove()):
            moves.append(Actions.MOVE_E)
        if (view[viewLen//2][viewLen//2-1][0].CanMove()):
            moves.append(Actions.MOVE_W)
        if (view[viewLen//2-1][viewLen//2-1][0].CanMove()):
            moves.append(Actions.MOVE_NW)
        if (view[viewLen//2-1][viewLen//2+1][0].CanMove()):
            moves.append(Actions.MOVE_NE)
        if (view[viewLen//2+1][viewLen//2-1][0].CanMove()):
            moves.append(Actions.MOVE_SW)
        if (view[viewLen//2+1][viewLen//2+1][0].CanMove()):
            moves.append(Actions.MOVE_SE)
        return moves

    def get_new_moves(self, moves):
        new_moves = []
        for move in moves:
            (dx, dy) = self.get_dx_dy(move)
            if self.visited[self.x + dx][self.y + dy] == False:
                new_moves.append(move)
        return new_moves

    # Picks a random move based on the view - don't crash into mountains!
    # REQUIRES: view (see call location)
    def FindRandomPath(self, view):
        moves = self.get_valid_moves(view)
        new_moves = self.get_new_moves(moves)
        if len(new_moves) > 0:
            moves = new_moves
        if self.prevDirection in moves and random.randint(0,100) <= 97:
            return self.prevDirection
        r = random.randint(0, len(moves)-1)
        return moves[r]

    # Returns actionToTake
    # REQUIRES: self.targetPath != []
    def UpdateTargetPath(self):
        actionToTake = None
        (x, y) = self.targetPath[0]

        if(self.targetPath[0] == (1,0)):
            actionToTake = Actions.MOVE_S
        elif(self.targetPath[0] == (1,1)):
            actionToTake = Actions.MOVE_SE
        elif(self.targetPath[0] == (0,1)):
            actionToTake = Actions.MOVE_E
        elif(self.targetPath[0] == (-1,1)):
            actionToTake = Actions.MOVE_NE
        elif(self.targetPath[0] == (-1,0)):
            actionToTake = Actions.MOVE_N
        elif(self.targetPath[0] == (-1,-1)):
            actionToTake = Actions.MOVE_NW
        elif(self.targetPath[0] == (0,-1)):
            actionToTake = Actions.MOVE_W
        elif(self.targetPath[0] == (1,-1)):
            actionToTake = Actions.MOVE_SW

        # Update destination using path
        self.targetDest = (self.targetDest[0]-x, self.targetDest[1]-y)
        # We will continue along our path    
        self.targetPath = self.targetPath[1:]

        return actionToTake