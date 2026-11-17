# Life Expectancy vs Fertility Rate

**Question:** How have life expectancy and fertility rate changed together across countries and continents since the 1950s?

**Data:** Country-level population, fertility rate, and life expectancy series, plus a continent lookup. The notebook merges them into `data/gapminder_total.csv`.

**Method**
- Checked the 2015 snapshot for null values, data types, and country counts per continent.
- Filtered by continent, population size, and fertility rate.
- Cleaned and merged the population, fertility, and life expectancy tables by country and year.
- Produced one scatter plot per year and assembled them into animated GIFs, covering all countries and Africa alone.

**Outputs** (in `Plots & Gifs/`)
- `all_years.gif`: life expectancy against fertility rate, all countries, by year
- `Africa_all_years.gif`: the same view restricted to African countries
- `Life_expectancy_fertility_rate_2015.svg`: the 2015 snapshot

**Files**
- `Notebook/Gif_Project.ipynb`: data preparation and the 2015 analysis
- `Plots & Gifs/plot.ipynb`: plot generation and GIF assembly
- `data/`: source and filtered datasets

**Reproducing:** Install `pandas`, `matplotlib`, `imageio`, and `xlrd`, then run the notebooks in order from their own folders.

**Note:** This project began as a Spiced Bootcamp coursework assignment. The data preparation, plots, and animations were extended by me.
