# -*- coding: utf-8 -*-
import pandas as pd
import plotly.io as pio
import numpy as np

number = 15
duration = 1000


def gen_color(country_data):
    color_country = {}
    for date, country in country_data.items():
        for _ in country['country']:
            if _ not in color_country:
                color_country[_] = f'rgb({np.random.randint(0,256)}, {np.random.randint(0,256)}, {np.random.randint(0,256)})'

    return color_country


def gen_data():
    cov_data = pd.read_csv('time_series_covid19_confirmed_global.csv')
    # 删除['Lat', 'Long']列
    cov_data = cov_data.drop(['Province/State', 'Lat', 'Long'], axis=1)
    # 对每个国家每日总数进行统计
    cov_data = cov_data.groupby(['Country/Region']).sum()
    # 计算每日全球总确诊人数
    cov_data.loc['Row_sum'] = cov_data.apply(lambda x: x.sum())
    all_top_countries = {}
    for i in cov_data.columns:
        #  统计每日总数前15的国家
        data_i = cov_data.sort_values(by=i, ascending=False)
        data_i = data_i[i]
        all_top_countries[i] = {'country': data_i.index.tolist()[1:number], 'confirmed': data_i.tolist()[1:number], 'total':data_i.tolist()[0]}

    return all_top_countries


def plot_animate(dict_data, color_country):
    first_record = dict_data[list(dict_data.keys())[0]]
    figure = {
      'data': [{
        'type': 'bar',
        'x':  first_record['confirmed'],
        'y':  first_record['country'],
        'orientation': 'h',
        'width': 0.7,
        'text': [i + ', ' + str(j) for i, j in zip(first_record['country'], first_record['confirmed'])],
        'textfont': {
            'family': 'Arial',
        },
        'textposition': 'outside',
        'marker': {
              'color': [color_country[i] for i in first_record['country']],
          }
      }],
      'layout': {
        "autosize": True,
        "height": 880,
        # "width": 1200,
        'xaxis': {
          'gridcolor': '#FFFFFF',
          'linecolor': '#000',
          'linewidth': 1,
          'zeroline': False,
          'side': 'top',
        },
        'yaxis': {
          'gridcolor': '#FFFFFF',
          'linecolor': '#000',
          'linewidth': 1,
          'autorange': 'reversed'  # Y 轴倒置
        },
        'title': 'Global Countries Confirmed top {} (Data updated once a week) '.format(number),
        'hovermode': 'closest',
        'template': "plotly_white",
        'updatemenus': [{
          "type": "buttons",
          'buttons': [{
              'label': 'Play',
              'method': 'animate',
              'args': [None, {
                'frame': {
                  'duration': duration,
                  'redraw': True
                },
                'fromcurrent': True,
                "mode": "immediate",
                'transition': {
                  'duration': duration,
                  'easing':'quadratic-in-out' # 'easeOutQuad'  #'easeOutSine' # 'easeInSine' #'quadratic-in-out'
                }
              }]
            },
            {
              'label': 'Stop',
              'method': 'animate',
              "args": [[None],
                         {"frame": {"duration": 0, "redraw": False},
                          "mode": "immediate",
                          "transition": {"duration": 0}}]
            }
          ],
          'direction': 'left',
          'pad': {
            'r': 20,
            't': 87
          },
          'showactive': False,
          'x': 0.05,
          'xanchor': 'right',
          'y': 0,
          'yanchor': 'top'
        }],
        'sliders': []
      },
      'frames': [],
    }
    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Date:",
            "visible": True,
            "xanchor": "left",
        },
        "transition": {"duration": duration, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.05,
        "y": 0,
        "steps": []
    }
    for date, date_data in dict_data.items():
        frame = {
            'data': [{
                'type': 'bar',
                'x': date_data['confirmed'],
                'y': date_data['country'],
                'text':  [i + ', ' + str(j) for i, j in zip(date_data['country'], date_data['confirmed'])],
                'marker': {
                    'color': [color_country[i] for i in date_data['country']],
                },
                'textfont': {
                    'family': 'Arial',
                    'size': 10
                },
            }],
            'name': str(date),
            'layout': {
                'title': 'Global Countries Confirmed top {} (Data updated once a week) '.format(number) + '<br> total:'+ str(date_data['total']) ,
            }
        }
        figure['frames'].append(frame)
        slider_step = {
            'args': [
                [date],
                {
                    'frame': {
                        'duration': duration,
                        'redraw': True
                    },
                    'mode': 'immediate',
                    'transition': {
                        'duration': duration
                    }
                }
            ],
            'label': date,
            'method': 'animate'
        }

        sliders_dict['steps'].append(slider_step)

    figure['layout']['sliders'] = [sliders_dict]
    # To display the figure defined by this dict, use the low-level plotly.io.show function
    pio.show(figure)


if __name__ == "__main__":
    data = gen_data()
    # print(data)
    color_countries = gen_color(data)
    plot_animate(data, color_countries)



