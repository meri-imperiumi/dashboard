# -*- coding:utf-8 -*-
signalk_host = 'localhost'
signalk_port = 80
dashboard = {
    'name': 'Curiosity',
    'time_format': '%H:%M',
    'assets': {
        'display_font': 'nasalization-rg.ttf',
        'body_font': 'Eurostile.ttf',
        'splash': 'voronoi1-splash.bmp'
    },
    'loading': {},
    'default': {
        # Main, max 3
        'navigation.speedOverGround': {
            'label': 'SOG',
            'unit': 'kn',
            'conversion': 'm/s',
            'max_age': 30
        },
        'navigation.courseOverGroundTrue': {
            'label': 'COG',
            'unit': '°',
            'conversion': 'rad',
            'max_age': 20
        },
        'environment.depth.belowTransducer': {
            'label': 'Depth',
            'unit': 'm',
            'conversion': 'm',
            'max_age': 20
        },
        # Additional, max 4
        'environment.outside.temperature': {
            'label': 'Temp',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 60
        },
        'environment.outside.pressure': {
            'label': 'Baro',
            'unit': 'hPa',
            'conversion': 'Pa',
            'max_age': 60
        },
        'environment.outside.humidity': {
            'label': 'Humid',
            'unit': '%',
            'conversion': '%',
            'max_age': 60
        },
        'environment.inside.salon.temperature': {
            'label': 'Inside',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 60
        }
    },
   'moored': {
        # Main, max 3
        'environment.outside.temperature': {
            'label': 'Temp',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 60
        },
        'environment.outside.pressure': {
            'label': 'Baro',
            'unit': 'hPa',
            'conversion': 'Pa',
            'max_age': 60
        },
        'environment.outside.humidity': {
            'label': 'Humid',
            'unit': '%',
            'conversion': '%',
            'max_age': 60
        },
        # Additional, max 4
        'environment.inside.salon.temperature': {
            'label': 'Inside',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 60
        },
        'environment.inside.refrigerator.temperature': {
            'label': 'Fridge',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 60
        },
        'environment.inside.freezer.temperature': {
            'label': 'Champagne',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 60
        },
        'environment.inside.engineRoom.temperature': {
            'label': 'Beer',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 60
        }
   },
   'anchored': {
        # Main, max 3
        'navigation.anchor.currentRadius': {
            'label': 'Anchor',
            'unit': 'm',
            'conversion': 'm',
            'max_age': 10
        },
        'environment.outside.temperature': {
            'label': 'Temp',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 60
        },
        'environment.outside.pressure': {
            'label': 'Baro',
            'unit': 'hPa',
            'conversion': 'Pa',
            'max_age': 60
        },
        # Additional, max 4
        'environment.outside.humidity': {
            'label': 'Humid',
            'unit': '%',
            'conversion': '%',
            'max_age': 60
        },
        'environment.inside.salon.temperature': {
            'label': 'Inside',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 60
        },
        'environment.inside.refrigerator.temperature': {
            'label': 'Fridge',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 60
        },
        'environment.inside.freezer.temperature': {
            'label': 'Champagne',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 60
        }
   },
  'sailing': {
        # Main, max 3
        'navigation.speedOverGround': {
            'label': 'SOG',
            'unit': 'kn',
            'conversion': 'm/s',
            'max_age': 30
        },
        'navigation.courseOverGroundTrue': {
            'label': 'COG',
            'unit': '°',
            'conversion': 'rad',
            'max_age': 20
        },
        'environment.outside.pressure': {
            'label': 'Baro',
            'unit': 'hPa',
            'conversion': 'Pa',
            'max_age': 60
        },
        # Additional, max 4
        'environment.outside.temperature': {
            'label': 'Temp',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 60
        },
        'environment.outside.humidity': {
            'label': 'Humid',
            'unit': '%',
            'conversion': '%',
            'max_age': 60
        },
        'environment.inside.salon.temperature': {
            'label': 'Inside',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 60
        },
        'environment.inside.refrigerator.temperature': {
            'label': 'Fridge',
            'unit': '°C',
            'conversion': 'K',
            'max_age': 60
        }
  }
# 'motoring';
}
