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

#my $be='777';
#my $msisdn='5538573678';
#my $free='123';
#my $tot='100.23';
#my $unsu='222';
#my $off='11111111';
#my $thv='10';
#my $vali='23';
#my $expire='20180427171226';
# "endpoint": "https://telefonica?wsdl"

if(length($msisdn)==10)
{
#Inserta info en BD
$connect="DBI:mysql:database=$data;$host:$port";
$dbh = DBI->connect($connect,$userid,$passwd);

$inserta=" insert into notificador.notificador_proxy(id_company,msisdn,freedata,total_amount,unsused_amount,offeringid,threshold,validity,fecha_notificacion,id_status) values ($be,$msisdn,$free,$tot,$unsu,$off,$thv,$vali,sysdate(),'1')";

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
valuesfinish;
$dbh->disconnect();
&datalog("$call");

#Envía ApiGee
#$manda=qq[curl -X POST \ https://altanredes-dev.apigee.net/ac/v1/clients/175/listener \ -H 'authorization: Bearer XXXXXXXXXXXXXXXXXXXXXXXXXXX' \ -H 'cache-control: no-cache' \ -H 'content-type: application/json' \ -H 'postman-token: 35f3e081-d4a9-da88-f58d-6cc53b543232' \ -d '{"eventType": "EVENT_UNITS","callback": "http://malmanza-eval-test.apigee.net/echoservice","event": {"id": "123","effectiveDate": "20180531205713","detail": "Order cancelled"}}'];
#my  $env=qx($manda);
#print "$env\n";
#&datalog("Envía ApiGee: $manda, $env");

#print $q->header("application/json");
#print $json->encode({ tificador_proxystatus => ok});
#print $json->encode({ url => $URL});
#&datalog($json->encode({status => ok}));

#Envía gorila
$cmd="perl /var/www/cgi-bin/bacth/funciones_gorilaV3.pl '' $be notificador '' '' '' $etype $call";
print "---->>>>>>>>>>>>>>>>>>>>>>>>$cmd<----------------------\n";
$ty=exec($cmd);
print "$ty \n";
&datalog($ty);
}
else
{
print $json->encode({ status => nok});
&datalog($json->encode({ status => nok}));
}



