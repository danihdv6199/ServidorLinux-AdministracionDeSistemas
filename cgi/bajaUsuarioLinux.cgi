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

my  $consulta=$conexion->prepare("SELECT nombreUsuario FROM users WHERE eliminar='1'");
        $consulta->execute();
my @usuario=$consulta->fetchrow_array(); #obtenemos los resultados

my $user=Linux::usermod->del($usuario[0]);

my $ruta = "/home/".$usuario[0]."/";
rmtree($ruta, 1, 1);
	
$conexion->do("DELETE FROM users WHERE nombreUsuario='$usuario[0]'");
print "<META HTTP-EQUIV='Refresh' CONTENT='1; URL=https://83.63.211.1/'>";



$consulta->finish();
$conexion->disconnect();





