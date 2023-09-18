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
  $error=~s/\"/\\\"/g;
  (my $seg, my $min, my $hora, my $dia, my $mes, my $ao, my @zape) = localtime(time);
  $ao += 1900;
  $mes=$mes+1;
  $mes=&bl($mes);
  $dia=&bl($dia);
  $hora=&bl($hora);
  $min=&bl($min);
  $seg=&bl($seg);
  my $log_file="/var/www/cgi-bin/log/resultado-agendaonlinetest-$ao-$mes-$dia.log";
  open (LOG," >> $log_file");
  print LOG "$ao-$mes-$dia-$hora:$min:$seg-$error\n";
  close (LOG);
  if($id_com=~/^\d[3,5]$/){
     my $log_file2="/var/www/cgi-bin/log/resultado-agendaonlinetest-$ao-$mes-$dia-$id_com.log";
     open (LOG," >> $log_file2");
     print LOG "$ao-$mes-$dia-$hora:$min:$seg-$error\n";
     close (LOG);
    }
}


use JSON qw(decode_json);

my $q  = CGI->new;
my $json  = JSON->new->utf8;

my $yu=$q->param('POSTDATA');
my $input=$json->decode($yu);
&escribelog($be,$yu);
my $be=$input->{'be_id'};
my $msisdn=$input->{'msisdn'};
my $idbss=$input->{'id_bss'};
&escribelog($be,"$be,$msisdn,$idbss");
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




if(!($idbss=~/^\d{9,}$/) && (!($be=~/^\d{3,5}$/) || !($msisdn=~/^\d{10}$/)))
{
$f=1;
}
if($f==0){
   use DBI;
   $dat="auditor";
   $host="10.0.0.23";
   $port="3306";
   $userid="operador";
   $passwd="operador01";
   $con2="DBI:mysql:database=$dat;$host:$port";
   $dbh = DBI->connect($con2,$userid,$passwd);
 
   if(($be=~/^\d{3,5}$/) && ($msisdn=~/^\d{10}$/)){
      $strsql="SELECT  *   FROM auditor.auditor_on_line_batch  WHERE id_company='$be' and msisdn='$msisdn' and fecha_ingreso > date_sub(now(), interval 3 month) order by fecha_ingreso desc limit 5  ";
      $as1x=&findinfo($strsql);
      $qryflag=1;
     }
   
   if(($idbss=~/^\d+$/)&& ($qryflag!=1)){
      $qryid="SELECT  *   FROM auditor.auditor_on_line_batch  WHERE order_id_bss='$idbss' order by fecha_ingreso desc limit 1";
      $as1x=&findinfo($qryid);
     
      $qryid2="SELECT msisdn,id_company  FROM auditor.auditor_on_line_batch  WHERE order_id_bss='$idbss' order by fecha_ingreso desc limit 1";
      $sth = $dbh->prepare($qryid2);
      $sth->execute or die("Couldn't execute $qryid2.".$dbh->errstr."\n"); 
      $ref = $sth->fetchrow_hashref();
      $be=$ref->{'id_company'};
      $msisdn=$ref->{'msisdn'};
     }

   $as1x=substr($as1x,0,-1);

   if($as1x!~/^\s*$/){
      $as1= $json->encode({be_id=>$be,msisdn=>$msisdn,description=>'search',status=>'ok',transationDate=>$fecg});
      #&escribelog($be,$as1);
      $as1x=substr($as1x,0,-1);
      $as1=substr($as1,0,-1);
      $as1.=',"data":['.$as1x.'}]}';
     }else{
           $as1= $json->encode({be_id=>$be,status=>'no-ok',description=>'Data not found ',transationDate=>$fecg});
          }
}else{
      $as1= $json->encode({be_id=>$be,status=>'no-ok',description=>'some data is not correct',id_transation_cudar=>$id,transationDate=>$fecg});
     }

&escribelog($be,$as1);


print $q->header("application/json");
print $as1;

sub findinfo{
 $qryf=shift;
 &escribelog($be, $qryf);
 $sth = $dbh->prepare($qryf);
 $sth->execute or die("Couldn't execute $qryf.".$dbh->errstr."\n");
 while(@row = $sth->fetchrow_array()){
       my $id=$row[0];
       my $ddd = $row[2];
       my $ofer = $row[4];
       my $dir = $row[5];
       my $fe = $row[7];
       my $op=$row[15];
       my $fe = $row[7];
       my $op=$row[19];
       my $sec=$row[18];
       my $fi = $row[16];
       my $fexp = $row[15];
       my $op=$row[19];
       my $oid_bss=$row[20];

       $strsql2="SELECT    descripcion FROM auditor.auditor_on_line_batch_estatus  WHERE id_estatus='$ddd'  ";
         $sth2 = $dbh->prepare($strsql2);
         $sth2->execute or die("Couldn't execute $strsql.".$dbh->errstr."\n");
         while(@row2 = $sth2->fetchrow_array()){
               $ddde = $row2[0];
              }

         if(!(defined $ofer))
           {
            $OFFID='"'.$ofer.'"';
           }else{
                 $OFFID=$ofer;
                }
       $asw1x.='{"id":"'.$id.'","status":"'.$ddde.'","offeringId":'.$OFFID.',"coordinates":"'.$dir.'","effectivedate":"'.$fe.'","operation":"'.$op.'","purchasedSequency":"'.$sec.'","expireEffectiveDate":"'.$fexp.'","startEffectiveDate":"'.$fi.'","order_bss":"'.$oid_bss.'"},';

      }
 &escribelog($be,$asw1x);
 return $asw1x;
}
