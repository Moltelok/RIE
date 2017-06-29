# RIE

Template a Utilizar https://blackrockdigital.github.io/startbootstrap-sb-admin-2/pages/index.html

Desde este sacaremos ideas para las nuevas vistas.

>>>Indicaciones para mi amigo polin.

##Generating a new SSH key

1.- Open Terminal.

2.- Paste the text below, substituting in your GitHub email address.

$ ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

This creates a new ssh key, using the provided email as a label.

>Generating public/private rsa key pair.

3.- When you're prompted to "Enter a file in which to save the key," press Enter. This accepts the default file location.

>Enter a file in which to save the key (/home/you/.ssh/id_rsa): [Press enter]

4.- At the prompt, type a secure passphrase. For more information, see "Working with SSH key passphrases".

>Enter passphrase (empty for no passphrase): [Type a passphrase]

>Enter same passphrase again: [Type passphrase again]

##Ubicacion clave

Si la clave la guardaste en home/~, presiona ctrl+h para que se vean los archivos ocultos.

El archivo con el nombre que le diste con extension .pub, dentro esta la clave que me debes enviar

##Comando git para jalar el proyecto

para jalar el proyecto, debes configurar los servidores Remotos.

$mkdir rie
$cd rie/
$git clone "ruta del repositorio"

*Esta ruta se copia del repositorio.

##VirtualEnv

Debes crear la maquina virtual en la carpeta del proyecto rie/

$virtualenv .env

Luego activala

$source .env/bin/activate

E instala los requerimientos

$pip install -r requirements.txt

##Migration

Luego de que todo este bien, realisas las migraciones

$python manage.py makemigrations

$python manage.py migrate


>>>Nota: con eso dudo que tengas Problemas
