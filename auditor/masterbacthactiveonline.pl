#!/usr/bin/perl

$dn=$ARGV[0];
$be_id=$ARGV[1];
$ofe=$ARGV[2];
#$id_com=$ARGV[3];
use DBI;
use Time::HiRes qw( time );
#Datos de la conexión
$dat="auditor";
$host="10.0.0.23";
$port="3306";
$userid="operador";
$passwd="operador01";
use Data::Dumper qw(Dumper);
use Parallel::ForkManager;

use JSON qw(decode_json);

my $json  = JSON->new->utf8;

$con="DBI:mysql:database=$dat;$host:$port";
$dbh = DBI->connect($con,$userid,$passwd);
sub bl
{
  my $tt=shift;
  return ((length($tt)==1))? "0".$tt : $tt;
}


###################################*********************************
sub changeprimary{
$msisdn=shift;
$id_com=shift;
$operacion=shift;
$ofe=shift;
$dir=shift;
$tra=shift;
$expi=shift;
$star=shift;
$rt=&parametro($id_com);
my $tii=Time::HiRes::gettimeofday();
#my($id_c,$user,$pass,$url)=split(',',$rt);
my($id_c,$user,$pass,$url,$yu,$user2,$token)=split(',',$rt);


$dir=~s/ //g;
@ffecha=split(" ",$star);
$ffecha[0]=~s/-//g;
@ffexp=split(" ",$expi);
$ffexp[0]=~s/-//g;
$io='curl -s -X PATCH "'.$url.$msisdn.'" -H "OperatorId:'.$user.'" -H  "Authorization: Bearer '.$token.'" -H  "Operation-User: '.$user2.' " -H  "Operation-Password: '.$pass.'" -H  "PartnerId: '.$id_com.'" -H "content-type: application/json" -d \'{"primaryOffering":{"address":"'.$dir.'","offeringId":"'.$ofe.'","startEffectiveDate":"'.$ffecha[0].'","expireEffectiveDate":"'.$ffexp[0].'"}}\'';
$io='curl -s  -X POST  "'.$url.''.$msisdn.'/offering" -H "OperatorId:'.$user.'" -H  "Authorization: Bearer '.$token.'" -H  "Operation-User: '.$user2.' " -H  "Operation-Password: '.$pass.'" -H  "PartnerId: '.$id_com.'" -H  "Content-Type: application/json"    -d "{ "\"primaryOffering"\": "{\"offeringId"\": "\"'.$ofe.'"\",\"startEffectiveDate\": "\"'.$ffecha[0].'"\" ,  \"expireEffectiveDate\": "\"'.$ffexp[0].'"\" }}"';


#print "$io\n";
&comova($io);
$re=qx($io);
&comova($re);
#print "$re\n";
my $end=Time::HiRes::gettimeofday();
my $run_time = sprintf("%.2f", $end - $tii);
$operacion="changeprimary";
if(($re=~"effectiveDate") or ($re=~"pending" && $re!="The subscriber has a default primary offering. You need to use activate operation first") or $re=~"Active" )
{
$rty1=sprintf("changeprimary,%s,%s,%s,%s,%s,ok",$msisdn,$id_com,$ofe,$run_time,$tra);
&escribelog($rty1,$id_com,$operacion,$id_tra);
$po=3;
return $po;
}
else{
#print "no-ok";
my $input=$json->decode($re);
my $err=$input->{'errorCode'};
my $desc=$input->{'description'};
$re =~ s/\n|\r|\t//g;
$desc=~s/\=|\[|\]|\{|\'|\,|\}//g;
$desc=~s/\}/\n/g;
$err=~s/\=|\[|\]|\{|\'|\,|\}//g;
$err=~s/\}/\n/g;
$rty=sprintf("|errocode:%s description:%s",$err,$desc);
$rty1=sprintf("changeprimary,%s,%s,%s,%s,%s,%s,no-ok",$msisdn,$id_com,$ofe,$rty,$run_time,$tra);
&escribelog($rty1,$id_com,$operacion,$id_tra);
$po=2;
return $po;
}
}


##########################

sub highbss{
$msisdn=shift;
$id_com=shift;
$operacion=shift;
$rt=&parametro($id_com);
my($id_c,$user,$pass,$url,$yu,$user2,$token)=split(',',$rt);
&comova("parametro:  $id_c,$user,$pass,$url,$yu,$user2,$token");
$ofe=shift;
$dir=shift;
$tra=shift;
$exeffdat=shift;
$steffdat=shift;
#my $tii2=Time::HiRes::gettimeofday();
&comova($url);
@ffecha=split(" ",$steffdat);
$ffecha[0]=~s/-//g;
@ffexp=split(" ",$exeffdat);
$ffexp[0]=~s/-//g;
$io='curl -s -X POST "'.$url.''.$msisdn.'/activatebatch" -H  "accept: application/json" -H "OperatorId: '.$user.'" -H  "Authorization: Bearer '.$token.' "  -H  "Operation-User: '.$user2.'" -H  "Operation-Password: '.$pass.'  " -H  "PartnerId: '.$id_com.' " -H  "Content-Type: application/json" -d \'{ "address": "'.$dir.'",  "offeringId": "'.$ofe.'" ,  "startEffectiveDate": "'.$ffecha[0].'" ,  "expireEffectiveDate": "'.$ffexp[0].'"}\' 2> /dev/null';
$io =~ s/\n|\r|\t//g;
#print "$io\n";
my $tii2=Time::HiRes::gettimeofday();
#print "$io\n";
$re=qx($io);
&comova($io);
#print "$re\n";
&comova($re);


$tyu=length($url);
&comova("->longitud url:>>$tyu<<<");
if(length($url)>23)
{
$ban=0;
}
else{
$ban=4;
}
if(($re=~"effectiveDate" or $re=~"pending business" or $re=~'successfully' or $re=~'Active' ) and $ban!=4)
{

my $input=$json->decode($re);
my $err=$input->{'msisdn'};
my $desc=$input->{'effectiveDate'};
my $idc=$input->{'order'}->{'id'};

my $end2=Time::HiRes::gettimeofday();
my $run_time2 = sprintf("%.2f", $end2 - $tii2);
#$rty1=sprintf("activate_batch,%s,%s,%s,%s,%s,%s,%s,%s,%s,ok",$msisdn,$id_com,$ofe,$desc,$tii2,$end,$run_time2,$idc); Con Orderid
$rty1=sprintf("activate_batch,%s,%s,%s,%s,%s,%s,%s,%s,%s,ok",$msisdn,$id_com,$ofe,$desc,$end,$run_time2,$tra); 
$rty=sprintf("respuesta:effectiveDate:%s",$err,$desc);
&escribelog($rty1,$id_com,$operacion,$id_tra);
$po=3;

}
else{
my $input=$json->decode($re);
my $err=$input->{'errorCode'};
my $desc=$input->{'description'};
#my $idc=$input->{'order'}->{'id'};
if($ban==4)
{
$det="url vacia be_id vacio";
$err=$det;
}
my $end2=Time::HiRes::gettimeofday();
my $run_time2 = sprintf("%.2f", $end2 - $tii2);
$re =~ s/\n|\r|\t//g;
$desc=~s/\=|\[|\]|\{|\'|\,//g;
$desc=~s/\}/\n/g;
$err=~s/\=|\[|\]|\{|\'|\,//g;
$err=~s/\}/\n/g;
$rty=sprintf("|errocode:%s|description:%s%s|",$err,$desc,$det);
#$rty1=sprintf("activate_batch,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,no-ok",$msisdn,$id_com,$ofe,$rty,$det,$tii2,$end,$run_time2,$idc);
$rty1=sprintf("activate_batch,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,no-ok",$msisdn,$id_com,$ofe,$rty,$run_time2,$tra);
&escribelog($rty1,$id_com,$operacion,$id_tra);
$po=2;

if($re=~"Suspend" )
{
$po=6;
}


}
return $po;

}



#######################

sub escribelogx{
(my $seg, my $min, my $hora, my $dia, my $mes, my $ao, my @zape) = localtime(time);
  $ao += 1900;
  $mes=$mes+1;
  $mes=&bl($mes);
  $dia=&bl($dia);
  $hora=&bl($hora);
  $min=&bl($min);
  $seg=&bl($seg);

  my $error=shift;
  my $id_com=shift;	
  my $log_file="/opt/blackbird/log/eventos/resultado_operaciontem_$id_com_$ao-$mes-dia.log";
  open (LOG," >> $log_file");
  print LOG "$error\n";
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
  my $log_file="/opt/blackbird/log/eventos/resultado-$oper-$ao-$mes-$dia-$id_com.log";
  open (LOG2," >> $log_file");
  print LOG2 "$ao-$mes-$dia-$hora:$min:$seg-$error\n";
  close (LOG2);
}

sub parametro{
$id_com=shift;
$ut="cat /var/www/cgi-bin/bacth/kingkong.conf | grep -m 1 '$id_com' ";
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
&comova($rt);
return $rt;
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
  my $log_file="/var/www/cgi-bin/log/logpatromaster$mes-$dia-$ao.txt";
  open (LOG," >> $log_file");
  print LOG "$mes-$dia-$ao $hora:$min:$seg $error\n";
  close (LOG);
}

sub trabajador{
  my $error=shift;
  (my $seg, my $min, my $hora, my $dia, my $mes, my $ao, my @zape) = localtime(time);
  $ao += 1900;
  $mes=$mes+1;
  $mes=&bl($mes);
  $dia=&bl($dia);
  $hora=&bl($hora);
  $min=&bl($min);
  $seg=&bl($seg);
  my $log_file="/opt/blackbird/log/trabajadortemactive-$ao-$mes-$dia.log";
  open (LOG," >> $log_file");
  print LOG "$error";
  close (LOG);
}
sub trabajadorx{
  my $error=shift;
  my $unico=shift;
  (my $seg, my $min, my $hora, my $dia, my $mes, my $ao, my @zape) = localtime(time);
  $ao += 1900;
  $mes=$mes+1;
  $mes=&bl($mes);
  $dia=&bl($dia);
  $hora=&bl($hora);
  $min=&bl($min);
  $seg=&bl($seg);
  my $log_file="/opt/blackbird/log/trabajadortemacpo-$ao-$mes-$dia.log";
  open (LOG," >> $log_file");
  print LOG "$error";
  close (LOG);
}



##########################procesos suspend bacth


###################################################


###################################################
#$goteo=10;
#$tps=2;
$tps=$tps;
#$tpsf=1000/$tps;
#print "$tpsf\n";
use Time::HiRes qw(usleep nanosleep);




$con="DBI:mysql:database=$dat;$host:$port";
$dbh = DBI->connect($con,$userid,$passwd);
$p=0;
$rec=&highbss($dn,$be_id,'highbss',$ofe,"$dir",$tra,$fexp,$finicio);
#print "->>$rec<<<";



#print ">>$rec\n";
if($rec==3)
{
$recc=&changeprimary($dn,$be_id,'activacionmega',$ofe,"$dir",$tra,$fexp,$finicio);

#print ">>chan:$recc\n";

if($recc==3)
{
print "1";
$strsql="insert into auditor.auditor_activate (id_company,id_estatus,msisdn,oferta,address,fecha_ingreso,transaccion_id,secuencia) values('$be','5','$dn','$ofe','$coe',now(),'$id','$secu')";

&comova($strsql);

}
else{
print "2";
$strsql="insert into auditor.auditor_activate (id_company,id_estatus,msisdn,oferta,address,fecha_ingreso,transaccion_id,secuencia) values('$be','2','$dn','$ofe','$coe',now(),'$id','$secu')";
&comova($strsql);

}
}
else{
print "2";
$strsql="insert into auditor.auditor_activate (id_company,id_estatus,msisdn,oferta,address,fecha_ingreso,transaccion_id,secuencia) values('$be','2','$dn','$ofe','$coe',now(),'$id','$secu')";
&comova($strsql);

}
$sth = $dbh->prepare($strsql);
$sth->execute;



