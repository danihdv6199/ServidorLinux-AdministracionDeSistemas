#!/usr/bin/perl

use strict;
use warnings;
use CGI qw();
use DBI;
use Email::Send;
use Email::Simple::Creator;
use Email::Send::SMTP::Gmail;

my $web = CGI->new;
my $usuario = $web->param('username');
my $flag=0;
print qq(Content-type: text/html\n\n);

if($usuario eq undef)
{
	$flag=1;
	print qq[<html><head><p>Rellene el campo nombre de usuario</p></head><a href="https://83.63.211.1/olvidoContrasena.html">Pulse aqui para volver.</a></html>];	
}

my $conexion = DBI->connect("DBI:mysql:database=usuarios;host=localhost","root","daniyalvi2017",{'RaiseError' => 1}); #conexion 
if($conexion == 1)
{
        $flag=1;
}

my  $consulta1=$conexion->prepare("SELECT nombreUsuario FROM users WHERE nombreUsuario='$usuario'");
    $consulta1->execute();
my @data1=$consulta1->fetchrow_array(); #obtenemos los resultados


if($usuario ne $data1[0]){
	$flag=1;
	print qq[<html><head><p>Nombre usuario incorrecto</p></head><a href="https://83.63.211.1/olvidoContrasena.html">Pulse aqui para volver.</a></html>];	
}

if($flag==0)
{

my  $consulta2=$conexion->prepare("SELECT correo FROM users WHERE nombreUsuario='$usuario'");
    $consulta2->execute();
my @data2=$consulta2->fetchrow_array(); #obtenemos los resultados

my  $consulta3=$conexion->prepare("SELECT clave FROM users WHERE nombreUsuario='$usuario'");
    $consulta3->execute();
my @data3=$consulta3->fetchrow_array(); #obtenemos los resultados
my $pass=$data3[0];

my ($mail,$error)=Email::Send::SMTP::Gmail->new( -smtp=>'smtp.gmail.com',
                                                 -login=>'daniyalvi2017@gmail.com',
                                                 -pass=>'calasanz2017');

print "session error: $error" unless ($mail!=-1); 

$mail->send(-to=>$data2[0], -subject=>'Su contrasena', -body=>"$pass");

$mail->bye;
print qq[<html><head><p>Revise su correo</p></head><a href="https://83.63.211.1/">Pulse aqui para volver.</a></html>];
}
