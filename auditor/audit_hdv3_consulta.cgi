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
  $dia=&bl($dia-1);
  $hora=&bl($hora);
  $min=&bl($min);
  $seg=&bl($seg);
  my $log_file="/var/www/cgi-bin/log/eventos/resultado-agenda-$ao-$mes-$dia-$id_com.log";

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
&escribelog("",$yu);
my $be=$input->{'be_id'};
my $msisdn=$input->{'msisdn'};
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
if($be<1 && length($msisdn)<5)
{
$f=1;
}
if($f==0)
{
use DBI;
$dat="auditor";
$host="10.0.0.23";
$port="3306";
$userid="operador";
$passwd="operador01";
$con2="DBI:mysql:database=$dat;$host:$port";
$dbh = DBI->connect($con2,$userid,$passwd);



$strsql="SELECT  *   FROM auditor.auditor_on_line_batch  WHERE id_company='$be' and msisdn='$msisdn' and fecha_ingreso > date_sub(now(), interval 3 month) order by fecha_ingreso desc limit 5  ";
#print $strsql;
$sth = $dbh->prepare($strsql);
$sth->execute or die("Couldn't execute $strsql.".$dbh->errstr."\n");
while(@row = $sth->fetchrow_array()){
    $id=$row[0]; 	     
    $ddd = $row[2];
	$ofer = $row[4];
	$dir = $row[5];
	$fe = $row[7];
	$sec=$row[18];
         $fi = $row[17];
	$fexp = $row[16];
        $op=$row[20];

$strsql2="SELECT    descripcion FROM auditor.auditor_on_line_batch_estatus  WHERE id_estatus='$ddd'  ";
$sth2 = $dbh->prepare($strsql2);
$sth2->execute or die("Couldn't execute $strsql.".$dbh->errstr."\n");
while(@row2 = $sth2->fetchrow_array()){
        $ddde = $row2[0];

}

if(length($ofer)==0)
{
$OFFID='"'.$ofer.'"';
}
else{
$OFFID=$ofer;
}


$as1x.='{"id":"'.$id.'","status":"'.$ddde.'","offeringId":'.$OFFID.',"coordinates":"'.$dir.'","effectivedate":"'.$fe.'","operation":"'.$op.'","purchasedSequency":"'.$sec.'","expireEffectiveDate":"'.$fexp.'","startEffectiveDate":"'.$fi.'"},';


$rt++;
}
$as1x=substr($as1x,0,-1);


if($rt>0)
{

#$as1x = substr($json_str,0, -1);
$as1= $json->encode({be_id=>$be,msisdn=>$msisdn,description=>'search',status=>'ok',transationDate=>$fecg});
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

&escribelog($be,'$as1');

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

