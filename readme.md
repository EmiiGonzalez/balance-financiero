# Gestor Financiero

Este es un gestor financiero desarrollado en Python utilizando Tkinter para la interfaz gráfica. Permite gestionar ingresos, egresos, activos y pasivos, así como visualizar gráficos de análisis financiero.

## Requisitos

- Python 3.7 o superior
- Tkinter
- Matplotlib

## Instalación

1. Clona este repositorio:

   ```sh
   git clone https://github.com/tu_usuario/gestor-financiero.git
   cd gestor-financiero
   ```
2. Instala las dependencias:

   ```sh
   pip install -r requirements.txt
   ```

## Uso

Para ejecutar la aplicación, simplemente ejecuta el siguiente comando:

```sh
python financial-manager.py
```

## Empaquetar como .exe

Para empaquetar la aplicación como un archivo .exe, puedes usar PyInstaller:

```sh
pyinstaller --onefile --windowed --icon=icono.ico --add-data "config.json;." --add-data "icono.png;." financial-manager.py
```

El archivo .exe se generará en la carpeta `dist`.

## Contribuir

Si deseas contribuir a este proyecto, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -am 'Agregar nueva funcionalidad'`).
4. Sube tus cambios a tu fork (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

## Licencia

* [ ] Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
