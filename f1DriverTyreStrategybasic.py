import fastf1 as ff1
import fastf1.plotting
from matplotlib import pyplot as plt
from commonf1 import *

fastf1.plotting.setup_mpl(misc_mpl_mods=False)

class AllDriversOneSessionTyreFetcher:
    def __init__(self, year, grand_prix, session_type):
        self.year       = year
        self.grand_prix = grand_prix
        self.session_type  = session_type

    def fetch_data(self):
        session = ff1.get_session(self.year, self.grand_prix, self.session_type)
        session.load()

        laps = session.laps

        drivers = session.drivers
        drivers = [session.get_driver(driver)['Abbreviation'] for driver in drivers]

        stints = laps[["Driver", "Stint", "Compound", "LapNumber"]]
        stints = stints.groupby(["Driver", "Stint", "Compound"])
        stints = stints.count().reset_index()
        stints = stints.rename(columns={"LapNumber": "StintLength"})

        return drivers, stints

class AllDriversOneSessionTyrePlotter:
    @staticmethod
    def plot_strategy(drivers, stints):
        fig, ax = plt.subplots(figsize=(5, 10))

        for driver in drivers:
            driver_stints = stints.loc[stints["Driver"] == driver]

            previous_stint_end = 0
            for idx, row in driver_stints.iterrows():
                plt.barh(
                    y=driver,
                    width=row["StintLength"],
                    left=previous_stint_end,
                    color=fastf1.plotting.COMPOUND_COLORS[row["Compound"]],
                    fill=True
                )

                previous_stint_end += row["StintLength"]

        plt.title(f"{year} {grand_prix} Grand Prix Strategies")
        plt.xlabel("Lap Number")
        plt.grid(False)
        ax.invert_yaxis()

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    year          = USER_YEAR_INPUT
    grand_prix    = USER_GRAND_PRIX_INPUT
    session_type  = USER_SESSION_TYPE_INPUT

    strategy_data_fetcher = AllDriversOneSessionTyreFetcher(year=year, grand_prix=grand_prix, session_type=session_type)
    drivers, stints = strategy_data_fetcher.fetch_data()

    AllDriversOneSessionTyrePlotter.plot_strategy(drivers, stints)