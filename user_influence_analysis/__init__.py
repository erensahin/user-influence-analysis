"""
BLG517E - Spring 2019 Term Project
User Influence Analysis for GitHub Developer Social Networks
Sefa Eren Sahin
504171526
"""

import os
import yaml

try:
    with open(os.path.join(os.path.dirname(__file__), 'secret_config.yaml'), 'r') as ymlfile:
        secret_config = yaml.load(ymlfile, Loader=yaml.SafeLoader)
except FileNotFoundError as e:
    print(e)
    print('Please provide secret_config.yaml file.')
except Exception as e:
    print(e)
