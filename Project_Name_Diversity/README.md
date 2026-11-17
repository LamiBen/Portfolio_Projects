# Baby Name Diversity, 1880–2022

**Question:** How has the variety of US baby names changed over 143 years, and how common have unisex names become?

**Data:** Annual US Social Security name files (1880–2022), the same data used in `Project_Babynames/`. Each file lists name, sex, and number of births for names given at least five times that year.

**Method**
- Combined all 143 yearly files.
- For each year, measured:
  - **Distinct names:** how many different names were used
  - **Top-100 share:** share of births given to the 100 most common names
  - **Entropy:** Shannon entropy of the name distribution, in bits (higher means more even spread)
  - **Unisex share:** share of births given to names where the less common sex accounts for at least 10% of that name's births
- Plotted all four measures over time.

**Results**

| Measure | 1880 | 2022 |
|---|---|---|
| Distinct names | 1,889 | 29,174 |
| Share of births in top 100 names | 66% | 24% |
| Name entropy (bits) | 8.2 | 11.6 |
| Share of births to unisex names | 2% | 10% |

The pattern is not a steady climb. The top-100 share held near 55–60% from about 1900 to 1950, then fell sharply after 1980, reaching 37% in 2000 and 24% in 2022. Distinct names peaked in 2008 at 32,533 and declined to 29,174 by 2022, so the most recent decade is one of consolidation rather than growth. Entropy rose overall, with a dip between about 1920 and 1945, and the unisex share has roughly quintupled.

**Caveats**
- The files only include names given at least five times in a year. Rare names are missing, so distinct-name counts are lower bounds, and the gap is largest in early years.
- Early years also have far fewer births in the file (about 0.2 million in 1880, against 3.4 million in 2022), so year-to-year changes in early years are based on smaller counts.
- The 10% threshold for "unisex" is a judgement call. At 5%, 20%, and 10%, the unisex share in 2022 is 15%, 6%, and 10%, and it rises from 1880 to 2022 under each threshold, though the level changes.

**Files**
- `name_diversity.py`: loads the data, computes the yearly metrics, and draws the figure (`python name_diversity.py`, about 6 seconds)
- `figures/name_diversity.png`: the four measures over time
- `figures/yearly_name_diversity.csv`: all yearly values

**Possible extensions:** Break the trends down by decade and by region, or test whether the spread in naming follows changes in birth rates.
