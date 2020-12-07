# COVID-19 global trend

Data analysis, visualization, writing: [Gianna-Carina Gruen](https://twitter.com/giannagruen)

You can find the resulting article [here](https://www.dw.com/en/coronavirus-trend-the-pandemic-is-far-from-over/a-53954594).

## Data source

This analysis is based on data by the [**European Centre for Disease Prevention and Control (ECDC)**](https://www.ecdc.europa.eu/en). They provide daily updated case numbers. The data can be downloaded [here](https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide). Details on how the data is gathered and processed by ECDC can be found on [this page](https://www.ecdc.europa.eu/en/covid-19/data-collection).

### *Update*

The ECDC announced to discontinue the publication of daily figures of newly reported cases/deaths from mid December.

To be able to maintain this trend as well as other COVID-19 coverage, we decided to add an additional data source: the [**Johns Hopkins University's Center for Systems Science and Engineering (JHU CSSE)**](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data#daily-reports-csse_covid_19_daily_reports), who publish daily datasets containing the number of accumulated cases/deaths up until the respective date.

To maintain this script as is, we introduced an additional preprocessing step. Scraper script and example data can be found [here](/preprocessing/)

## Preprocessing

The data until November 30th, 2020 are from the ECDC. All datapoints starting December 1st, 2020 are based on JHU CSSE data.

However JHU CSSE data is not taken as is, because it is the all time accumulated number of cases until date x whereas we need the newly reported cases on date x.

So we re-configure the JHU CSSE data in preprocessing: For every country, we load today's data and yesterday's data and substract the latter from the former, with the difference being the number of newly reported cases by country on this date. This is saved as a new dataset.

This new dataset is then added to the base of ECDC data until November 30th and saved as `ecdc_base-plus_update.csv` which gets loaded by a scraper on the next day as a new base, adding the next day's data to it.


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