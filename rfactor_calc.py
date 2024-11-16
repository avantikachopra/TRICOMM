import sportsdataverse as sdv
import sportsdataverse.mbb.mbb_loaders as mbb_loaders
import pandas as pd
import numpy as np
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Step 1: Load NCAA Data using the correct function
def load_ncaa_data(year):
    # Use SDV to fetch men's college basketball schedule for a given year
    games = mbb_loaders.load_mbb_schedule(seasons=[year], return_as_pandas=True)
    
    # Filter to include only necessary columns
    games = games[['home_name', 'away_name', 'home_score', 'away_score', 'season', 'game_date']]
    
    return games

# Step 2: Prepare Data by Splitting Seasons into Halves
def prepare_win_fraction_data(games):
    # Add win indicator for each game
    games['home_win'] = games['home_score'] > games['away_score']
    games['away_win'] = games['away_score'] > games['home_score']
    
    # Split games by first and second half based on date
    midpoint_date = games['game_date'].median()  # Approximate midpoint of the season
    
    # First half
    first_half = games[games['game_date'] <= midpoint_date]
    second_half = games[games['game_date'] > midpoint_date]
    
    # Calculate win fractions for each team in both halves
    teams_first_half = (first_half.groupby('home_name')['home_win'].sum() / first_half['home_name'].value_counts()).fillna(0)
    teams_second_half = (second_half.groupby('home_name')['home_win'].sum() / second_half['home_name'].value_counts()).fillna(0)
    
    win_fractions = pd.DataFrame({
        'W_first': teams_first_half,
        'W_second': teams_second_half
    }).dropna()  # Drop any teams with missing data for full halves
    
    return win_fractions

# Step 3: Calculate R Factor
def calculate_r_factor(win_fractions):
    # Calculate S and T components
    win_fractions['S'] = (win_fractions['W_first'] + win_fractions['W_second']) / np.sqrt(2)
    win_fractions['T'] = (win_fractions['W_first'] - win_fractions['W_second']) / np.sqrt(2)
    
    # Variance along S and T axes
    sigma_S_squared = win_fractions['S'].var()
    sigma_T_squared = win_fractions['T'].var()
    
    # Calculate R factor
    R = (sigma_S_squared - sigma_T_squared) / (sigma_S_squared + sigma_T_squared)
    
    return R

# Step 4: Calculate R Factor for Multiple Seasons
def calculate_r_for_multiple_seasons(start_year, end_year):
    r_values = {}
    for year in range(start_year, end_year + 1):
        games = load_ncaa_data(year)
        win_fractions = prepare_win_fraction_data(games)
        R = calculate_r_factor(win_fractions)
        r_values[year] = R
        print(f"Calculated R for {year}: {R}")
    return r_values

# Run the function for a range of seasons
start_year = 2015  # Adjust start and end years as desired
end_year = 2024
r_factors = calculate_r_for_multiple_seasons(start_year, end_year)

# Display results
print("R factors by season:", r_factors)
