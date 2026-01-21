import pandas as pd
import glob
import os


key = "products"




def load_movies_data(path: str) -> pd.DataFrame:
    """
    Load movie data from a file or a folder.

    Parameters
    ----------
    path : str
        - CSV file path  (e.g. data/clean/movies_clean.csv)
        - Folder path    (e.g. data/financial)

    Returns
    -------
    pd.DataFrame
        Concatenated dataframe
    """

    if not os.path.exists(path):
        raise FileNotFoundError(f"Path not found: {path}")

    # -------- Case 1: single CSV --------
    if os.path.isfile(path):
        if not path.endswith(".csv"):
            raise ValueError("Only CSV files are supported")
        return pd.read_csv(path)

    # -------- Case 2: folder with CSVs --------
    csv_files = glob.glob(os.path.join(path, "*.csv"))

    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in folder: {path}")

    dfs = []
    for file in csv_files:
        df = pd.read_csv(file)
        df["_source"] = os.path.basename(file)  # optional, for debugging / insight
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)


MOVIE_PATH = "data/clean/movies_clean.csv"


def load_movies():
    return pd.read_csv(MOVIE_PATH)


def save_movies(df: pd.DataFrame):
    df.to_csv(MOVIE_PATH, index=False)


def create_movie(movie: dict):
    df = load_movies()

    # Duplicate rule: same title + year
    duplicate = df[
        (df["title"].str.lower() == movie["title"].lower())
        & (df["year"] == movie["year"])
    ]

    if not duplicate.empty:
        raise ValueError("Movie already exists")

    df = pd.concat([df, pd.DataFrame([movie])], ignore_index=True)
    save_movies(df)



def update_movie(index: int, updated_movie: dict):
    df = load_movies()
    for col, val in updated_movie.items():
        df.at[index, col] = val
    save_movies(df)


def delete_movie(index: int):
    df = load_movies()
    df = df.drop(index).reset_index(drop=True)
    save_movies(df)

