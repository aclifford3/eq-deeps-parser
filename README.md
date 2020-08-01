![Python application](https://github.com/aclifford3/eq-deeps-parser/workflows/Python%20application/badge.svg)

# eq-deeps-parser
Program that parses EverQuest combat logs and uses them to visualize character damage and healing amounts for the last
fight.

## Fights
As players of the game wanting to measure character effectiveness, we want to define some unit of time over which to
perform such measurements.  Often we try to optimize a fight to defeat a particular creature.  Because this is a common
use case, we choose to associate combat logs with each fight.  At some point, we need to consider
a fight terminated.  

### State Changes
A fight should be considered started upon receiving `You have entered combat...` message.  A fight
should be considered over when receiving the `You are no longer in combat` message.

## Development
This describes the setup for developing this program.

1.  Ensure you have installed a [Python 3 version](https://www.python.org/downloads/)
2.  Pull down this code base
3.  Install project dependencies in `requirements.txt`
4.  Try to run the unit tests in `test_eq_deeps_parser.py`
5.  Try to run the program `eq_deeps_parser.py`


## Usage
1. Have Python3 installed
2. Install Python dependencies with `pip install -r requirements.txt`
3. Update `config.ini` to point at your log file path.
4. Run the script `python eq_deeps_parser.py`

