#!/usr/bin/perl -w

use strict;
use warnings;
use CGI qw();
use DBI;
use File::Xcopy;


my $q=CGI->new;
my $usuario=$q->param('username');
my $contrasena=$q->param('password');
my $rcontrasena=$q->param('rpassword');
my $nombre=$q->param('name');


if($contrasena ne $rcontrasena)
{
#       print("contraseñas distintassss");#Contraseña seg mal
         print qq[<html><head><p>LAS CONTRASEÑAS NO COINCIDEN</p></head><a href="https://83.63.211.1/">Pulse aqui para volver.</a></html>];
        exit;
}


my $conexion = DBI->connect("DBI:mysql:database=wordpress;host=localhost","root","daniyalvi2017",{'RaiseError' => 1}); #conexion a la base de datos usuarios
if($conexion == 1)
{
        
        print qq[<html><head><p>NO SE HA PODIDO CONECTAR CON LA BASE DE DATOS</p></head><a href="https://83.63.211.1/registroLinux.html">Pulse aqui para volver.</a></html>];
	exit;
}

my  $consulta=$conexion->prepare("create database $nombre");
$consulta->execute();

$consulta=$conexion->prepare("use $nombre");
$consulta->execute();

$consulta=$conexion->prepare("create user \'$usuario\'@\'localhost\'");                                                                        
$consulta->execute();

$consulta=$conexion->prepare("grant all privileges on $nombre\.* to \'$usuario\'@\'localhost\' identified by \'$contrasena\' ");          
$consulta->execute();

$consulta=$conexion->prepare("flush privileges");
$consulta->execute();

$consulta->finish();



my $fx = new File::Xcopy;
$fx->from_dir("/var/www/html/wordpress");
$fx->to_dir("/var/www/html/" . $usuario . "_wordpress");
$fx->param('s',1);

$fx->xcopy;



print "<META HTTP-EQUIV='Refresh' CONTENT='0; URL=https://83.63.211.1/"  . $usuario . "_wordpress/wordpress'>";





