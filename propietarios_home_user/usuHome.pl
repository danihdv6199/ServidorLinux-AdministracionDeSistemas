#!/usr/bin/perl
use strict;
use warnings;
use CGI;
use DBI;
use File::chown;
use File::lchown qw( lchown lutimes );

my $conexion = DBI->connect("DBI:mysql:database=usuarios;host=localhost","root","daniyalvi2017",{'RaiseError' => 1}); #conexion a la base de datos usuarios
	if($conexion == 1)
	{
		exit;
	}
	
	my  $consulta=$conexion->prepare("SELECT nombreUsuario,esProfesor FROM users where permisos='1' ");
	    $consulta->execute();
my $datos;
my @usuarios;
my $grupo;
my $ruta="/home/";

while( $datos = $consulta->fetchrow_arrayref() )
{
	push @usuarios,@$datos;
	my $usuario=$usuarios[0];
	if($usuarios[1] ==1){ $grupo=1004; }
	else{ $grupo=1006; }
	chown $usuario,$grupo, "/home/" . $usuario;
	my $query =$conexion->prepare( "UPDATE users set permisos=0 where nombreUsuario='$usuario'");
	$query->execute();
}

