import fastf1 as ff1
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from commonf1 import *

class OneDriverFastestLapFetcher:
    def __init__(self, year, grand_prix, session_type, driver_codes):
        self.year         = year
        self.grand_prix   = grand_prix
        self.session_type = session_type
        self.driver_codes = driver_codes

    def fetch_data(self):
        session = ff1.get_session(self.year, self.grand_prix, self.session_type)
        session.load()
        lap = session.laps.pick_driver(self.driver_codes).pick_fastest()

        return session.event, lap

class OneDriverFastestLapTrackSpeedPlotter:
    @staticmethod
    def plot_telemetry(event, lap, colormap=mpl.cm.plasma):
        x     = lap.telemetry['X']
        y     = lap.telemetry['Y']
        color = lap.telemetry['Speed']

        points   = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
        fig.suptitle(f'{event.name} {event.year} - {lap["Driver"]} - Speed', size=24, y=0.97)

        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
        ax.axis('off')

        ax.plot(lap.telemetry['X'], lap.telemetry['Y'], color='black', linestyle='-', linewidth=16, zorder=0)

        norm = plt.Normalize(color.min(), color.max())
        lc   = LineCollection(segments, cmap=colormap, norm=norm, linestyle='-', linewidth=5)
        lc.set_array(color)

        line = ax.add_collection(lc)

        cbaxes     = fig.add_axes([0.25, 0.05, 0.5, 0.05])
        normlegend = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
        legend     = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap, orientation="horizontal")

        plt.show()

if __name__ == "__main__":
    year         = USER_YEAR_INPUT
    grand_prix   = USER_GRAND_PRIX_INPUT
    session_type = USER_SESSION_TYPE_INPUT
    driver_codes = USER_MULTI_DRIVER_INPUT

    telemetry_data_fetcher = OneDriverFastestLapFetcher(year=year, grand_prix=grand_prix, session_type=session_type, driver_codes=driver_codes)
    event, lap = telemetry_data_fetcher.fetch_data()

    OneDriverFastestLapTrackSpeedPlotter.plot_telemetry(event, lap)
