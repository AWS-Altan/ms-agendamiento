#!/usr/bin/perl -w

use CGI ();
use Data::Dumper qw(Dumper);

sub bl
{
  my $tt=shift;
  return ((length($tt)==1))? "0".$tt : $tt;
}

sub escribelog{
  my $id_com=shift;
  my $error=shift;
  (my $seg, my $min, my $hora, my $dia, my $mes, my $ao, my @zape) = localtime(time);
  $ao += 1900;
  $mes=$mes+1;
  $mes=&bl($mes);
  $dia=&bl($dia);
  $hora=&bl($hora);
  $min=&bl($min);
  $seg=&bl($seg);
  my $log_file="/var/www/cgi-bin/log/resultado-agenda-async-$ao-$mes-$dia-$id_com.log";

  open (LOG," >> $log_file");
  print LOG "$ao-$mes-$dia-$hora:$min:$seg-$error\n";
  close (LOG);
}


use JSON qw(decode_json);

my $q  = CGI->new;
my $json  = JSON->new->utf8;
use JSON::XS;
my $j = JSON::XS->new->utf8->pretty(1);


my $yu=$q->param('POSTDATA');


my $input=$json->decode($yu);
&escribelog("",$yu);
my $inoutr=$input->{'Inout'};
my $trans=$input->{'Transactionid'};
my $subt=$input->{'Subtransationid'};
my $tar=$input->{'Target'};
my $resor=$input->{'Resource'};
my $part=$input->{'ParnerId'};
my $timesa=$input->{'Timestamp'};
my $opera=$input->{'Operation'};
my $asin=$input->{'async'};
my $data=$input->{'Data'};
my $dn=$input->{'Data'}->{msisdn};
my $fe=$input->{'Data'}->{effectiveDate};
my $be=$input->{'Data'}->{be_id};
my $coe=$input->{'Data'}->{coordinates};
my $expx=$input->{'Data'}->{expireEffectiveDate};
my $fi=$input->{'Data'}->{startEffectiveDate};
my $secu=$input->{'Data'}->{purchasedSecuency};
my $rspTime=$input->{'Data'}->{rspTime};
my $order_id = $input->{'Data'}->{orderId};
#my $asin=$input->{'Data'}->{async};

&escribelog($be,$yu);


#$ofer=$input->{'Resource'};
#$ofer=$yu;

my $ofer=$input->{'Data'}->{offeringId};
$ofer2=$ofer;

if($yu=~'purchase' )
{

#my @ofer=$input->{'Data'}->{offerings};
#my $pos = index($yu,"offerings",10);
#my $pos3 = index($yu,"]",10);
#my $pos2 = index($yu,"[",10);
#print "$pos|$pos2|$pos3\n";
#$ofer=substr($yu,$pos2,$pos3);
#$ofer =~ s/\"|\[|\]|}|{| |\n|\\n//g;
#$ofer=$yu;
$yu =~ s/\\n//g;
$larg=length($yu);
 my $pos = index($yu,"offerings");
my $pos3 = index($yu,"]");
my $pos2 = index($yu,"[");
#print "$pos|$pos2|$pos3\n";

$sdf=substr($yu,$pos2,$pos3-$larg);
$sdf =~ s/\"|\[|\]|\\| //g;
$ofer=$sdf;
}

if($yu=~'replaceExpireEffectiveDate')
{

$yu =~ s/\\n//g;
$larg=length($yu);
my $pos = index($yu,"offerings");
my $pos3 = index($yu,"]");
my $pos2 = index($yu,"[");
#print "$pos|$pos2|$pos3\n";

$sdf=substr($yu,$pos2,$pos3-$larg);
$sdf =~ s/|\[|\]|\\| //g;

#$ofer=$sdf;
#$sdf =~ s/\"//g;
#$sdf =~ s/\\:/=>/g;
$ofer='{"offerings":['.$sdf.']}';
$oprr="replaceExpireEffectiveDate";
}

if($yu=~'cancelProductsEffectiveDate')
{
$ofer=$ofer2;

}
#$fe="2018-07-07";

  (my $seg, my $min, my $hora, my $dia, my $mes, my $ao, my @zape) = localtime(time);
  $ao += 1900;
  $mes=$mes+1;
  $mes=&bl($mes);
  $dia=&bl($dia-1);
  $hora=&bl($hora);
  $min=&bl($min);
  $seg=&bl($seg);
  $fecg="$ao-$mes-$dia $hora:$min:$seg";


#$data =~ s/\{\}//g;


#$data=substr($data,2);
if(length($be)==0)
{
#$f=1;
}
if(length($im)!=15)
{
#$f=1;

}
if(length($dn)!=10)
{
$f=1;
}
if(length($ofer)>3 && $resor=~'purchase')
{
#$f=1;
}

if($f==0)
{
use DBI;
$dat="auditor";
$host="10.0.0.23";
#$host="127.0.0.1";
$port="3306";
$userid="operador";
$passwd="operador01";
$con2="DBI:mysql:database=$dat;$host:$port";
$dbh = DBI->connect($con2,$userid,$passwd);




if($oprr=~'replaceExpire')
{
$strsql=" SELECT  case when operacion like '%replaceExpireEffectiveDate%' and count(*)  >0 then '88888'   when operacion not like '%replaceExpireEffectiveDate%' and count(*)>0 then '2'   else '0'   end conteo     FROM auditor.auditor_on_line_batch_async  WHERE id_company='$be' and id_estatus=1 and msisdn='$dn'  and operacion like '%$oprr%' ";
}
else{
if($resor=~'purchasesupplementary')
{
$strsql="SELECT 0,0,'na'";
}
else{
#$strsql="SELECT    count(*) FROM auditor.auditor_on_line_batch_async  WHERE id_company='$be' and id_estatus=2 and msisdn='$dn'   ";
$strsql="SELECT count(*), group_concat(id_auditor_alta separator ','), group_concat(operacion separator ',') FROM auditor.auditor_on_line_batch_async  WHERE id_company='$be' and id_estatus=2 and msisdn='$dn' ";
}
}


#print "$strsql\n";
$sth = $dbh->prepare($strsql);
$sth->execute or die("Couldn't execute $strsql.".$dbh->errstr."\n");

#print "content-type: text/html \n\n";
#print"Incia el insert...oferta: $ofer  secuencia: $secu";

while(@row = $sth->fetchrow_array()){
        $ddd = $row[0];
	$id_auditor_altaa = $row[1];
	$operacionn = $row[2];
}

if($ddd=='88888')
{
$ty22="update auditor.auditor_on_line_batch_async set id_estatus='8888' where id_estatus='1' and operacion like '%replaceExpireEffectiveDate%' and msisdn='$dn'  ";
$sthx33 = $dbh->prepare($ty22);
$sthx33->execute;
$ddd=0;
}



if($ddd==0 or ($operacionn =~ /changevinculacion/) or ($ddd < 5 and ($operacionn =~ /resume/ or $operacionn =~ /suspend/)))
{
$strsql="insert into auditor.auditor_on_line_batch_async (id_company,id_estatus,msisdn,oferta,address,fecha_ingreso,fecha_expiracion,fecha_inicio,transaccion_id,secuencia,operacion,asyncrono,rspTime,order_id_bss) values('$be','1','$dn','$ofer','$coe','$fe','$expx','$fi','$id','$secu','$resor','$asin','$rspTime','$order_id')";
&escribelog($be,"$strsql,'inserta'");
$sth = $dbh->prepare($strsql);
$sth->execute or die("Couldn't execute $strsql.".$dbh->errstr."\n");

$strsql1="update auditor.auditor_on_line_batch_async set id_estatus=2 where msisdn='$dn' and operacion='$resor' and id_estatus='1' ";
&escribelog($be,"$strsql1,'actualiza'");
$sth1 = $dbh->prepare($strsql1);
$sth1->execute or die("Couldn't execute $strsql1.".$dbh->errstr."\n");



#$ids=1;
$ids=$sth->{mysql_insertid};
$as1= $json->encode({be_id=>$be,imsi=> $im,msisdn=> $dn, Resource=>$resor,effectiveDate=>$fe,startEffectiDate=>$fi,expireEffectiveDate=>$expx,coordinates=>$coe,offeringId=>$ofer,status=>ok,id_transation_cudar=>$ids});
#$as1= $json->encode({offeringId=>$ofer});


}
else{
$as1= $json->encode({be_id=>$be,imsi=> $im,msisdn=> $dn, Resource=>$resor,effectiveDate=>$fecg,startEffectiDate=>$fi,expireEffectiveDate=>$expx,coordinates=>$coe,offeringId=>$ofer,status=>nok,description=>'found the data duplicate or  has a process in the agenda, asyncOrder: '.$id_auditor_altaa.', operation: '.$operacionn.'',purchasedSecuency=>$secu});


}
}
else{
$as1= $json->encode({be_id=>$be,imsi=> $im,msisdn=> $dn, Resource=>$resor,effectiveDate=>$fecg,startEffectiDate=>$fi,expireEffectiveDate=>$expx,coordinates=>$coe,offeringId=>$ofer,status=>nok,description=>'some the data is not correct',purchasedSecuency=>$secu});


}

&escribelog($be,$as1);

print $q->header("application/json");
use JSON::XS;
my $j = JSON::XS->new->utf8->pretty(1);
#$as1=$ut;
#$ty= $j->encode({resp=>{$as1}});

#$as1=$data;
#$ty= $j->encode({$as1});

#$ty =~ s/\\//g;
#&escribelog($as1,$be);
#$ty=substr $ty,0,-10;
#print $ty;

print $as1;


