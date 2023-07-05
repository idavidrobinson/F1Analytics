from matplotlib import pyplot as plt
import fastf1 as ff1
import fastf1.plotting
from commonf1 import *

fastf1.plotting.setup_mpl(misc_mpl_mods=False)

class RacePositionChangeFetcher:
    def __init__(self, year, grand_prix, session_type):
        self.year         = year
        self.grand_prix   = grand_prix
        self.session_type = session_type

    def fetch_data(self):
        session = ff1.get_session(self.year, self.grand_prix, self.session_type)
        session.load(telemetry=False, weather=False)

        return session

class RacePositionChangePlotter:
    @staticmethod
    def plot_race_data(session):
        fig, ax = plt.subplots(figsize=(8.0, 4.9))

        for drv in session.drivers:
            drv_laps = session.laps.pick_driver(drv)

            abb = drv_laps['Driver'].iloc[0]
            color = DRIVER_TEAM_COLORS.get(abb, 'black')

            ax.plot(drv_laps['LapNumber'], drv_laps['Position'], label=abb, color=color)

        ax.set_ylim([20.5, 0.5])
        ax.set_yticks([1, 5, 10, 15, 20])
        ax.set_xlabel('Lap')
        ax.set_ylabel('Position')

        ax.legend(bbox_to_anchor=(1.0, 1.02))
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    year         = USER_YEAR_INPUT
    grand_prix   = USER_GRAND_PRIX_INPUT
    session_type = USER_SESSION_TYPE_INPUT

    race_data_fetcher = RacePositionChangeFetcher(year=year, grand_prix=grand_prix, session_type=session_type)
    session = race_data_fetcher.fetch_data()

    RacePositionChangePlotter.plot_race_data(session)
