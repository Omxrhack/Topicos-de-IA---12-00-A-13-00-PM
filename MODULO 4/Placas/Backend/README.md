# Sistema de Detección de Placas Vehiculares – Backend

Este repositorio contiene el **servidor backend** para el sistema de detección de placas vehiculares desarrollado para el **Módulo IV – Redes Neuronales**.

El backend expone una API REST que:

- Recibe una imagen de un vehículo.
- Detecta la región de la placa usando **OpenCV**.
- Extrae el texto de la matrícula usando **EasyOCR**.
- Consulta una base de datos **SQLite** para vincular la placa con su propietario.
- Devuelve la información en formato **JSON** para ser consumida por una app móvil iOS.

---

##  Tecnologías utilizadas

- **Python 3**
- **Flask** (API REST)
- **Flask-CORS** (para permitir peticiones desde iOS)
- **Gunicorn** (servidor WSGI para producción)
- **OpenCV** (procesamiento de imágenes)
- **EasyOCR** (reconocimiento de texto en placas)
- **NumPy**
- **SQLite** (base de datos embebida)
- **Render** (hosting del backend en la nube – opcional)

---

##  Estructura del proyecto

```text
Placas-backend/
├── api.py                # Punto de entrada Flask (API REST)
├── database.py           # Conexión SQLite, creación y seed de tablas
├── models.py             # Lógica de consulta a la BD (propietarios / vehículos)
├── plate_detector.py     # Detección aproximada de placa con OpenCV
├── ocr_engine.py         # OCR de la matrícula con EasyOCR
├── requirements.txt      # Dependencias de Python
├── Procfile              # Configuración de arranque para Render / Gunicorn
├── uploads/              # Carpeta donde se guardan imágenes subidas
└── vehicles.db           # Base de datos SQLite (se genera automáticamente)
