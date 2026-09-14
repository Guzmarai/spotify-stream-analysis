# Imports e Definições de Constantes
import pandas as pd

#File paths
INPUT_BASEPATH = "data/bronze/"
OUTPUT_BASEPATH = "data/silver/"
INPUT_FILENAME = "spotify_artist_streaming_2020_2025.csv"
FILEPATH = f"{INPUT_BASEPATH}{INPUT_FILENAME}"

#URL Constants
SPOTIFY_TRACK_BASE = "https://open.spotify.com/track/"

# Load the dataset
data = pd.read_csv(FILEPATH, sep=",", encoding="utf-8")

# ===[Tratamento Básico]===
def remove_duplicates(dataset):
    dataset = dataset.dropna(subset=['track_id'])
    dataset = dataset.sort_values(by='release_date', ascending=True)
    dataset = dataset.drop_duplicates(subset=['track_id'], keep='first')
    return dataset

def categorize_duration(dataset):
    bin_limit_length = [0, 1, 2, 3, 4, 5, 6, 9999]
    bin_labels_length = ['0-1 minutes', '1-2 minutes', '2-3 minutes', '3-4 minutes', '4-5 minutes', '5-6 minutes', '6+ minutes']

    dataset['duration_category'] = pd.cut(dataset['duration_minutes'], bins=bin_limit_length, labels=bin_labels_length, right=False)

    dataset = dataset.drop(columns=['duration_ms', 'duration_minutes'])
    
    return dataset

def remove_unnecessary_columns(dataset):
    columns_to_remove = ['key', 'mode', 'artist_track_count']
    dataset = dataset.drop(columns=columns_to_remove)
    return dataset

#===[Tabelas de Dimensão]===


def dimensions(dataset):
    dim_genres = dataset['genre'].unique()
    dim_countries = dataset['country'].unique()
    dim_urls = [dataset['track_id'], dataset['track_id'].apply(lambda x: SPOTIFY_TRACK_BASE + str(x))]

    return dim_genres, dim_countries, dim_urls

#===[Geração de Arquivos]===
def generate_files(dataset, genres, countries, urls):
    dataset.to_csv(f"{OUTPUT_BASEPATH}spotify_cleaned.csv", index=False)
    pd.DataFrame(genres).to_csv(f"{OUTPUT_BASEPATH}spotify_genres.csv", index=False)
    pd.DataFrame(countries).to_csv(f"{OUTPUT_BASEPATH}spotify_countries.csv", index=False)
    pd.DataFrame(urls).to_csv(f"{OUTPUT_BASEPATH}spotify_urls.csv", index=False)

#===[Função Principal]===
def run_cleanup(dataset):
    print("Starting data cleanup process...")
    
    # 1. Remove colunas inúteis
    data = remove_unnecessary_columns(dataset)
    print("Unnecessary columns removed.")
    
    # 2. Remove duplicatas (Passando o 'data' que veio da função anterior)
    data = remove_duplicates(data)
    print("Duplicates removed.")
    
    # 3. Categoriza duração (Passando o 'data' que veio da função anterior)
    data = categorize_duration(data)
    print("Duration categorized.")
    
    # 4. Extrai dimensões (Passando o 'data' que já passou por todos os tratamentos)
    genres, countries, urls = dimensions(data)
    print("Dimensions extracted.")
    
    # 5. Gera os arquivos
    generate_files(data, genres, countries, urls)
    print("Files generated successfully.")

#===[Execução de Debug]===
if __name__ == "__main__":
    run_cleanup(data)