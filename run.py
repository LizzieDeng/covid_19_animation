import plotly.io as pio

years = ['2010', '2011', '2012']
items = ['A', 'B', 'C', 'D']
count = [
  [1, 2, 3, 4],
  [2, 3, 4, 1],
  [3, 4, 1, 2]
]


figure = {
  'data': [{
    'type': 'bar',
    'x': count[0],
    'y': items,
    'name':'SF Zoo',
    'orientation': 'h',
    'width': 0.1,
    'text': count[0],
    'textposition': 'outside'
  }],
  'layout': {
    'xaxis': {
      'gridcolor': '#FFFFFF',
      'linecolor': '#000',
      'linewidth': 1,
      'zeroline': False,
      # 'autorange': False
    },
    'yaxis': {
      'gridcolor': '#FFFFFF',
      'linecolor': '#000',
      'linewidth': 1,
    },
    'title': 'Example Title',
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


for index, year in enumerate(years):
    frame = {
        'data': [{
          'type': 'bar',
          'x': count[index],
          'y': items,
        }],
        'name': str(year)
        }
    figure['frames'].append(frame)

    slider_step = {
      'args': [
        [year],
        {
          'frame': {
            'duration': 300,
            'redraw': True
          },
          'mode': 'immediate',
          'transition': {
            'duration': 300
          }
        }
      ],
      'label': year,
      'method': 'animate'
    }
    # sliders_dict['steps'].append(slider_step)

# figure['layout']['sliders'] = [sliders_dict]


# To display the figure defined by this dict, use the low-level plotly.io.show function
pio.show(figure)
