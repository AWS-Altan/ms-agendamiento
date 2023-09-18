#!/usr/bin/perl -w




#use strict;
use Time::Piece;
use warnings FATAL => 'all';
#use CGI qw();
use POSIX qw/strftime/;
use LWP::UserAgent;
use HTTP::Request;
use XML::Simple;
use SOAP::WSDL;
use SOAP::WSDL::Deserializer::Hash;
use SOAP::Lite;
use Time::Piece;
use XML::LibXML;
use XML::Twig;
use Data::Dumper;
use CGI ();

$dirlog="/var/www/cgi-bin/log/notificador";

sub bl
{
  my $tt=shift;
  return ((length($tt)==1))? "0".$tt : $tt;
}

sub parametro{
$id_com=shift;
$ut="cat /var/www/cgi-bin/bacth/kingkong.conf | grep $id_com ";
#print "$ut\n";
$rt=qx($ut);
#chomp $rt;
$rt =~ s/\n|\r|\t//g;
#$rt =~ s/'$'/\\$/g;
#$rt =~ s/@/\\@/g;
$utt="cat /var/www/cgi-bin/bacth/kingtoken.conf 2> /dev/null  ";
#print "$utt\n";
$rtt=qx($utt);
#print "->$rtt<-\n";
#chomp $rt;
#$rtt =~ s/\n|\r|\t//g;
$rt.=",";
$rt.=$rtt;
return $rt;
}


sub datalog{
$error=shift;
(my $seg, my $min, my $hora, my $dia, my $mes, my $ao, my @zape) = localtime(time);
  $ao += 1900;
  $mes=$mes+1;
  $mes=&bl($mes);
  $dia=&bl($dia);
  $hora=&bl($hora);
  $min=&bl($min);
  $seg=&bl($seg);
  my $log_file="$dirlog/log-notifBSS-$ao$mes$dia.log";
  open (LOG," >> $log_file");
  print LOG "$ao$mes$dia-$hora:$min:$seg - $error\n";
  close (LOG);
}

 
my $op='notificador';
my $be=$ARGV[0];
my $dn=$ARGV[1];
my $free=$ARGV[2];
my $tot=$ARGV[3];
my $uni=$ARGV[4];
my $esx=$ARGV[5];
my $tr=$ARGV[6];
my $ofe=$ARGV[7];

use DBI;
#Datos de la conexión
$data="notificador";
$host="10.0.0.23";
#$host="127.0.0.1";
$port="3306";
$userid="operador";
$passwd="operador01";
#$msisdn=$dn;
#Inserta info en BD
$connect="DBI:mysql:database=$data;$host:$port";
$dbh = DBI->connect($connect,$userid,$passwd);


$strsql = "select  count(*) from notificador.notificador_proxy where msisdn='$dn' and fecha_notificacion >  DATE_SUb(sysdate(), INTERVAL 50 minute) ";

print "$strsql \n";
$sth = $dbh->prepare($strsql);
$sth->execute or die("Couldn't execute $strsql.".$dbh->errstr."\n");


while(@row = $sth->fetchrow_array()){
          $id_tr = $row[0];


}

&datalog("conteo $id_tr");
if($id_tr==0)
{
$inserta=" insert into notificador.notificador_proxy(id_company,msisdn,freedata,total_amount,unsused_amount,offeringid,threshold,validity,fecha_notificacion,id_status) values ('$be','$dn','$free','$tot','$uni','$esx','$tr','$ofe',sysdate(),'0')";
&datalog($inserta);

$ejin = $dbh->prepare($inserta);
$ejin->execute or die("Couldn't execute $inserta $DBI::errstr.\n");
$inserta=" insert into notificador.notificador_proxy_history(id_company,msisdn,freedata,total_amount,unsused_amount,offeringid,threshold,validity,fecha_notificacion,id_status,reintento) values ('$be','$dn','$free','$tot','$uni','$esx','$tr','$ofe',sysdate(),'0','1')";

$ejin = $dbh->prepare($inserta);
$ejin->execute or die("Couldn't execute $inserta $DBI::errstr.\n");

}
else{
$inserta=" insert into notificador.notificador_proxy_history(id_company,msisdn,freedata,total_amount,unsused_amount,offeringid,threshold,validity,fecha_notificacion,id_status,reintento) values ('$be','$dn','$free','$tot','$uni','$esx','$tr','$ofe',sysdate(),'0','2')";
&datalog($inserta);

$ejin = $dbh->prepare($inserta);
$ejin->execute or die("Couldn't execute $inserta $DBI::errstr.\n");

&datalog("reintento de huawei $dn");
}



 $ejin->finish;
  $dbh->disconnect();

