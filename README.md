<p align="center">
<FONT FACE="times new roman" SIZE=5>
<i><b>Big Data e Ingeniería de Datos</b></i>
<br>
<img src="https://res-5.cloudinary.com/crunchbase-production/image/upload/c_lpad,h_256,w_256,f_auto,q_auto:eco/v1455514364/pim02bzqvgz0hibsra41.png"
width="150" height="150">
</img>
<br>
<i><b>Docente:</b></i><br> Camilo Rodriguez
<br>
<i><b>Autores:</b></i>
<br>
Santiago Nohrá Nieto
<br>
Juan Camilo Rodríguez Fonseca
<br>
<i><b>Programa:</b></i>
<br>
Ciencias de la computación e inteligencia artificial
<br>

# Proyecto de scraping con AWS Lambda y Zappa
Este proyecto tiene como objetivo realizar scraping de la página web de <a href="https://casas.mitula.com.co/">Mitula</a> para obtener información de casas en el sector de Chapinero. Se utilizará AWS Lambda y Zappa para descargar la página web y extraer la información necesaria, y se almacenará en un archivo CSV en un bucket de S3.

## Requerimientos

- AWS CLI
- Cuenta de AWS con permisos para crear funciones Lambda, buckets de S3 y roles IAM
- Python 3.8 para garantizar funcionamiento de Zappa
- Zappa

## Instalación

- Clonar el repositorio
**En linux
- Instalar lo necesario para crear un ambiente de python: sudo apt install virtualenv
- Instalar python3.8 y luego ejecutar el siguiente comando: virtualenv -p python3.8 env
- Instalar las dependencias con pip: pip install -r requirements.txt
- Configurar las credenciales de AWS en la terminal: aws configure (Puede configurarlas en su repositorio de git)
- Configurar el archivo zappa_settings.json con los valores necesarios, teniendo en cuenta desencadenadores y demás.
- El paso anterior se realiza con 'zappa init' y editando el zappa_settings.json generado.

## Uso

### Lambda para descargar página (lambda1 - lambda1_html.py)

Para crear la función lambda que descarga la página web, ejecutar los siguientes comandos:

- cd lambda1
- zappa deploy

La función se ejecutará todos los lunes a las 9am. El resultado (yyyy-mm-dd.html) se guardará en el bucket de S3 especificado en el archivo zappa_settings.json.

### Lambda para procesamiento de información

Cuando la página web se haya descargado y almacenado en el bucket de S3, se ejecutará automáticamente la segunda función lambda que extraerá la información y la guardará en un archivo CSV en el bucket de S3 especificado en el archivo zappa_settings.json.

Para crear la función lambda que procesa la información, ejecutar el siguiente comando:

- cd lambda2
- zappa deploy

### Pruebas unitarias

Para ejecutar las pruebas unitarias, se pueden utilizar los siguientes comandos:

- cd lambda1
- pytest
- cd ..
- cd lambda2
- pytest

## Despliegue continuo con GitHub Actions

Se ha configurado un pipeline de despliegue continuo utilizando GitHub Actions. Cada vez que se haga un push o un pull request al repositorio, se ejecutarán las siguientes etapas:

- Revisión de código limpio con flake8
- Ejecución de pruebas unitarias
- Despliegue automático en AWS mediante Zappa

Para utilizar este pipeline, se deben configurar las variables de entorno AWS_ACCESS_KEY_ID y AWS_SECRET_ACCESS_KEY en el repositorio de GitHub. También puede necesitar AWS_SESSION_TOKEN en caso de tener un lab temporal de AWS.

*En el repositorio encuentra '**.github/workflows**', el cual contiene el pipeline mencionado.
