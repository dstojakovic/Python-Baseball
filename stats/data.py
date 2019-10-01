import os
import glob
import logging
import pandas as pd

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


game_files = glob.glob(os.path.join(os.getcwd(), 'games', '*.EVE'))
# sort filenames
game_files.sort()

logger.info('Loaded %s game file names.', len(game_files))

column_names = [
        ]

game_frames = []
for game_file in game_files:
    # load each csv file into pandas data frame
    game_frame = pd.read_csv(
            game_file,
            names=[
                'type',
                'multi2',
                'multi3',
                'multi4',
                'multi5',
                'multi6',
                'event',
                ])
    game_frames.append(game_frame)

logger.info('Loaded %s game frames.', len(game_frames))
# Concatenate DataFrames
games = pd.concat(game_frames)

# Clean Values
games.loc[games['multi5'] == '??', 'multi5'] = ''

# Extract Identifiers
identifiers = games['multi2'].str.extract(r'(.LS(\d{4})\d{5})')
# identifiers has 2 columns now
# print(identifiers.head())

# Forward Fill Identifiers
identifiers = identifiers.fillna(method='ffill')
# print(identifiers.head())

# Rename Columns
identifiers.columns = ['game_id', 'year']
# print(identifiers.head())

# Concatenate Identifier Columns
games = pd.concat([games, identifiers], axis=1, sort=False)

# Fill NaN Values
games = games.fillna(' ')

# Categorical Event Type
games.loc[:, 'type'] = pd.Categorical(games.loc[:, 'type'])

# Print DataFrame
# print(games.head())
