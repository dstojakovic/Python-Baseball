import os
import glob
import logging
import pandas as pd

# logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s [%(pathname)s:%(lineno)d]')
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


game_files = glob.glob(os.path.join(os.getcwd(), 'games', '*.EVE'))
# sort filenames
game_files.sort()

logger.info('Loaded %s game files.', len(game_files))

names = ['type', 'multi2', 'multi3', 'multi4', 'multi5', 'multi6', 'event']

game_frames = []
for game_file in game_files:
    # read csv file
    game_frame = pd.read_csv(game_file, names=names)
    game_frames.append(game_frame)

# Concatenate DataFrames
games = pd.concat(game_frames)
# Clean Values
games.loc[games['multi5'] == '??', 'multi5'] = ''
# Extract Identifiers
identifiers = games['multi2'].str.extract(r'(.LS(\d{4}\d{5}))')
# identifiers has 2 columns now
# Forward Fill Identifiers
identifiers = identifiers.fillna(method='ffill')
# Rename Columns
identifiers.columns = ['game_id', 'year']
# Concatenate Identifier Columns
games = pd.concat([games, identifiers], axis=1, sort=False)
# Fill NaN Values
games = games.fillna(' ')
# Categorical Event Type
games.loc[:, 'type'] = pd.Categorical(games.loc[:, 'type'])
# Print DataFrame
print(games.head())
