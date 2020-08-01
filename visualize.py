import pandas as pd
import matplotlib.pyplot as plt
import logging

def plot(fight):
    if len(fight.actor_fight_performances.keys()) > 0:
        data = []
        index = []
        for actor in fight.actor_fight_performances.keys():
            performance = fight.actor_fight_performances[actor]
            data.append([performance.damage_dealt, performance.healing_dealt])
            index.append(actor)
        df = pd.DataFrame(data, columns=['Damage', 'Healing'], index=index)
        df = df.sort_values(by=['Damage'])
        ax = df.plot.barh()
        ax.set_xlabel('')
        plt.show()
    else:
        logging.debug('Nothing to plot')
