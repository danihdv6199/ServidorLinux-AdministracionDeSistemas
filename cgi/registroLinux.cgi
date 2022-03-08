#!/usr/bin/perl

use strict;
use warnings;
use Email::Send::SMTP::Gmail;
use CGI;
use Linux::usermod;
use Authen::Simple::PAM;
use DBI;
use DBD::mysql;
use File::Copy::Recursive qw(dircopy);
use File::chown;
use File::lchown qw( lchown lutimes );
use File::Xcopy;

my $q=CGI->new;

my $usuario=$q->param('username');
my $contrasena=$q->param('password');
my $grupo=1006;
my $flag=0;
my $fx = new File::Xcopy; 

print qq(Content-type: text/html\n\n);
if($usuario eq undef || $contrasena eq undef)
{
	$flag=1;
	print qq[<html><head><p>HAY CAMPOS VACIOS</p></head><a href="https://83.63.211.1/registroLinux.html">Pulse aqui para volver.</a></html>];	
}

my $conexion = DBI->connect("DBI:mysql:database=usuarios;host=localhost","root","daniyalvi2017",{'RaiseError' => 1}); #conexion a la base de datos usuarios
if($conexion == 1)
{
        $flag=1;
        print qq[<html><head><p>NO SE HA PODIDO CONECTAR CON LA BASE DE DATOS</p></head><a href="https://83.63.211.1/registroLinux.html">Pulse aqui para volver.</a></html>];
}

my  $consulta=$conexion->prepare("SELECT nombreUsuario FROM users WHERE nombreUsuario='$usuario'");
    $consulta->execute();
my @data=$consulta->fetchrow_array(); #obtenemos los resultados

if($usuario ne $data[0]){ #no se encuentra usuario en BDD
 print qq[<html><head><p>usuario incorrecto</p></head><a href="https://83.63.211.1/registroLinux.html">Pulse aqui para volver.</a></html>];
       # print $q->redirect('https://83.63.211.1/registro.html');#no existe
	$flag=1;        
	exit;
}


my  $consulta2=$conexion->prepare("SELECT clave FROM users WHERE nombreUsuario='$usuario'");
    $consulta2->execute();
my @data2=$consulta2->fetchrow_array(); #obtenemos los resultados

if($contrasena ne $data2[0]){ #la clave no coincide con la del usuario en BBD
 print qq[<html><head><p>Contrasena incorrecta</p></head><a href="https://83.63.211.1/registroLinux.html">Pulse aqui para volver.</a></html>];
        #print $q->redirect('https://83.63.211.1/registro.html');#cont incorrecta
	$flag=1;
        exit;
}

my  $consulta5=$conexion->prepare("SELECT confirmacion FROM users WHERE nombreUsuario='$usuario'");
	$consulta5->execute();
my @data5=$consulta5->fetchrow_array(); #obtenemos los resultados

if($data5[0] == 1){#usuario ya confirmado
	 print qq[<html><head><p>Usuario ya confirmado</p></head><a href="https://83.63.211.1/">Pulse aqui para volver.</a></html>];
	$flag=1;
	exit;
}

$consulta->finish();
$consulta2->finish();


if($flag==0)
{
	
	my  $consulta3=$conexion->prepare("SELECT esProfesor FROM users WHERE nombreUsuario='$usuario'");
	    $consulta3->execute();
	my @data3=$consulta3->fetchrow_array(); #obtenemos los resultados

	if($data3[0] == 1){ #Es profesor
		$grupo=1004;
	}else
	{
		$grupo=1006;
	}

	#GENERAMOS EL DIRECTORIO DEL USUARIO Y MODIFICAMOS SUS PERMISOS
	my $ruta="/home/" . $usuario . "/";#creamos la ruta para su directorio personal
	mkdir $ruta;
	chmod(0755,$ruta);

	my $rutaPublic = $ruta . "/" . "public_html";
	mkdir $rutaPublic;

	
	my $rutaAdmin = "/home/admin" . "/" . "Apuntes";
	my $rutaApuntes = $ruta . "/" . "Apuntes";

	my $rutaWordpress =  "/var/www/html/" . $usuario . "_wordpress";
	mkdir $rutaWordpress ;	
	
	Linux::usermod->add($usuario,$contrasena,'',$grupo,'',$ruta,"/bin/bash") || print "USERADD: $! \n"; #Creamos el usuario

	#Obtenemos el usuario mediante Linux::usermod->new y lo almacenamos en la variable $user.
	my $user=Linux::usermod->new($usuario);

#	chown($user , $ruta) || print "CHOWN: $! \n";
#	chown($user->get(uid), $user->get(gid), $ruta) || print "CHOWN USER: $! \n";
#	$fx->xcp("/home/scriptuser/condiciones.txt" , $ruta );
	$fx->xcp("/home/scriptuser/", $rutaPublic , "condiciones.txt");
	
	#chown({deref=>0}, $usuario, $grup, $ruta);
	
#	`sudo chown $usuario, $ruta`;
	
	#my $uid = $user->get(uid);
	dircopy("/etc/skel",$ruta);

	my $link = symlink($rutaAdmin,$rutaApuntes);
	lchown "root",1004, $link;

	`sudo setquota -u $usuario 68359 78125 0 0 -a $ruta`;#creamos la cuata de 80mb para el usuario
	`sudo setquota -t 172800 172800 -a $ruta`;#establece el periodo de gracia de 2 dias

	#`setquota -u $usuario 0 5120 0 0 -a $ruta`;
	my $query =$conexion->prepare( "UPDATE users set confirmacion=1 where nombreUsuario='$usuario'");
	$query->execute();

	my $query1 =$conexion->prepare( "UPDATE users set permisos=1 where nombreUsuario='$usuario'");
        $query1->execute();
	

	print "\nUsuario $usuario creado con éxito\n";
	print "\n";

	my $pam = Authen::Simple::PAM->new(
	    service => 'login'
	);#iniciamos una sesion al usuario que ha confirmado su cuenta

	if ( $pam->authenticate( $usuario, $contrasena ) ) {
		print("Content-Type: text/html\n\n");
		print "Logeadooo\n";

		my  $consulta4=$conexion->prepare("SELECT correo FROM users WHERE nombreUsuario='$usuario'");#sacamos el correo del usuario
		    $consulta4->execute();
		my @data4=$consulta4->fetchrow_array();


		my ($mail,$error)=Email::Send::SMTP::Gmail->new( -smtp=>'smtp.gmail.com',
                                                 -login=>'daniyalvi2017@gmail.com',
                                                 -pass=>'calasanz2017');

		print "session error: $error" unless ($mail!=-1); #mandamos el correo con conddiciones de uso del servidor

		$mail->send(-to=>$data4[0], -subject=>'Enhorabuena, se ha dado de alta en el sistema!', -body=>'A disfrutar...');

		$mail->bye;

		$consulta4->finish();
		print "<META HTTP-EQUIV='Refresh' CONTENT='0; URL=https://83.63.211.1/'>";
	}
}

