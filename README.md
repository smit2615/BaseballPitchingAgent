# Agent Based Model for Baseball Pitching #

**Purpose -** Simulate two agents pitching a baseball in various wind speeds.
One agent stores memory of its previous pitches while the other
does not.

## Simple Reflex Agent ##
- No memory model
- Single decision making algorithm
<br>

The simple reflex agent maps the current wind speed
to an internal category. It uses that category to randomly
generate an integer in an appropriate range. This happens on a
pitch by pitch basis.

## Model Based Agent ##
- Keeps record of previous wind conditions, 
its decision in those conditions, and the outcome
of that decision

- Two decision making algorithms

The model based agent responds to a change in wind by
searching its memory model for a similar wind speed to the 
current wind speed. If the agent happened to throw a strike
in that condition, it mimics that throw by aiming in the same
location as the pitch found in memory.

## Simulation Results ##

