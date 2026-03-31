# Netflix Shows & Movies — Visual Analytics

> **Assignment project** — Data Preparation · Cleaning · Exploration · Visualisation (Python + R)

---

## Project Structure

```
Netflix_shows_movies/
│
├── netflix_data.zip                <- Original zipped dataset (source)
├── Netflix_shows_movies.csv        <- Extracted & renamed dataset (Task 1 output)
│
├── netflix_analysis.py             <- Main Python script (Tasks 1–4)
├── netflix_visualisation.R         <- R script (Task 5)
│
├── outputs/                        <- Generated charts (auto-created on first run)
│   ├── most_watched_genres.png       # Task 4a
│   ├── ratings_distribution.png      # Task 4b
│   ├── movies_vs_tvshows.png         # Bonus
│   └── content_over_time.png         # Bonus
│
└── README.md
```

---

## Dataset — `Netflix_shows_movies.csv`

| Column | Description |
|---|---|
| `show_id` | Unique title identifier |
| `type` | Movie or TV Show |
| `title` | Title name |
| `director` | Director(s) |
| `cast` | Cast members |
| `country` | Country of origin |
| `date_added` | Date added to Netflix |
| `release_year` | Original release year |
| `rating` | Content rating (TV-MA, PG-13, R …) |
| `duration` | Minutes (movies) or seasons (TV) |
| `listed_in` | Genres (comma-separated) |
| `description` | Short synopsis |

**6,234 rows · 12 columns**

---

## Assignment Task Coverage

### Task 1 — Data Preparation
`netflix_analysis.py` uses Python's built-in `zipfile` module to:
- Open `netflix_data.zip`
- Extract `netflix_data.csv`
- Copy and rename it to `Netflix_shows_movies.csv` using `shutil.copy()`

### Task 2 — Data Cleaning
| Issue | Resolution |
|---|---|
| `director` — 1,969 missing (31.6%) | Filled with `"Unknown"` |
| `cast` — 570 missing (9.1%) | Filled with `"Unknown"` |
| `country` — 476 missing (7.6%) | Filled with `"Unknown"` |
| `date_added` — 11 missing | Filled with `"Unknown"` |
| `rating` — 10 missing | Rows dropped (< 0.2%) |
| Whitespace in strings | `.str.strip()` applied to all `object` columns |
| `date_added` as plain string | Parsed into `datetime64` with `pd.to_datetime` |

### Task 3 — Data Exploration
- `df.info()` — column types and non-null counts
- `df.describe(include=[np.number])` — numeric statistical summary
- `value_counts()` for `type`, `rating`, `country`, `release_year`
- Genre explosion — comma-separated genres split and counted individually

### Task 4 — Python Visualisations
| # | Chart | Libraries | Output |
|---|---|---|---|
| 4a | **Most Watched Genres** — horizontal bar | `matplotlib`, `seaborn` | `most_watched_genres.png` |
| 4b | **Ratings Distribution** — count plot | `seaborn`, `matplotlib.pyplot` | `ratings_distribution.png` |
| 4c | Movies vs TV Shows — pie chart | `matplotlib` | `movies_vs_tvshows.png` |
| 4d | Content Added Over Time — line chart | `matplotlib` | `content_over_time.png` |

### Task 5 — R Visualisation
`netflix_visualisation.R` re-implements both the ratings distribution and genres charts
using `ggplot2`, matching the dark Netflix theme.

---

## Requirements

### Python (≥ 3.9)

```bash
pip install pandas numpy matplotlib seaborn
```

### R (≥ 4.0)

```r
install.packages(c("ggplot2", "dplyr", "scales", "forcats"))
```

---

## How to Run

### Python script

```bash
# From the project folder
python netflix_analysis.py
```

This will:
1. Unzip `netflix_data.zip` → extract `netflix_data.csv`
2. Rename to `Netflix_shows_movies.csv`
3. Clean the data
4. Print exploration stats to console
5. Save all charts to `outputs/`

### R script

```bash
Rscript netflix_visualisation.R
```

Or open `netflix_visualisation.R` in RStudio and click **Source**.

---

## Key Findings

- **International Movies** is the most listed genre, followed by **Dramas** and **Comedies**
- **TV-MA** is the dominant rating — Netflix targets adult audiences
- **Movies (~68%)** outnumber **TV Shows (~32%)** in the catalogue
- Content additions peaked around **2018–2019**, then plateaued

---

*Submitted as a ZIP archive per assignment instructions.*
