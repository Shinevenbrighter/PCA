# PCA

Proyecto PCA para jugadores (backend Django + frontend React).

Descripción
- Backend: API REST en Django REST Framework que permite crear/editar/eliminar jugadores con métricas físicas y estadísticas. Al crear jugadores, se dispara una tarea de Celery que agrupa jugadores pendientes para entrenar un modelo IncrementalPCA (scikit-learn). El modelo se guarda en `pca_model.pkl` y se genera una imagen con la proyección 2D en `static/pca_actual.png`.
- Frontend: Interfaz en React (Vite) ubicada en `front/nfl-pca` que muestra la gráfica y un formulario para enviar jugadores.

Rutas principales
- `POST/GET/PUT/DELETE /api/jugadores/` — CRUD de jugadores (DRF ViewSet).
- `GET /api/grafica/` — Devuelve la imagen PNG generada con la visualización PCA.

Dependencias (backend)
- Python, Django, djangorestframework, celery, redis, scikit-learn, numpy, matplotlib, python-dotenv.
- Archivo: `back/requirements.txt`.

Guía rápida de ejecución (Windows / PowerShell)

1) Ejecutar Redis (recomendado con Docker):
```powershell
docker run -p 6379:6379 -d --name redis redis:latest
```

2) Backend
```powershell
cd back/pca_proyect
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r ..\requirements.txt
python manage.py migrate
python manage.py createsuperuser   # opcional
```

3) Iniciar Celery (en una terminal, con el venv activo):
```powershell
cd back/pca_proyect
celery -A pca_proyect worker -l info
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

Probar la API (ejemplo `curl` JSON)
```bash
curl -X POST http://127.0.0.1:8000/api/jugadores/ \
	-H "Content-Type: application/json" \
	-d '{"nombre":"Juan", "velocidad":5.0, "agilidad":6.0, "fuerza":7.0, "potencia":6.5, "edad":25, "peso":90, "altura":1.85, "partidos_jugados":10, "puntos_anotados":50, "partidos_ganados":6}'
```

Notas útiles
- La tarea de entrenamiento es asíncrona (Celery). Si Celery/Redis no están corriendo, los jugadores se guardan pero no se entrenará el PCA automáticamente.
- Para forzar la verificación sin Celery: ejecutar en shell Django:
```python
from jugadores.services import verificar_modelo
verificar_modelo()
```
- La imagen generada se sirve en `/api/grafica/`.

