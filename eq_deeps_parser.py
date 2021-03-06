"""
This class uses a log puller to read new combat logs every second.  It keeps track of character
performances for each fight.
"""

import configparser
import logging
import re
import time

import visualize
from log_puller import LogPuller

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)

class FightReport:
    '''Fight object containing a list of fight participants and their contributions'''
    def __init__(self):
        self.is_complete = False
        self.contribution_aggregates = {}

class ContributionAggregate:
    '''Total contribution for a given participant for a given fight'''
    def __init__(self, participant):
        self.participant = participant
        self.damage_dealt = 0
        self.healing_dealt = 0

class Contribution:
    '''A single contribution for a participant to be added to aggregate contribution'''
    def __init__(self, participant, target, damage_dealt, healing_dealt):
        self.participant = participant
        self.target = target
        self.damage_dealt = damage_dealt
        self.healing_dealt = healing_dealt


def is_combat_log(log):
    '''Returns true if log is a combat log'''
    if is_new_fight(log) or is_fight_complete(log) or 'points of damage' in log:
        return True
    return False


def is_new_fight(combat_log):
    '''Returns true if a new fight has begun'''
    return 'You have entered combat...' in combat_log


def is_fight_complete(combat_log):
    '''Returns true if the fight is completed'''
    return 'You are no longer in combat.' in combat_log

def is_damage_shield_message(combat_log):
    '''We treat damage shield as a separate participant, if log is for damage shield damage
    returns True
    '''
    return 'was hit by non-melee for' in combat_log

def get_participant(log_message, verb_start_pos):
    '''Gets the participant that is performing the combat action'''
    return log_message[0:verb_start_pos - 1]

def get_damage_shield_contribution(log_message, verb_start_pos, amount):
    '''Get contribution of damage shield'''
    return Contribution('Damage Shield', log_message[0:verb_start_pos-1], amount, 0)

def get_healing_contribution(log_message, amount):
    '''Get participant healing contribution'''
    for_pos = log_message.find(' for ')
    verb_match = re.search('((has|have) healed)', log_message)
    participant = get_participant(log_message, verb_match.start())
    target = log_message[verb_match.end() + 1:for_pos]
    return Contribution(participant, target, 0, amount)

def get_damage_contribution(log_message, amount, verb_match):
    '''Get participant damage contribution'''
    for_pos = log_message.find(' for ')
    participant = get_participant(log_message, verb_match.start())
    target = log_message[verb_match.end() + 1:for_pos]
    return Contribution(participant, target, amount, 0)

def is_healing_log(log_message):
    '''Returns true if log message is a healing event'''
    verb_match = re.search('((has|have) healed)', log_message)
    return verb_match is not None


def get_contribution(combat_log):
    '''Converts raw combat log into a more usable Contribution object'''
    # Split timestamp from the rest of the log message
    log_message = combat_log.split('] ')[1]
    amount = int(((log_message.split(' for ')[1]).split(' '))[0])
    # Locate the attack verb to use in figuring out the participant and target
    verb_match = re.search('(was )?(bite[s]?|bash[es]?|strike[s]?|slash[es]?|punch[es]?|hit[s]?'
                           '|pierce[s]?|crush[es]?|gore[s]?|kick[s]?|slap[s]?|claw[s]?|maul[s]?'
                           '|shoot[s]?|sting[s]?)',
                           log_message)
    if is_damage_shield_message(log_message):
        return get_damage_shield_contribution(log_message, verb_match.start(), amount)
    if is_healing_log(log_message):
        return get_healing_contribution(log_message, amount) 
    return get_damage_contribution(log_message, amount, verb_match)

def update_fight_contribution(contribution_aggregates, combat_log):
    '''Updates a participant's fight contribution based on combat log'''
    try:
        contribution = get_contribution(combat_log)
        logging.debug("Created contribution for actor %s", contribution.participant)
        if contribution.participant in contribution_aggregates.keys():
            contribution_aggregate = contribution_aggregates[contribution.participant]
        else:
            contribution_aggregate = ContributionAggregate(contribution.participant)
        contribution_aggregate.damage_dealt += contribution.damage_dealt
        contribution_aggregate.healing_dealt += contribution.healing_dealt
        contribution_aggregates[contribution.participant] = contribution_aggregate
    except KeyError:
        logging.exception('Failed to get combat event for log:  %s \n ', combat_log)


def process_combat_logs(logs, fight_reports):
    '''Given new combat logs, create fight reports'''
    if len(fight_reports) > 0:
        current_fight_report = fight_reports.pop()
    else:
        current_fight_report = FightReport()
    for combat_log in logs:
        if is_new_fight(combat_log):
            if not current_fight_report.is_complete:
                current_fight_report.is_complete = True
            else:
                current_fight_report = FightReport()
                fight_reports.append(current_fight_report)
        elif is_fight_complete(combat_log):
            current_fight_report.is_complete = True
        else:
            update_fight_contribution(current_fight_report.contribution_aggregates, combat_log)
    fight_reports.append(current_fight_report)


def filter_combat_logs(logs):
    '''Filter out logs other than combat logs'''
    return list(filter(is_combat_log, logs))


def get_log_file_path():
    '''Gets the EQ log file path from configuration file'''
    config = configparser.ConfigParser()
    config.read('./config.ini')
    return config['DEFAULT']['COMBAT_LOG_PATH']

if __name__ == '__main__':
    path = get_log_file_path()
    logging.info("Starting parser.")
    fights_reports = []
    log_puller = LogPuller(path)
    MAX_FIGHTS_TO_RETAIN = 1
    while True:
        new_logs = log_puller.pull_new_logs()
        combat_logs = filter_combat_logs(new_logs)
        process_combat_logs(combat_logs, fights_reports)
        while len(fights_reports) > MAX_FIGHTS_TO_RETAIN:
            fights_reports.pop(0)
        for fight_report in fights_reports:
            logging.debug('Found %s total fights', len(fights_reports))
            logging.debug('Found fight report %s', fight_report.contribution_aggregates)
            visualize.plot(fights_reports[0])
        time.sleep(4)
