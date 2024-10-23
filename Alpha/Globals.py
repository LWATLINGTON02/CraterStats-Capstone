import os

PATH = os.path.dirname(os.path.abspath(__file__))

chron_systems = {
    # Moon Systems
    "Moon, Neukum (1983)": ["Moon, Neukum (1983)",
                            "Moon, Neukum (1983)"],
    "Moon, Neukum et al. (2001)": ['Moon, Neukum et al. (2001)',
                                   'Moon, Neukum et al. (2001)'],
    "Moon, Hartmann 2010 iteration": ['Moon, Hartmann 2010 iteration',
                                      'Moon, Hartmann 2010 iteration'],
    "Moon, Yue et al. (2022)": ["Moon, Yue et al. (2022)",
                                "Moon, Nuekem et al. (2001)"],
    # Mars systems
    "Mars, Neukum-Ivanov 2001": ['Mars, Hartmann & Neukum (2001)',
                                 'Mars, Ivanov (2001)'],
    "Mars, Ivanov 2001": ['Mars, Ivanov (2001)',
                          'Mars, Ivanov (2001)'],
    "Mars, Hartmann 2004 iteration": ['Mars, Hartmann (2005) [Michael (2013)]',
                                      'Mars, Hartmann (2005)'],
    "Mars, Hartmann & Daubar (2016)": ['Mars, Hartmann (2005) [Michael (2013)]',
                                       'Mars, Hartmann & Daubar (2016)'],
    # Mercury Systems
    "Mercury, Strom & Neukum (1988)": ['Mercury, Strom & Neukum (1988)',
                                       'Mercury, Strom & Neukum (1988)'],
    'Mercury, Neukum et al. (2001)': ['Mercury, Neukum et al. (2001)',
                                      'Mercury, Neukum et al. (2001)'],
    'Mercury, Le Feuvre and Wieczorek 2011 non-porous': ['Mercury, Le Feuvre and Wieczorek (2011) non-porous',
                                                         'Mercury, Le Feuvre and Wieczorek (2011) non-porous'],
    'Mercury, Le Feuvre and Wieczorek 2011 porous': ['Mercury, Le Feuvre and Wieczorek (2011) porous',
                                                     'Mercury, Le Feuvre and Wieczorek (2011) porous'],
    ### SMALL BODIES ###
    # Vesta
    'Vesta, Rev4, Schmedemann et al (2014)': ['Vesta, Rev4, Schmedemann et al (2014)',
                                              'Vesta, Rev4, Schmedemann et al (2014)'],
    'Vesta, Rev3, Schmedemann et al (2014)': ['Vesta, Rev3, Schmedemann et al (2014)',
                                              'Vesta, Rev3, Schmedemann et al (2014)'],
    "Vesta, Marchi & O'Brien (2014)": ["Vesta, O'Brien et al. (2014)",
                                       'Vesta, Marchi et al (2013) [inferred, NS]'],
    # Ceres
    'Ceres, Hiesinger et al. (2016)': ['Ceres, Hiesinger et al. (2016)',
                                       'Ceres, Hiesinger et al. (2016)'],

    # Ida
    'Ida, Schmedemann et al (2014)': ['Ida, Schmedemann et al (2014)',
                                      'Ida, Schmedemann et al (2014)'],

    # Gaspra
    'Gaspra, Schmedemann et al (2014)': ['Gaspra, Schmedemann et al (2014)',
                                         'Gaspra, Schmedemann et al (2014)'],

    # Lutetia
    'Lutetia, Schmedemann et al (2014)': ['Lutetia, Schmedemann et al (2014)',
                                          'Lutetia, Schmedemann et al (2014)'],

    # Phobos
    'Phobos, Case A - SOM, Schmedemann et al (2014)': ['Phobos, Case A - SOM, Schmedemann et al (2014)',
                                                       'Phobos, Case A - SOM, Schmedemann et al (2014)'],
    'Phobos, Case B - MBA, Schmedemann et al (2014)': ['Phobos, Case B - MBA, Schmedemann et al (2014)',
                                                       'Phobos, Case B - MBA, Schmedemann et al (2014)']

}

colours = ['Black', 'Red', 'Green', 'Blue', 'Yellow',
           'Violet', 'Grey', 'Brown', 'Orange', 'Pink', 'Purple', 'Teal']

symbols = ['Square', 'Circle', 'Star', 'Triangle', 'Diagonal cross',
           'Cross', 'Point', 'Inverted triangle', 'Filled square',
           'Filled circle', 'Filled star', 'Filled triangle', 'Filled inverted triangle']

plots_dict = {}


template_file = PATH + '/craterstats_config_files/default.plt'

template_dict = {
    "set": [{"format": {"png"}}],
    "plot": [],
}

"""
DEMO CAROUSEL GLBOALS
"""
demo_mode = False
image_index = 0
demo_cmd_str = ''
