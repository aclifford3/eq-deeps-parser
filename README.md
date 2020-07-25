# eq-deeps-parser
Program that parses EverQuest logs into objects for usage in creating DPS charts.  By parsing the raw data into objects,
we can more easily work with the data programmatically to achieve our goals.

## Objectives
* Collect combat logs data from EQ log files as objects.  This program should be able to process logs near real-time
* Group objects belonging to the same fight
* Surface data to client programs via an API

## Fights
As players of the game wanting to measure character effectiveness, we want to define some unit of time over which to
perform such measurements.  Often we try to optimize a fight to defeat a particular creature.  Because this is a common
use case, we choose to associate combat logs with each fight.  At some point, we need to consider
a fight terminated.  

### State Changes
A fight should be considered started upon receiving `You have entered combat...` message.  A fight
should be considered over when receiving the `You are no longer in combat` message.

## Data
The section should describe the data models to be used