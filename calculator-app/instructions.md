# GHG Emissions Calculator: User Notes & Instructions

*By: Daniel Rosehill*

*V1: 20-Dec-24*

## Access & Installation

The purpose of this calculator and demo application is to allow the user to conduct monetizations of companies' quantitative greenhouse gas emissions data at various proposed social cost of carbon numbers. 

These social costs of carbon proposals have been gathered as a data file in the repository located under data sources.

<br>

**Data Source Links (raw CSV):**

| Platform     | URL                                                                                                                                                                  |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Hugging Face |  [![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Data-blue)](https://huggingface.co/spaces/danielrosehill/Monetised-GHG-Emissions-Calculator/raw/main/calculator-app/data.csv) |
| GitHub       |  [![GitHub](https://img.shields.io/badge/GitHub-Data-green)](https://raw.githubusercontent.com/danielrosehill/Emissions-Monetisation-Calculator/refs/heads/main/calculator-app/data.csv)                                     |

<br>

This repository can be accessed both from GitHub and Hugging Face as a demonstration space that allows usage. Alternatively, you may wish to clone this repository onto your local machine and run it locally. It uses Streamlit.

##  Monetizing environmental data: use-cases and interest groups. 

Various groups of stakeholders have highlighted the public interest in estimating the approximate cost of companies' pollution activities in the form of various metrics. At the governmental and intergovernmental level, the best known of these is the social cost of carbon. The social cost of carbon has been suggested as a mechanism for approximating the cost of carbon emissions on the planet as a whole. 

Beyond the policy context, those advocating for a practice known as impact accounting, have suggested that the cost of this particular environmental impact be integrated into a broader and further-reaching set of practices by which companies' environmental impacts, as well as their social impacts, would be incorporated into their financial reporting. In this practice, the cost of carbon is only one of the environmental impacts that would be thusly "monetized". 

## Unit Standardisation

The practice of monetizing companies' greenhouse gas emissions is nowhere near as simple as might be expected. Additionally, attempting to do so often entails following methodologies that are to a degree, inherently flawed.  The motivation for the creation of this calculator, however, and the proposals to do roughly this, is that it's better to use an imperfect methodology than to use none at all. 

The first comparability challenge is that the various proposals for estimating the societal cost of emissions are frequently limited to considering carbon dioxide emissions whereas companies' greenhouse gas emissions reporting more commonly reports on their carbon dioxide equivalents, encompassing both their carbon dioxide emissions as well as other gasses which have been linked to pollution, some of which are typically far less prevalent in their emissions but have a higher global warming potential. 

The result is that although the multiplier might be mismatched, the end approximation for the monetized emissions will actually be an understatement, because the multiplier is only monetizing a portion of the companies' reported emissions. If a company reports its greenhouse gas emissions as carbon dioxide equivalents, and the multiplier is only the social cost of carbon, then the non-carbon dioxide constituents of the CO2E number are not being "monetised." Depending on the constitution of a company's mix of greenhouse gas emissions, this would result in understatements to greater and lesser extents.

Another challenge in comparing greenhouse gas emissions between industries is that different units of measurements can be used, and the units of measurements used in emissions reporting and those attempts to set a social cost are usually not the same. 

## MTCO2(E) vs TCO2(E)

The social cost of carbon numbers are typically proposed as prices per ton of carbon dioxide equivalents or carbon dioxide. But depending on the extent of their missions, companies typically report this number in their sustainability and ESG disclosures in higher units. The units which companies report in in their reporting literature are frequently chosen to best align with industry norms. In the case of oil and gas, the units are typically millions of tons of carbon dioxide equivalents but in some industries with far less emissions, such a large single unit would be nonsensical. To complicate matters further, different units are seen as well. But it suggested that tons of carbon dioxide equivalents and millions of tons provide two units that can cater for conversions from the wide range of intermediate units that are occasionally encountered. Therefore, this calculator provides only those two units.

## Conversion Values & Logic

In order to simplify the calculation of the monetizations, the calculator assumes that tons of carbon dioxide equivalents is the reporting unit. 

In instances where the user is inputting a value expressed as the higher unit (millions of tonnes of CO 2 equivalents) a multiplication factor of 1 million is used in order to convert this value from tonnes into millions of tonnes. 

An additional value is provided in the data CSV, although it's not used in the calculator. That value is USD conversion value MTCO2E. This is the conversion factor expressed already in millions. Therefore the conversion logic should be different. 

## Currency Conversions & Geospecificity

Proposals for the social cost of carbon have been expressed over the course of time in different currencies. Additionally, different estimates have dealt with the question of geographical specificity in different ways. A more selective social cost of carbon would be stratified on a per country basis. But most proposals so far have provided the number as a single globally applicable figure, expressed in US dollars. 

To enable Comparisons between Proposals expressed in different currencies all non US dollar proposals were converted to the US dollar at a specific date noted in the CSV. The accuracy of this dynamic value could be improved through integrating this calculator with financial exchange APIs.

## Range Handling

In some instances, the proposed social cost of carbon has not been expressed as one value, but rather as a range of values. 

Again, and solely for the purpose of streamlining comparison in this demonstration app. In cases where this was the case, both the range values were noted and the average was used as the figure. In cases where an average was proposed in a currency other than the US dollar, the average was taken and then that average was converted to USD at the date noted in the data.

A Boolean value called `is_range` was added to the data set in order to help analysts distinguish easily between those estimated social costs of carbon, denoted as a single figure, and those expressed as ranges. The logic is that one or positive means that it was a range and zero is not a range.

## ISO Values

 For the purpose of making this small data set comparable, ISO values were added where possible in order to further analysis of this data set by policy analysts and other interested parties. The currency values were expressed in their 3-letter ISO codes. Similarly, the country of the proposing organization was noted and its ISO codes were also provided. 

 The country value here was chosen based upon the location of the headquarters of the organization. In the case of international organizations whose headquarters are in a specific country. This value might be slightly misleading, as it's reflective of a global worldview rather than the specific country in which the organization has its formal headquarters. But for the purpose of data conformity, it was added nevertheless.

 ## HDI Values

An interesting policy question is the question of whether more affluent countries have expressed their proposed social cost of carbon differently than less affluent countries, who may be more  adversely affected by emissions produced by wealthier countries.  

In order to suggest that this data could be included in any analytical uses of this CSV, the latest available Human Development Index value for each country was added. 

In the case of the data points in the current grouping, the addition of this parameter doesn't add much to the analysis because the countries which have proposed this value are all in the very high tranche of the HDI index. Additionally, this dataset Is unlikely to ever be very sizable, given that formal proposals for social cost of carbon are not advanced that easily nor frequently. But it may be an interesting angle of exploration if more developing world countries attempt this proposal.