#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import pandas as pd


# # Part 1: Reading and investigating data
# 
# Open up the `player_data.json` and investigate the data structure.

# In[26]:


with open('player_data.json') as file:
    data = json.load(file)


# In[27]:


data


# # Part 2:  Creating the Dataframe
# 
# Create a data frame where each row corresponds to a game for each player. You must have atleast the following columns in your final dataframe:
# 
# 'DISPLAY_FIRST_LAST', 'PERSON_ID', 'TEAM_ID', 'AST', 'BLK', 'DREB','Game_ID',  'MIN', 'PTS', 'REB', 'TEAM_ABBREVIATION'
# 
# *You can include additional columns in your dataframe, so you don't have to do additional work to remove other columns.*  

# In[30]:


data[0]['GAMELOG']


# In[31]:


df = pd.DataFrame()

for person in data:
    if len(person['GAMELOG']) == 0:
        continue
    df1 = pd.DataFrame(person, columns=['DISPLAY_FIRST_LAST', 'PERSON_ID', 'TEAM_ID'], index=[0])
    df2 = pd.DataFrame(person['GAMELOG'])
    merged = pd.merge(df1, df2, left_on='PERSON_ID', right_on='Player_ID', how='outer')
    df = pd.concat([df, merged])
    
df.reset_index(drop=True, inplace=True)


# In[394]:


df.head()


# # Part 3: Pandas Questions
# 
# Answer the following questions

# ## 1 
# - Find the player who scored the most points in an individual game last season.
# 
# -  Now do the same for rebounds, blocks, and assists.

# In[54]:


df.columns


# In[405]:


df.loc[df['PTS'].idxmax()]


# In[55]:


# Your code here
# MOST POINTS
df[df['PTS'] == df['PTS'].max()]


# In[56]:


# MOST REBOUNDS
df[df['REB'] == df['REB'].max()]


# In[57]:


# MOST BLOCKS
df[df['BLK'] == df['BLK'].max()]


# In[58]:


# MOST ASSISTS
df[df['AST'] == df['AST'].max()]


# ## 2: 
# 
# - Find the player who scored the most points for the entire season.
# 
# - Now do the same for rebounds, blocks, and assists.

# In[350]:


#your code here
# MOST POINTS IN SEASON
pdf = df.groupby('DISPLAY_FIRST_LAST')[['PTS']].sum()
pdf[pdf['PTS'] == pdf['PTS'].max()]


# In[92]:


# MOST REBS IN SEASON
rdf = df.groupby('DISPLAY_FIRST_LAST')[['REB']].sum()
rdf[rdf['REB'] == rdf['REB'].max()]


# In[93]:


# MOST BLOCKS IN SEASON
bdf = df.groupby('DISPLAY_FIRST_LAST')[['BLK']].sum()
bdf[bdf['BLK'] == bdf['BLK'].max()]


# In[94]:


# MOST ASSISTS IN SEASON
adf = df.groupby('DISPLAY_FIRST_LAST')[['AST']].sum()
adf[adf['AST'] == adf['AST'].max()]


# In[96]:


# MOST STEALS IN SEASON
sdf = df.groupby('DISPLAY_FIRST_LAST')[['STL']].sum()
sdf[sdf['STL'] == sdf['STL'].max()]


# ## 3:
# How many players played in at least 82 games last season?

# In[408]:


(df['DISPLAY_FIRST_LAST'].value_counts()>=82).sum()


# In[113]:


#your code here
game_count = df.groupby('DISPLAY_FIRST_LAST')[['Game_ID']].count()
len(game_count[game_count['Game_ID'] >= 82])


# ## 4: 
# - Find which team scored the most points for the entire season.
# 
# - Now do the same for rebounds, blocks, and assists.

# In[115]:


df.columns


# In[141]:


# your code here
tpts = df.groupby('TEAM_ABBREVIATION')[['PTS']].sum()
tpts[tpts['PTS'] == tpts['PTS'].max()]


# In[142]:


treb = df.groupby('TEAM_ABBREVIATION')[['REB']].sum()
treb[treb['REB'] == treb['REB'].max()]


# In[144]:


tblk = df.groupby('TEAM_ABBREVIATION')[['BLK']].sum()
tblk[tblk['BLK'] == tblk['BLK'].max()]


# In[145]:


tast = df.groupby('TEAM_ABBREVIATION')[['AST']].sum()
tast[tast['AST'] == tast['AST'].max()]


# ## 5:
# Which team had the most players play for them last season?

# In[355]:


#your code here
player_count = df.groupby(['TEAM_ABBREVIATION'])[['PERSON_ID']].nunique()
# player_count
player_count[player_count.PERSON_ID == player_count.PERSON_ID.max()]


# ## 6:
# - How many players played for more than one team last year?
# 
# - What is the most number of teams a player played for last season?

# In[158]:


df.columns


# In[414]:


df.groupby('DISPLAY_FIRST_LAST')['TEAM_ABBREVIATION'].nunique().max()


# In[412]:


df6 = df[['Player_ID','DISPLAY_FIRST_LAST','TEAM_ID_x','TEAM_ID_y']].drop_duplicates()
df6.groupby('DISPLAY_FIRST_LAST')[['Player_ID']].count().sort_values('Player_ID',ascending=False)


# In[365]:


df6 = df[['Player_ID','DISPLAY_FIRST_LAST','TEAM_ID_x','TEAM_ID_y']].drop_duplicates()
dfdup = df6[df6.duplicated(subset='Player_ID', keep=False)].groupby('DISPLAY_FIRST_LAST')[['TEAM_ID_y']].count()
dfdup


# In[366]:


dfdup.max()


# ## 7:
# 
# Find the player who scored the least amount of points while playing in at least 40 games last season.

# In[258]:


#your code here
df7 = df.groupby('DISPLAY_FIRST_LAST').agg({'Game_ID': ['count'], 'PTS': ['sum']})
df40 = df7[df7['Game_ID']['count']>=40]
df40[df40['PTS']['sum'] == df40['PTS']['sum'].min()]


# # Part 4: Pandas and Probability

# ## 8: 
# 
# What is the probability that a random player had a game where they scored more than 40 points?

# In[384]:


#your code here
df[df['PTS']>40].shape[0]/df.shape[0]


# ## 9:
# 
# What is the probability that a randomly selected player from last season would average more than 20 points per game?

# In[416]:


# your code here
pt_avg = df.groupby('DISPLAY_FIRST_LAST').agg({'PTS': 'mean'})
pt_avg
pt_avg[pt_avg['PTS']>20].shape[0]/pt_avg.shape[0]


# # Advanced Questions

# ## 10: 
# Find the player who scored the least amount of points while playing in at least 40 games and averageing at least 15 minutes per game last season.

# In[317]:


#your code here
df10 = df.groupby('DISPLAY_FIRST_LAST').agg({'Game_ID': ['count'], 'PTS': ['sum'], 'MIN': 'mean'})
df40 = df10[df10['Game_ID']['count']>=40]
dfminutes = df40[df40['MIN']['mean']>=15]
dfminutes[dfminutes['PTS']['sum'] == dfminutes['PTS']['sum'].min()]


# ## 11: 
# Which player scored the largest share of points for their team throughout the season.

# In[422]:


#your code here
dfshare = df.groupby(["TEAM_ABBREVIATION", "DISPLAY_FIRST_LAST"]).agg({'PTS': 'sum'})
dfshare.groupby(level=0).apply(lambda x: x / float(x.sum())).sort_values(by='PTS', ascending=False)


# ## 12:
# 
# What is the probability that a randomly selected player had at least one game in which they scored 40 points last season. 

# In[425]:


# your code here
len(df.loc[df['PTS']>=40]['DISPLAY_FIRST_LAST'].unique())/len(df['DISPLAY_FIRST_LAST'].unique())


# ## 13: 
# 
# A double-double is when a player records for any of the two follow categories: points, rebounds, assists, steals, or blocks. 
# What is the probability that a randomly selected player had a double-double in a game last season?
# 

# In[433]:


#your code here
df.query("""PTS>=10 and REB>=10""")


# ## 14:
# 
# What is the probability that a randomnly selected game had a player record a triple-double in that game?

# In[ ]:


#your code here


# # Part 5: Super Duper Challenge
# 
# 

# ## 15:
# 
# How many players last season averaged more points per game than their career average?

# In[ ]:




