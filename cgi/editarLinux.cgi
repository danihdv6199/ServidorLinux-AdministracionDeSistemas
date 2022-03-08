#!/usr/bin/perl

use strict;
use warnings;
use CGI qw();
use DBI;
use Linux::usermod;
use File::Path;
use Sudo;
use Passwd::Unix;

my $flag=0;

print("Content-Type: text/html\n\n");

my $conexion = DBI->connect("DBI:mysql:database=usuarios;host=localhost","root","daniyalvi2017",{'RaiseError' => 1}); #conexion a la base de datos usuarios
if($conexion == 1)
{
	$flag=1;
	print qq[<html><head><p>NO SE HA PODIDO CONECTAR CON LA BASE DE DATOS</p></head><a href="https://83.63.211.1/sesionIniciada.html">Pulse aqui para volver.</a></html>];
	exit;
}

my  $consulta=$conexion->prepare("SELECT nombreUsuario FROM users WHERE editar='1'");
        $consulta->execute();
my @usuario=$consulta->fetchrow_array(); #obtenemos los resultados

my  $consulta2=$conexion->prepare("SELECT clave FROM users WHERE editar='1' AND nombreUsuario='$usuario[0]'");
        $consulta2->execute();
my @pass=$consulta2->fetchrow_array(); #obtenemos los resultados

	
my $user=Linux::usermod->new($usuario[0]);
$user->set("password", $pass[0]);	
	
$conexion->do("UPDATE users SET editar=0 WHERE nombreUsuario='$usuario[0]' AND clave='$pass[0]'");	

print qq[<html><head><p>Usuario editado</p></head><a href="https://83.63.211.1/sesionIniciada.html">Pulse aqui para volver.</a></html>];
$consulta->finish();
$conexion->disconnect();


