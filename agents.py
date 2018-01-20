from random import randint
from abc import abstractmethod, ABC

"""
Agent is an abstract class that defines the similar functionality
between both a simple reflex agent and a model based agent.

It leaves the decision making implementation abstract as to enforce an
implementation in a subclass.
"""
class Agent(ABC):

    """
    Sets the initial state of this agent

    @:param environment - the current simulated environment
    """
    def __init__(self):
        self.horizontalOffset = 0  # represents the offset in inches from the center of the plate
        # where a negative number is aiming to the left and positive to the right
        self.pitchCount = 0  # the number of pitches this agent has thrown
        self.currentStrikes = 0
        self.currentBalls = 0
        self.outs = 0  # the number of simulated outs this agent has gotten
        self.state = None  # this agent's culmination of the current string
        # of percepts
        self.strikeTotal = 0

    """
    Updates the internal state of this agent

    @:param environment - the current simulated environment
    """
    def updateState(self, environment):
        pass

    """
    Uses the current state to choose changes to the next pitch
    """
    @abstractmethod
    def mapStateToAction(self):
        pass

    """
    Updates the agent's state and decided upon a course of action.
    Then the result of the pitch is calculated and feedback is given by the agent.
    
    @:param environment - the current environment used for updating the agent's state
    """
    @abstractmethod
    def throwPitch(self, environment):
        pass

    """
    Calculates if the pitch was a strike.
    Home plate is 17 inches wide so the absolute value of the pitch's offset must
    by lower than half the width of the plate.
    
    @:param pitchLocationHorizontal - the offset, in inches, to the left or right of a pitch
    @:return if the pitch was a strike
    """
    def isStrike(self, pitchLocationHorizontal):
        return True if abs(pitchLocationHorizontal) < 8.5 else False

    """
    Updates the number of balls and strikes that have been thrown for an at bat.
    At 3 strikes, the agent's number of outs is incremented.
    At 4 balls, the at bat is reset and the agent continues trying to get outs.
    
    @:param pitch - information to tell if the pitch was a strike or a ball
    """
    def updateAtBat(self, pitch):
        if(pitch == 'strike'):
            self.currentStrikes += 1
            self.strikeTotal += 1
        else:
            self.currentBalls += 1

        if self.currentStrikes == 3 or self.currentBalls == 4:
            self.resetAtBat()

    """
    Sets the agent's count of current balls and strikes to 0 while appropriately 
    updating the number of outs if the occurrence was caused by 3 strikes. 
    """
    def resetAtBat(self):
        self.outs = self.outs + 1 if self.currentStrikes == 3 else self.outs
        self.currentStrikes = 0
        self.currentBalls = 0

    """
    An inning ends after 3 outs.
    
    @:return whether or not the inning is over
    """
    def inningIsOver(self):
        return self.outs == 3


##############################################################################################



"""
SimpleReflexAgent class defines a simple-reflex agent that considers information
about only the current percepts in order to make a decision

This agent requires sensors for the speed and direction of the crosswind
This agent requires actuators for throwing a baseball with horizontal aiming capabilities
We keep track of the number of pitches thrown, the number of simulated outs
(to help with performance measurement), a current
state reflected by the environment, and rules for mapping a state to an action
"""
class SimpleReflexAgent(Agent):

    def updateState(self, environment):
        self.state = [environment.windSpeed, environment.windDirection]

    """
    Uses the current state to choose changes to the next pitch
    For the simple agent, this means taking into account the current wind speed
    and direction only
    """
    def mapStateToAction(self):

        """
        map the wind speed to one of the agent's categorizations
        :return: this agent's categorization of the wind
        """
        def getRule(windSpeed):
            if windSpeed >= 60:
                return 'extreme'
            elif windSpeed >= 40:
                return 'high'
            elif windSpeed >= 20:
                return 'moderate'
            else:
                return 'low'

        """
        make a decision based upon the severity of the wind
        :return: this agent's decision on how fair off the aim the ball
        """
        def getAction(rule):
            return {
              'extreme' : randint(10, 30),
              'high' : randint(3, 27),
              'moderate' : randint(0, 21),
              'low' : randint(0, 12)
            }[rule]

        windSpeed = self.state[0]
        windDirection = self.state[1]
        #categorize the wind
        rule = getRule(windSpeed)
        print("I detect the wind level to be {} blowing to the {}".format(rule, windDirection))
        #choose the magnitude of the offset of the aim
        delta = getAction(rule)
        #choose the correct direction to aim the ball
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
        if (self.isStrike(pitchLocationHorizontal)):
            print("I threw a strike!")
            pitch = "strike"
        else:
            print("I threw a ball")
            pitch = "ball"
        self.updateAtBat(pitch)
        self.pitchCount += 1
        if (self.outs == 3):
            print("I finished the inning after {} pitches".format(self.pitchCount))
        print("================================================")



##############################################################################################


class ModelBasedAgent(Agent):

    def __init__(self):
        super().__init__()
        self.model = [] #a stored history of previous states, the resulting pitch, and the outcome

    def updateState(self, environment):
        self.state = [environment.windSpeed, environment.windDirection]

    def updateMemory(self, pitch):
        memory = [self.state[0], self.state[1], abs(self.horizontalOffset), pitch]
        self.model.append(memory)

    def mapStateToAction(self):

        """
        map the wind speed to one of the agent's categorizations
        :return: this agent's categorization of the wind
        """
        def getRule(windSpeed):
            if windSpeed >= 60:
                return 'extreme'
            elif windSpeed >= 40:
                return 'high'
            elif windSpeed >= 20:
                return 'moderate'
            else:
                return 'low'

        """
        make a decision based upon the severity of the wind
        :return: this agent's decision on how fair off the aim the ball
        """
        def getAction(rule):
            return {
              'extreme' : randint(6, 30),
              'high' : randint(3, 27),
              'moderate' : randint(0, 21),
              'low' : randint(0, 12)
            }[rule]

        def checkMemory(windSpeed):
            delta = None
            for memory in self.model:
                if abs(windSpeed - memory[0]) < 10 and memory[3] == 'strike':
                    print("I remember a similar situation to this and did well")
                    print("I will try to mimic that throw")
                    delta = memory[2]
                    break
            return delta

        windSpeed = self.state[0]
        windDirection = self.state[1]
        delta = checkMemory(windSpeed)
        if delta == None:
            print("I don't remember a suitable match to my current situation")
            print("I'll continue to categorize the wind as usual...")
            #categorize the wind
            rule = getRule(windSpeed)
            print("I detect the wind level to be {} blowing to the {}".format(rule, windDirection))
            #choose the magnitude of the offset of the aim
            delta = getAction(rule)
        #choose the correct direction to aim the ball
        self.horizontalOffset = delta if windDirection == 'left' else (-1 * delta)
        print("I've decided to aim {} inches to the {}"
            .format(abs(self.horizontalOffset), 'right' if windDirection == 'left' else 'left'))

    """
            Updates the agent's state and decided upon a course of action.
            Then the result of the pitch is calculated and feedback is given by the agent.

            @:param environment - the current environment used for updating the agent's state
            """

    def throwPitch(self, environment):
        print("================================================")
        print("Pitch # {}".format(self.pitchCount + 1))
        self.updateState(environment)
        self.mapStateToAction()
        windEffect = (environment.windSpeed / 10) * 3
        pitchLocationHorizontal = (self.horizontalOffset + windEffect if environment.windDirection == 'right'
        else self.horizontalOffset - windEffect)
        if (self.isStrike(pitchLocationHorizontal)):
            print("I threw a strike!")
            pitch = "strike"
        else:
            print("I threw a ball")
            pitch = "ball"
        self.updateMemory(pitch)
        self.updateAtBat(pitch)
        self.pitchCount += 1
        if (self.outs == 3):
            print("I finished the inning after {} pitches".format(self.pitchCount))
        print("================================================")



##############################################################################################




"""
Environment contains the logic behind the wind.

It contains a method for randomly generating the speed of the wind
as well as its direction
"""
class Environment:

    """
    Set the initial speed and direction of the wind.
    """
    def __init__(self):
        self.windSpeed = randint(0, 70)
        self.windDirection = 'right' if randint(0, 1) == 0 else 'left'

    """
    Update the speed and direction of the wind.
    """
    def updateWindEffects(self):
        self.windSpeed = randint(0, 70)
        self.windDirection = 'right' if randint(0, 1) == 0 else 'left'


##############################################################################################



"""
Conatins the logic for running a simulation

Creates an agent of a given type and an evironment to generate wind speeds.
Calls the agent to throw pitches and the evironment to change wind speeds until
the inning is over.
"""
def simulate(agent, environment):
    while(not agent.inningIsOver()):
        agent.throwPitch(environment)
        environment.updateWindEffects()

########## Beginning of execution ##########
simpleAgent = SimpleReflexAgent()
memoryAgent = ModelBasedAgent()
environment = Environment()
#simulate(simpleAgent, environment)
#simulate(memoryAgent, environment)
while simpleAgent.pitchCount < 1000:
    simpleAgent.throwPitch(environment)

while memoryAgent.pitchCount < 1000:
    memoryAgent.throwPitch(environment)

print("======================== Simulation Stats ========================")
print("Required Pitches:")
print("\tSimple Reflex Agent: {}".format(simpleAgent.pitchCount))
print("\tModel Reflex Agent: {}\n".format(memoryAgent.pitchCount))

print("Total Strikes:")
print("\tSimple Reflex Agent: {}".format(simpleAgent.strikeTotal))
print("\tModel Reflex Agent: {}\n".format(memoryAgent.strikeTotal))

