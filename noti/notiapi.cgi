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
  my $log_file="$dirlog/log-notif2-$ao$mes$dia.log";
  open (LOG," >> $log_file");
  print LOG "$ao$mes$dia-$hora:$min:$seg - $error\n";
  close (LOG);
}

my $cgi = CGI->new;
print $cgi->header(-type => "text/xml", -charset => "utf-8");
my $xml = $cgi->param("POSTDATA");
&datalog( "$xml");
#my $xml='<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:com="http://www.huawei.com/bss/soaif/interface/common/" xmlns:off="http://www.huawei.com/bss/soaif/interface/OfferingService/">
my $twig = new XML::Twig(twig_handlers => {'off:ConsumptionNotifyTOThirdPartyReqMsg' => \&ServiceException});
$twig->parse($xml);

sub ServiceException
  {
     my ( $twig, $ServiceException ) = @_;
     my @f = ($ServiceException->field('off:BEID'),$ServiceException->field('off:MSISDN'),$ServiceException->field('off:FreeUnitTypeName'),$ServiceException->field('off:TotalAmount'),$ServiceException->field('off:UnUsedAmount'),$ServiceException->field('off:ExpiryDate'),$ServiceException->field('off:ThresholdValue'),$ServiceException->field('off:OfferingID'));
&datalog(print "$f[0],", "$f[1],");

 
my $op='notificador';
my $be=$f[0];
my $dn=$f[1];
my $free=$f[2];
my $tot=$f[3];
my $uni=$f[4];
my $esx=$f[5];
my $tr=$f[6];
my $ofe=$f[7];

if ($be =~ /\S/){
#$cm=&quehora;
#$pre=qx($cm);
  my $fg= '<?xml version="1.0" encoding="UTF-8"?>\n<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:off="http://www.huawei.com/bss/soaif/interface/OfferingService/" xmlns:com="http://www.huawei.com/bss/soaif/interface/common/">
  <soapenv:Header/>
  <soapenv:Body>
  <off:ConsumptionNotifyTOThirdPartyRspMsg>
  <com:RspHeader>
  <com:Version>1</com:Version>
  <com:ReturnCode>200</com:ReturnCode>
  <com:ReturnMsg>Success.</com:ReturnMsg>
  <com:RspTime>';
#$fg.=$cm;
$fg.='</com:RspTime>
  </com:RspHeader>
  </off:ConsumptionNotifyTOThirdPartyRspMsg>
  </soapenv:Body>
  </soapenv:Envelope>';
return $fg;
&datalog(print $fg);
#####Envia
#my $send = "perl /var/www/cgi-bin/noti/notification.cgi $be $dn $free $tot $uni $esx $tr $ofe";
#my $exsend=qx($send);
#&datalog($exsend);
print $fg;
  }
else{
print "Internal Server Error";
}
}
