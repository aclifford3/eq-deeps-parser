import csv
import logging

"""
This class parses real time logs to configured EQ logging file, converts those logs to combat log objects and then adds
those objects to the current fight.  This class maintains a list of the last N fights.
"""


def get_starting_line(path):
    with open(path) as log_file:
        csv_reader = csv.reader(log_file)
        log_lines = 0
        for row in csv_reader:
            log_lines = log_lines + 1
        logging.debug("Starting on line %s", log_lines)
    return log_lines


class LogPuller:
    def __init__(self, path):
        self.path = path
        # self.last_processed_log_line = get_starting_line(path)
        self.last_processed_log_line = 111

    """
    Returns the log file line on which to start parsing.  We only want to process new events that come in, so we will
    just point our process to the last line in the log file to begin with.
    """

    def pull_new_logs(self):
        logs = []
        with open(self.path) as log_file:
            csv_reader = csv.reader(log_file)
            current_log_line = 0
            for row in csv_reader:
                current_log_line = current_log_line + 1
                if len(row) > 0 and self.last_processed_log_line < current_log_line:
                    self.last_processed_log_line = current_log_line
                    log = row[0]
                    logs.append(log)
        return logs
