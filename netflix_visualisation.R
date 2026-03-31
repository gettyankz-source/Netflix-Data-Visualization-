# ============================================================
#  Netflix Shows & Movies — R Visualisation
#  Chart: Ratings Distribution (ggplot2)
# ============================================================
#
#  Requirements:
#    install.packages(c("ggplot2", "dplyr", "scales", "forcats"))
#
#  Run from the project root:
#    Rscript netflix_visualisation.R
# ============================================================

library(ggplot2)
library(dplyr)
library(scales)
library(forcats)

# ── 1. Load data ──────────────────────────────────────────────
DATA_PATH <- file.path(dirname(sys.frame(1)$ofile %||% "."),
                       "Netflix_shows_movies.csv")

# Fallback for interactive use
if (!file.exists(DATA_PATH)) {
  DATA_PATH <- "Netflix_shows_movies.csv"
}

df <- read.csv(DATA_PATH, stringsAsFactors = FALSE, na.strings = c("", "NA"))
cat(sprintf("Loaded dataset: %d rows × %d columns\n", nrow(df), ncol(df)))

# ── 2. Clean ──────────────────────────────────────────────────
df <- df[!is.na(df$rating), ]
df$rating <- trimws(df$rating)

# ── 3. Summarise for ratings distribution ────────────────────
rating_summary <- df %>%
  count(rating, name = "count") %>%
  mutate(rating = fct_reorder(rating, count, .desc = TRUE))

# ── 4. Plot — Ratings Distribution ───────────────────────────
netflix_red  <- "#E50914"
bg_dark      <- "#0D0D0D"
panel_dark   <- "#1A1A1A"
text_light   <- "#FFFFFF"
grid_color   <- "#333333"

p <- ggplot(rating_summary, aes(x = rating, y = count, fill = count)) +
  geom_col(width = 0.65, color = NA) +
  geom_text(aes(label = scales::comma(count)),
            vjust = -0.5, size = 3.5, color = text_light, fontface = "bold") +
  scale_fill_gradient(low = "#831010", high = netflix_red, guide = "none") +
  scale_y_continuous(labels = scales::comma,
                     expand = expansion(mult = c(0, 0.12))) +
  labs(
    title    = "Ratings Distribution of Netflix Content",
    subtitle = "Count of Movies and TV Shows per content rating",
    x        = "Content Rating",
    y        = "Number of Titles"
  ) +
  theme_minimal(base_size = 13) +
  theme(
    plot.background   = element_rect(fill = bg_dark,   color = NA),
    panel.background  = element_rect(fill = panel_dark, color = NA),
    panel.grid.major.y = element_line(color = grid_color, linewidth = 0.4),
    panel.grid.major.x = element_blank(),
    panel.grid.minor   = element_blank(),
    plot.title    = element_text(color = netflix_red, face = "bold",
                                 size = 18, margin = margin(b = 4)),
    plot.subtitle = element_text(color = text_light,  size = 11,
                                 margin = margin(b = 14)),
    axis.title    = element_text(color = text_light,  size = 12),
    axis.text     = element_text(color = text_light,  size = 10),
    plot.margin   = margin(20, 24, 16, 16)
  )

# ── 5. Save ────────────────────────────────────────────────────
out_dir <- file.path(dirname(DATA_PATH), "outputs")
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)
out_path <- file.path(out_dir, "ratings_distribution_R.png")

ggsave(out_path, plot = p, width = 11, height = 6, dpi = 150, bg = bg_dark)
cat(sprintf("Plot saved → %s\n", out_path))

# ── 6. Bonus: Most Watched Genres (horizontal bar) ───────────
genres_raw <- strsplit(df$listed_in, ",")
genres_flat <- trimws(unlist(genres_raw))
genre_df <- as.data.frame(table(genres_flat), stringsAsFactors = FALSE)
colnames(genre_df) <- c("genre", "count")
top15 <- genre_df %>%
  arrange(desc(count)) %>%
  slice_head(n = 15) %>%
  mutate(genre = fct_reorder(genre, count))

p2 <- ggplot(top15, aes(x = count, y = genre, fill = count)) +
  geom_col(width = 0.65, color = NA) +
  geom_text(aes(label = scales::comma(count)),
            hjust = -0.15, size = 3.5, color = text_light, fontface = "bold") +
  scale_fill_gradient(low = "#831010", high = netflix_red, guide = "none") +
  scale_x_continuous(labels = scales::comma,
                     expand = expansion(mult = c(0, 0.14))) +
  labs(
    title    = "Top 15 Most Listed Genres on Netflix",
    subtitle = "Based on the 'listed_in' field (multi-genre titles counted once per genre)",
    x        = "Number of Titles",
    y        = NULL
  ) +
  theme_minimal(base_size = 13) +
  theme(
    plot.background    = element_rect(fill = bg_dark,    color = NA),
    panel.background   = element_rect(fill = panel_dark, color = NA),
    panel.grid.major.x = element_line(color = grid_color, linewidth = 0.4),
    panel.grid.major.y = element_blank(),
    panel.grid.minor   = element_blank(),
    plot.title    = element_text(color = netflix_red, face = "bold",
                                 size = 18, margin = margin(b = 4)),
    plot.subtitle = element_text(color = text_light,  size = 11,
                                 margin = margin(b = 14)),
    axis.title    = element_text(color = text_light,  size = 12),
    axis.text     = element_text(color = text_light,  size = 10),
    plot.margin   = margin(20, 24, 16, 16)
  )

out_path2 <- file.path(out_dir, "most_watched_genres_R.png")
ggsave(out_path2, plot = p2, width = 12, height = 7, dpi = 150, bg = bg_dark)
cat(sprintf("Plot saved → %s\n", out_path2))

cat("\n[Done] R visualisations complete.\n")
