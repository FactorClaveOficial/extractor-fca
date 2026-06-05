# 📊 Extractor CFDI - FCA

Herramienta web moderna para extraer facturas electrónicas (CFDI) de archivos ZIP y generar reportes en Excel estructurados.

## ✨ Características Principales

✅ **Carga de ZIP** → Soporte drag & drop  
✅ **Búsqueda recursiva** → Encuentra XMLs en todas las subcarpetas  
✅ **Extracción inteligente** → Parsea datos de facturas CFDI  
✅ **Excel con 4 pestañas:**
   - **Encabezados:** 1 fila por factura con datos principales
   - **Conceptos:** Líneas de factura con detalles de productos/servicios
   - **Impuestos:** Trasladados y retenciones
   - **Timbres TFD:** Información de timbre fiscal digital

✅ **Interfaz moderna** → Diseño responsivo y fácil de usar  
✅ **Manejo de errores** → Campos vacíos si no existen en XML  
✅ **Descarga automática** → Obtén el Excel inmediatamente

## 🚀 Instalación Rápida

### Requisitos
- Python 3.8+
- pip

### Pasos

1. **Clona el repositorio:**
```bash
git clone https://github.com/FactorClaveOficial/extractor-fca.git
cd extractor-fca
```

2. **Crea un entorno virtual (opcional pero recomendado):**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instala las dependencias:**
```bash
pip install -r requirements.txt
```

4. **Ejecuta la aplicación:**
```bash
python app.py
```

5. **Abre en tu navegador:**
```
http://localhost:5000
```

## 📁 Estructura del Proyecto

```
extractor-fca/
├── app.py                 # Aplicación Flask principal
├── xml_parser.py          # Parser de XMLs CFDI
├── excel_generator.py     # Generador de reportes Excel
├── processor.py           # Orquestador del procesamiento
├── requirements.txt       # Dependencias del proyecto
├── README.md             # Este archivo
├── .gitignore            # Archivos a ignorar en Git
└── templates/
    └── index.html        # Interfaz web
```

## 🔧 Módulos

### `xml_parser.py`
Parser CFDI que extrae:
- **Datos de encabezado:** Folio, serie, fechas, RFC, nombres
- **Conceptos:** Cantidad, descripción, precios
- **Impuestos:** Trasladados y retenciones
- **Timbre:** UUID, fecha de timbrado, RFC de proveedor

### `excel_generator.py`
Generador de reportes con:
- Estilos profesionales
- 4 pestañas temáticas
- Bordes y formato automático
- Columnas ajustadas al contenido

### `processor.py`
Orquestador que:
- Descomprime ZIPs
- Busca XMLs recursivamente
- Parsea múltiples archivos
- Genera reportes unificados

### `app.py`
Aplicación Flask con:
- Endpoint `/upload` para cargar archivos
- Endpoint `/download` para descargar Excel
- Interfaz web con HTML5

## 📊 Formato de Salida

El Excel generado contiene 4 pestañas:

### Pestaña 1: Encabezados
| Folio | Serie | Fecha | RFC Emisor | Total | ... |
|-------|-------|-------|-----------|-------|-----|

### Pestaña 2: Conceptos
| Folio | Serie | Descripción | Cantidad | Importe | ... |
|-------|-------|-------------|----------|---------|-----|

### Pestaña 3: Impuestos
| Folio | Serie | Tipo | Impuesto | Tasa | Importe |
|-------|-------|------|----------|------|---------|

### Pestaña 4: Timbres TFD
| Folio | Serie | UUID | Fecha Timbrado | RFC Proveedor | ... |
|-------|-------|------|-----------------|---------------|-----|

## 💡 Casos de Uso

- 📈 **Auditoría fiscal:** Procesa cientos de facturas en minutos
- 📋 **Contabilidad:** Integra datos en sistemas contables
- 🔍 **Análisis:** Estudia patrones en facturas
- 📊 **Reportes:** Genera informes estructurados

## ⚙️ Dependencias

- **Flask 3.0.0:** Framework web
- **Werkzeug 3.0.1:** Utilidades WSGI
- **openpyxl 3.11.0:** Generación de Excel

## 🐛 Solución de Problemas

### "No se encontraron archivos XML"
- Verifica que el ZIP contiene archivos `.xml`
- Los archivos XML deben estar en cualquier subcarpeta

### "Error al generar Excel"
- Asegúrate de tener espacio en disco
- Verifica permisos de escritura en la carpeta `outputs/`

### "Puerto 5000 en uso"
```python
# Modifica el puerto en app.py
app.run(port=5001)
```

## 📝 Ejemplo de Uso

```python
from processor import ZIPProcessor

processor = ZIPProcessor()
success, message, stats = processor.process_zip(
    'facturas.zip',
    'reporte_facturas.xlsx'
)

if success:
    print(f"✅ {message}")
    print(f"Procesadas: {stats['xml_files_processed']} facturas")
```

## 🔐 Notas de Seguridad

- ⚠️ Los archivos subidos se limpian automáticamente después de procesar
- 🔒 Usa HTTPS en producción
- 📦 Máximo 500 MB por archivo
- 🛡️ Valida los XMLs antes de procesar datos sensibles

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios mayores:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver `LICENSE` para más detalles.

## 👨‍💻 Autor

**FactorClaveOficial**

## 📧 Contacto

Para preguntas o sugerencias, abre un issue en el repositorio.

---

**Última actualización:** Junio 2026  
**Versión:** 1.0.0
