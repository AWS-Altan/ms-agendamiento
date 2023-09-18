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
  my $log_file="/var/www/cgi-bin/log/eventos/resultado-agenda-$ao-$mes-$dia-$id_com.log";

  open (LOG," >> $log_file");
  print LOG "$ao-$mes-$dia-$hora:$min:$seg-$error\n";
  close (LOG);
}


use JSON qw(decode_json);

my $q  = CGI->new;
my $json  = JSON->new->utf8;


my $yu=$q->param('POSTDATA');


my $input=$json->decode($yu);
#&escribelog("",$yu);
my $inoutr=$input->{'Inout'};
my $trans=$input->{'Transactionid'};
my $subt=$input->{'Subtransationid'};
my $tar=$input->{'Target'};
my $resor=$input->{'Resource'};
my $part=$input->{'Parnetid'};
my $timesa=$input->{'Timestamp'};
my $data=$input->{'Data'};
my $dn=$input->{'Data'}->{msisdn};
my $im=$input->{'Data'}->{imsi};
my $fe=$input->{'Data'}->{effectiveDate};
my $be=$input->{'Data'}->{be_id};
my $coe=$input->{'Data'}->{coordinates};
#$ofer=$input->{'Resource'};
#$ofer=$yu;

my $ofer=$input->{'Data'}->{offeringId};

if($yu=~'purchase')
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
#$fe="2018-07-07";
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
$port="3306";
$userid="operador";
$passwd="operador01";
$con2="DBI:mysql:database=$dat;$host:$port";
$dbh = DBI->connect($con2,$userid,$passwd);



$strsql="SELECT    count(*) FROM auditor.auditor_on_line_batch  WHERE id_company='$be' and id_estatus=1 and msisdn='$dn'   ";
$sth = $dbh->prepare($strsql);
$sth->execute or die("Couldn't execute $strsql.".$dbh->errstr."\n");
while(@row = $sth->fetchrow_array()){
        $ddd = $row[0];
}
if($ddd==0)
{
$strsql="insert into auditor.auditor_on_line_batch (id_company,id_estatus,msisdn,oferta,address,fecha_ingreso,transaccion_id,operacion) values('$be','1','$dn','$ofer','$coe','$fe','$id','$resor')";

$sth = $dbh->prepare($strsql);
$sth->execute or die("Couldn't execute $strsql.".$dbh->errstr."\n");
$ids=$sth->{mysql_insertid};
$as1= $json->encode({be_id=>$be,imsi=> $im,msisdn=> $dn, Resource=>$resor,effectiveDate=>$fe,coordinates=>$coe,offeringId=>$ofer,status=>ok,id_transation_cudar=>$ids});
}
else{
$as1= $json->encode({be_id=>$be,imsi=> $im,msisdn=> $dn, Resource=>$resor,effectiveDate=>$fecg,coordinates=>$coe,offeringId=>$ofer,status=>nok,description=>'found the data duplicate or  has a process in the agenda'});


}
}
else{
$as1= $json->encode({be_id=>$be,imsi=> $im,msisdn=> $dn, Resource=>$resor,effectiveDate=>$fecg,coordinates=>$coe,offeringId=>$ofer,status=>nok,description=>'some the data is not correct'});


}

&escribelog($be,'$as1');

print $q->header("application/json");
use JSON::XS;
my $j = JSON::XS->new->utf8->pretty(1);
#$as1=$ut;
#$ty= $j->encode({resp=>{$as1}});

#$as1=$data;
#$ty= $j->encode({$as1});

#$ty =~ s/\\//g;
#&escribelog('$as1',$be);
#$ty=substr $ty,0,-10;
#print $ty;

print $as1;



