#  Monetised GHG Emissions Calculator

This repository supports a Streamlit interface which will be made available through Hugging Face Spaces to provide a simple interface for converting from companies' greenhouse gas emissions disclosures, released in quantitative terms, and for converting those into their monetized rates according to various social cost of carbon proposals .

This is a second version of an earlier calculator I put together. The reason that this is a new repository is because I accidentally overwrote the data in the first calculator, and since then I've decided to take a slightly different direction with this calculator by including a few additional social cost of carbon (SCC) numbers. Rather than attempt to salvage my first calculator, I figured that it was easier to start this project from scratch bundling together a few changes.  

## Disclaimer

I was drawn to this work as a result of my employment. Nevertheless, at least in its first iterations, my work with data in the realm of environmental and sustainability topics should not be perceived as anything other than my own first entry notes and attempts at exploring various questions. High among them is the question of whether and how companies' far-reaching environmental impacts could be monetized and integrated into financial accounting - an idea, at least in some implementations, called impact accounting. I open source technical projects as a matter of course and I haven't thought it is important to distinguish between my initial work in this and other areas. 

## The Social Cost ... But Of What, Exactly!?

The idea of trying to integrate environmental data into financial reporting is anything but straightforward. 

This is unfortunate, because the idea of doing this has important ramifications for public policy, financial policy, and the question of how our economic systems should be structured. It should be added: the idea of investigating what effect monetized emissions may have on companies profitability is not an attempt to be punitive. But rather to open the door to what this type of policy might look like in practice. If the purview of the analysis were widened to considering both companies environmental and social impacts, positive impacts could be added to move the analysis away from a framework that only estimates degrees of harm. 

Although obvious, it's important to highlight the following, too: 

Greenhouse gas emissions are often used for this purpose for a plurality of reasons, but chief among them is probably the fact that they are relatively widely available as a datapoint. To calculate what monetized environmental emissions would look like in practice, two things are necessary: Firstly the quantitative data about those emissions and secondly the multiplication factors to convert those to monetary units. To call the latter merely multipliers is also to greatly oversimplify what these are. In reality, to the extent that a simple number is ultimately proposed, the number is the result of a extensive modeling process underpinned by detailed scientific information. 

The broad idea behind proposing a social cost of carbon at all is to fix a number on the extent to which companies emissions have effects that could be monetized. However, there are two large deficiencies in even this approach. The first is that while it might be the most prominent gas in companies emissions profiles, carbon dioxide is but one of several gasses they may be emitting in their overall GHG emissions basket that have been demonstrated scientifically to have damaging effects on the environment (express, numerically, through their GWP values). One approach arround this is to consider for calculation a social cost of greenhouse gasses or SC-GHG. 

The second is the point made previously, that while companies greenhouse gas emissions, even if considered collectively, are relatively easy to document, monitor and report upon, together, they only consider one part of a company's environmental impacts. The Global Value Factors Database released by the International Foundation for Valuing Impacts l(IFVI) in 2024 considers a wide variety of environmental impacts, including in areas such as air pollution, waste management and land use displacement. 

## Proposals Included In Dataset

When working with data for analysis one generally tries to always compare like with like. 

In the case of aggregating different policy proposals for the social cost of carbon, however, this is extremely difficult. 

But aggregating them together in some corpus *is* useful to the extent that one may wish to compare the monetized emissions against these different proposals. 

This can be a revealing analysis because it can demonstrate tangibly how even small differences in the proposed social cost of carbon can have outsized effects once they are applied to quantity metrics that are often rather vast in nature. 

Consider, for example, the case of the oil and gas industry, which reports its GHG emissions in millions of tons of carbon dioxide equivalents by convention. In scope three, where the values often eclipse scopes 1 and two by a multiple, small differences in the value factor here can result in dramatic changes in the computed social cost of carbon, which, if compared against financial accounts, could 'cause huge differences In the calculated values for financials after monetized emissions

It's for this reason that this calculator is made available as a tool for analysis, calculation and policy ideation. That is to say, with an understanding that the comparisons are imperfect. But with the belief and hope that even imperfect comparisons can be useful in this context. As our struggles in the realm of climate change make abundantly clear, bringing good policy forward is a matter of urgency. 

## Author

Daniel Rosehill  
(public at danielrosehill dot com)

## Licensing

This repository is licensed under CC-BY-4.0 (Attribution 4.0 International) 
[License](https://creativecommons.org/licenses/by/4.0/)

### Summary of the License
The Creative Commons Attribution 4.0 International (CC BY 4.0) license allows others to:
- **Share**: Copy and redistribute the material in any medium or format.
- **Adapt**: Remix, transform, and build upon the material for any purpose, even commercially.

The licensor cannot revoke these freedoms as long as you follow the license terms.

#### License Terms
- **Attribution**: You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- **No additional restrictions**: You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

For the full legal code, please visit the [Creative Commons website](https://creativecommons.org/licenses/by/4.0/legalcode).