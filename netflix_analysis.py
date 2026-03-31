"""
Netflix Shows & Movies — Visual Analytics
==========================================
Assignment: Data Preparation, Cleaning, Exploration, and Visualization
Author:     Netflix Developer Assignment
Dataset:    netflix_data.zip  ->  Netflix_shows_movies.csv

Tasks covered
-------------
1. Data Preparation  - unzip the dataset and rename to Netflix_shows_movies
2. Data Cleaning     - handle missing values
3. Data Exploration  - describe data, statistical analysis
4. Data Visualization - most watched genres & ratings distribution
                        (Seaborn, Pyplot, Matplotlib)
5. R Integration     - see netflix_visualisation.R
"""

# -----------------------------------------------------------------------------
# 0.  Imports
# -----------------------------------------------------------------------------
import os
import zipfile
import shutil
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")           # non-interactive backend (works everywhere)
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
ZIP_PATH    = os.path.join(BASE_DIR, "netflix_data.zip")
RENAMED_CSV = os.path.join(BASE_DIR, "Netflix_shows_movies.csv")
OUTPUT_DIR  = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 65)
print("  NETFLIX VISUAL ANALYTICS")
print("=" * 65)

# =============================================================================
# TASK 1 - DATA PREPARATION
#   * Unzip the dataset using Python's zipfile module
#   * Rename the extracted file to "Netflix_shows_movies"
# =============================================================================
print("\n[TASK 1]  DATA PREPARATION - Unzip & Rename")
print("-" * 65)

if not os.path.exists(ZIP_PATH):
    raise FileNotFoundError(
        f"Source zip not found: {ZIP_PATH}\n"
        "Please place netflix_data.zip in the same folder as this script."
    )

# --- Unzip ---
EXTRACT_DIR = os.path.join(BASE_DIR, "_extracted")
os.makedirs(EXTRACT_DIR, exist_ok=True)

with zipfile.ZipFile(ZIP_PATH, "r") as zf:
    members = zf.namelist()
    print(f"  Archive contents : {members}")
    zf.extractall(EXTRACT_DIR)
    print(f"  Extracted to     : {EXTRACT_DIR}")

# --- Find the CSV inside the extracted folder ---
extracted_csv = None
for m in members:
    if m.lower().endswith(".csv"):
        extracted_csv = os.path.join(EXTRACT_DIR, m)
        break

if extracted_csv is None:
    raise RuntimeError("No CSV found inside the zip archive.")

# --- Rename / copy to Netflix_shows_movies.csv ---
shutil.copy(extracted_csv, RENAMED_CSV)
print(f"  Renamed to       : Netflix_shows_movies.csv")

# --- Load ---
df = pd.read_csv(RENAMED_CSV)
print(f"\n  Dataset loaded  ->  {df.shape[0]:,} rows  x  {df.shape[1]} columns")
print(f"  Columns: {df.columns.tolist()}")

# =============================================================================
# TASK 2 - DATA CLEANING
#   * Identify and address all missing values
# =============================================================================
print("\n\n[TASK 2]  DATA CLEANING")
print("-" * 65)

missing_before = df.isnull().sum()
print("\n  Missing values BEFORE cleaning:")
print(
    missing_before[missing_before > 0]
    .rename("missing_count")
    .to_frame()
    .assign(pct=lambda x: (x["missing_count"] / len(df) * 100).round(2))
    .to_string()
)

# Fill categorical NaN with "Unknown" placeholder
for col in ["director", "cast", "country", "date_added"]:
    df[col] = df[col].fillna("Unknown")

# Drop the 10 rows where 'rating' is missing
rows_before = len(df)
df.dropna(subset=["rating"], inplace=True)
print(f"\n  Dropped {rows_before - len(df)} rows with missing 'rating'.")

# Strip leading/trailing whitespace from all string columns
str_cols = df.select_dtypes(include="object").columns
df[str_cols] = df[str_cols].apply(lambda c: c.str.strip())

# Parse date_added into a proper datetime column
df["date_added_parsed"] = pd.to_datetime(
    df["date_added"], format="%B %d, %Y", errors="coerce"
)

df.reset_index(drop=True, inplace=True)

print("\n  Missing values AFTER cleaning:")
still_missing = df.isnull().sum()
leftover = still_missing[still_missing > 0]
if leftover.empty:
    print("  None - dataset is fully clean.")
else:
    print(leftover.to_string())

print(f"\n  Clean dataset shape: {df.shape}")

# =============================================================================
# TASK 3 - DATA EXPLORATION
#   * Describe the data
#   * Conduct statistical analysis
# =============================================================================
print("\n\n[TASK 3]  DATA EXPLORATION")
print("-" * 65)

print("\n  --- Column types & non-null counts ---")
df.info()

print("\n  --- Numeric statistical summary (describe) ---")
print(df.describe(include=[np.number]).to_string())

print("\n  --- Content type breakdown ---")
type_counts = df["type"].value_counts()
print(type_counts.to_string())

print("\n  --- Rating distribution ---")
print(df["rating"].value_counts().to_string())

print("\n  --- Top 10 countries ---")
print(df["country"].value_counts().head(10).to_string())

print("\n  --- Top 5 release years ---")
print(df["release_year"].value_counts().head(5).to_string())

# Genre explosion (multi-genre rows counted per genre)
genre_series = (
    df["listed_in"]
    .dropna()
    .str.split(",")
    .explode()
    .str.strip()
)
genre_counts = genre_series.value_counts()
print("\n  --- Top 15 genres (exploded) ---")
print(genre_counts.head(15).to_string())

print("\n  --- Top 10 duration values ---")
print(df["duration"].value_counts().head(10).to_string())

# =============================================================================
# TASK 4 - DATA VISUALIZATION
#   Libraries: Seaborn, Pyplot (matplotlib.pyplot), Matplotlib
#   Required:  (a) Most watched genres  (b) Ratings distribution
# =============================================================================
print("\n\n[TASK 4]  DATA VISUALIZATION")
print("-" * 65)

# Shared theme
NETFLIX_RED = "#E50914"
BG_COLOR    = "#0D0D0D"
PANEL_COLOR = "#1A1A1A"
TEXT_COLOR  = "#FFFFFF"
GRID_COLOR  = "#2E2E2E"

sns.set_theme(style="darkgrid")
plt.rcParams.update({
    "figure.facecolor": BG_COLOR,
    "axes.facecolor":   PANEL_COLOR,
    "axes.labelcolor":  TEXT_COLOR,
    "xtick.color":      TEXT_COLOR,
    "ytick.color":      TEXT_COLOR,
    "text.color":       TEXT_COLOR,
    "grid.color":       GRID_COLOR,
    "grid.linewidth":   0.5,
    "font.family":      "DejaVu Sans",
})

# ---- Chart 4.1: MOST WATCHED GENRES (Matplotlib horizontal bar) -------------
print("\n  Rendering: Most Watched Genres ...")

top_genres = genre_counts.head(15)
bar_colors = sns.color_palette("rocket_r", len(top_genres))

fig, ax = plt.subplots(figsize=(13, 8))
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(PANEL_COLOR)

bars = ax.barh(
    top_genres.index[::-1],
    top_genres.values[::-1],
    color=bar_colors[::-1],
    edgecolor="none",
    height=0.68,
)

for bar in bars:
    w = bar.get_width()
    ax.text(
        w + 18, bar.get_y() + bar.get_height() / 2,
        f"{int(w):,}", va="center", ha="left",
        fontsize=9.5, color=TEXT_COLOR, fontweight="bold",
    )

ax.set_xlabel("Number of Titles", fontsize=12, labelpad=10)
ax.set_title("Top 15 Most Watched Genres on Netflix",
             fontsize=16, fontweight="bold", pad=18, color=NETFLIX_RED)
ax.tick_params(axis="y", labelsize=10.5)
ax.set_xlim(0, top_genres.values.max() * 1.16)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
fig.tight_layout()

genres_path = os.path.join(OUTPUT_DIR, "most_watched_genres.png")
fig.savefig(genres_path, dpi=150, bbox_inches="tight", facecolor=BG_COLOR)
plt.close(fig)
print(f"  Saved -> {genres_path}")

# ---- Chart 4.2: RATINGS DISTRIBUTION (Seaborn countplot + Pyplot) -----------
print("\n  Rendering: Ratings Distribution ...")

rating_order = df["rating"].value_counts().index.tolist()

fig, ax = plt.subplots(figsize=(13, 6))
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(PANEL_COLOR)

sns.countplot(
    data=df, x="rating", order=rating_order,
    hue="rating", palette="rocket", legend=False,
    ax=ax, edgecolor="none",
)

for p in ax.patches:
    height = int(p.get_height())
    ax.annotate(
        f"{height:,}",
        xy=(p.get_x() + p.get_width() / 2, height),
        ha="center", va="bottom",
        fontsize=9.5, color=TEXT_COLOR, fontweight="bold",
    )

ax.set_xlabel("Content Rating", fontsize=12, labelpad=10)
ax.set_ylabel("Number of Titles", fontsize=12, labelpad=10)
ax.set_title("Ratings Distribution of Netflix Content",
             fontsize=16, fontweight="bold", pad=18, color=NETFLIX_RED)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()

ratings_path = os.path.join(OUTPUT_DIR, "ratings_distribution.png")
fig.savefig(ratings_path, dpi=150, bbox_inches="tight", facecolor=BG_COLOR)
plt.close(fig)
print(f"  Saved -> {ratings_path}")

# ---- Chart 4.3: MOVIES vs TV SHOWS (Matplotlib pie) -------------------------
print("\n  Rendering: Movies vs TV Shows ...")

fig, ax = plt.subplots(figsize=(7, 7))
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

wedges, texts, autotexts = ax.pie(
    type_counts.values, labels=type_counts.index, autopct="%1.1f%%",
    colors=[NETFLIX_RED, "#831010"], startangle=90,
    wedgeprops={"edgecolor": BG_COLOR, "linewidth": 3},
    textprops={"color": TEXT_COLOR, "fontsize": 13},
)
for at in autotexts:
    at.set_fontsize(14)
    at.set_fontweight("bold")

ax.set_title("Movies vs TV Shows on Netflix",
             fontsize=15, fontweight="bold", pad=20, color=NETFLIX_RED)
fig.tight_layout()

pie_path = os.path.join(OUTPUT_DIR, "movies_vs_tvshows.png")
fig.savefig(pie_path, dpi=150, bbox_inches="tight", facecolor=BG_COLOR)
plt.close(fig)
print(f"  Saved -> {pie_path}")

# ---- Chart 4.4: CONTENT ADDED OVER TIME (Matplotlib line) -------------------
print("\n  Rendering: Content Added Over Time ...")

df_dated = df.dropna(subset=["date_added_parsed"]).copy()
df_dated["year_added"] = df_dated["date_added_parsed"].dt.year
yearly = (
    df_dated.groupby(["year_added", "type"])
    .size()
    .reset_index(name="count")
)

fig, ax = plt.subplots(figsize=(13, 6))
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(PANEL_COLOR)

colors_map = {"Movie": NETFLIX_RED, "TV Show": "#1DB954"}
for content_type, grp in yearly.groupby("type"):
    c = colors_map.get(content_type, "#FFFFFF")
    ax.plot(grp["year_added"], grp["count"],
            marker="o", label=content_type, color=c, linewidth=2.5, markersize=7)
    ax.fill_between(grp["year_added"], grp["count"], alpha=0.12, color=c)

ax.set_xlabel("Year", fontsize=12, labelpad=10)
ax.set_ylabel("Titles Added", fontsize=12, labelpad=10)
ax.set_title("Netflix Content Added Per Year",
             fontsize=16, fontweight="bold", pad=18, color=NETFLIX_RED)
ax.legend(fontsize=11, framealpha=0.2, labelcolor=TEXT_COLOR)
ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()

timeline_path = os.path.join(OUTPUT_DIR, "content_over_time.png")
fig.savefig(timeline_path, dpi=150, bbox_inches="tight", facecolor=BG_COLOR)
plt.close(fig)
print(f"  Saved -> {timeline_path}")

# -----------------------------------------------------------------------------
print("\n" + "=" * 65)
print("  ALL TASKS COMPLETE")
print(f"  Charts saved to: {OUTPUT_DIR}")
print("=" * 65)
