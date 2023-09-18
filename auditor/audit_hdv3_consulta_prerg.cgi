#!/usr/bin/perl

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
  my $log_file="/var/www/cgi-bin/log/resultado-consulta_preregistro-$ao-$mes-$dia-$id_com.log";
  open (LOG," >> $log_file");
  print LOG "$ao-$mes-$dia-$hora:$min:$seg-$error\n";
  close (LOG);
}


use JSON qw(decode_json);

my $q  = CGI->new;
my $json  = JSON->new->utf8;
#$msisdn=1000020000;
#$be=175;

my $yu=$q->param('POSTDATA');
my $input=$json->decode($yu);
&escribelog($be,$yu);
my $be=$input->{'be_id'};
my $msisdn=$input->{'msisdn'};
my $idtran=$input->{'id_auditor_cudar'};
use JSON::XS;
my $j = JSON::XS->new->utf8->pretty(1);

  (my $seg, my $min, my $hora, my $dia, my $mes, my $ao, my @zape) = localtime(time);
  $ao += 1900;
  $mes=$mes+1;
  $mes=&bl($mes);
  $dia=&bl($dia);
  $hora=&bl($hora);
  $min=&bl($min);
  $seg=&bl($seg);
  $fecg="$ao-$mes-$dia $hora:$min:$seg";
#$data =~ s/\{\}//g;
#$data=substr($data,2);

if(length($be)<1 && length($msisdn)<5){
$f=1;
}
if(length($msisdn)==10){
$f=0;
}

if(length($idtran)>1){
$f=0;
$transaction_id = "preregistered_on_line_batch$idtran";
}

if($f==0){
use DBI;
$dat="auditor";
$host="10.0.0.23";
#$host="10.12.62.244";
$port="3306";
$userid="operador";
$passwd="operador01";
$con2="DBI:mysql:database=$dat;$host:$port";
$dbh = DBI->connect($con2,$userid,$passwd);



$strsql="SELECT  
cast(replace(transaccion_id,'preregistered_on_line_batch','') as int)
,CASE when id_estatus=1 then 'Scheduled' when id_estatus=2 then 'Failed' when id_estatus=3 then 'Successful' END
,id_estatus
,msisdn
,oferta
,'preregistered'
,fecha_ingreso
,fecha_update
,substring(replace(error_de_plataforma,SUBSTRING_INDEX(error_de_plataforma,' ',1),''),14,100)
,substring(SUBSTRING_INDEX(error_de_plataforma,' ',1),10,10)
,CASE when id_estatus=1 then fecha_ingreso when ( (id_estatus=2) OR  (id_estatus=4) )  then fecha_update when (id_estatus=3 OR id_estatus=5  )then 
(
select max(fecha_ingreso) from auditor.auditor_activate where 
(id_estatus=3 or id_estatus=5) and transaccion_id like 'preregistered_on_line_batch%'
and cast(replace(transaccion_id,'preregistered_on_line_batch','') as int)=cast(replace(pr.transaccion_id,'preregistered_on_line_batch','') as int)
)
END
, Case  when (order_id_bss is null) then '' else order_id_bss END
, msisdnported
, idpos
, address
FROM auditor.auditor_pregistered pr
WHERE (id_company='$be' and transaccion_id like '$transaction_id' ) 
or 
(transaccion_id like '$transaction_id')
or  
(id_company='$be' and  msisdn='$msisdn')
or
( msisdn='$msisdn')
order by 1 desc ";
#print $strsql;
&escribelog($be,$strsql);
$sth = $dbh->prepare($strsql);
$sth->execute or die("Couldn't execute $strsql.".$dbh->errstr."\n");
while(@row = $sth->fetchrow_array()){
    $id=$row[0];
    $ddde=$row[1]; 	     
    $ddd=$row[2];
    $dn2=$row[3];
    $ofer=$row[4];
    $op=$row[5];
    $fe=$row[6];
    $fupdate=$row[7];
    $err=$row[8];
    $errcode=$row[9];
    $fest=$row[10];
    $orderidbss=$row[11];
    $msisdnported=$row[12];
    $idpos=$row[13];
    $addr=$row[14];
#$strsql2="SELECT    descripcion FROM auditor.auditor_on_line_batch_estatus  WHERE id_estatus='$ddd'  ";
#$sth2 = $dbh->prepare($strsql2);
#$sth2->execute or die("Couldn't execute $strsql.".$dbh->errstr."\n");
#while(@row2 = $sth2->fetchrow_array()){
#        $ddde = $row2[0];
#
#}

if(length($ofer)==0)
{
$OFFID='"'.$ofer.'"';
}
else{
$OFFID=$ofer;
}


#if($ddd==2)
#{
#$as1x.='{"id":"'.$id.'","status":"'.$ddde.'","offeringId":'.$OFFID.',"recorddate":"'.$fe.'","operation":"'.$op.'","errordate":"'.$ferr.'","errordescription":"'.$err.'","errorcode":"'.$errcode.'","statusdate":"'.$fest.'"},';
$as1x.='{"id":"'.$id.'","status":"'.$ddde.'","offeringid":'.$OFFID.',"address":"'.$addr.'","recorddate":"'.$fe.'","operation":"'.$op.'","statusdate":"'.$fest.'","errordescription":"'.$err.'","errorcode":"'.$errcode.'","msisdnported":"'.$msisdnported.'","orderidbss":"'.$orderidbss.'","idPos":"'.$idpos.'"},';

#}else
#{
#$as1x.='{"id":"'.$id.'","status":"'.$ddde.'","offeringId":'.$OFFID.',"recorddate":"'.$fe.'","operation":"'.$op.'","statusdate":"'.$fest.'"},';  
#}

$rt++;
}
$as1x=substr($as1x,0,-1);


if($rt>0)
{

#$as1x = substr($json_str,0, -1);
$as1= $json->encode({be_id=>$be,msisdn=>$dn2,description=>'search',status=>'ok',transationDate=>$fecg});
$as1x=substr($as1x,0,-1);
$as1=substr($as1,0,-1);
$as1.=',"data":['.$as1x.'}]}';
#print "$as1x\n";
}
else{
$as1= $json->encode({be_id=>$be,status=>'no-ok',description=>'Data not found ',transationDate=>$fecg});


}
}
else{
$as1= $json->encode({be_id=>$be,status=>'no-ok',description=>'some data is not correct',id_transation_cudar=>$id,transationDate=>$fecg});
}

&escribelog($be,$as1);

print $q->header("application/json");
use JSON::XS;
my $j = JSON::XS->new->utf8->pretty(1);
#$as1=$ut;
#$ty= $j->encode($as1);

#$as1=$data;
#$ty= $j->encode({$as1});

#$ty =~ s/\\//g;
#&escribelog('$as1',$be);
#$ty=substr $ty,0,-10;
#print $ty;

print $as1;

#print "$as1x\n";


