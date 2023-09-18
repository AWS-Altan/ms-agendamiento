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
  my $log_file="/efs/ms/agendamiento/resultado-agenda-$ao-$mes-$dia-$id_com.log";

  open (LOG," >> $log_file");
  print LOG "$ao-$mes-$dia-$hora:$min:$seg-$error\n";
  close (LOG);
}


use JSON qw(decode_json);

my $q  = CGI->new;
my $json  = JSON->new->utf8;


my $yu=$q->param('POSTDATA');
my $input=$json->decode($yu);
&escribelog("",$yu);
my $id=$input->{'id_transation_cudar'};
my $be=$input->{'be_id'};
my $msisdn=$input->{'msisdn'};
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


#$data =~ s/\{\}//g;


#$data=substr($data,2);
if(length($id)==0 && length($msisdn)>5)
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



#$strsql="SELECT  *   FROM auditor.auditor_on_line_batch  WHERE id_company='$be' and msisdn='$msisdn' ";

$strsql="SELECT    id_estatus FROM auditor.auditor_on_line_batch  WHERE id_company='$be' and id_auditor_alta='$id' and msisdn='$msisdn' ";
$sth = $dbh->prepare($strsql);
$sth->execute or die("Couldn't execute $strsql.".$dbh->errstr."\n");
while(@row = $sth->fetchrow_array()){
        $ddd = $row[0];
}
$strsql="SELECT    descripcion FROM auditor.auditor_on_line_batch_estatus  WHERE id_estatus='$ddd'  ";
$sth = $dbh->prepare($strsql);
$sth->execute or die("Couldn't execute $strsql.".$dbh->errstr."\n");
while(@row = $sth->fetchrow_array()){
        $ddde = $row[0];
}

if($ddd==1)
{
$strsql="update auditor.auditor_on_line_batch set id_estatus=999 where id_auditor_alta='$id'";
$sth = $dbh->prepare($strsql);
$sth->execute or die("Couldn't execute $strsql.".$dbh->errstr."\n");
$ids=$sth->{mysql_insertid};
$as1= $json->encode({be_id=>$be,status=>'ok',description=>'Cancel'});
}
else{
$as1= $json->encode({be_id=>$be,status=>'no-ok',description=>$ddde });
$as1= $json->encode({be_id=>$be,status=>'no-ok',description=>'Data not found' });


}
}
else{
$as1= $json->encode({be_id=>$be,status=>'no-ok',description=>'Some data is not correct',id_transation_cudar=>$id});
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



