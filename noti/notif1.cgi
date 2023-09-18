#!/usr/bin/perl -w
use strict;
use Time::Piece;
use warnings FATAL => 'all';
use CGI qw();
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

my $cgi = CGI->new;
print $cgi->header(-type => "text/xml", -charset => "utf-8");
my $xml = $cgi->param("POSTDATA");
#print "$xml";
#my $xml='<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:com="http://www.huawei.com/bss/soaif/interface/common/" xmlns:off="http://www.huawei.com/bss/soaif/interface/OfferingService/">
my $twig = new XML::Twig(twig_handlers => {'off:ConsumptionNotifyTOThirdPartyReqMsg' => \&ServiceException});
$twig->parse($xml);

sub ServiceException
  {
     my ( $twig, $ServiceException ) = @_;
     my @f = ($ServiceException->field('off:BEID'),$ServiceException->field('off:MSISDN'),$ServiceException->field('off:FreeUnitTypeName'),$ServiceException->field('off:TotalAmount'),$ServiceException->field('off:UnUsedAmount'),$ServiceException->field('off:ExpiryDate'),$ServiceException->field('off:ThresholdValue'),$ServiceException->field('off:OfferingID'));
#    print "$f[0],";
#    print "$f[1],";
 #    print $f[2];
 #    print $f[3];
 #    print $f[4];
 #    print $f[5];
 #    print $f[6];
 #    print $f[7];
##     print $f[2], "\n";
#


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
  <com:ReturnCode>0000</com:ReturnCode>
  <com:ReturnMsg>Success.</com:ReturnMsg>
  <com:RspTime>';
#$fg.=$cm;
$fg.='</com:RspTime>
  </com:RspHeader>
  </off:ConsumptionNotifyTOThirdPartyRspMsg>
  </soapenv:Body>
  </soapenv:Envelope>';
#return $fg;
#print $op;
#####Envia
#$send ='curl -X POST -H "Content-Type: application/json" -d '"{ "'id_company'": "175","'msisdn'" : "525538573678", "'free_unit_type'": "123",  "'total_amount'": "100.23", "'unused_amount'": "222", "'offer_id'": "11111111", "'threshold_value'": "10", "'validity'": "23", "'expiration_date'": "20180427171226"}"' "http://52.5.233.163/cgi-bin/noti/notification.cgi"';
#$exsend=qx($send);
my $send = "perl /var/www/cgi-bin/noti/notification.cgi $be $dn $free $tot $uni $esx $tr $ofe";
my $exsend=qx($send);
print $fg;
  }
else{
print "Internal Server Error";
}
}

