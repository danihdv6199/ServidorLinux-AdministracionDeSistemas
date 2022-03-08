#! /usr/bin/perl

use strict;
use warnings;
use DBI;
use Linux::usermod;
use File::Path;
use CGI;

my $q=CGI->new;
my $usuario=$q->param('username');
my $contrasena=$q->param('pass');

print qq(Content-type: text/html\n\n);

my $conexion = DBI->connect("DBI:mysql:database=usuarios;host=localhost","root","daniyalvi2017",{'RaiseError' => 1}); #conexion a la base de datos usuarios
if($conexion == 1)
{
        print qq[<html><head><p>NO SE HA PODIDO CONECTAR CON LA BASE DE DATOS</p></head><a href="https://83.63.211.1/">Pulse aqui para volver.</a></html>];
	exit;
}

my $consulta=$conexion->prepare("SELECT * FROM users WHERE nombreUsuario='$usuario' AND clave='$contrasena'");
$consulta->execute();

my $datos;
my @usuarios;

while( $datos = $consulta->fetchrow_arrayref() )
{
        push @usuarios,@$datos[0];

}

if(scalar @usuarios == 0)
{
print qq[<html><head><p>NO EXISTE ESE USUARIO EN EL SISTEMA, O LA CONTRASEÑA ES INCORRECTA.</p></head><a href="https://83.63.211.1/bajaUsuario.html">Pulse aqui para volver.</a></html>];
exit;
}
else
{
	$conexion->do("UPDATE users SET eliminar=1 WHERE nombreUsuario='$usuario' AND clave='$contrasena'");
	print "<META HTTP-EQUIV='Refresh' CONTENT='2; URL=https://83.63.211.1/cgi-bin/bajaUsuarioLinux.cgi'>";
}
