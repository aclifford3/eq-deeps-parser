'''Creates visualizations of fight reports'''

import logging

import matplotlib.pyplot as plt
import pandas as pd

def plot(fight_report):
    '''Plots fight report on a horizontal bar graph'''
    if len(fight_report.contribution_aggregates.keys()) > 0:
        data = []
        index = []
        for participant in fight_report.contribution_aggregates.keys():
            performance = fight_report.contribution_aggregates[participant]
            data.append([performance.damage_dealt, performance.healing_dealt])
            index.append(participant)
        data_frame = pd.DataFrame(data, columns=['Damage', 'Healing'], index=index)
        data_frame = data_frame.sort_values(by=['Damage'])
        axes = data_frame.plot.barh()
        axes.set_xlabel('')
        plt.show()
    else:
        logging.debug('Nothing to plot')
