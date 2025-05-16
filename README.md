# Crear Entorno Virtual + Instalar Requisitos (`satuc3`)

Clona el repositorio:  
`git clone https://github.com/pagliardini/satuc3.git && cd satuc3`  

Crea el entorno virtual:  
`python -m venv venv`  

Activa el entorno (Windows: `.\venv\Scripts\activate`, macOS/Linux: `source venv/bin/activate`)  

Instala los requisitos:  
`pip install -r requirements.txt`

Swagger corre en http://localhost:5000/api/docs

En el repositorio ya hay una base de datos creada con registros de ejemplo, en caso de necesitar reiniciarla, borrar el archivo database.db en /instance y ejecutar create_db.py, opcionalmente se pueden insertar ejemplos aleatorios ejecutando insertar_datos.py
