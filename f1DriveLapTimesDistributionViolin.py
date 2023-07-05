import fastf1 as ff1
import fastf1.plotting
import seaborn as sns
from matplotlib import pyplot as plt
from commonf1 import *


class DriverLapTimeViolinDistributionFetcher:
    def __init__(self, year, grand_prix, session_type):
        self.year         = year
        self.grand_prix   = grand_prix
        self.session_type = session_type
        
        fastf1.plotting.setup_mpl(mpl_timedelta_support=False, misc_mpl_mods=False)
        self.session      = ff1.get_session(self.year, self.grand_prix, self.session_type)
        self.session.load() 

        self.point_finishers = self.session.drivers[:10]
        self.driver_laps = self.session.laps.pick_drivers(self.point_finishers).pick_quicklaps()
        self.driver_laps = self.driver_laps.reset_index()

        self.finishing_order = [self.session.get_driver(abv)["Abbreviation"] for abv in self.point_finishers]
        self.driver_colors = {abv: fastf1.plotting.DRIVER_COLORS[driver] for abv, driver in fastf1.plotting.DRIVER_TRANSLATE.items()}
        self.driver_laps["LapTime(s)"] = self.driver_laps["LapTime"].dt.total_seconds()


class DriverLapTimeViolinDistributionPlotter:
    def __init__(self, ff1_session):
        self.ff1_session = ff1_session

    def plot_data(self):
        fig, ax = plt.subplots(figsize=(10, 5))

        sns.violinplot(data=self.ff1_session.driver_laps,
                       x="Driver",
                       y="LapTime(s)",
                       inner=None,
                       scale="area",
                       order=self.ff1_session.finishing_order,
                       palette=self.ff1_session.driver_colors)

        sns.swarmplot(data=self.ff1_session.driver_laps,
                      x="Driver",
                      y="LapTime(s)",
                      order=self.ff1_session.finishing_order,
                      hue="Compound",
                      palette=fastf1.plotting.COMPOUND_COLORS,
                      hue_order=["SOFT", "MEDIUM", "HARD"],
                      linewidth=0,
                      size=5)

        ax.set_xlabel("Driver")
        ax.set_ylabel("Lap Time(s)")
        plt.suptitle(f"{self.ff1_session.year} {self.ff1_session.grand_prix} Grand Prix Lap Time Distributions")
        sns.despine(left=True, bottom=True)

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    # get user input
    year         = USER_YEAR_INPUT
    grand_prix   = USER_GRAND_PRIX_INPUT
    session_type = USER_SESSION_TYPE_INPUT

    # create FastF1Session object
    fastf1_session = DriverLapTimeViolinDistributionFetcher(year, grand_prix, session_type)

    # create LapTimePlot object and plot data
    lap_time_plot = DriverLapTimeViolinDistributionPlotter(fastf1_session)
    lap_time_plot.plot_data()
