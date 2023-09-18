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

my $inoutr=$input->{'Inout'};
my $trans=$input->{'Transactionid'};
my $subt=$input->{'Subtransationid'};
my $tar=$input->{'Target'};
my $resor=$input->{'Resource'};
my $part=$input->{'Parnetid'};
my $timesa=$input->{'Timestamp'};
my $data=$input->{'Data'};


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

if($be>1)
{
#$f=1;
}
if(length($im)!=15)
{
$f=1;

}
if(length($dn)!=12)
{
$f=1;
}

if($f==0)
{
#$ut="python3 /var/www/cgi-bin/bigd/inactivacion.py '$be' '$im' '$dn' '$ofer' '$fe' 2> /dev/null";
#$rt=qx($ut);
#&escribelog($ut);
#$rt =~ s/\n|\r//g;

#my($be1,$im1,$dn1,$ofer1)=split(' ',$rt);

#$as1=qq(be_id":"$be1","imsi": "$im1","msisdn": "$dn1", "OferringId":"$ofer1", "effectiveDate": "$fecg", "description":"Success");

$as1= $json->encode({be_id=>$be1,imsi=> $im1,msisdn=> $dn1, effectiveDate=>$fecg,description=>"Success"});

}
else{
#$as1=qq(be_id":"$be","imsi": "$im","msisdn": "$dn", "effectiveDate": "$fecg", "description":"error");
$as1= $json->encode({be_id=>$be,imsi=> $im,msisdn=> $dn, OferringId=>$ofer,effectiveDate=>$fecg,description=>"error"});


}


print $q->header("application/json");
use JSON::XS;
my $j = JSON::XS->new->utf8->pretty(1);
#$as1=$ut;
#$ty= $j->encode({resp=>{$as1}});

#$as1=$data;
$ty= $j->encode({$as1});

$ty =~ s/\\//g;
#&escribelog($as11);
print $ty;


