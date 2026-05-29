# PCA

- Valentina Tejeda Fuentes
- Anairam San Nicolas Rodríguez
- Pedro Enrique Mendoza García 

Proyecto PCA para jugadores (backend Django + frontend React).
El sistema utiliza IncrementalPCA de scikit-learn para reducir 10 variables numéricas de cada jugador a una representación bidimensional (PCA_X, PCA_Y), permitiendo visualizar similitudes entre jugadores en una gráfica 2D.

Descripción
- Backend: API REST en Django REST Framework que permite crear/editar/eliminar jugadores con métricas físicas y estadísticas.
- Al crear jugadores, se dispara una tarea de Celery que agrupa jugadores pendientes para entrenar un modelo IncrementalPCA (scikit-learn).
- El modelo se guarda en `pca_model.pkl` y se genera una imagen con la proyección 2D en `static/pca_actual.png`.
- Frontend: Interfaz en React (Vite) ubicada en `front/nfl-pca` que muestra la gráfica más reciente y un formulario para enviar jugadores.

## Endpoints principales

POST /api/jugadores/
Crear jugador.

GET /api/grafica/
Obtiene la gráfica PCA más reciente en PNG.



Guía rápida de ejecución (Windows / PowerShell)
Se recomienda trabajar dentro de un entorno virtual (`venv`) para aislar las dependencias del proyecto.

1) Ejecutar Redis (recomendado con Docker):
```powershell
docker run -p 6379:6379 -d --name redis redis:latest
```

2) Backend
Para instalar las dependencias instalar requirements.txt. 
```powershell
cd back/pca_proyect
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r ..\requirements.txt
python manage.py migrate
```

3) Iniciar Celery (en una terminal, con el venv activo):
```powershell
cd back/pca_proyect
celery -A pca_proyect worker -l info -P solo
```

4) Iniciar servidor Django (otra terminal):
```powershell
cd back/pca_proyect
python manage.py runserver
```

5) Frontend (opcional):
```bash
cd front/nfl-pca
npm install
npm run dev
# Abrir la URL que indique Vite (por defecto http://localhost:5173)
```


Notas útiles
- La tarea de entrenamiento es asíncrona (Celery). Si Celery/Redis no están corriendo, los jugadores se guardan pero no se entrenará el PCA automáticamente.
- Para forzar la verificación sin Celery: ejecutar en shell Django:
```python
from jugadores.services import verificar_modelo
verificar_modelo()
```

