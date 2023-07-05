import fastf1 as ff1
import fastf1.plotting
import seaborn as sns
from matplotlib import pyplot as plt
from commonf1 import *

# The misc_mpl_mods option enables minor grid lines which clutter the plot
fastf1.plotting.setup_mpl(misc_mpl_mods=False)

class OneDriverLapTimeByTyrePlot:
    def __init__(self, year, grand_prix, session_type, driver_code):
        self.year         = year
        self.grand_prix   = grand_prix
        self.session_type = session_type
        self.driver_code  = driver_code

    def load_data(self):
        # Load race session
        self.session = ff1.get_session(self.year, self.grand_prix, self.session_type)
        self.session.load()

        # Get all laps for single driver - filter out slow laps that distort graph axis
        self.driver_laps = self.session.laps.pick_driver(self.driver_code).pick_quicklaps().reset_index()

    def plot(self):
        # make scatterplot with lap number as x-axis and lap time as y axis
        # marker colors correspond to compounds used - Note: as LapTime is represented by timedelta
        fig, ax = plt.subplots(figsize=(8,8))

        sns.scatterplot(data      = self.driver_laps, 
                        x         = "LapNumber",
                        y         = "LapTime",
                        ax        = ax,
                        hue       = "Compound",
                        palette   = fastf1.plotting.COMPOUND_COLORS,
                        s         = 80,
                        linewidth = 0,
                        legend    ='auto')

        # make the plot more aesthetic
        ax.set_xlabel("Lap Number")
        ax.set_ylabel("Lap Time")

        # the y-axis increases from bottom to top by default
        # since we are plotting time, it makes sense to invert the axis
        ax.invert_yaxis()
        plt.suptitle(f"{self.driver_code} Laptimes in the {self.year} {self.grand_prix} Grand Prix")

        # turn on major grid lines
        plt.grid(color='w', which='major', axis='both')
        sns.despine(left=True, bottom=True)

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    year         = USER_YEAR_INPUT
    grand_prix   = USER_GRAND_PRIX_INPUT
    session_type = USER_SESSION_TYPE_INPUT
    driver_code  = USER_ONE_DRIVER_CODE_INPUT

    plotter = OneDriverLapTimeByTyrePlot(year, grand_prix, session_type, driver_code)
    plotter.load_data()
    plotter.plot()