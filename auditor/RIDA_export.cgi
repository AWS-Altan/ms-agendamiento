#!/usr/bin/perl

use CGI ();

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
  my $log_file="/var/www/cgi-bin/log/resultado-export-$ao-$mes-$dia.log";

  open (LOG," >> $log_file");
  print LOG "$ao-$mes-$dia-$hora:$min:$seg,$error\n";
  close (LOG);
}

use JSON qw(decode_json);

my $q  = CGI->new;
my $json  = JSON->new->utf8;

#$msisdn="5555555555";
#$be_id="175";
my $yu=$q->param('POSTDATA');
my $input=$json->decode($yu);
my $dn = $input->{msisdn};
#my $be_id = $input->{be_id};

$cmd="perl /opt/blackbird/masterbacthactiveonline.pl $dn $be_id $ofe ";

$re=qx($cmd);
$re =~ s/\\//g;

print $q->header("application/json");
use JSON::XS;
my $j = JSON::XS->new->utf8->pretty(1);
$as1= $json->encode({$re,envi=>$cmd});

print $re;


