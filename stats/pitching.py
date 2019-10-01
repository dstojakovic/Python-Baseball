import logging
import pandas as pd
import matplotlib.pyplot as plt
from data import games

# logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_format = '%(asctime)s - %(name)s - %(levelname)s'
log_format += ' - %(message)s [%(pathname)s:%(lineno)d]'
formatter = logging.Formatter(log_format)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# Select All Plays
plays = games[games['type'] == 'play']
logger.debug(
        'Plays data frame %s column(s): %s.',
        len(plays.columns), ', '.join(plays.columns)
        )

# Select All Strike Outs
# strike_outs = plays[plays['event'] == 'K']
strike_outs = plays[plays['event'].str.contains('K')]
logger.info('Strikeouts data frame: %s.', len(strike_outs))

# Group by Year and Game
strike_outs = strike_outs.groupby(['year', 'game_id']).size()
logger.info('Strikeouts grouped by %s and %s.', 'year', 'group_id')

# Reset Index
strike_outs = strike_outs.reset_index(name='strike_outs')
logger.info('Strikeouts data frame: %s.', len(strike_outs))

# Apply an Operation to Multiple Columns
logger.debug('Change columns to numeric.')
strike_outs = strike_outs.loc[:, ['year', 'strike_outs']].apply(pd.to_numeric)

# Change Plot Formatting
strike_outs.plot(
        x='year',
        y='strike_outs',
        kind='scatter').legend('Strike Outs')
plt.show()
