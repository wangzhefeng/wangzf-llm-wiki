---
source_type: web
title: "Amelia II: A Program for Missing Data"
author: 
created_at: 2026-04-06
topics:
  - 待分类
status: inbox
source: "https://gking.harvard.edu/amelia"
published: 
created: 2026-04-06
description: 
tags:
  - 
  - "clippings"
---

### Authors: James Honaker, Gary King, Matthew Blackwell

Amelia II "multiply imputes" missing data in a single cross-section (such as a survey), from a time series (like variables collected for each year in a country), or from a time-series-cross-sectional data set (such as collected by years for each of several countries). Amelia II implements our bootstrapping-based algorithm that gives essentially the same answers as the standard IP or EMis approaches, is usually considerably faster than existing approaches and can handle many more variables. Unlike Amelia I and other statistically rigorous imputation software, it virtually never crashes (but please let us know if you find to the contrary!). The program also generalizes existing approaches by allowing for trends in time series across observations within a cross-sectional unit, as well as priors that allow experts to incorporate beliefs they have about the values of missing cells in their data. Amelia II also includes useful diagnostics of the fit of multiple imputation models. The program works from the R command line or via a graphical user interface that does not require users to know R.

  
Amelia is named after this famous missing person.

![[gallery19.jpg|pilot]]

Amelia is named after this famous missing person.

Multiple imputation involves imputing *m* values for each missing cell in your data matrix and creating *m* "completed" data sets. (Across these completed data sets, the observed values are the same, but the missing values are filled in with different imputations that reflect our uncertainty about the missing data.) After imputation, Amelia will then save the *m* data sets. You then apply whatever statistical method you would have used if there had been no missing values to each of the *m* data sets, and use a simple procedure to combine the results. Under normal circumstances, you only need to impute once and can then analyze the *m* imputed data sets as many times and for as many purposes as you wish. The advantage of Amelia is that it combines the comparative speed and ease-of-use of our algorithm with the power of multiple imputation, to let you focus on your substantive research questions rather than spending time developing complex application-specific models for nonresponse in each new data set. Unless the rate of missingness is exceptionally high, *m=5* (the program default) will usually be adequate. Other methods of dealing with missing data, such as listwise deletion, mean substitution, or single imputation, are in common circumstances biased, inefficient, or both. When multiple imputation works properly, it fills in data in such a way as to not change any relationships in the data but which enables the inclusion of all the observed data in the partially missing rows.

Amelia II is a new program, and follows in the spirit with the same purpose as the first version of Amelia by James Honaker, Anne Joseph, Gary King, Kenneth Scheve, and Naunihal Singh.  

- **Reporting Bugs and Issues:** Please use our Github Issue [form.](https://github.com/IQSS/amelia/issues/new)
- **Questions and feature requests:** Discuss the software on our Discussions [page](https://github.com/IQSS/amelia/discussions).
- **Github:** [https://github.com/IQSS/amelia](https://github.com/IQSS/amelia)
- **Documentation**: [PDF](http://r.iq.harvard.edu/docs/amelia/amelia.pdf)
- **AmeliaView for Windows** (for those who don't know R): to install:
	1. [install the current version of R](http://www.r-project.org/) if you haven't already
		2. download and run [this file](https://www.dropbox.com/s/9d77tym8an0xp8f/amelia-setup.exe?dl=0)
		3. click on the "AmeliaView" shortcut from the Desktop or the Start Menu.
- **Amelia for R**: To install on any system: at the R command line, type
	- install.packages("Amelia")
- To use a development version of Amelia, enter the following commands at the R prompt:
	- `library(devtools)`
		`install_github("IQSS/Amelia")`
- To automatically combine multiply imputed data sets: in R see [Zelig](https://gking.harvard.edu/zelig "Zelig: Everyone's Statistical Software"); In Stata see [Clarify](https://gking.harvard.edu/clarify "Clarify: Software for Interpreting and Presenting Statistical Results") or Ken Scheve's [MI program](https://github.com/IQSS/garyking_website_files/blob/main/mi.zip).
- **Papers related to Amelia:**
	- James Honaker and Gary King, " [What to do About Missing Values in Time Series Cross-Section Data](https://gking.harvard.edu/files/abs/pr-abs.shtml) " *American Journal of Political Science* Vol. 54, No. 2 (April, 2010): Pp. 561-581. [Article PDF](https://gking.harvard.edu/sites/g/files/omnuum7116/files/2025-08/pr.pdf "pr.pdf")
		- Gary King, James Honaker, Anne Joseph, and Kenneth Scheve. " [Analyzing Incomplete Political Science Data: An Alternative Algorithm for Multiple Imputation](https://gking.harvard.edu/files/abs/evil-abs.shtml) ", *American Political Science Review*, Vol. 95, No. 1 (March, 2001): Pp. 49-69. [Article](https://github.com/IQSS/garyking_website_files/blob/main/evil.pdf)
		- Matthew Blackwell, James Honaker, and Gary King. A Unified Approach to Measurement Error and Missing Data: [Overview](https://gking.harvard.edu/publications/multiple-Overimputation-Unified-Approach-Measurement-Error-And-Missing-Data) and [Details And Extensions](https://gking.harvard.edu/publications/unified-Approach-Measurement-Error-And-Missing%c2%a0Data-Details-And-Extensions) both in *Sociological Methods and Research*, forthcoming.
- A [short course video](http://vimeo.com/18534025) circa 1999 which James, Ann, and Ken gave some years ago that explains mulitiple imputation in general, and the innovation in Amelia I in particular. Viewers will need to impute about 10 minutes of the video (at 10:19), which might have been when we reported the location of Ms. Earhart's plane.
- A [review](http://www.math.smith.edu/~nhorton/muchado.pdf) of software for missing data