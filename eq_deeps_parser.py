"""
This class uses a log puller to read new combat logs every second.  It keeps track of character performances for each
fight.
"""

import time
import os
import logging
import re
import visualize
from log_puller import LogPuller
import configparser

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)


class Fight:
    def __init__(self):
        self.is_complete = False
        self.actor_fight_performances = {}


class FightPerformance:
    def __init__(self, actor):
        self.actor = actor
        self.damage_dealt = 0
        self.healing_dealt = 0


class CombatEvent:
    def __init__(self, actor, target, damage_dealt, healing_dealt):
        self.actor = actor
        self.target = target
        self.damage_dealt = damage_dealt
        self.healing_dealt = healing_dealt


def is_combat_log(log):
    if is_new_fight(log) or is_fight_complete(log) or 'points of damage' in log:
        return True


def is_new_fight(combat_log):
    return 'You have entered combat...' in combat_log


def is_fight_complete(combat_log):
    return 'You are no longer in combat.' in combat_log


def get_combat_event(combat_log):
    is_healing_event = False
    # Split timestamp from the rest of the log message
    message = combat_log.split('] ')[1]
    # Locate the attack verb to use in figuring out the actor and target
    verb_match = re.search('(was )?(bite[s]?|bash[es]?|strike[s]?|slash[es]?|punch[es]?|hit[s]?|pierce[s]?'
                           '|crush[es]?|gore[s]?|kick[s]?|slap[s]?|claw[s]?|maul[s]?|shoot[s]?|sting[s]?)',
                           message)
    if not verb_match:
        verb_match = re.search('((has|have) healed)', message)
        is_healing_event = True

    actor = message[0:verb_match.start() - 1]
    for_pos = message.find(' for ')

    target = message[verb_match.end() + 1:for_pos]

    amount = int(((message.split(' for ')[1]).split(' '))[0])
    if is_healing_event:
        return CombatEvent(actor, target, 0, amount)
    return CombatEvent(actor, target, amount, 0)


def update_fight_performance(unit_fight_performances, combat_log):
    try:
        combat_event = get_combat_event(combat_log)
        logging.debug("Created combat event for actor %s", combat_event.actor)
        if combat_event.actor in unit_fight_performances.keys():
            fight_performance = unit_fight_performances[combat_event.actor]
        else:
            fight_performance = FightPerformance(combat_event.actor)
        fight_performance.damage_dealt += combat_event.damage_dealt
        fight_performance.healing_dealt += combat_event.healing_dealt
        unit_fight_performances[combat_event.actor] = fight_performance
    except Exception as e:
        logging.error('Failed to get combat event for log:  \n %s', combat_log, e)


def process_combat_logs(logs, fights):
    if len(fights) > 0:
        current_fight = fights.pop()
    else:
        current_fight = Fight()
    for combat_log in logs:
        if is_new_fight(combat_log):
            if not current_fight.is_complete:
                current_fight.is_complete = True
            else:
                current_fight = Fight()
                fights.append(current_fight)
        elif is_fight_complete(combat_log):
            current_fight.is_complete = True
        else:
            update_fight_performance(current_fight.actor_fight_performances, combat_log)
    fights.append(current_fight)


def filter_combat_logs(logs):
    return list(filter(lambda x: is_combat_log(x), logs))


def get_log_file_path():
    config = configparser.ConfigParser()
    config.read('./config.ini')
    return config['DEFAULT']['COMBAT_LOG_PATH']

if __name__ == '__main__':
    path = get_log_file_path()
    log_file_size = os.path.getsize(path)
    logging.info("Starting parser.")
    fights = []
    log_puller = LogPuller(path)
    max_fights_to_retain = 1
    while True:
        new_logs = log_puller.pull_new_logs()
        combat_logs = filter_combat_logs(new_logs)
        process_combat_logs(combat_logs, fights)
        while len(fights) > max_fights_to_retain:
            fights.pop(0)
        for fight in fights:
            logging.debug('Found %s total fights', len(fights))
            logging.debug('Found fight %s', fight.actor_fight_performances)
            visualize.plot(fights[0])
        time.sleep(4)

