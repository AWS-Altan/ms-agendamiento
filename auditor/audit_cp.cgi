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
use JSON::XS;
my $j = JSON::XS->new->utf8->pretty(1);


my $yu=$q->param('POSTDATA');


my $input=$json->decode($yu);
#&escribelog("",$yu);
my $dn=$input->{msisdn};
my $be=$input->{be_id};
my $coe=$input->{coordinates};
#my $expx=$input->{'Data'}->{expireEffectiveDate};
#my $fi=$input->{'Data'}->{startEffectiveDate};
#my $secu=$input->{'Data'}->{purchasedSecuency};




my $ofer=$input->{offeringId};
$ofer2=$ofer;

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
if(length($dn)!=10)
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


$strsql="SELECT    count(*) FROM auditor.auditor_changeprimary  WHERE id_company='$be' and id_estatus=1 and msisdn='$dn'   ";
#print "$strsql\n";
$sth = $dbh->prepare($strsql);
$sth->execute or die("Couldn't execute $strsql.".$dbh->errstr."\n");

#print "content-type: text/html \n\n";
#print"Incia el insert...oferta: $ofer  secuencia: $secu";

while(@row = $sth->fetchrow_array()){
        $ddd = $row[0];
}
if($ddd==0)
{
$ofer="1799917006";
$strsql="insert into auditor.auditor_changeprimary (id_company,id_estatus,msisdn,oferta,address,fecha_ingreso,transaccion_id,secuencia) values('$be','1','$dn','$ofer','$coe',now(),'$id','$secu')";
&escribelog($strsql,'inserta');
$sth = $dbh->prepare($strsql);
$sth->execute or die("Couldn't execute $strsql.".$dbh->errstr."\n");


#$ids=1;
#$ids=$sth->{mysql_insertid};
#$as1= $json->encode({be_id=>$be,msisdn=> $dn,offeringId=>$ofer,status=>ok});
#$as1= $json->encode({offeringId=>$ofer});


}

$as1= $json->encode({status=>ok});
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


}

