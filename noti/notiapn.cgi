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



(my $seg, my $min, my $hora, my $dia, my $mes, my $ao, my @zape) = localtime(time);
  $ao += 1900;
  $mes=$mes+1;
  $mes=&bl($mes);
  $dia=&bl($dia);
  $hora=&bl($hora);
  $min=&bl($min);
  $seg=&bl($seg);
my $timestamp ="$ao$mes$dia$hora$min$seg";


use JSON qw(decode_json);

my $q  = CGI->new;
my $json  = JSON->new->utf8;
use JSON::XS;
my $j = JSON::XS->new->utf8->pretty(1);


my $yu=$q->param('POSTDATA');

my $input=$json->decode($yu);
#&escribelog("",$yu);
my $dn=$input->{msisdn};
my $be=$input->{be_id};
my $ofe=$input->{offeringId};

&datalog("Recibe CRM:$yu<<<<");

my $op="notificador";
my $tot="10";
my $uni="9";
my $esx="20361231180000";
my $tr="10";
my $free="National_SMS_MT_Portal_cautivo";

print $q->header("application/json");
$fgx="perl /var/www/cgi-bin/noti/inser_activa.cgi $be $dn $free $tot $uni $esx $tr $ofe 2>/dev/null";
$rt=qx($fgx);
#$as1=$json->encode({status=>"ok",msisdn=>$dn,tran=>$fgx});
$as1=$json->encode({status=>"Envio ok",msisdn=>$dn});



print $as1;
#$fgx="perl /var/www/cgi-bin/noti/inser.cgi $be $dn $free $tot $uni $esx $tr $ofe 2>/dev/null";
#$fgx="perl /var/www/cgi-bin/noti/inser_activa.cgi $be $dn $free $tot $uni $esx $tr $ofe 2>/dev/null";
#&datalog($fgx);



#qx($fgx);
#print $fg;



