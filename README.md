## Regression Project: Estimating Home Value

###### Chad Allen
###### 15 June 2021

<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

### Project Summary
<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

#### Project Description

The Zillow Data Science team wants to be able to predict the values of single unit properties that the tax district assesses using the property data from those with a transaction during the "hot months" (in terms of real estate demand) of May-August, 2017.

Additionally, information is needed outside of the model. Because property taxes are assessed at the county level, the team would like to know:

> - What states and counties these are located in?
> - What is the distribution of tax rates for each county?

#### Goals
> - Identify the drivers(features) for predicting the property values using the appraised value.
> - Document the process and analysis through the data science pipeline.
> - Construct a regression model for predicting home values that will do better than a baseline model.

#### Project Deliverables
> - Presentation with slides that summarizes finding about the drivers of property value.
> - Jupyter Notebook report detailing the process through the pipeline.
> - Acquire and Prepare files for recreating the process.
> - README file that documents the project planning with instructions on how to recreate.

<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

#### Project Planning

What is the definition of a single unit property?
> - "A housing unit is a single unit within a larger structure that can be used by an individual or household to eat, sleep, and live. The unit can be in any type of residence, such as a house, apartment, or mobile home, and may also be a single unit in a group of rooms." -www.investopedia.com
> - For the purposes of this project, decided to use properties described as Residential General(260), Single Family Residential(261), Rural Residence(262), Mobile Home(263), and Townhouse(264) from the Zillow database.
> - Using the above codes and the dates specified produced 28,185 records for initial analysis.

What features are the best for predicting a property's value?
> - Initial focus on number of bathrooms, number of bedrooms, square feet and age.

What are the counties and tax rates for the transactions in the project?
> - Use the FIPS code provide in the Zillow database to determine the counties included in the project.
> - The Federal Information Processing Standard Publication 6-4 is a five-digit Federal Information Processing Standards code which uniquely identified counties and county equivalents in the United States, certain U.S. possessions, and certain freely associated states.

<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

#### Project Context
> - The dataset came from the Zillow database.

#### Data Dictionary

The Zillow database contains many tables. The properties_2017 and predictions_2017 tables were joined together to pull the data into a single pandas DataFrame for this project.

After preparing the data, the remaining features and values are listed below: