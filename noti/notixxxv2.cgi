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

my $cgi = CGI->new;
print $cgi->header(-type => "text/xml", -charset => "utf-8");
my $xml = $cgi->param("POSTDATA");
my $twig = new XML::Twig(twig_handlers => {'off:ConsumptionNotifyTOThirdPartyReqMsg' => \&ServiceException});
$twig->parse($xml);
&datalog("Recibe BSS:$xml");

sub ServiceException
 {
     my ( $twig, $ServiceException ) = @_;
     my @f = ($ServiceException->field('off:BEID'),$ServiceException->field('off:MSISDN'),$ServiceException->field('off:FreeUnitTypeName'),$ServiceException->field('off:TotalAmount'),$ServiceException->field('off:UnUsedAmount'),$ServiceException->field('off:ExpiryDate'),$ServiceException->field('off:ThresholdValue'),$ServiceException->field('off:OfferingID'));
 
my $op='notificador';
my $be=$f[0];
my $dn=$f[1];
my $free=$f[2];
my $tot=$f[3];
my $uni=$f[4];
my $esx=$f[5];
my $tr=$f[6];
my $ofe=$f[7];

}


if ($be =~ /\S/ and $dn =~ /\S/ and $free =~ /\S/ and $tot =~ /\S/ and $uni =~ /\S/ and $tr =~ /\S/){
#$cm=&quehora;
#$pre=qx($cm);
(my $seg, my $min, my $hora, my $dia, my $mes, my $ao, my @zape) = localtime(time);
  $ao += 1900;
  $mes=$mes+1;
  $mes=&bl($mes);
  $dia=&bl($dia);
  $hora=&bl($hora);
  $min=&bl($min);
  $seg=&bl($seg);
my $timestamp ="$ao$mes$dia$hora$min$seg";


my $fg= '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:off="http://www.huawei.com/bss/soaif/interface/OfferingService/" xmlns:com="http://www.huawei.com/bss/soaif/interface/common/"><soapenv:Header/><soapenv:Body><off:ConsumptionNotifyTOThirdPartyRspMsg><com:RspHeader><com:Version>1</com:Version><com:ReturnCode>0000</com:ReturnCode><com:ReturnMsg>Success.</com:ReturnMsg><com:RspTime>'.$timestamp.'</com:RspTime></com:RspHeader></off:ConsumptionNotifyTOThirdPartyRspMsg></soapenv:Body></soapenv:Envelope>';
#return $fg;
##print $op;
##create a object
##$xml = new XML::Simple;
## read XML file
##$data = $xml->XMLin($fg);
## print output
## print Dumper($data);


print $fg;

}

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

$er="select  count(*) from notificador.notificador_proxy where msisdn='$dn' and fecha_notificacion >  DATE_SUb(sysdate(), INTERVAL 5 minute)";

my $sth = $dbh->prepare($er);
$sth->execute or die("Couldn't execute $er $DBI::errstr.\n");
while (@row = $sth->fetchrow_array)
{
my $cou = $row[0];
}

if($cou==0)
{
$inserta=" insert into notificador.notificador_proxy(id_company,msisdn,freedata,total_amount,unsused_amount,offeringid,threshold,validity,fecha_notificacion,id_status) values ('$be','$dn','$free','$tot','$uni','$esx','$tr','$ofe',sysdate(),'0')";

$ejin = $dbh->prepare($inserta);
$ejin->execute or die("Couldn't execute $inserta $DBI::errstr.\n");

$inserta=" insert into notificador.notificador_proxy_history(id_company,msisdn,freedata,total_amount,unsused_amount,offeringid,threshold,validity,fecha_notificacion,id_status,reintento) values ('$be','$dn','$free','$tot','$uni','$esx','$tr','$ofe',sysdate(),'0','1')";

$ejin = $dbh->prepare($inserta);
$ejin->execute or die("Couldn't execute $inserta $DBI::errstr.\n");


}
else{
$inserta=" insert into notificador.notificador_proxy_history(id_company,msisdn,freedata,total_amount,unsused_amount,offeringid,threshold,validity,fecha_notificacion,id_status,reintento) values ('$be','$dn','$free','$tot','$uni','$esx','$tr','$ofe',sysdate(),'0','$cou')";

$ejin = $dbh->prepare($inserta);
$ejin->execute or die("Couldn't execute $inserta $DBI::errstr.\n");
}

#$inserta=" insert into notificador.notificador_proxy(id_company,msisdn,freedata,total_amount,unsused_amount,offeringid,threshold,validity,fecha_notificacion,id_status) values ('$be','$dn','$free','$tot','$uni','$esx','$tr','$ofe',sysdate(),'0')";

#$ejin = $dbh->prepare($inserta);
#$ejin->execute or die("Couldn't execute $inserta $DBI::errstr.\n");

#Consulta Endpoint en BD
#my $ty="select end_point, event_type from notificador.notificador_ws where id_company='$be'";
#my $sth = $dbh->prepare($ty);
#$sth->execute or die("Couldn't execute $ty $DBI::errstr.\n");
#while (@row = $sth->fetchrow_array)
#{
#my $call = $row[0];
#my $etype = $row[1];
#}


 # }
#}

 $ejin->finish;
  $dbh->disconnect();

