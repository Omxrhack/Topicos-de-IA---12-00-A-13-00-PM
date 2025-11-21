#  Sistema de Detección de Placas Vehiculares  
### Proyecto – Módulo IV: Redes Neuronales  
**Autores:** Omar Bermejo Osuna y Diego Araujo

## Descripción General

Este proyecto implementa un **sistema completo de detección y vinculación de matrículas vehiculares**, compuesto por:

###  Backend con Inteligencia Artificial
- Detección de placas con **OpenCV**
- OCR (lectura de caracteres) con **EasyOCR**
- Base de datos **SQLite** con propietarios y vehículos
- API REST desarrollada en **Flask**
- Servidor desplegado en **Render** para uso externo

###  App móvil iOS (SwiftUI)
- Tomar fotografías desde la cámara
- Seleccionar imágenes de la galería
- Enviar imágenes al backend para su procesamiento
- Mostrar placa detectada + información del propietario

###  Despliegue en la nube
- Backend disponible desde cualquier dispositivo iOS
- Peticiones HTTPS a través de Render
- App totalmente funcional sin conexión a laptop

##  Arquitectura del Sistema

```
iOS App (SwiftUI)
       │
       ▼
  HTTP POST (imagen)
       │
       ▼
Backend Flask (Render.com)
   - OpenCV (detección)
   - EasyOCR (OCR)
   - SQLite (propietarios/vehículos)
       │
       ▼
  JSON Response
```

##  Estructura del Proyecto

```
placas-project/
│
├── backend/
│   ├── api.py
│   ├── database.py
│   ├── models.py
│   ├── plate_detector.py
│   ├── ocr_engine.py
│   ├── requirements.txt
│   ├── Procfile
│   ├── uploads/
│   └── vehicles.db
│
└── Frontend/
    ├── PlacasApp.swift
    ├── Home.swift
    ├── PlateService.swift
    ├── ImagePicker.swift
    ├── Models.swift
    └── Assets.xcassets
```

##  Tecnologías Utilizadas

### Backend
- Python 3  
- Flask  
- Flask-CORS  
- OpenCV  
- EasyOCR  
- SQLite  
- Gunicorn  
- Render (hosting)

### iOS
- Swift  
- SwiftUI  
- PhotosUI  
- UIImagePickerController  
- URLSession

##  Base de Datos (SQLite)

### Tabla `owners`
| Campo | Tipo |
|-------|------|
| id | INTEGER PK |
| name | TEXT |
| phone | TEXT |
| email | TEXT |

### Tabla `vehicles`
| Campo | Tipo |
|--------|------|
| id | INTEGER PK |
| plate | TEXT UNIQUE |
| brand | TEXT |
| model | TEXT |
| year | INTEGER |
| owner_id | FK → owners.id |

##  API REST

### `POST /api/lookup_plate`

#### Parámetros
- `image` → archivo JPG/PNG (multipart/form-data)

#### Respuesta exitosa
```json
{
  "plate": "VBA1234",
  "ocr_confidence": 0.91,
  "owner": {
    "owner_name": "Juan Pérez",
    "owner_phone": "6671234567",
    "owner_email": "juan@example.com",
    "vehicle_brand": "Nissan",
    "vehicle_model": "Versa",
    "vehicle_year": 2020
  }
}
```

#### Si no existe en BD
```json
{
  "plate": "XYZ9988",
  "ocr_confidence": 0.89,
  "owner": null
}
```

#### Si no se detecta placa
```json
{
  "error": "No se detectó ninguna placa."
}
```

##  Instalación Local

```bash
git clone https://github.com/TU_USUARIO/placas-project.git
cd placas-project/backend
pip install -r requirements.txt
python api.py
```

Servidor local:
```
http://127.0.0.1:5000
```

##  Despliegue en Render

1. Subir backend a GitHub  
2. Crear Web Service en Render  
3. Build command:

```bash
pip install -r requirements.txt
```

4. Start command:

```bash
gunicorn api:app
```

5. Render genera una URL pública HTTPS, por ejemplo:

```
https://placas-omar.onrender.com
```

6. En la app iOS, actualizar:

```swift
let baseURL = URL(string: "https://placas-omar.onrender.com")!
```

## Uso en la App iOS

1. Seleccionar imagen o tomar foto  
2. Pulsar “Escanear placa”  
3. La imagen se envía al backend  
4. El servidor detecta:
   - Placa
   - Confianza OCR
   - Propietario (si existe)  
5. La app muestra el resultado

## Datasets recomendados

| Dataset | Imágenes | Tipo | URL |
|--------|----------|------|------|
| Roboflow LPR | 10k | Detección/OCR | https://universe.roboflow.com |
| Kaggle OCR Plates | 2.6M | OCR | https://kaggle.com |
| UFPR-ALPR | 4.5k | LATAM | https://web.inf.ufpr.br |

##  Casos de prueba

- Placa visible y clara → éxito  
- Placa con suciedad/luz baja → OCR más bajo  
- Imagen sin placa → error controlado  
- Placa detectada pero no registrada en BD → `owner: null`

