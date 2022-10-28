#!/bin/bash

# Variables
curr_dir=`pwd`
venv_name="beeware-env"
venv="$curr_dir/$venv_name"
requirements="$curr_dir/requirements.txt"

# Si no está creado el entorno virtual se crea
if [[ ! -d $venv ]]; then
  # Creamos y activamos el entorno virtual
  python3 -m venv $venv_name
  source "$venv/bin/activate"

  # Instalamos briefcase
  python -m pip install briefcase
  
  # Para instalar las dependencias requeridas por beeware -> briefcase new
  briefcase new --no-input
  cd helloworld
  briefcase dev --no-run

  # Borramos el proyecto creado para instalar las dependencias
  cd ..
  rm -rf helloworld
fi

# Se instalan las depencias externas a beeware
source "$venv/bin/activate"
python -m pip install -r $requirements

# Se informa de que se ha finalizado la configuración del entorno
echo -e "\n\n¡Todo OK! Entorno configurado"
echo -e "Para ejecutar tests -> pytest tests/"
echo -e "Para ejecutar app   -> briefcase dev"
echo -e "\n"
echo -e "RECUERDA:"
echo -e "\tAl EMPEZAR a trabajar, ACTIVA el entorno virtual -> source $venv/bin/activate"
echo -e "\tAl TERMINAR de trabajar, DESACTIVA el entorno virtual -> deactivate"
echo -e "\n"
