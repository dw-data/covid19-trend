# Covid-19 global trend

Data analysis, visualization, writing: [Gianna-Carina Gruen](https://twitter.com/giannagruen)

You can find the resulting article [here](https://www.dw.com/en/coronavirus-trend-the-pandemic-is-far-from-over/a-53954594).

## Data source

This analysis is based on data by the [European Centre for Disease Prevention and Control (ECDC)](https://www.ecdc.europa.eu/en). They provide daily updated case numbers. The data can be downloaded [here](https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide). Details on how the data is gathered and processed by ECDC can be found on [this page](https://www.ecdc.europa.eu/en/covid-19/data-collection).


## Analysis

**Update:** *Starting calendar week 35, we change the anaylsis interval. Instead of 7 day intervals, we will be comparing 14 day intervals. We deemed this change necessary, as we observed a lot of variability in the overall trend picture that was not due to an actual change of the situation but could rather be traced back to irregularities in data reporting. By widening the interval, we hope to to better account for that and have our trend only reflect a change when there's an actual change in the situation.*


The Python script (refer to [this jupyter notebook](Trend-Corona-this-week-from-cw35.ipynb)) sums up the daily reported case numbers in 14-day-chunks (until calendar week 34: 7 day), starting with this week's Friday and tracing back 14 days to Saturday of the week before. The sum of daily reported case numbers in this 14 day period is referred to as "this current two weeks".

The next 14-day-chunk for comparison is created by summing up the daily reported case numbers, starting with Friday two weeks ago and tracing back 14 days up until the Saturday. The sum of daily reported case numbers in this seven day period is referred to as "last week".

`|<-Saturday four weeks ago --- *last two weeks* --- Friday two weeks ago->||<-Saturday two weeks ago--- *this current weeks* --- Friday (now)->|`

Together, those two 14-day-chunks cover a period of 28 days. According to the available information at this time, 14 days equal the maximum "incubation time" of Covid-19, meaning that someone infected on any day is highly likely to show symptoms within 14 days thereafter. Additionally, there's a duty for authorities to report new cases within 14 days.

The script then compares the sum of daily reported cases in "this two weeks" with that of "last two weeks", assigning a trend class (see methodology below).

The second script (refer to [this jupyter notebook](Trend-Corona-year-trend-from-cw35.ipynb)) does the same, but rolls back over all past Fridays in this year to calculate the same sums and generate a year-long-trend week by week.


## Methodology

Based on the sums for the current week (past seven days) and last week (seven days before that), every country is classified into a trend class. There are six trend classes, the goal is for all countries to arrive in the class "zero cases two weeks in a row" and stay there.

**More than twice as many cases compared to last week:**
Includes all countries whose case numbers doubled compared to the last week, as long as the last week's number is not zero.

**More cases compared to last week:**
Includes all countries whose numbers of cases in the current week increased by more than seven from to the last week. It also includes countries whose case numbers rose from zero cases in the last week to more than seven cases in the current week.

**Approximately same number of cases in both weeks:**
Includes all countries that have the same case numbers in both weeks, plus/minus two percent of cases (until calendar week 34, this was set to plus/minus 7 cases). Additionally, if daily reported case numbers are negative for a 14 day interval a country is classified in this category as no change in actual new cases is the best guess in this situation (rather than a decrease). Countries with negative case numbers are additionally checked manually.

**Less cases this week compared to last week:**
Includes all countries that have reported at least seven fewer cases this week, compared to the last week.

**Less than half the cases compared to last week:**
Included all countries whose weekly case numbers halfed between the two weeks as well as countries that reported zero cases in the current week, but not in the last week.

**Zero cases two week in a row:**
Includes all countries that reported zero cases for 14 days in a row.