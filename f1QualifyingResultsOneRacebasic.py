import matplotlib.pyplot as plt
import pandas as pd
from timple.timedelta import strftimedelta

import fastf1 as ff1
import fastf1.plotting
from fastf1.core import Laps
from commonf1 import *

fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None, misc_mpl_mods=False)

class SingleSessionFastestLapAllDriversFetcher:
    def __init__(self, year, grand_prix, session_type):
        self.year         = year
        self.grand_prix   = grand_prix
        self.session_type = session_type

    def fetch_fastest_laps(self):
        session = ff1.get_session(self.year, self.grand_prix, self.session_type)
        session.load()

        drivers = pd.unique(session.laps['Driver'])

        list_fastest_laps = list()
        for driver in drivers:
            drivers_fastest_lap = session.laps.pick_driver(driver).pick_fastest()
            list_fastest_laps.append(drivers_fastest_lap)
        
        fastest_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)

        return fastest_laps, session.event['EventName'], session.event.year

    def calculate_laptime_delta(self, fastest_laps):
        pole_lap = fastest_laps.pick_fastest()
        fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime']

        return fastest_laps, pole_lap

class SingleSessionFastestLapAllDriversPlotter:
    @staticmethod
    def plot_fastest_laps(fastest_laps, pole_lap, event_name, year):
        team_colors = [DRIVER_TEAM_COLORS.get(lap['Driver'], 'black') for _, lap in fastest_laps.iterlaps()]

        fig, ax = plt.subplots()
        ax.barh(fastest_laps.index, fastest_laps['LapTimeDelta'], color=team_colors, edgecolor='grey')
        ax.set_yticks(fastest_laps.index)
        ax.set_yticklabels(fastest_laps['Driver'])

        ax.invert_yaxis()

        ax.set_axisbelow(True)
        ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)

        lap_time_string = strftimedelta(pole_lap['LapTime'], '%m:%s.%ms')

        plt.suptitle(f"{event_name} {year} Qualifying \n"
                     f"Fastest Lap: {lap_time_string} ({pole_lap['Driver']})")

        plt.show()

if __name__ == "__main__":
    year         = USER_YEAR_INPUT
    grand_prix   = USER_GRAND_PRIX_INPUT
    session_type = USER_SESSION_TYPE_INPUT

    fastest_lap_fetcher = SingleSessionFastestLapAllDriversFetcher(year=year, grand_prix=grand_prix, session_type=session_type)
    fastest_laps, event_name, year = fastest_lap_fetcher.fetch_fastest_laps()

    fastest_laps, pole_lap = fastest_lap_fetcher.calculate_laptime_delta(fastest_laps)

    SingleSessionFastestLapAllDriversPlotter.plot_fastest_laps(fastest_laps, pole_lap, event_name, year)