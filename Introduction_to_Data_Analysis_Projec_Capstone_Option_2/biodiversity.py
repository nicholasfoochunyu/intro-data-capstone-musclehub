
# coding: utf-8

# # Capstone 2: Biodiversity Project

# # Introduction
# You are a biodiversity analyst working for the National Parks Service.  You're going to help them analyze some data about species at various national parks.
# 
# Note: The data that you'll be working with for this project is *inspired* by real data, but is mostly fictional.

# # Step 1
# Import the modules that you'll be using in this assignment:
# - `from matplotlib import pyplot as plt`
# - `import pandas as pd`

# In[4]:


# import revelent modules
from matplotlib import pyplot as plt
import pandas as pd


# # Step 2
# You have been given two CSV files. `species_info.csv` with data about different species in our National Parks, including:
# - The scientific name of each species
# - The common names of each species
# - The species conservation status
# 
# Load the dataset and inspect it:
# - Load `species_info.csv` into a DataFrame called `species`

# In[5]:


# load species_info.csv(a csv file) into species (a dataframe)
species = pd.read_csv('species_info.csv')
species.info()


# Inspect each DataFrame using `.head()`.

# In[6]:


# inspect species(dataframe)
print species.head()


# # Step 3
# Let's start by learning a bit more about our data.  Answer each of the following questions.

# How many different species are in the `species` DataFrame?

# In[7]:


# no. diff. sp. in species(dataframe)
species_count = species.category.nunique()
print species_count


# What are the different values of `category` in `species`?

# In[8]:


# values of sp. in species(dataframe)
species_type = species.category.unique()
print species_type


# In[12]:


# counting the number of species in each category
number_of_species_in_each_category = species.groupby('category').scientific_name.nunique().reset_index()
number_of_species_in_each_category


# In[18]:


# produring a bar plot of number of organisms in each category
plt.figure(figsize=(16,4))
ax = plt.subplot()
plt.bar(range(len(number_of_species_in_each_category)), number_of_species_in_each_category.scientific_name)
ax.set_xticks(range(len(number_of_species_in_each_category)))
ax.set_xticklabels(number_of_species_in_each_category.category.values)
plt.xlabel('Categories for Organisms')
plt.ylabel('Number of Species')
plt.title('Number of Species in Each Category')
plt.show()
plt.savefig('number_of_species_in_each_category.png')


# In[22]:


# producing a pie chart of same information above
plt.figure(figsize=(16,4))
plot_data = number_of_species_in_each_category.scientific_name
plot_labels = number_of_species_in_each_category.category.values
plt.pie(plot_data, labels = plot_labels, autopct='%d%%')
plt.axis('equal')
plt.show()
plt.savefig('number_of_species_pie.png')


# What are the different values of `conservation_status`?

# In[23]:


# values of conservation_status in species(dataframe)
conservation_status = species.conservation_status.unique()
print conservation_status


# # Step 4
# Let's start doing some analysis!
# 
# The column `conservation_status` has several possible values:
# - `Species of Concern`: declining or appear to be in need of conservation
# - `Threatened`: vulnerable to endangerment in the near future
# - `Endangered`: seriously at risk of extinction
# - `In Recovery`: formerly `Endangered`, but currnetly neither in danger of extinction throughout all or a significant portion of its range
# 
# We'd like to count up how many species meet each of these criteria.  Use `groupby` to count how many `scientific_name` meet each of these criteria.

# In[24]:


# number of scientific_name in each conservation_status
conservation_counts = species.groupby('conservation_status').scientific_name.nunique().reset_index()
print conservation_counts
print '\n'
# note how this is different from when use .count()
# will have additional scientific_name values under species_of_concern category
# probably due to repetition of scientific_name(redundancy)
conservation_counts_1= species.groupby('conservation_status').scientific_name.count().reset_index()
print conservation_counts_1


# As we saw before, there are far more than 200 species in the `species` table.  Clearly, only a small number of them are categorized as needing some sort of protection.  The rest have `conservation_status` equal to `None`.  Because `groupby` does not include `None`, we will need to fill in the null values.  We can do this using `.fillna`.  We pass in however we want to fill in our `None` values as an argument.
# 
# Paste the following code and run it to see replace `None` with `No Intervention`:
# ```python
# species.fillna('No Intervention', inplace=True)
# ```

# In[25]:


# replace NaN values in dataframe with 'No Intervention', under conservation_status
species.fillna('No Intervention', inplace = True)


# Great! Now run the same `groupby` as before to see how many species require `No Protection`.

# In[26]:


# running conservation_counts code above
conservation_counts_fixed = species.groupby('conservation_status').scientific_name.nunique().reset_index()
print conservation_counts_fixed


# Let's use `plt.bar` to create a bar chart.  First, let's sort the columns by how many species are in each categories.  We can do this using `.sort_values`.  We use the the keyword `by` to indicate which column we want to sort by.
# 
# Paste the following code and run it to create a new DataFrame called `protection_counts`, which is sorted by `scientific_name`:
# ```python
# protection_counts = species.groupby('conservation_status')\
#     .scientific_name.count().reset_index()\
#     .sort_values(by='scientific_name')
# ```

# In[27]:


# to rearrange new dataframe(protection_counts) in ascending value of scientific_name
protection_counts = species.groupby('conservation_status').scientific_name.nunique().reset_index().sort_values(by='scientific_name')

print protection_counts


# In[28]:


# same as above
conservation_counts_fixed.sort_values(by='scientific_name').reset_index(drop=True)


# Now let's create a bar chart!
# 1. Start by creating a wide figure with `figsize=(10, 4)`
# 1. Start by creating an axes object called `ax` using `plt.subplot`.
# 2. Create a bar chart whose heights are equal to `scientific_name` column of `protection_counts`.
# 3. Create an x-tick for each of the bars.
# 4. Label each x-tick with the label from `conservation_status` in `protection_counts`
# 5. Label the y-axis `Number of Species`
# 6. Title the graph `Conservation Status by Species`
# 7. Plot the grap using `plt.show()`

# In[43]:


# producing a bar chart
plt.figure(figsize=(10,4))
ax = plt.subplot()
# note don't have to use conservation_status for x-axis as length of protection_counts (an object) is the same length (5)
plt.bar(range(len(protection_counts)), protection_counts.scientific_name)
ax.set_xticks(range(len(protection_counts)))
ax.set_xticklabels(protection_counts.conservation_status.values)
plt.xlabel('Conservation Status')
plt.ylabel('Number of Species')
plt.title('Conservation Status by Species')
plt.show()
plt.savefig('conservation_status_by_species.png')


# # Step 4
# Are certain types of species more likely to be endangered?

# Let's create a new column in `species` called `is_protected`, which is `True` if `conservation_status` is not equal to `No Intervention`, and `False` otherwise.

# In[31]:


# adding new column (is_protected) to dataframe (species)
species['is_protected'] = species.conservation_status != 'No Intervention'


# Let's group by *both* `category` and `is_protected`.  Save your results to `category_counts`.

# In[32]:


# grouping category and is_protected columns
category_counts = species.groupby(['category','is_protected']).scientific_name.nunique().reset_index()


# Examine `category_count` using `head()`.

# In[33]:


print category_counts.head()


# It's going to be easier to view this data if we pivot it.  Using `pivot`, rearange `category_counts` so that:
# - `columns` is `conservation_status`
# - `index` is `category`
# - `values` is `scientific_name`
# 
# Save your pivoted data to `category_pivot`. Remember to `reset_index()` at the end.

# In[34]:


# pivoting dataframe category_counts
category_pivot = category_counts.pivot(columns='is_protected', index='category', values='scientific_name').reset_index()


# Examine `category_pivot`.

# In[35]:


category_pivot


# Use the `.columns` property to  rename the categories `True` and `False` to something more description:
# - Leave `category` as `category`
# - Rename `False` to `not_protected`
# - Rename `True` to `protected`

# In[36]:


# renaming categories True and False
category_pivot.columns = ['category','not_protected','protected']


# Let's create a new column of `category_pivot` called `percent_protected`, which is equal to `protected` (the number of species that are protected) divided by `protected` plus `not_protected` (the total number of species).

# In[37]:


# create new columns(percent_protected) in dataframe(category_pivot)
category_pivot['percent_protected'] = category_pivot.protected/(category_pivot.not_protected + category_pivot.protected)


# Examine `category_pivot`.

# In[38]:


category_pivot


# In[44]:


# producing a bar plot of not_protected and protected for each category
n = 1
t = 2
d = 7
w = 0.8
x_values_1 = [t*element + w*n for element in range(d)]
n = 2
t = 2
d = 7
w = 0.8
x_values_2 = [t*element + w*n for element in range(d)]
plt.figure(figsize=(16,4))
ax = plt.subplot()
plt.bar(x_values_1, category_pivot.not_protected.values)
plt.bar(x_values_2, category_pivot.protected.values)
ax.set_xticks(x_values_1)
ax.set_xticklabels(category_pivot.category)
plt.legend(['Not Protected','Protected'], loc=0)
plt.xlabel('Categories of Organisms')
plt.ylabel('Number of Species')
plt.title('Number of Species Protected and Not Protected in Each Category')
plt.show()
plt.savefig('number_of_species_protected_and_not_protected_in_each_category.png')


# In[46]:


# changing percent_protected column to appropriate value
category_pivot['percent_protected'] = category_pivot.percent_protected*100


# In[48]:


# producing a bar plot of percentage of protected species in each category
plt.figure(figsize=(16,4))
ax = plt.subplot()
plt.bar(range(len(category_pivot)), category_pivot.percent_protected)
ax.set_xticks(range(len(category_pivot)))
ax.set_xticklabels(category_pivot.category.values)
plt.xlabel('Categories of Organisms')
plt.ylabel('Percentage of Protected Species (%)')
plt.title('Percentage of Protected Species in Each Category')
plt.show()
plt.savefig('percentage_of_protected_species_in_each_category.png')


# It looks like species in category `Mammal` are more likely to be endangered than species in `Bird`.  We're going to do a significance test to see if this statement is true.  Before you do the significance test, consider the following questions:
# - Is the data numerical or categorical?
# - How many pieces of data are you comparing?

# Based on those answers, you should choose to do a *chi squared test*.  In order to run a chi squared test, we'll need to create a contingency table.  Our contingency table should look like this:
# 
# ||protected|not protected|
# |-|-|-|
# |Mammal|?|?|
# |Bird|?|?|
# 
# Create a table called `contingency` and fill it in with the correct numbers

# In[51]:


# create a contingency table
contingency  = [[30,146],[75,413]]
print contingency


# In order to perform our chi square test, we'll need to import the correct function from scipy.  Past the following code and run it:
# ```py
# from scipy.stats import chi2_contingency
# ```

# In[55]:


# importing revelent modules
from scipy.stats import chi2_contingency


# Now run `chi2_contingency` with `contingency`.

# In[56]:


chi2, pval, dof, expected = chi2_contingency(contingency)
print pval


# It looks like this difference isn't significant!
# 
# Let's test another.  Is the difference between `Reptile` and `Mammal` significant?

# In[57]:


contingency_2 = [[30,146],[5,73]]
chi2, pval_reptile_mammal, dof, expected = chi2_contingency(contingency_2)
print pval_reptile_mammal


# Yes! It looks like there is a significant difference between `Reptile` and `Mammal`!

# # Step 5

# Conservationists have been recording sightings of different species at several national parks for the past 7 days.  They've saved sent you their observations in a file called `observations.csv`.  Load `observations.csv` into a variable called `observations`, then use `head` to view the data.

# In[33]:


# loading observations.csv file as dataframe object (observations)
observations = pd.read_csv('observations.csv')
print observations.head()


# Some scientists are studying the number of sheep sightings at different national parks.  There are several different scientific names for different types of sheep.  We'd like to know which rows of `species` are referring to sheep.  Notice that the following code will tell us whether or not a word occurs in a string:

# In[34]:


# Does "Sheep" occur in this string?
str1 = 'This string contains Sheep'
'Sheep' in str1


# In[35]:


# Does "Sheep" occur in this string?
str2 = 'This string contains Cows'
'Sheep' in str2


# Use `apply` and a `lambda` function to create a new column in `species` called `is_sheep` which is `True` if the `common_names` contains `'Sheep'`, and `False` otherwise.

# In[36]:


# creating a new column (is_sheep) in dataframe (species) to check if species in scientific_name is a sheep
species['is_sheep'] = species.common_names.apply(lambda x: True if 'Sheep' in x else False)


# Select the rows of `species` where `is_sheep` is `True` and examine the results.

# In[38]:


# select rows in species where is_sheep is True
species_is_sheep = species[species.is_sheep ==True]
print species_is_sheep


# Many of the results are actually plants.  Select the rows of `species` where `is_sheep` is `True` and `category` is `Mammal`.  Save the results to the variable `sheep_species`.

# In[39]:


# remove plant species from dataframe
sheep_species = species[(species.is_sheep==True) & (species.category=='Mammal')]
print sheep_species


# Now merge `sheep_species` with `observations` to get a DataFrame with observations of sheep.  Save this DataFrame as `sheep_observations`.

# In[40]:


# merging sheep_species and observations
sheep_observations = pd.merge(sheep_species,observations)
print sheep_observations.head()


# How many total sheep observations (across all three species) were made at each national park?  Use `groupby` to get the `sum` of `observations` for each `park_name`.  Save your answer to `obs_by_park`.
# 
# This is the total number of sheep observed in each park over the past 7 days.

# In[41]:


# calculating total sheep sightings across all 3 species at each national park
obs_by_park = sheep_observations.groupby('park_name').observations.sum().reset_index()
print obs_by_park


# Create a bar chart showing the different number of observations per week at each park.
# 
# 1. Start by creating a wide figure with `figsize=(16, 4)`
# 1. Start by creating an axes object called `ax` using `plt.subplot`.
# 2. Create a bar chart whose heights are equal to `observations` column of `obs_by_park`.
# 3. Create an x-tick for each of the bars.
# 4. Label each x-tick with the label from `park_name` in `obs_by_park`
# 5. Label the y-axis `Number of Observations`
# 6. Title the graph `Observations of Sheep per Week`
# 7. Plot the grap using `plt.show()`

# In[42]:


# bar chart demonstrating different number of observations per week at each park
plt.figure(figsize=(16,4))
ax = plt.subplot()
plt.bar(range(len(obs_by_park)), obs_by_park.observations)
ax.set_xticks(range(len(obs_by_park)))
ax.set_xticklabels(obs_by_park.park_name.values)
plt.ylabel('Number of Observations')
plt.title('Observations of Sheep per Week')
plt.show()


# Our scientists know that 15% of sheep at Bryce National Park have foot and mouth disease.  Park rangers at Yellowstone National Park have been running a program to reduce the rate of foot and mouth disease at that park.  The scientists want to test whether or not this program is working.  They want to be able to detect reductions of at least 5 percentage point.  For instance, if 10% of sheep in Yellowstone have foot and mouth disease, they'd like to be able to know this, with confidence.
# 
# Use the sample size calculator at <a href="https://www.optimizely.com/sample-size-calculator/">Optimizely</a> to calculate the number of sheep that they would need to observe from each park.  Use the default level of significance (90%).
# 
# Remember that "Minimum Detectable Effect" is a percent of the baseline.

# In[58]:


baseline = 15
minimum_detectable_effect = 100*5/baseline
sample_size_per_variant = 510 # use minimum_detectable_effect of 33.33% instead of 33%


# How many weeks would you need to observe sheep at Bryce National Park in order to observe enough sheep?  How many weeks would you need to observe at Yellowstone National Park to observe enough sheep?

# In[48]:


# number of weeks required by scientist to observe enough sheep at Yellowstone National Park
yellowstone_weeks_observing = sample_size_per_variant/507. # use of. to get float
print yellowstone_weeks_observing
# number of weeks required by scientist to observe enough sheep at Bryce National Park
bryce_weeks_observing = sample_size_per_variant/250.
print bryce_weeks_observing

