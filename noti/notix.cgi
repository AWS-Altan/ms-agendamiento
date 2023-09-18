#!/usr/bin/perl
#use SOAP::Lite;
use SOAP::Lite +trace => 'debug';
use SOAP::Transport::HTTP; 
#use Time::localtime;
 SOAP::Transport::HTTP::CGI
    -> dispatch_to('ConsumptionNotifyTOThirdPartyReqMsg')
    -> handle;

  package ConsumptionNotifyTOThirdPartyReqMsg;


#  sub dated{
#use Time::localtime;

#my $seg, my $min, my $hora, my $dia, my $mes, my $ao) = localtime(time);
 # $ao += 1900;
  #$mes=$mes+1;
  #$mes=&bl($mes);
  #$dia=&bl($dia);
  #$hora=&bl($hora);
  #$min=&bl($min);
  #$seg=&bl($seg);
#return $ao;
#}
  sub ConsumptionNotifyTOThirdPartyReqMsg{

#$op=shift;
#$be=shift;
#$dn=shift;
#$free=shift;
#$tot=shift;
#$uni=shift;
#$esx=shift;
#$tr=shift;
#$ofe=shift;
#$ty="python3 /var/www/cgi-bin/bigd/suspendmovi.py 2018-06-25 2018-06-27 $op 2>/dev/null";
#print $ty;
#$cmd=qx($ty);
if ($op =~ "\s")
{
$fg='<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:off="http://www.huawei.com/bss/soaif/interface/OfferingService/" xmlns:com="http://www.huawei.com/bss/soaif/interface/common/">
<soapenv:Header/>
<soapenv:Body>
<off:ConsumptionNotifyTOThirdPartyRspMsg>
<com:RspHeader>
<com:Version>1</com:Version>
<com:ReturnCode>0000</com:ReturnCode>
<com:ReturnMsg>Success.</com:ReturnMsg>
<com:RspTime>20180510000000</com:RspTime>
</com:RspHeader>
</off:ConsumptionNotifyTOThirdPartyRspMsg>
</soapenv:Body>
</soapenv:Envelope>';
#$fg='<?xml version="1.0" encoding="UTF-8"?><soap:Envelope soap:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:off="http://www.huawei.com/bss/soaif/interface/OfferingService/" xmlns:com="http://www.huawei.com/bss/soaif/interface/common/">    <soapenv:Header/>    <soapenv:Body>     <off:ConsumptionNotifyTOThirdPartyRspMsg>          <com:RspHeader>             <com:Version>1</com:Version>            <com:ReturnCode>0000</com:ReturnCode>            <com:ReturnMsg>Success.</com:ReturnMsg>         <com:RspTime>20180510000000</com:RspTime>          </com:RspHeader>  <comx:Version>'.$cmd.'</comx:Version>      </off:ConsumptionNotifyTOThirdPartyRspMsg>   </soapenv:Body></soapenv:Envelope>';
return $fg;
#return $hj;
}
}
sub bl
{
  my $tt=shift;
  return ((length($tt)==1))? "0".$tt : $tt;
}


