# Baby Names: Frequency Trends

**Question:** How have specific names and total birth counts changed over time?

**Data:** Annual US Social Security name-frequency files, 1880 onwards, stored in `data/names/` as `yobYYYY.txt`.

**Method**
- Wrote `parse_dataset(year)` to load one year's file into a DataFrame with `name`, `gender`, and `frequency` columns.
- Practised selecting rows and columns: single names, several names at once, every second row.
- Combined all years into `data/all_years_baby_names.csv`.
- Tracked the frequency of one name (Emily) across years and exported it separately.
- Totalled births per year from the parsed data.

**Files**
- `notebook/Project_Babynames.ipynb`: the analysis notebook
- `data/`: yearly name files and the combined datasets

**Note:** This project began as a Spiced Bootcamp coursework assignment. The parsing function, combined dataset, and per-name analysis are my own additions.
