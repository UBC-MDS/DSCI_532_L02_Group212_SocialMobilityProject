## DSCI 532 Group 212 Proposal: Social Mobility Project

### Section 1: Motivation and Purpose

In an ideal world, every child would have the opportunity to achieve success regardless of what social class they happened to be born into. 
Having a low potential for socio-economic mobility means that a child's ultimate life prospects are more or less predetermined by the education or income level of their parents, whereas a high mobility is an indication of an equal-opportunity society.  Research has shown that higher social mobility also leads to increased economic growth and social stability (Source: [GDIM, 2018](https://openknowledge.worldbank.org/bitstream/handle/10986/28428/9781464812101.pdf)).  We feel that this makes it a better metric for measuring societal success over other traditional factors such as GDP.
We are proposing to build a visualization app that uses educational mobility as a proxy for overall socio-economic mobility to show how it has changed globally over the last four generations. 

### Section 2: Description of the data

The dataset we are using was compiled by the World Bank, and includes estimates of "absolute and relative intergenerational mobility (IGM) by 10-year cohorts, covering individuals born between 1940 and 1989" (Source: [GDIM, 2018](http://pubdocs.worldbank.org/en/734501527703249115/GDIM-Description-May29.pdf)).  We are going to be focusing on the education mobility data which covers 148 countries for at least one generation, and 111 countries over multiple generations.

The main variable we are plotting in all our visualizations is educational mobility. The raw dataset includes a column named `IGP` which represents intergenerational persistance in education. This is calculated from drawing a regression line between a child's years of schooling (or highest education level) and the highest education level of their parents.  The `IGP` s calculated in a way that higher values mean less mobility and lower values mean more mobility. This takes more cognitive effort when looking at plots, so for our visualiztion purposes we have made a new variable called `ed_mob_index` that maps the best World Bank `IGP` to a value of 1 and the worst to a value of 0. We feel that using this index makes the plots easier to follow (higher index = improved mobility!).

 We also use the following variables to allow the user to make selections for comparisons:
 - `countryname`: name of the country
 - `region`: continent name
 - `incgroup2`: either high-income economies or developing economies
 - `incgroup4`: this further splits developing economies into 3 subcategories: low, middle, and high.
 - `year`: this is the decade children are born in. Options are 1940, 1950, 1960, 1970, or 1980. 
 - `child`: either son or daughter

 There are many other columns in the raw dataset that we will not be including in our visualizations. Many of these are indicators or coefficients that are used to calculate the `IGP` and another mobility index relating to economic mobility, `IGE`.  For the purposes of this dashboard, we are excluding data relating to economic mobility since there is very little data available compared to educational mobility. We also take the `IGP` as a starting point instead of re-calculating all the estimation parameters.  A detailed description of each of these columns can also be found [here](http://pubdocs.worldbank.org/en/734501527703249115/GDIM-Description-May29.pdf).
 

### Section 3: Research questions and usage scenarios

This app lets users explore how education opportunity has changed globally over time.  Specifically it can help answer questions such as:
- How does the education mobility change for certain countries, regions, or economies over time?
- How do different countries or regions compare to each other? 
- Which countries have the highest education mobility for a given generation?
- For all of the above questions, is the education mobility different for different genders?

People who might be interested in exploring these questions could inlude sociology students or policy advisors. For example, a sociology student might use this app to explore how different countries have compared over time and then pick a specific country to do a research project on.  Policy advisors might be interested to seeing how their country compares to similar countries in their region, or how it compares to all countries in their region to help support decisions around increasing education funding or setting up more funding or opportunities for girls (if there is a gap between girls and boys).




