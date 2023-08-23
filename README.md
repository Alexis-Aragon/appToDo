# task Manager - Project
Esta es una app minimalista para crear una lista de tareas diarias pendientes, permite maracar las tareas realizadas para posteriormente eliminarlas y agregar nuevas tareas. 

Para correr la app taskmanager desde la terminal
necesitará instalar los siguientes módulos

```sh
pip3 install customtkinter
pip3 install appdirs

```
o use 
```sh
pip3 install -r requirements.txt
```
Después puede ejecutar el archivo con
```sh
python3 taskManager.py
```

También puede usar pyinstaller para crear un ejecutable

En linux mint puede usar
```sh
pyinstaller --onefile -n "taskManager" --add-data "taskmanager.png:." taskManager.py
```

En windows puede usar
```sh
pyinstaller --onefile -n "taskManager" --add-data "taskmanager.ico;." taskManager.py