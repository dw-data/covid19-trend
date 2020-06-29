# Covid-19 global trend

Data analysis, visualization, writing: [Gianna-Carina Gruen](https://twitter.com/giannagruen)

You can find the resulting article [here]().

## Data source

This analysis is based on data by the [European Centre for Disease Prevention and Control (ECDC)](https://www.ecdc.europa.eu/en). They provide daily updated case numbers. The data can be downloaded [here](https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide). Details on how the data is gathered and processed by ECDC can be found on [this page](https://www.ecdc.europa.eu/en/covid-19/data-collection).


## Analysis

The Python script (refer to [this jupyter notebook](Trend-Corona.ipynb)) sums up the daily reported case numbers in seven-day-chunks, starting with this week's Friday and tracing back seven days to Saturday of the week before. The sum of daily reported case numbers in this seven day period is referred to as "this current week".

The next seven-day-chunk for comparison is created by summing up the daily reported case numbers, starting with last week's Friday and tracing back seven days up until the Saturday. The sum of daily reported case numbers in this seven day period is referred to as "previous week".

`|<-Saturday --- *previous week* --- Friday->||<-Saturday --- *this current week* --- Friday (now)->|`

Together, those two seven-day-chunks cover a period of 14 days. According to the available information at this time, 14 days equal the maximum "incubation time" of Covid-19, meaning that someone infected on any day is highly likely to show symptoms within 14 days thereafter.

The script then compares the sum of daily reported cases in "this week" with that of "previous week", assigning a trend class (see methodology below).

The second script (refer to [this jupyter notebook](Trend-Corona-Past-Weeks.ipynb)) does the same, but rolls back over all past Fridays in this year to calculate the same sums and generate a year-long-trend week by week.


## Methodology

Based on the sums for the current week (past seven days) and previous week (seven days before that), every country is classified into a trend class. There are six trend classes, the goal is for all countries to arrive in the class "zero cases two weeks in a row" and stay there.

**More than twice as many cases compared to previous week:**
Includes all countries whose case numbers doubled compared to the previous week, as long as the previous week's number is not zero.

**More cases compared to previous week:**
Includes all countries whose weekly case numbers of the current week increased by more than seven cases compared to the previous week. It also includes countries whose case numbers rose from zero cases in the previous week to more than seven cases in the current week.

**Approximately same number of cases in both weeks:**
Includes all countries that have the same case numbers in both weeks, plus/minus seven cases.

**Less cases this week compared to previous week:**
Includes all countries that have reported at least seven fewer cases this week, compared to the previous week.

**Less than half the cases compared to previous week:**
Included all countries whose weekly case numbers halfed between the two weeks as well as countries that reported zero cases in the current week, but not in the previous week.

**Zero cases two week in a row:**
Includes all countries that reported zero cases for 14 days in a row.