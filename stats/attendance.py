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

# Select Attendance
attendance = games.loc[
        (games['type'] == 'info') & (games['multi2'] == 'attendance'),
        ['year', 'multi3']
        ]
logger.info(
        'Attendance dataframe %s row(s); %s column(s).',
        len(attendance), len(attendance.columns)
        )

# Column Labels
attendance.columns = ['year', 'attendance']
logger.info(
        'Attendance dataframe column(s) name(s): %s.',
        ', '.join(attendance.columns)
        )

# Convert to Numeric
attendance.loc[:, 'attendance'] = pd.to_numeric(
        attendance.loc[:, 'attendance']
        )

logger.debug(
        'Column attendance type: %s.', attendance.loc[:, 'attendance'].dtype
        )

# Plot DataFrame
attendance.plot(x='year', y='attendance', figsize=(15, 7), kind='bar')
# Axis Labels
plt.xlabel('Year')
plt.xlabel('Attendance')
plt.show()

# Mean Line
plt.axhline(
        label=attendance['attendance'].mean(),
        linestyle='dashed',
        color='green'
        )
