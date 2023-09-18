#!/usr/bin/perl

$som = SOAP::SOM->new;
use strict;
use SOAP::Lite;
#use SOAP::Lite +trace => 'debug';    
#on_fault => sub { my($soap, $res) = @_; 
 #     die ref $res ? $res->faultdetail : $soap->transport->status, "\n";
  #  };
#  my $soap = SOAP::Lite
 #   -> uri('http://localhost/ConsumptionNotifyTOThirdPartyReqMsg')
  #  -> proxy('http://localhost/cgi-bin/noti/notix.cgi');
my $op = shift;
   my $soap = SOAP::Lite
     ->readable(1)
     -> uri('xmlns:soapenv=http://schemas.xmlsoap.org/soap/envelope/ xmlns:off=http://www.huawei.com/bss/soaif/interface/OfferingService/ xmlns:com=http://www.huawei.com/bss/soaif/interface/common/')
     -> proxy('http://localhost/cgi-bin/noti/notix.cgi');
     
eval { 
print $soap->ConsumptionNotifyTOThirdPartyReqMsg(130,5538573678,10.00)->result; 
1 } or die;
# my $som = $soap->notii();
#print $som->value('//off:ConsumptionNotifyTOThirdPartyReqMsg/off:BEID');

