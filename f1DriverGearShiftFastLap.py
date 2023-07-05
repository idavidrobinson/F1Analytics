import fastf1 as ff1
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib import cm
import numpy as np
from commonf1 import *

class OneDriverLapGearsFetcher:
    def __init__(self, year, grand_prix, session_type, driver_code):
        self.year         = year
        self.grand_prix   = grand_prix
        self.session_type = session_type
        self.driver_code  = driver_code
        
        self.session      = ff1.get_session(self.year, self.grand_prix, self.session_type)
        self.session.load() 
        
        self.driver_laps = self.session.laps.pick_driver(self.driver_code)
        self.lap         = self.driver_laps.pick_fastest()
        self.tel         = self.lap.get_telemetry() 

class OneDriverLapGearsPlotter:
    def __init__(self, ff1_session):
        self.ff1_session = ff1_session

        self.x        = np.array(self.ff1_session.tel['X'].values)
        self.y        = np.array(self.ff1_session.tel['Y'].values)

        self.points   = np.array([self.x, self.y]).T.reshape(-1, 1, 2)
        self.segments = np.concatenate([self.points[:-1], self.points[1:]], axis=1)
        self.gear     = self.ff1_session.tel['nGear'].to_numpy().astype(float)

    def plot_data(self):
        cmap         = cm.get_cmap('Paired')
        self.lc_comp = LineCollection(self.segments, norm=plt.Normalize(1, cmap.N+1), cmap=cmap)
        self.lc_comp.set_array(self.gear)
        self.lc_comp.set_linewidth(4)

        plt.gca().add_collection(self.lc_comp)
        plt.axis('equal')
        plt.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)

        title=plt.suptitle(

            f"{self.ff1_session.lap['Driver']} - {self.ff1_session.session.event['EventName']} {self.ff1_session.session.event.year}"            f"Fastest Lap Gear Shift Visualization \n"
        )

        cbar = plt.colorbar(mappable=self.lc_comp, label="Gear", boundaries=np.arange(1, 10))
        cbar.set_ticks(np.arange(1.5, 9.5))
        cbar.set_ticklabels(np.arange(1,9))

        plt.show()


if __name__ == "__main__":
    # get user input
    year         = USER_YEAR_INPUT
    grand_prix   = USER_GRAND_PRIX_INPUT
    session_type = USER_SESSION_TYPE_INPUT
    driver_code  = USER_ONE_DRIVER_CODE_INPUT

    # create FastF1Session object
    fastf1_session = OneDriverLapGearsFetcher(year, grand_prix, session_type, driver_code)

    # create GearShiftPlot object and plot data
    gear_shift_plot = OneDriverLapGearsPlotter(fastf1_session)
    gear_shift_plot.plot_data()
