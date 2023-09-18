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

#sub ConsumptionNotifyTOThirdPartyReqMsg
 
my $op=$f[0];
#my $be=shift;
#my $dn=shift;
#my $free=shift;
#my $tot=shift;
#my $uni=shift;
#my $esx=shift;
#my $tr=shift;
#my $ofe=shift;

 if ($op == '175'){


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
print $fg;
  }}

