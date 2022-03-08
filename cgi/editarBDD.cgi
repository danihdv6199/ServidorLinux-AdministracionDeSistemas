#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use DBI;
use Linux::usermod;
use File::Path;
use CGI qw(:standard);

my $q=CGI->new;
my $query=new CGI;
my $usuario=$q->param('username');
my $nombre;
$nombre=$q->param('name');
my $contrasena=$q->param('pass');
my $nuevaContrasena;
$nuevaContrasena=$q->param('newPass');
my $apellidos=$q->param('surnames');
my $dPostal=$q->param('dPostal');
my $correo=$q->param('email');
my$flag=0;

print qq(Content-type: text/html\n\n);

my $conexion = DBI->connect("DBI:mysql:database=usuarios;host=localhost","root","daniyalvi2017",{'RaiseError' => 1}); #conexion a la base de datos usuarios
if($conexion == 1)
{
	$flag=1;
	print qq[<html><head><p>NO SE HA PODIDO CONECTAR CON LA BASE DE DATOS</p></head><a href="https://83.63.211.1/">Pulse aqui para volver.</a></html>];	
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
	print qq[<html><head><p>NO EXISTE ESE USUARIO EN EL SISTEMA, O LA CONTRASEÑA ES INCORRECTA.</p></head><a href="https://83.63.211.1/editarInfo.html">Pulse aqui para volver.</a></html>];	
	exit;
}
else
{
#print qq(Content-type: text/html\n\n);
	$conexion->do("UPDATE users SET editar=1 WHERE nombreUsuario='$usuario'");
	
	if($nombre ne undef)
	{
		$conexion->do("UPDATE users SET nombre='$nombre' where nombreUsuario='$usuario'");

	}

	if($apellidos ne undef)
	{
		$conexion->do("UPDATE users SET apellidos='$apellidos' where nombreUsuario='$usuario'");

	}

	if($correo ne undef)
	{
		$conexion->do("UPDATE users SET correo='$correo' where nombreUsuario='$usuario'");
	}
	
	if($nuevaContrasena ne undef)
	{
		$conexion->do("UPDATE users SET clave='$nuevaContrasena' where nombreUsuario='$usuario'");
	}
	
	if($dPostal ne undef)
	{
		$conexion->do("UPDATE users SET direccionPostal='$dPostal' where nombreUsuario='$usuario'");
	}

#	print "<META HTTP-EQUIV='Refresh' CONTENT='2; URL=https://83.63.211.1/cgi-bin/editarLinux.cgi'>";	
}
print "<META HTTP-EQUIV='Refresh' CONTENT='2; URL=https://83.63.211.1/cgi-bin/editarLinux.cgi'>";
$consulta->finish();
$conexion->disconnect();
exit;


