#!/usr/bin/perl

use strict;
use warnings;
use Authen::Simple::PAM; 
use CGI;

    # create a CGI object (query) for use
my $q = CGI->new;


my $username;
my $password;
my $flag=0;

print $q->header();

$username = $q->param('username');
$password = $q->param('password');



my $pam = Authen::Simple::PAM->new(
    service => 'login'
);

if ( $pam->authenticate($username , $password ) ) {

#    print qq[<html><head><p>Login Correcto</p></head><a href="https://83.63.211.1/sesionIniciada.html">Pulse aqui para iniciar.</a></html>];
	print "<META HTTP-EQUIV='Refresh' CONTENT='0; URL=https://83.63.211.1/sesionIniciada.html'>";

}else
{
	print(" Incorrecto");
	print qq[<html><head><p>Login Incorrecto</p></head><a href="https://83.63.211.1/">Pulse aqui para volver.</a></html>];
}

