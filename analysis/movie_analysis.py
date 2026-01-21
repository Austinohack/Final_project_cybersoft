


# =========================
# 01. SETUP & LOAD DATA
# =========================
import sys
from pathlib import Path
ROOT_DIR = Path().resolve().parents[0]  
sys.path.append(str(ROOT_DIR))

import pandas as pd
import numpy as np
import glob
import os
import matplotlib.pyplot as plt
from constants import DATA_URL 

df = pd.read_csv(DATA_URL)
print("Total movies:", len(df))

# In[2]:


# =========================
# 02. DATA CLEANING
# =========================

# Standardize numeric columns
num_cols = ["budget", "gross", "votes", "score", "runtime", "year"]
for c in num_cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

# Drop rows without core financial data
if {"budget", "gross"}.issubset(df.columns):
    df = df.dropna(subset=["budget", "gross"])

# Fill missing numeric values
df = df.fillna(df.mean(numeric_only=True))

# -------------------------
# Standardize movie title column
# -------------------------
title_candidates = ["title", "movie", "movie_title", "name", "film"]

for c in title_candidates:
    if c in df.columns:
        df = df.rename(columns={c: "title"})
        break


# In[3]:



# =========================
# 03. KPI CALCULATIONS
# =========================
# ROI
if {"budget", "gross"}.issubset(df.columns):
    df["ROI"] = (df["gross"] - df["budget"]) / df["budget"]

# Engagement
if {"votes", "gross"}.issubset(df.columns):
    df["engagement"] = df["votes"] / df["gross"]

# CPM
if {"budget", "votes"}.issubset(df.columns):
    df["CPM"] = df["budget"] / df["votes"]

# In[4]:


# =========================
# 04. DATASET OVERVIEW (Slides 1–4)
# =========================
print("Year range:", int(df["year"].min()), "-", int(df["year"].max()))
print(df.describe())


# In[5]:



# =========================
# 05. RATING & GENRE DISTRIBUTION (Slide 5)
# =========================
if "rating" in df.columns:
    rating_dist = df["rating"].value_counts()
    rating_dist.plot(kind="bar", title="Rating Distribution")
    plt.show()

    genre_rating = pd.crosstab(df["genre"], df["rating"])
    genre_rating.plot(kind="bar", stacked=True, figsize=(12,6))
    plt.title("Genre vs Rating")
    plt.show()


# In[6]:



# =========================
# 06. AUDIENCE & QUALITY – SCORE (Slide 6)
# =========================
if "score" in df.columns:
    score_genre = df.groupby("genre")["score"].mean().sort_values()
    score_genre.plot(kind="barh", title="Average Score by Genre")
    plt.show()

    if "rating" in df.columns:
        score_rating = df.groupby("rating")["score"].mean()
        score_rating.plot(kind="bar", title="Average Score by Rating")
        plt.show()

# In[7]:



# =========================
# 07. POPULARITY – VOTES (Slide 7)
# =========================
if {"votes", "score"}.issubset(df.columns):
    plt.scatter(df["votes"], df["score"], alpha=0.3)
    plt.xlabel("Votes")
    plt.ylabel("Score")
    plt.title("Votes vs Score")
    plt.show()

    votes_genre = df.groupby("genre")["votes"].sum().sort_values()
    votes_genre.plot(kind="barh", title="Total Votes by Genre")
    plt.show()


# In[8]:


# =========================
# 08. FINANCIAL OVERVIEW (Slide 8)
# =========================
plt.hist(df["budget"], bins=50)
plt.title("Budget Distribution")
plt.show()

plt.scatter(df["budget"], df["gross"], alpha=0.3)
plt.xlabel("Budget")
plt.ylabel("Gross")
plt.title("Budget vs Gross")
plt.show()


# In[9]:



# =========================
# 09. ROI ANALYSIS (Slide 9)
# =========================
roi_genre = df.groupby("genre")["ROI"].mean().sort_values()
roi_genre.plot(kind="barh", title="Average ROI by Genre")
plt.show()

if "rating" in df.columns:
    roi_rating = df.groupby("rating")["ROI"].mean()
    roi_rating.plot(kind="bar", title="Average ROI by Rating")
    plt.show()


# In[10]:



# =========================
# 10. TOP & BOTTOM MOVIES (Slide 10)
# =========================
top10 = df.sort_values("ROI", ascending=False).head(10)
bottom10 = df.sort_values("ROI").head(10)


print("Top 10 ROI Movies")
display(top10[["title", "genre", "ROI", "budget", "gross"]])

print("Bottom 10 ROI Movies")
display(bottom10[["title", "genre", "ROI", "budget", "gross"]])


# In[11]:



# =========================
# 11. MARKETING EFFICIENCY – CPM (Slide 11)
# =========================
if "CPM" in df.columns:
    cpm_genre = df.groupby("genre")["CPM"].mean().sort_values()
    cpm_genre.plot(kind="barh", title="Average CPM by Genre")
    plt.show()

    plt.scatter(df["CPM"], df["gross"], alpha=0.3)
    plt.xlabel("CPM")
    plt.ylabel("Gross")
    plt.title("CPM vs Gross")
    plt.show()

# In[12]:



# =========================
# 12. ENGAGEMENT ANALYSIS (Slide 12)
# =========================
if "engagement" in df.columns:
    engagement_genre = df.groupby("genre")["engagement"].mean().sort_values()
    engagement_genre.plot(kind="barh", title="Engagement by Genre")
    plt.show()

    plt.scatter(df["engagement"], df["ROI"], alpha=0.3)
    plt.xlabel("Engagement")
    plt.ylabel("ROI")
    plt.title("Engagement vs ROI")
    plt.show()

# In[13]:



# =========================
# 13. DIRECTOR & STAR IMPACT (Slide 13)
# =========================
if "director" in df.columns:
    director_roi = df.groupby("director")["ROI"].mean().sort_values(ascending=False).head(10)
    display(director_roi)

if "star" in df.columns:
    star_gross = df.groupby("star")["gross"].mean().sort_values(ascending=False).head(10)
    display(star_gross)


# In[14]:


# =========================
# 14. PRODUCTION COMPANY (Slide 14)
# =========================
if "company" in df.columns:
    company_perf = df.groupby("company").agg(
        avg_ROI=("ROI", "mean"),
        movie_count=("title", "count")
    ).sort_values("avg_ROI", ascending=False)
    display(company_perf.head(10))

# In[15]:



# =========================
# 15. TIME TREND ANALYSIS (Slide 15)
# =========================
trend = df.groupby("year").agg(
    avg_budget=("budget", "mean"),
    avg_gross=("gross", "mean"),
    avg_ROI=("ROI", "mean")
)
trend.plot(subplots=True, figsize=(10,8))
plt.show()


# In[16]:



# =========================
# 16. RUNTIME ANALYSIS (Slide 16)
# =========================
if "runtime" in df.columns:
    plt.scatter(df["runtime"], df["score"], alpha=0.3)
    plt.xlabel("Runtime")
    plt.ylabel("Score")
    plt.title("Runtime vs Score")
    plt.show()

# In[17]:



# =========================
# 17. SEGMENTATION (Slide 17)
# =========================
gross_threshold = df["gross"].quantile(0.9)
budget_median = df["budget"].median()

conditions = [
    df["gross"] >= gross_threshold,
    (df["budget"] < budget_median) & (df["ROI"] > df["ROI"].quantile(0.75)),
    (df["budget"] >= budget_median) & (df["ROI"] < 0)
]
choices = ["Blockbuster", "Indie Hit", "Failure"]

df["segment"] = np.select(conditions, choices, default="Other")
print(df["segment"].value_counts())

# In[18]:


from pathlib import Path

def ensure_dir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)

BASE_DIR = "../data"

DIRS = [
    f"{BASE_DIR}/clean",
    f"{BASE_DIR}/overview",
    f"{BASE_DIR}/financial",
    f"{BASE_DIR}/marketing",
    f"{BASE_DIR}/trend",
    f"{BASE_DIR}/audience",
    f"{BASE_DIR}/segmentation",
]

for d in DIRS:
    ensure_dir(d)


# In[19]:


# =========================
# 18. EXPORT FOR STREAMLIT & PPT
# =========================

# Dataset clean
df.to_csv("../data/clean/movies_clean.csv", index=False)

# Slides 6 – Audience & Quality
df.groupby("genre", as_index=False)["score"].mean() \
  .to_csv("../data/audience/score_by_genre.csv", index=False)
df.groupby("rating", as_index=False)["score"].mean() \
  .to_csv("../data/audience/score_by_rating.csv", index=False)

# Slides 8–10 – Financial & ROI
df.groupby("genre", as_index=False)["ROI"].mean() \
  .to_csv("../data/financial/roi_by_genre.csv", index=False)
df.groupby("rating", as_index=False)["ROI"].mean() \
  .to_csv("../data/financial/roi_by_rating.csv", index=False)
top_bottom = pd.concat([
    df.sort_values("ROI", ascending=False).head(10).assign(type="Top"),
    df.sort_values("ROI").head(10).assign(type="Bottom")
])
top_bottom.to_csv("../data/financial/top_bottom_roi.csv", index=False)

# Slides 11–12 – Marketing & Engagement
df.groupby("genre", as_index=False)["CPM"].mean() \
  .to_csv("../data/marketing/cpm_by_genre.csv", index=False)
df.groupby("genre", as_index=False)["engagement"].mean() \
  .to_csv("../data/marketing/engagement_by_genre.csv", index=False)

# Slides 15–17 – Trend & Segmentation
df.groupby("year", as_index=False).agg(
    avg_budget=("budget", "mean"),
    avg_gross=("gross", "mean"),
    avg_ROI=("ROI", "mean")
).to_csv("../data/trend/yearly_trend.csv", index=False)
df[["title", "genre", "budget", "gross", "ROI", "segment"]] \
  .to_csv("../data/segmentation/movie_segments.csv", index=False)

print("Clean data success!")
