#!/usr/bin/perl

use CGI ();
use Data::Dumper qw(Dumper);
use DBI;
use JSON qw(decode_json);

#Datos de la conexión
$data="notificador";
#$host="10.0.0.23";
$host="127.0.0.1";
$port="3306";
$userid="root";
$passwd="94170308";

my $q  = CGI->new;
my $json  = JSON->new->utf8;

my $yu=$q->param('POSTDATA');
my $input=$json->decode("$yu");
print $q->header("application/json");

my $be=$input->{'id_company'};
my $msisdn=$input->{'msisdn'};
my $free=$input->{'free_unit_type'};
my $tot=$input->{'total_amount'};
#my $ini=$input->{'initial_amount'};
my $unsu=$input->{'unused_amount'};
my $off=$input->{'offer_id'};
my $thv=$input->{'threshold_value'};
my $vali=$input->{'validity'};
my $expire=$input->{'expiration_date'};

$dirlog="/var/www/cgi-bin/log/notificador/";

sub bl
{
  my $tt=shift;
  return ((length($tt)==1))? "0".$tt : $tt;
}

sub datalog{
my $error=shift;
(my $seg, my $min, my $hora, my $dia, my $mes, my $ao, my @zape) = localtime(time);
  $ao += 1900;
  $mes=$mes+1;
  $mes=&bl($mes);
  $dia=&bl($dia);
  $hora=&bl($hora);
  $min=&bl($min);
  $seg=&bl($seg);
  my $log_file="$dirlog/log-notif-$ao$mes$dia.log";
  open (LOG," >> $log_file");
  print LOG "$ao$mes$dia-$hora:$min:$seg - $error\n";
  close (LOG);
}

if(length($msisdn)=='10' and ($be=='175' || $be=='130'))
{
#Inserta info en BD
$connect="DBI:mysql:database=$data;$host:$port";
$dbh = DBI->connect($connect,$userid,$passwd);

$inserta=" insert into notificador.notificador_proxy(id_company,msisdn,freedata,total_amount,unsused_amount,offeringid,threshold,validity,fecha_notificacion,id_status) values ($be,$msisdn,$free,$tot,$unsu,$off,$thv,$vali,sysdate(),'0')";

$ejin = $dbh->prepare($inserta);
$ejin->execute or die("Couldn't execute $inserta $DBI::errstr.\n");
$re=$dbh->errstr;
#&log("$ejin");
#Consulta Endpoint en BD
my $ty="select end_point, event_type from notificador.notificador_ws where id_company='$be'";
my $sth = $dbh->prepare($ty);
$sth->execute or die("Couldn't execute $ty $DBI::errstr.\n");
while (@row = $sth->fetchrow_array) 
{ 
$call = $row[0];
$etype = $row[1];
}
#valuesfinish;
#$dbh->disconnect();
&datalog("$call");
#Envía gpiGee Gorila
$cmd="perl /var/www/cgi-bin/bacth/funciones_gorilaV3.pl '' $be notificador '' '' '' $etype $call";
#$cmd="perl /opt/blackbird/masterbacthv8_notificador.pl $be notificador $etype $call";
print "---->>>>>>>>>>>>>>>>>>>>>>>>$cmd<----------------------\n";
my $ty=qx($cmd);
print "$ty \n";
&datalog("$ty");

if($ty=~"effectiveDate"){
$up="update notificador.notificador_proxy set id_status='1' where msisdn='$msisdn'";
my $sth = $dbh->prepare($up);
$sth->execute or die("Couldn't execute $apg $DBI::errstr.\n");
print "$sth\n";
&datalog("$sth");
#{"beId":"175","effectiveDate":"20180613192336"
				}
else{
$up="update notificador_proxy set id_status='3' where msisdn='$msisdn'";
my $sth = $dbh->prepare($up);
$sth->execute or die("Couldn't execute $apg $DBI::errstr.\n");
print "$sth\n";
}
}
else
	{
print "El msisdn o el id_company no es válido";
#print $json->encode({ status => nok});
#&datalog($json->encode({ status => nok}));
	}

valuesfinish;
$dbh->disconnect();

