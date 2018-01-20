from random import randint

"""
Agent class defines a simple-reflex agent that considers information
about only the current percepts in order to make a decision

This agent requires sensors for the speed and direction of the crosswind
This agent requires actuators for throwing a baseball with horizontal aiming capabilities
We keep track of the number of pitches thrown, the number of simulated outs
(to help with performance measurement), a current
state reflected by the environment, and rules for mapping a state to an action
"""
class Agent:

    """
    Sets the initial state of this agent

    @:param environment - the current simulated environment
    """
    def __init__(self):
        self.horizontalOffset = 0 #represents the offset in inches from the center of the plate
                                  #where a negative number is aiming to the left and positive to the right
        self.pitchCount = 0 #the number of pitches this agent has thrown
        self.currentStrikes = 0
        self.currentBalls = 0
        self.outs = 0 #the number of simulated outs this agent has gotten
        self.state = None #this agent's culmination of the current string
                                                                        #of percepts

    """
    Updates the internal state of this agent
    
    @:param environment - the current simulated environment
    """
    def updateState(self, environment):
        self.state = [environment.windSpeed, environment.windDirection]

    """
    Uses the current state to choose changes to the next pitch
    """
    def mapStateToAction(self):
        def getRule():
            windSpeed = self.state[0]
            if windSpeed >= 60:
                return 'extreme'
            elif windSpeed >= 40:
                return 'high'
            elif windSpeed >= 20:
                return 'moderate'
            else:
                return 'low'

        def getAction(rule):
            return {
              'extreme' : randint(12, 24),
              'high' : randint(6, 12),
              'moderate' : randint(0, 9),
              'low' : randint(0, 6)
            }[rule]

        windDirection = self.state[1]
        rule = getRule()
        print("I detect the wind level to be {} blowing to the {}".format(rule, windDirection))
        delta = getAction(rule)
        self.horizontalOffset = delta if windDirection == 'left' else (-1 * delta)
        print("I've decided to aim {} inches to the {}"
              .format(abs(self.horizontalOffset), 'right' if windDirection == 'left' else 'left'))

    def throwPitch(self, environment):
        print("================================================")
        print("Pitch # {}".format(self.pitchCount + 1))
        self.updateState(environment)
        self.mapStateToAction()
        windEffect = (environment.windSpeed / 10) * 3
        pitchLocationHorizontal = (self.horizontalOffset + windEffect if environment.windDirection == 'right'
            else self.horizontalOffset - windEffect)
        if(self.isStrike(pitchLocationHorizontal)):
            print("I threw a strike!")
            pitch = "strike"
        else:
            print("I threw a ball")
            pitch = "ball"
        self.updateAtBat(pitch)
        self.pitchCount += 1
        if(self.outs == 3):
            print("I finished the inning after {} pitches".format(self.pitchCount))
        print("================================================")

    def isStrike(self, pitchLocationHorizontal):
        return True if abs(pitchLocationHorizontal) < 8.5 else False

    def updateAtBat(self, pitch):
        if(pitch == 'strike'):
            self.currentStrikes += 1
        else:
            self.currentBalls += 1

        if self.currentStrikes == 3 or self.currentBalls == 4:
            self.resetAtBat()

    def resetAtBat(self):
        self.outs = self.outs + 1 if self.currentStrikes == 3 else self.outs
        self.currentStrikes = 0
        self.currentBalls = 0

    def inningIsOver(self):
        return self.outs == 3

class Environment:

    def __init__(self):
        self.windSpeed = randint(0, 70)
        self.windDirection = 'right' if randint(0, 1) == 0 else 'left'

    def updateWindEffects(self):
        self.windSpeed = randint(0, 70)
        self.windDirection = 'right' if randint(0, 1) == 0 else 'left'

agent = Agent()
environment = Environment()
while(not agent.inningIsOver()):
    agent.throwPitch(environment)
    environment.updateWindEffects()

