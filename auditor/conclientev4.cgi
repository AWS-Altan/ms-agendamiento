#!/usr/bin/perl

use CGI ();
use Data::Dumper qw(Dumper);
use DBI;
use JSON qw(decode_json);

my $q  = CGI->new;
my $json  = JSON->new->utf8;



sub perfil{
$msisdn=shift;
$id_com=shift;
$operacion=shift;
$user="hwbss";

$rt=&parametro($id_com);
my($id_c,$user,$pass,$url,$yu,$user2,$token)=split(',',$rt);
#my $tii=Time::HiRes::gettimeofday();
$io='curl -X GET "'.$url.''.$msisdn.'/subscriberFreeUnitsData"   -H "OperatorId: '.$user.'"  -H  "accept: application/json" -H  "Authorization: Bearer '.$token.' "  -H  "Operation-User: '.$user2.' " -H  "Operation-Password: '.$pass.'   " -H  "PartnerId: '.$id_com.' " 2> /dev/null';
&comova($io);
use Data::Dumper qw(Dumper);
use JSON qw(decode_json);
my $json  = JSON->new->utf8;

$re=qx($io);
&comova($re);
my $input=$json->decode($re);
my $im=$input->{responseSubscriber}->{information}->{'IMSI'};
##my $imo=$input->{subStatus}->{status};
my $input=$json->decode($re);
my $idc=$input->{'order'}->{'id'};
#my $end=Time::HiRes::gettimeofday();

#my $run_time = sprintf("%.2f", $end - $tii);

if($re=~"Active" )
{
$rty1=sprintf("profile,%s,%s,%s,%s,%s,%s,%s,%s,%s,ok",$msisdn,$id_com,$ofe,$err,$desc,$tii,$end,$run_time,$tra);
#&escribelog($rty1,$id_com,$operacion,$id_tra,$idc);
#$im =~ s/\n|\r|\t|' '//g;
#$im=~s/\"|\[|\]|\{|\'|\||\}//g;
#my($a,$imsii)=split(":",$im);
#return "Active,$im";
}
else{
$rty1=sprintf("profile,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,no-ok",$msisdn,$id_com,$ofe,$err,$desc,$det,$tii,$end,$run_time,$tra);
#&escribelog($rty1,$id_com,$operacion,$id_tra,$idc);
#return $re;
#return "Active,$im";
}

return $re;

}
sub bl
{
  my $tt=shift;
  return ((length($tt)==1))? "0".$tt : $tt;
}

sub escribelog{
  my $error=shift;
  my $id_com=shift;
  my $oper=shift;
  (my $seg, my $min, my $hora, my $dia, my $mes, my $ao, my @zape) = localtime(time);
  $ao += 1900;
  $mes=$mes+1;
  $mes=&bl($mes);
  $dia=&bl($dia);
  $hora=&bl($hora);
  $min=&bl($min);
  $seg=&bl($seg);
  my $log_file="/opt/blackbird/log/eventos/resultado-consultaIMEIactiva-$ao-$mes-$dia-$id_com.log";
  open (LOG," >> $log_file");
  print LOG "$ao-$mes-$dia-$hora:$min:$seg-$error\n";
  close (LOG);
}

sub comova{
  my $error=shift;
  (my $seg, my $min, my $hora, my $dia, my $mes, my $ao, my @zape) = localtime(time);
  $ao += 1900;
  $mes=$mes+1;
  $mes=&bl($mes);
  $dia=&bl($dia);
  $hora=&bl($hora);
  $min=&bl($min);
  $seg=&bl($seg);
  my $log_file="/var/www/cgi-bin/log/comova-consultacrm-$ao-$mes-$dia.log";
  open (LOG," >> $log_file");
  print LOG "$ao-$mes-$dia-$hora:$min:$seg-$error\n";
  close (LOG);
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





my $yu=$q->param('POSTDATA');
my $input=$json->decode($yu);

my $a = $input->{id_company};
my $b = $input->{msisdn};
#my $c = $input->{imsi};

$prf=&perfil($b,$a);




print $q->header("application/json");
#$fg= $json->encode({status=>$rt,imsi=>$cc,msisdn=>$bb,imei=>$dd});
#$fg =~ s/\\n//g;

print $prf;

#print $cmd;

