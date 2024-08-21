from fastapi import FastAPI
import pandas as pd
from fastapi import HTTPException
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

# Cargar el dataset
movies = pd.read_parquet('Dataset/Credits_movies_final.parquet')  # Asegúrate de especificar la ruta correcta

 #Crear el vectorizador y ajustar al dataset
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(movies['overview'].fillna(''))

# Convertir las fechas si no lo has hecho aún
movies['fecha_lanzamiento'] = pd.to_datetime(movies['release_date'], errors='coerce')

# Ruta raíz que redirige a /docs
@app.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse(url="/docs")

# 1. Función para cantidad de filmaciones por mes
@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    meses = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
        "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
        "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
    mes_num = meses.get(mes.lower())
    if mes_num:
        cantidad = movies[movies['fecha_lanzamiento'].dt.month == mes_num].shape[0]
        return f"{cantidad} películas fueron estrenadas en el mes de {mes.capitalize()}."
    else:
        return "Mes no válido."

# 2. Función para cantidad de filmaciones por día
@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    dias = {
        "lunes": 0, "martes": 1, "miércoles": 2, "jueves": 3,
        "viernes": 4, "sábado": 5, "domingo": 6
    }
    dia_num = dias.get(dia.lower())
    if dia_num is not None:
        cantidad = movies[movies['fecha_lanzamiento'].dt.weekday == dia_num].shape[0]
        return f"{cantidad} películas fueron estrenadas en los días {dia.capitalize()}."
    else:
        return "Día no válido."

# 3. Función para obtener el score por título
@app.get("/score_titulo/{titulo}")
def score_titulo(titulo: str):
    film = movies[movies['title'].str.lower() == titulo.lower()]
    if not film.empty:
        titulo = film.iloc[0]['title']
        año = film.iloc[0]['release_year']
        score = film.iloc[0]['popularity']
        return f"La película {titulo} fue estrenada en el año {año} con un score/popularidad de {score}."
    else:
        return "Película no encontrada."

# 4. Función para obtener los votos por título
@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo: str):
    film = movies[movies['title'].str.lower() == titulo.lower()]
    if not film.empty:
        votos = film.iloc[0]['vote_count']
        promedio_votos = film.iloc[0]['vote_average']
        if votos >= 2000:
            return f"La película {titulo} cuenta con un total de {votos} valoraciones, con un promedio de {promedio_votos}."
        else:
            return "La película no tiene suficientes valoraciones (menos de 2000)."
    else:
        return "Película no encontrada."

# Función para obtener información sobre el actor
@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor: str):
    try:
        # Filtrar las películas en las que el actor ha participado, respetando mayúsculas y minúsculas
        actor_films = movies[movies['nameActor'].str.contains(nombre_actor, case=True, na=False)]
        
        if not actor_films.empty:
            cantidad = actor_films.shape[0]
            retorno_total = actor_films['return'].sum()
            promedio_retorno = actor_films['return'].mean()
            return {
                "Actor": nombre_actor,
                "Cantidad de filmaciones": cantidad,
                "Retorno total": retorno_total,
                "Promedio de retorno": promedio_retorno
            }
        else:
            return {"mensaje": "Actor no encontrado."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# 6. Función para obtener información sobre un director
@app.get("/get_director/{nombre_director}")
def get_director(nombre_director: str):
    director_films = movies[movies['reparto_name'].str.contains(nombre_director, case=False, na=False)]
    if not director_films.empty:
        film_list = []
        for _, film in director_films.iterrows():
            nombre = film['title']
            fecha = film['release_date']
            retorno = film['return']
            costo = film['budget']
            ganancia = film['revenue'] - costo
            film_list.append({
                "nombre": nombre,
                "fecha": fecha,
                "retorno": retorno,
                "costo": costo,
                "ganancia": ganancia
            })
        return {
            "director": nombre_director,
            "filmaciones": film_list
        }
    else:
        return "Director no encontrado."

#Funcion para el  Sistema de recomendación de Peliculas
def recomendar_peliculas(titulo_pelicula, num_recomendaciones=5):
    # Obtener el índice de la película
    idx = movies[movies['title'] == titulo_pelicula].index
    if idx.empty:
        return []

    idx = idx[0]

    # Calcular la similitud con todas las demás películas
    cosine_similarities = cosine_similarity(tfidf_matrix[idx:idx+1], tfidf_matrix).flatten()

    # Obtener los índices de las películas más similares
    similar_indices = cosine_similarities.argsort()[-num_recomendaciones-1:-1]

    # Obtener los nombres de las películas más similares
    similar_movies = movies.iloc[similar_indices]['title'].tolist()
    return similar_movies

@app.get("/recomendacion/")
async def recomendacion(titulo: str):
    # Obtener las recomendaciones
    peliculas_recomendadas = recomendar_peliculas(titulo)

    # Verificar si la película fue encontrada
    if not peliculas_recomendadas:
        raise HTTPException(status_code=404, detail="Película no encontrada")

    return {"recomendaciones": peliculas_recomendadas}
