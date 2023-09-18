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
&datalog("Recibe BSS:$xml<<<<");

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
$free =~ s/\n|\r|\t|\s//g;
$free=~s/\=|\[|\]|\{|\'//g;
#$free=~s/\}/\s/g;

#$fgx="perl /var/www/cgi-bin/noti/inser.cgi $be $dn $free $tot $uni $esx $tr $ofe 2>/dev/null";
$fgx="perl /var/www/cgi-bin/noti/inser_activa.cgi $be $dn $free $tot $uni $esx $tr $ofe 2>/dev/null";
&datalog($fgx);

#&datalog("respuesta: $be");
#&datalog("respuesta: $dn");

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
&datalog($fg);

qx($fgx);
print $fg;


}
