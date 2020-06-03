# -*- coding: utf-8 -*- 
"""
Project: covid_19_animation
Creator: Administrator
Create time: 2020-06-03 10:52
IDE: PyCharm
Introduction:
"""
import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio
import numpy as np

def gen_data():
    data = pd.read_csv('time_series_covid19_confirmed_global.csv')
    # 删除['Lat', 'Long']列
    data = data.drop(['Province/State', 'Lat', 'Long'], axis=1)
    # 对每个国家每日总数进行统计
    data = data.groupby(['Country/Region']).sum()
    # data.to_csv('sum_country.csv')
    # 统计每日总数前20的国家
    all_top20_country = {}
    for i in data.columns:
        data_i = data.sort_values(by=i, ascending=False)
        data_i = data_i[i]
        all_top20_country[i] = {'country': data_i.index.tolist()[:20], 'confirmed': data_i.tolist()[:20]}
    # print(all_top20_country, len(all_top20_country))
    return all_top20_country

# colors = ['rgba(50, 171, 96, 0.6)', 'rgba(50, 171, 96, 0.6)' ]
# y = np.array([7, 10, 12, 15, 19, 28, 25, 31, 33, 43, 50, 59, 67, 70, 73, 79, 82, 89, 93, 96])
# colors =np.array(['rgb(255,255,255)']*y.shape[0])


def plot_animate(dict_data):
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
            # 'size': 90
        },
        # 'text': dict_data[list(dict_data.keys())[0]]['country'] + dict_data[list(dict_data.keys())[0]]['confirmed'],
        'textposition': 'outside',
        'marker': {
              # 'color': colors,
              'color': 'rgba(50, 171, 96, 0.6)',
                # 'line': {
                #     'color': 'rgba(50, 171, 96, 1.0)',
                #     'width': 1
                # }
          }
      }],
      'layout': {
        'xaxis': {
          'gridcolor': '#FFFFFF',
          'linecolor': '#000',
          'linewidth': 1,
          'zeroline': False,
           # 'autorange': False,
            # 'range': []
        },
        'yaxis': {
          'gridcolor': '#FFFFFF',
          'linecolor': '#000',
          'linewidth': 1,
          'autorange' :'reversed'  # Y 轴倒置
        },
        'title': 'Covid confirmed top 20 countries',
        'hovermode': 'closest',
        'template': "plotly_white",
        'updatemenus': [{
          'type': 'buttons',
          'buttons': [{
              'label': 'Play',
              'method': 'animate',
              'args': [None, {
                'frame': {
                  'duration': 200,
                  'redraw': True
                },
                'fromcurrent': True,
                'transition': {
                  'duration': 300,
                  'easing': 'quadratic-in-out'
                }
              }]
            },
            {
              'label': 'End',
              'method': 'animate',
              'args': [None, {
                'frame': {
                  'duration': 0,
                  'redraw': True
                },
                'fromcurrent': True,
                'mode': 'immediate',
                'transition': {
                  'duration': 0
                }
              }]
            }
          ],
          'direction': 'left',
          'pad': {
            'r': 10,
            't': 87
          },
          'showactive': False,
          'type': 'buttons',
          'x': 0.1,
          'xanchor': 'right',
          'y': 0,
          'yanchor': 'top'
        }]
      },
      'frames': []
    }

    for date, date_data in dict_data.items():
        frame = {
            'data': [{
                'type': 'bar',
                'x': date_data['confirmed'],
                'y': date_data['country'],
                'text':  [i + ', ' + str(j) for i, j in zip(date_data['country'], date_data['confirmed'])],
                'marker': {
                    'color': 'rgba(50, 171, 96, 0.6)',
                },
                'textfont': {
                    'family': 'Arial',
                    # 'size': 10
                },
            }],
            'name': str(date)
        }
        figure['frames'].append(frame)
    pio.show(figure)


if __name__ == "__main__":
    data = gen_data()
    plot_animate(data)



