#!/usr/bin/perl

use CGI ();
use Data::Dumper qw(Dumper);

sub bl
{
  my $tt=shift;
  return ((length($tt)==1))? "0".$tt : $tt;
}

sub escribelog{
  my $error=shift;
  (my $seg, my $min, my $hora, my $dia, my $mes, my $ao, my @zape) = localtime(time);
  $ao += 1900;
  $mes=$mes+1;
  $mes=&bl($mes);
  $dia=&bl($dia);
  $hora=&bl($hora);
  $min=&bl($min);
  $seg=&bl($seg);
  my $log_file="/var/www/cgi-bin/log/eventos/resultado-servid-$ao-$mes-$dia-$id_com.log";

  open (LOG," >> $log_file");
  print LOG "$ao-$mes-$dia-$hora:$min:$seg-$error\n";
  close (LOG);
}


use JSON qw(decode_json);

my $q  = CGI->new;
my $json  = JSON->new->utf8;


my $yu=$q->param('POSTDATA');
my $input=$json->decode($yu);
@input2=$yu;
my $inoutr=$input->{'Inout'};
my $trans=$input->{'Transactionid'};
#my $subt=$input->{'Subtransationid'};
#my $tar=$input->{'Target'};
my $resor=$input->{'Resource'};
#my $part=$input->{'Parnetid'};
#my $timesa=$input->{'Timestamp'};
my $data=$input->{'Data'};
my $payload=$input->{'Data'}->{'Payload'};
my $opera=$input->{'Operation'};
my $dn=$input->{'Data'}->{'payload'}->{'msisdn'};
my $be=$input->{'Data'}->{'be_id'};
my $im=$input->{'Data'}->{'payload'}->{'imsi'};
my $fe=$input->{'Data'}->{'payload'}->{'effecdate'};
my $ofer=$input->{'Data'}->{'payload'}->{'offeringId'};
foreach $re1(@input2)
{
if($re1=~'be_id')
{
#$be=$re1;
}
}

#my $input2=$json->decode($data);
# my $im=$input2->{'payload'}->{'imsi'};


#$payload =~ s/\n|\r|{|\"//g;


#$fe="2018-07-07";
use JSON::XS;
my $j = JSON::XS->new->utf8->pretty(1);

  (my $seg, my $min, my $hora, my $dia, my $mes, my $ao, my @zape) = localtime(time);
  $ao += 1900;
  $mes=$mes+1;
  $mes=&bl($mes);
  $dia=&bl($dia-1);
  $hora=&bl($hora);
  $min=&bl($min);
  $seg=&bl($seg);
  $fecg="$ao-$mes-$dia $hora:$min:$seg";

$f=0;


if($opera=~'Activacion')
{
$ut="python3 /var/www/cgi-bin/bigd/validaactivacion.py '$be' '$im' '$dn' '$ofer' '$fe' 2> /dev/null";
$rt=qx($ut);
$rt =~ s/\n|\r//g;
my($be1,$im1,$dn1,$ofer1,$fe,$val_be,$val_imsi,$val_oferta,$val_usuario)=split(' ',$rt);
if($val_be=~'ERROR' or  $val_imsi=~'ERROR' or $val_usuario=~'ERROR' or $val_oferta=~'ERROR')
{
if($val_be=~'ERROR')
{
$de=001;
$def="be_id $val_be";
}
if($val_usuario=~'ERROR') 
{
$de=002;
$def="usuario $val_usuario";
}
if($val_oferta=~'ERROR') 
{$de=003;
$def="oferta $val_oferta ";
}
if($val_imsi=~'ERROR')
{$de=004;
$def="imsi $val_imsi";
}

$as1=$json->encode({errorCode=>$de,description=>$def});

}
else{

$as1=(effectiveDate=>$fecg,imsi=>$im1);

}
}

if($opera=~'inactivacion')
{
$ut="python3 /var/www/cgi-bin/bigd/inactivacion.py '$be' '$im' '$dn' '$fe' 2> /dev/null";
$rt=qx($ut);
$rt =~ s/\n|\r//g;
my($be1,$im1,$dn1,$fe,$val_be,$val_imsi,$esta)=split(' ',$rt);
if($val_be=~'ERROR' or  $val_imsi=~'ERROR' or  $val_imsi=~'ERROR' or $esta=~'ERROR')
{
if($val_be=~'ERROR')
{
$de=001;
$def="be_id $val_be";
}
if($esta=~'ERROR')
{
$de=002;
$def="estatus $esta";
}
if($val_imsi=~'ERROR')
{$de=004;
$def="imsi $val_imsi";
}

$as1=$json->encode({errorCode=>$de,description=>$def});

}
else{

$as1=(effectiveDate=>$fecg,imsi=>$im1);

}
}


if($opera=~'reactivacion')
{
$ut="python3 /var/www/cgi-bin/bigd/reactivacion.py '$be' '$im' '$dn' '$fe' 2> /dev/null";
$rt=qx($ut);
$rt =~ s/\n|\r//g;
my($be1,$im1,$dn1,$fe,$val_be,$val_imsi,$val_usu)=split(' ',$rt);
if($val_be=~'ERROR' or  $val_imsi=~'ERROR' or  $val_imsi=~'ERROR' or $val_usu=~'ERROR')
{
if($val_be=~'ERROR')
{
$de=001;
$def="be_id $val_be";
}
if($val_usu=~'ERROR')
{
$de=002;
$def="usuario $val_usu";
}
if($val_imsi=~'ERROR')
{$de=004;
$def="imsi $val_imsi";
}

$as1=$json->encode({errorCode=>$de,description=>$def});

}
else{

$as1=(effectiveDate=>$fecg,imsi=>$im1);

}
}

#for my $item( @{$json_object->{Data}} ){
#   $be_id= $payload->{be_id} ;
#}
$as1=(data=>$be);


print $q->header("application/json");
use JSON::XS;
my $j = JSON::XS->new->utf8->pretty(1);

print $as1;

