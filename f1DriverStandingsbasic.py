import pandas as pd
import plotly.express as px
from fastf1.ergast import Ergast
from commonf1 import *

class F1DataFetcher:
    def __init__(self, year):
        self.year   = year
        self.ergast = Ergast()

    def fetch_data(self):
        races   = self.ergast.get_race_schedule(self.year)
        results = []

        for rnd, race in races['raceName'].items():
            temp = self._get_race_results(rnd)
            temp = self._process_sprint_results(rnd, temp)
            temp = self._add_additional_info(rnd, race, temp)
            results.append(temp)

        results = pd.concat(results)
        races   = results['race'].drop_duplicates()
        results = results.pivot(index='driverCode', columns='round', values='points')
        results = self._rank_drivers(results)
        results.columns = races

        return results

    def _get_race_results(self, rnd):
        temp = self.ergast.get_race_results(year=self.year, round=rnd + 1)
        return temp.content[0]

    def _process_sprint_results(self, rnd, temp):
        sprint = self.ergast.get_sprint_results(year=self.year, round=rnd + 1)
        if sprint.content and sprint.description['round'][0] == rnd + 1:
            sprint_results = sprint.content[0]
            merged_results = pd.merge(temp, sprint_results, on='driverCode', suffixes=('_race', '_sprint'))
            merged_results['points'] = merged_results['points_race'] + merged_results['points_sprint']
            merged_results.drop(columns=['points_race', 'points_sprint'], inplace=True)
            return merged_results
        else:
            return temp

    def _add_additional_info(self, rnd, race, temp):
        temp['round'] = rnd + 1
        temp['race'] = race.removesuffix(' Grand Prix')
        return temp[['round', 'race', 'driverCode', 'points']]

    def _rank_drivers(self, results):
        results['total_points'] = results.sum(axis=1)
        results = results.sort_values(by='total_points', ascending=False)
        results.drop(columns='total_points', inplace=True)
        return results


class F1DataPlotter:
    @staticmethod
    def plot_heatmap(data):
        fig = px.imshow(data, 
                        text_auto=True, 
                        aspect='auto',
                        labels={'x': 'Race', 'y': 'Driver', 'color': 'Points'},
                        color_continuous_scale=[[   0, BLUE_SCALE['very_light_blue']],
                                                [0.25, BLUE_SCALE['light_blue']],
                                                [ 0.5, BLUE_SCALE['blue']],
                                                [0.75, BLUE_SCALE['dark_blue']],
                                                [   1, BLUE_SCALE['very_dark_blue']]]
        )

        fig.update_xaxes(title_text='', 
                         showgrid=False, 
                         showline=False)
        
        fig.update_yaxes(title_text='', 
                         tickmode='linear', 
                         showgrid=True, 
                         gridwidth=1,
                         gridcolor='LightGrey', 
                         showline=False, 
                         tickson='boundaries')
        
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', 
                          coloraxis_showscale=False,
                          xaxis=dict(side='top'), 
                          margin=dict(l=0,r=0,t=0,b=0))

        fig.show()


if __name__ == "__main__":
    year         = USER_YEAR_INPUT
    data_fetcher = F1DataFetcher(season=year)
    f1_data      = data_fetcher.fetch_data()

    F1DataPlotter.plot_heatmap(f1_data)
