# Sistema de Recomendación de Películas de Disney

Este proyecto consiste en el desarrollo de una API utilizando FastAPI para ofrecer funcionalidades relacionadas con un sistema de recomendación de películas de Disney. La API proporciona varias consultas sobre los datos de películas, actores y directores, además de un sistema de recomendación basado en la similitud de las películas.

## Contenidos

- [Descripción del Proyecto](#descripción-del-proyecto)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Cómo Ejecutar el Proyecto](#cómo-ejecutar-el-proyecto)
- [Endpoints de la API](#endpoints-de-la-api)
- [Modelo de Recomendación](#modelo-de-recomendación)
- [Despliegue](#despliegue)
- [Video de Demostración](#video-de-demostración)

## Descripción del Proyecto

El objetivo de este proyecto es proporcionar una API que permita consultar datos de películas, actores y directores, y además, recomendar películas similares a la ingresada por el usuario. La recomendación se basa en la similitud de la descripción de las películas.

## Estructura del Proyecto

- `main.py`: Archivo principal donde se define la API y todas las rutas.
- `Dataset/`: Carpeta que contiene el dataset utilizado para el análisis y las recomendaciones.
- `requirements.txt`: Archivo con las dependencias necesarias para ejecutar el proyecto.
- `README.md`: Archivo de documentación del proyecto.

## Requisitos

- Python 3.9 o superior
- FastAPI
- Pandas
- Scikit-learn
- Uvicorn

## Cómo Ejecutar el Proyecto

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/valenntesta/primer-proyecto.git
   cd primer-proyecto

2. Instala las dependencias:
   pip install -r requirements.txt

3. Ejecuta la aplicación:
   uvicorn main:app --reload

4.Accede a la API:
Abre tu navegador y dirígete a https://primer-proyecto-tga1.onrender.com/docs#/

*Endpoints de la API*
1. GET /cantidad_filmaciones_mes/{mes}
Devuelve la cantidad de películas estrenadas en un mes específico (en español).

2. GET /cantidad_filmaciones_dia/{dia}
Devuelve la cantidad de películas estrenadas en un día de la semana específico (en español).

3. GET /score_titulo/{titulo}
Devuelve el título, año de estreno y score de una película específica.

4. GET /votos_titulo/{titulo}
Devuelve el número de votos y el promedio de puntuaciones de una película específica. Solo se muestran películas con más de 2000 votos.

5. GET /get_actor/{nombre_actor}
Devuelve la cantidad de filmaciones y el retorno total y promedio de un actor específico.

6. GET /get_director/{nombre_director}
Devuelve la información de las películas dirigidas por un director específico.

7. GET /recomendacion/
Recomienda películas similares a la ingresada basadas en la similitud de sus descripciones.

Modelo de Recomendación
Propósito:
El modelo de recomendación sugiere películas similares a una película dada, basándose en las descripciones de las películas.

Cómo Funciona:
Entrada: El usuario proporciona el título de una película.
Proceso: El modelo analiza las descripciones (sinopsis) de todas las películas en el dataset y calcula cuán similares son entre sí.
Salida: El modelo devuelve una lista de 5 películas que son más similares a la película proporcionada, según la similitud de sus descripciones.

Video de Demostración
Aquí puedes encontrar un video que demuestra el funcionamiento de la API y del sistema de recomendación: 

Contribuciones
Si deseas contribuir a este proyecto, siéntete libre de hacer un fork del repositorio y enviar un pull request.





