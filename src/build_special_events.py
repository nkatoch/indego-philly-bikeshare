"""Build data/special_events.csv from curated Philadelphia event dates.

Sources:
- Phillies + Eagles home games: Wikipedia season pages (2022-2025)
- Festivals + academic events: approximate annual dates from public calendars

Run from project root:  python src/build_special_events.py
"""
from pathlib import Path
import pandas as pd

OUT = Path(__file__).resolve().parent.parent / 'data' / 'special_events.csv'


# ---------------------------------------------------------------- Phillies ---
PHILLIES_HOME_2022 = [
    ('2022-04-11', 'Mets'), ('2022-04-12', 'Mets'), ('2022-04-13', 'Mets'),
    ('2022-04-22', 'Brewers'), ('2022-04-23', 'Brewers'), ('2022-04-24', 'Brewers'),
    ('2022-04-25', 'Rockies'), ('2022-04-26', 'Rockies'), ('2022-04-27', 'Rockies'), ('2022-04-28', 'Rockies'),
    ('2022-04-30', 'Mets'), ('2022-05-05', 'Mets'), ('2022-05-08', 'Mets DH'),
    ('2022-05-17', 'Padres'), ('2022-05-18', 'Padres'), ('2022-05-19', 'Padres'),
    ('2022-05-20', 'Dodgers'), ('2022-05-21', 'Dodgers'), ('2022-05-22', 'Dodgers'),
    ('2022-05-23', 'Braves'),
    ('2022-05-30', 'Giants'), ('2022-05-31', 'Giants'), ('2022-06-01', 'Giants'),
    ('2022-06-03', 'Angels'), ('2022-06-04', 'Angels'), ('2022-06-05', 'Angels'),
    ('2022-06-10', 'Diamondbacks'), ('2022-06-11', 'Diamondbacks'), ('2022-06-12', 'Diamondbacks'),
    ('2022-06-13', 'Marlins'), ('2022-06-14', 'Marlins'), ('2022-06-15', 'Marlins'),
    ('2022-06-28', 'Braves'), ('2022-06-29', 'Braves'), ('2022-06-30', 'Braves'),
    ('2022-07-01', 'Cardinals'), ('2022-07-02', 'Cardinals'), ('2022-07-03', 'Cardinals'),
    ('2022-07-05', 'Nationals'), ('2022-07-06', 'Nationals'), ('2022-07-07', 'Nationals'),
    ('2022-07-22', 'Cubs'), ('2022-07-23', 'Cubs'), ('2022-07-24', 'Cubs'),
    ('2022-07-25', 'Braves'), ('2022-07-26', 'Braves'), ('2022-07-27', 'Braves'),
    ('2022-08-04', 'Nationals'), ('2022-08-05', 'Nationals'),
    ('2022-08-06', 'Nationals'), ('2022-08-07', 'Nationals'),
    ('2022-08-09', 'Marlins'), ('2022-08-10', 'Marlins'), ('2022-08-11', 'Marlins'),
    ('2022-08-19', 'Mets'), ('2022-08-20', 'Mets DH'), ('2022-08-21', 'Mets'),
    ('2022-08-22', 'Reds'), ('2022-08-23', 'Reds'),
    ('2022-08-24', 'Reds'), ('2022-08-25', 'Reds'),
    ('2022-08-26', 'Pirates'), ('2022-08-27', 'Pirates'), ('2022-08-28', 'Pirates'),
    ('2022-09-06', 'Marlins'), ('2022-09-07', 'Marlins'), ('2022-09-08', 'Marlins'),
    ('2022-09-09', 'Nationals'), ('2022-09-10', 'Nationals'), ('2022-09-11', 'Nationals'),
    ('2022-09-20', 'Blue Jays'), ('2022-09-21', 'Blue Jays'),
    ('2022-09-22', 'Braves'), ('2022-09-23', 'Braves'), ('2022-09-24', 'Braves'), ('2022-09-25', 'Braves'),
    # Postseason home games
    ('2022-10-14', 'Braves NLDS'), ('2022-10-15', 'Braves NLDS'),
    ('2022-10-21', 'Padres NLCS'), ('2022-10-22', 'Padres NLCS'),
    ('2022-10-25', 'Padres NLCS'),
    ('2022-11-02', 'Astros WS'),
]

PHILLIES_HOME_2023 = [
    ('2023-04-07', 'Reds'), ('2023-04-08', 'Reds'), ('2023-04-09', 'Reds'),
    ('2023-04-10', 'Marlins'), ('2023-04-11', 'Marlins'), ('2023-04-12', 'Marlins'),
    ('2023-04-21', 'Rockies'), ('2023-04-22', 'Rockies'), ('2023-04-23', 'Rockies'),
    ('2023-04-26', 'Mariners'), ('2023-04-27', 'Mariners'),
    ('2023-05-07', 'Red Sox'),
    ('2023-05-09', 'Blue Jays'), ('2023-05-10', 'Blue Jays'),
    ('2023-05-19', 'Cubs'), ('2023-05-20', 'Cubs'), ('2023-05-21', 'Cubs'),
    ('2023-05-22', 'Diamondbacks'), ('2023-05-23', 'Diamondbacks'), ('2023-05-24', 'Diamondbacks'),
    ('2023-06-09', 'Dodgers'), ('2023-06-10', 'Dodgers'), ('2023-06-11', 'Dodgers'),
    ('2023-06-23', 'Mets'), ('2023-06-24', 'Mets'), ('2023-06-25', 'Mets'),
    ('2023-06-30', 'Nationals'), ('2023-07-01', 'Nationals'), ('2023-07-02', 'Nationals'),
    ('2023-07-14', 'Padres'), ('2023-07-15', 'Padres DH'), ('2023-07-16', 'Padres'),
    ('2023-07-18', 'Brewers'), ('2023-07-19', 'Brewers'), ('2023-07-20', 'Brewers'),
    ('2023-07-24', 'Orioles'), ('2023-07-25', 'Orioles'), ('2023-07-26', 'Orioles'),
    ('2023-08-03', 'Marlins'),
    ('2023-08-04', 'Royals'), ('2023-08-05', 'Royals'), ('2023-08-06', 'Royals'),
    ('2023-08-08', 'Nationals DH'), ('2023-08-09', 'Nationals'), ('2023-08-10', 'Nationals'),
    ('2023-08-11', 'Twins'), ('2023-08-12', 'Twins'), ('2023-08-13', 'Twins'),
    ('2023-08-21', 'Giants'), ('2023-08-22', 'Giants'), ('2023-08-23', 'Giants'),
    ('2023-08-25', 'Cardinals'), ('2023-08-26', 'Cardinals'), ('2023-08-27', 'Cardinals'),
    ('2023-08-28', 'Angels'), ('2023-08-29', 'Angels'), ('2023-08-30', 'Angels'),
    ('2023-09-08', 'Marlins'), ('2023-09-09', 'Marlins'), ('2023-09-10', 'Marlins'),
    ('2023-09-11', 'Braves DH'), ('2023-09-12', 'Braves'), ('2023-09-13', 'Braves'),
    ('2023-09-21', 'Mets'), ('2023-09-22', 'Mets'), ('2023-09-23', 'Mets'), ('2023-09-24', 'Mets'),
    # Postseason
    ('2023-10-03', 'Marlins WC'), ('2023-10-04', 'Marlins WC'),
    ('2023-10-11', 'Braves NLDS'), ('2023-10-12', 'Braves NLDS'),
    ('2023-10-16', 'Diamondbacks NLCS'), ('2023-10-17', 'Diamondbacks NLCS'),
    ('2023-10-23', 'Diamondbacks NLCS'), ('2023-10-24', 'Diamondbacks NLCS'),
]

PHILLIES_HOME_2024 = [
    ('2024-03-29', 'Braves'), ('2024-03-30', 'Braves'), ('2024-03-31', 'Braves'),
    ('2024-04-01', 'Reds'), ('2024-04-02', 'Reds'), ('2024-04-03', 'Reds'),
    ('2024-04-11', 'Pirates'), ('2024-04-12', 'Pirates'), ('2024-04-13', 'Pirates'), ('2024-04-14', 'Pirates'),
    ('2024-04-15', 'Rockies'), ('2024-04-16', 'Rockies'), ('2024-04-17', 'Rockies'),
    ('2024-04-19', 'White Sox'), ('2024-04-20', 'White Sox'), ('2024-04-21', 'White Sox'),
    ('2024-05-03', 'Giants'), ('2024-05-04', 'Giants'), ('2024-05-05', 'Giants'), ('2024-05-06', 'Giants'),
    ('2024-05-07', 'Blue Jays'), ('2024-05-08', 'Blue Jays'),
    ('2024-05-15', 'Mets'), ('2024-05-16', 'Mets'),
    ('2024-05-17', 'Nationals'), ('2024-05-18', 'Nationals'), ('2024-05-19', 'Nationals'),
    ('2024-05-21', 'Rangers'), ('2024-05-22', 'Rangers'), ('2024-05-23', 'Rangers'),
    ('2024-06-01', 'Cardinals'), ('2024-06-02', 'Cardinals'),
    ('2024-06-03', 'Brewers'), ('2024-06-04', 'Brewers'), ('2024-06-05', 'Brewers'),
    ('2024-06-09', 'Mets'),
    ('2024-06-17', 'Padres'), ('2024-06-18', 'Padres'), ('2024-06-19', 'Padres'),
    ('2024-06-21', 'Diamondbacks'), ('2024-06-22', 'Diamondbacks'), ('2024-06-23', 'Diamondbacks'),
    ('2024-06-27', 'Marlins'), ('2024-06-28', 'Marlins'),
    ('2024-06-29', 'Marlins'), ('2024-06-30', 'Marlins'),
    ('2024-07-09', 'Dodgers'), ('2024-07-10', 'Dodgers'), ('2024-07-11', 'Dodgers'),
    ('2024-07-12', 'Athletics'), ('2024-07-13', 'Athletics'), ('2024-07-14', 'Athletics'),
    ('2024-08-13', 'Marlins'), ('2024-08-14', 'Marlins'),
    ('2024-08-15', 'Nationals'), ('2024-08-16', 'Nationals'),
    ('2024-08-17', 'Nationals'), ('2024-08-18', 'Nationals'),
    ('2024-08-29', 'Braves'), ('2024-08-30', 'Braves'),
    ('2024-08-31', 'Braves'), ('2024-09-01', 'Braves'),
    ('2024-09-09', 'Rays'), ('2024-09-10', 'Rays'), ('2024-09-11', 'Rays'),
    ('2024-09-13', 'Mets'), ('2024-09-14', 'Mets'), ('2024-09-15', 'Mets'),
    ('2024-09-23', 'Cubs'), ('2024-09-24', 'Cubs'), ('2024-09-25', 'Cubs'),
    # Postseason
    ('2024-10-06', 'Mets NLDS'),
]

PHILLIES_HOME_2025 = [
    ('2025-03-31', 'Rockies'), ('2025-04-02', 'Rockies'), ('2025-04-03', 'Rockies'),
    ('2025-04-04', 'Dodgers'), ('2025-04-05', 'Dodgers'), ('2025-04-06', 'Dodgers'),
    ('2025-04-14', 'Giants'), ('2025-04-15', 'Giants'), ('2025-04-16', 'Giants'), ('2025-04-17', 'Giants'),
    ('2025-04-18', 'Marlins'), ('2025-04-19', 'Marlins'), ('2025-04-20', 'Marlins'),
    ('2025-04-29', 'Nationals'), ('2025-04-30', 'Nationals'), ('2025-05-01', 'Nationals'),
    ('2025-05-02', 'Diamondbacks'), ('2025-05-03', 'Diamondbacks'), ('2025-05-04', 'Diamondbacks'),
    ('2025-05-12', 'Cardinals'), ('2025-05-14', 'Cardinals DH'),
    ('2025-05-16', 'Pirates'), ('2025-05-17', 'Pirates'), ('2025-05-18', 'Pirates'),
    ('2025-05-27', 'Braves'), ('2025-05-29', 'Braves DH'),
    ('2025-05-30', 'Brewers'), ('2025-05-31', 'Brewers'), ('2025-06-01', 'Brewers'),
    ('2025-06-09', 'Cubs'), ('2025-06-10', 'Cubs'), ('2025-06-11', 'Cubs'),
    ('2025-06-13', 'Blue Jays'), ('2025-06-14', 'Blue Jays'), ('2025-06-15', 'Blue Jays'),
    ('2025-06-20', 'Mets'), ('2025-06-21', 'Mets'), ('2025-06-22', 'Mets'),
    ('2025-06-30', 'Padres'), ('2025-07-02', 'Padres DH'),
    ('2025-07-04', 'Reds'), ('2025-07-05', 'Reds'), ('2025-07-06', 'Reds'),
    ('2025-07-18', 'Angels'), ('2025-07-19', 'Angels'), ('2025-07-20', 'Angels'),
    ('2025-07-21', 'Red Sox'), ('2025-07-22', 'Red Sox'), ('2025-07-23', 'Red Sox'),
    ('2025-08-01', 'Tigers'), ('2025-08-02', 'Tigers'), ('2025-08-03', 'Tigers'),
    ('2025-08-04', 'Orioles'), ('2025-08-05', 'Orioles'), ('2025-08-06', 'Orioles'),
    ('2025-08-18', 'Mariners'), ('2025-08-19', 'Mariners'), ('2025-08-20', 'Mariners'),
    ('2025-08-22', 'Nationals'), ('2025-08-23', 'Nationals'), ('2025-08-24', 'Nationals'),
    ('2025-08-28', 'Braves'), ('2025-08-29', 'Braves'),
    ('2025-08-30', 'Braves'), ('2025-08-31', 'Braves'),
    ('2025-09-08', 'Mets'), ('2025-09-09', 'Mets'), ('2025-09-10', 'Mets'), ('2025-09-11', 'Mets'),
    ('2025-09-12', 'Royals'), ('2025-09-13', 'Royals'),
    ('2025-09-23', 'Marlins'), ('2025-09-24', 'Marlins'), ('2025-09-25', 'Marlins'),
    ('2025-09-26', 'Twins'),
    # Postseason
    ('2025-10-04', 'Dodgers NLDS'), ('2025-10-06', 'Dodgers NLDS'),
]


# ------------------------------------------------------------------ Eagles ---
# Each tuple lists (date, opponent) - we record the calendar year the game falls in.
EAGLES_HOME = [
    # 2022 season (Sep 2022 - Jan 2023)
    ('2022-09-19', 'Vikings'),
    ('2022-10-02', 'Jaguars'),
    ('2022-10-16', 'Cowboys'),
    ('2022-10-30', 'Steelers'),
    ('2022-11-27', 'Packers'),
    ('2022-12-04', 'Titans'),
    ('2023-01-01', 'Saints'),
    ('2023-01-08', 'Giants'),
    ('2023-01-21', 'Giants NFC Divisional'),
    ('2023-01-29', '49ers NFC Championship'),
    # 2023 season
    ('2023-09-14', 'Vikings'),
    ('2023-10-01', 'Commanders'),
    ('2023-10-22', 'Dolphins'),
    ('2023-11-05', 'Cowboys'),
    ('2023-11-26', 'Bills'),
    ('2023-12-03', '49ers'),
    ('2023-12-25', 'Giants'),
    # 2024 season
    ('2024-09-16', 'Falcons'),
    ('2024-10-13', 'Browns'),
    ('2024-10-20', 'Giants'),
    ('2024-10-27', 'Bengals'),
    ('2024-11-03', 'Jaguars'),
    ('2024-11-14', 'Commanders'),
    ('2024-12-08', 'Panthers'),
    ('2024-12-15', 'Steelers'),
    ('2024-12-29', 'Cowboys'),
    ('2025-01-05', 'Giants'),
    ('2025-01-12', 'Packers Wild Card'),
    ('2025-01-19', 'Rams NFC Divisional'),
    ('2025-01-26', 'Commanders NFC Championship'),
    # 2025 season
    ('2025-09-04', 'Cowboys'),
    ('2025-09-21', 'Rams'),
    ('2025-10-05', 'Broncos'),
    ('2025-10-26', 'Giants'),
    ('2025-11-16', 'Lions'),
    ('2025-12-14', 'Raiders'),
]


# --------------------------------------------------------------- Festivals ---
# Approximate annual dates from public Philadelphia event calendars.
FESTIVALS = [
    # Mummers Parade - January 1 each year
    ('2022-01-01', 'Mummers Parade', 'Broad Street'),
    ('2023-01-01', 'Mummers Parade', 'Broad Street'),
    ('2024-01-01', 'Mummers Parade', 'Broad Street'),
    ('2025-01-01', 'Mummers Parade', 'Broad Street'),
    # Penn Relays - last weekend of April (Thu-Sat)
    ('2022-04-28', 'Penn Relays', 'Franklin Field'),
    ('2022-04-29', 'Penn Relays', 'Franklin Field'),
    ('2022-04-30', 'Penn Relays', 'Franklin Field'),
    ('2023-04-27', 'Penn Relays', 'Franklin Field'),
    ('2023-04-28', 'Penn Relays', 'Franklin Field'),
    ('2023-04-29', 'Penn Relays', 'Franklin Field'),
    ('2024-04-25', 'Penn Relays', 'Franklin Field'),
    ('2024-04-26', 'Penn Relays', 'Franklin Field'),
    ('2024-04-27', 'Penn Relays', 'Franklin Field'),
    ('2025-04-24', 'Penn Relays', 'Franklin Field'),
    ('2025-04-25', 'Penn Relays', 'Franklin Field'),
    ('2025-04-26', 'Penn Relays', 'Franklin Field'),
    # Broad Street Run - first Sunday in May (resumed 2022 after COVID)
    ('2022-05-01', 'Broad Street Run', 'Broad Street 10-miler'),
    ('2023-05-07', 'Broad Street Run', 'Broad Street 10-miler'),
    ('2024-05-05', 'Broad Street Run', 'Broad Street 10-miler'),
    ('2025-05-04', 'Broad Street Run', 'Broad Street 10-miler'),
    # Wawa Welcome America - July 4th week, multi-day; main day is July 4
    ('2022-07-04', 'Welcome America Fireworks', 'Ben Franklin Parkway'),
    ('2023-07-04', 'Welcome America Fireworks', 'Ben Franklin Parkway'),
    ('2024-07-04', 'Welcome America Fireworks', 'Ben Franklin Parkway'),
    ('2025-07-04', 'Welcome America Fireworks', 'Ben Franklin Parkway'),
    # Made In America Festival (2022, 2023; cancelled 2024+)
    ('2022-09-03', 'Made In America Festival', 'Ben Franklin Parkway'),
    ('2022-09-04', 'Made In America Festival', 'Ben Franklin Parkway'),
    ('2023-09-02', 'Made In America Festival', 'Ben Franklin Parkway'),
    ('2023-09-03', 'Made In America Festival', 'Ben Franklin Parkway'),
    # Philly Marathon - mid-late November
    ('2022-11-19', 'Philly Marathon Weekend', 'half marathon'),
    ('2022-11-20', 'Philly Marathon', 'full marathon'),
    ('2023-11-18', 'Philly Marathon Weekend', 'half marathon'),
    ('2023-11-19', 'Philly Marathon', 'full marathon'),
    ('2024-11-23', 'Philly Marathon Weekend', 'half marathon'),
    ('2024-11-24', 'Philly Marathon', 'full marathon'),
    ('2025-11-22', 'Philly Marathon Weekend', 'half marathon'),
    ('2025-11-23', 'Philly Marathon', 'full marathon'),
]


# ---------------------------------------------------------------- Academic ---
# Penn + Drexel commencement weekends - approximate annual dates
ACADEMIC = [
    # Penn Commencement (mid-May, Monday is main day)
    ('2022-05-16', 'Penn Commencement',   'University City'),
    ('2023-05-15', 'Penn Commencement',   'University City'),
    ('2024-05-13', 'Penn Commencement',   'University City'),
    ('2025-05-19', 'Penn Commencement',   'University City'),
    # Drexel Commencement (mid-June, multi-day)
    ('2022-06-10', 'Drexel Commencement', 'University City'),
    ('2022-06-11', 'Drexel Commencement', 'University City'),
    ('2023-06-16', 'Drexel Commencement', 'University City'),
    ('2023-06-17', 'Drexel Commencement', 'University City'),
    ('2024-06-14', 'Drexel Commencement', 'University City'),
    ('2024-06-15', 'Drexel Commencement', 'University City'),
    ('2025-06-13', 'Drexel Commencement', 'University City'),
    ('2025-06-14', 'Drexel Commencement', 'University City'),
]


def build():
    rows = []

    for season in (PHILLIES_HOME_2022, PHILLIES_HOME_2023,
                   PHILLIES_HOME_2024, PHILLIES_HOME_2025):
        for date, opponent in season:
            rows.append({
                'date':       date,
                'event_type': 'phillies_home',
                'event_name': f'Phillies vs. {opponent}',
                'notes':      'Citizens Bank Park',
            })

    for date, opponent in EAGLES_HOME:
        rows.append({
            'date':       date,
            'event_type': 'eagles_home',
            'event_name': f'Eagles vs. {opponent}',
            'notes':      'Lincoln Financial Field',
        })

    for date, name, note in FESTIVALS:
        rows.append({
            'date':       date,
            'event_type': 'festival',
            'event_name': name,
            'notes':      note,
        })

    for date, name, note in ACADEMIC:
        rows.append({
            'date':       date,
            'event_type': 'academic',
            'event_name': name,
            'notes':      note,
        })

    df = pd.DataFrame(rows).sort_values(['date', 'event_type']).reset_index(drop=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)

    print(f'Wrote {len(df)} rows to {OUT}')
    print()
    print('By type:')
    print(df['event_type'].value_counts().to_string())
    print()
    print('By year:')
    df['year'] = pd.to_datetime(df['date']).dt.year
    print(df.groupby(['year', 'event_type']).size().unstack(fill_value=0).to_string())


if __name__ == '__main__':
    build()
