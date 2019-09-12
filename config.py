# -*- coding:utf-8 -*-
dashboard = {
    'name': 'Curiosity',
    'time_format': '%H:%M',
    'assets': {
        'display_font': 'nasalization-rg.ttf',
        'body_font': 'Eurostile.ttf'
    },
    'loading': {},
    'default': {
        'environment.inside.salon.temperature': {
            'label': 'Temp',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 60
        },
        'environment.inside.salon.pressure': {
            'label': 'Baro',
            'unit': 'hPa',
            'conversion': 'Pa',
            'max_age': 60
        },
        'environment.inside.salon.humidity': {
            'label': 'Humid',
            'unit': '%',
            'conversion': 'int',
            'max_age': 60
        }
    }
}
