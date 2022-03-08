#!/usr/bin/perl
use strict;
use warnings;
use CGI;
use DBI;
use Email::Send;
use Email::Simple::Creator;
use Email::Send::SMTP::Gmail;
use Regexp::Common 'number';

my $q=CGI->new;

my $usuario=$q->param('username');
my $contrasena=$q->param('password');
my $rcontrasena=$q->param('rpassword');
my $nombre=$q->param('name');
my $apellidos=$q->param('surnames');
my $correo=$q->param('email');
my $direccionPostal=$q->param('dPostal');
my $grupo=$q->param('grupo');

my $esProfesor = 0;
my $eliminar = 0;
my $editar =0;
my $flag=0;
my $confirmacion=0;
my $permisos=0;

print qq(Content-type: text/html\n\n);
if($correo eq undef || $usuario eq undef || $contrasena eq undef || $rcontrasena eq undef || $nombre eq undef || $apellidos eq undef || $direccionPostal == undef || $grupo eq undef)
{
	$flag=1;
	#print $q->redirect('https://www.elmundo.es/');
	print qq[<html><head><p>HAY CAMPOS VACIOS</p></head><a href="https://83.63.211.1/">Pulse aqui para volver.</a></html>];	
}
if($grupo eq "profesor")
{
	$esProfesor=1;
}
if($contrasena ne $rcontrasena)
{
#	print("contraseñas distintassss");#Contraseña seg mal
	 print qq[<html><head><p>LAS CONTRASEÑAS NO COINCIDEN</p></head><a href="https://83.63.211.1/">Pulse aqui para volver.</a></html>];

	$flag=1;
}

if($flag==0)
{
	my $conexion = DBI->connect("DBI:mysql:database=usuarios;host=localhost","root","daniyalvi2017",{'RaiseError' => 1}); #conexion a la base de datos usuarios
	if($conexion == 1)
	{
		$flag=1;
		print qq[<html><head><p>NO SE HA PODIDO CONECTAR CON LA BASE DE DATOS</p></head><a href="https://83.63.211.1/registro.html">Pulse aqui para volver.</a></html>];	
	}
	
	my  $consulta=$conexion->prepare("SELECT nombreUsuario FROM users WHERE nombreUsuario='$usuario'");
	    $consulta->execute();
	my @data=$consulta->fetchrow_array(); #obtenemos los resultados
	
	if($usuario eq $data[0]){
		print qq[<html><head><p>ya existe ese usuario</p></head><a href="https://83.63.211.1/">Pulse aqui para volver.</a></html>];
		exit;
	}

	$consulta->finish();

	my $query =$conexion->prepare( "INSERT INTO users (nombreUsuario,correo,nombre,apellidos,direccionPostal,esProfesor,clave,confirmacion,eliminar,editar,permisos) VALUES
	(\'$usuario'\,\'$correo'\,\'$nombre'\,\'$apellidos'\,\'$direccionPostal'\,\'$esProfesor'\,\'$contrasena'\,\'$confirmacion'\,\'$eliminar'\,\'$editar'\,\'$permisos'\)");
	$query->execute();

	        my ($mail,$error) = Email::Send::SMTP::Gmail->new( -smtp=>'smtp.gmail.com',
                                                           -login=>'daniyalvi2017@gmail.com',
                                                           -pass=>'calasanz2017',
                                                           -layer=>'ssl');

        print "Error: $error" unless ($mail !=-1);

        $mail->send(-to=>$correo, -subject=>'Confirmación de cuenta', -body=>'https://83.63.211.1/registroLinux.html');

        $mail->bye;
	#print $q->header;
	#print $q->redirect('https://83.63.211.1/registro.html');#
	print qq[<html><head><p>Revisa tu correo</p></head><a href="https://83.63.211.1/">Pulse aqui para volver.</a></html>];

exit;
}
