from commonf1 import *
from matplotlib import pyplot as plt
import fastf1 as ff1
import fastf1.plotting

fastf1.plotting.setup_mpl(misc_mpl_mods=False)


class MultiDriverFastestLapFetcher:
    def __init__(self, year, grand_prix, session_type):
        self.year         = year
        self.grand_prix   = grand_prix
        self.session_type = session_type

    def fetch_data(self, driver_codes):
        driver_data = {}
        session     = ff1.get_session(self.year, self.grand_prix, self.session_type)
        session.load(weather=False)

        for driver_code in driver_codes:
            driver_lap               = session.laps.pick_driver(driver_code).pick_fastest()
            driver_tel               = driver_lap.get_car_data().add_distance()
            driver_data[driver_code] = driver_tel

        return driver_data, session.event['EventName'], session.event.year

class MultiDriverFastestLapPlotter:
    @staticmethod
    def plot_telemetry(driver_data_dict, event_name, year, driver_codes, session_type):
        fig, ax = plt.subplots()

        for driver_code, driver_data in driver_data_dict.items():
            driver_color = DRIVER_TEAM_COLORS.get(driver_code, 'black')
            ax.plot(driver_data['Distance'], 
                    driver_data['Speed'], 
                    color=driver_color, 
                    label=driver_code)

        ax.set_xlabel('Distance in m')
        ax.set_ylabel('Speed in km/h')

        ax.legend()
        plt.suptitle(f"Fastest Lap Comparison: {', '.join(driver_codes)} \n"
                     f"{event_name} {year} {session_type}")
        plt.show()

if __name__ == "__main__":
    year         = USER_YEAR_INPUT
    grand_prix   = USER_GRAND_PRIX_INPUT
    session_type = USER_SESSION_TYPE_INPUT
    driver_codes = USER_MULTI_DRIVER_INPUT 

    telemetry_fetcher = MultiDriverFastestLapFetcher(year=year, grand_prix=grand_prix, session_type=session_type)
    driver_data_dict, event_name, year = telemetry_fetcher.fetch_data(driver_codes)

    MultiDriverFastestLapPlotter.plot_telemetry(driver_data_dict, event_name, year, driver_codes, session_type)
