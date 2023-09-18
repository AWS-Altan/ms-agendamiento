#!/usr/bin/perl -w
use CGI;
use XML::Simple;
use Data::Dumper;
my $q = CGI->new; # create new CGI object
my $be=$q->param('BEID');

print "$be";
my $simple = XML::Simple->new();
my $data   = $simple->XMLin($be);

#my $be = $data->{'soapenv:Body'}->{'off:ConsumptionNotifyTOThirdPartyReqMsg'}->{'off:BEID'};
#my $msisdn = $data->{'soapenv:Body'}->{'off:ConsumptionNotifyTOThirdPartyReqMsg'}->{'off:MSISDN'};
#my $free = $data->{'soapenv:Body'}->{'off:ConsumptionNotifyTOThirdPartyReqMsg'}->{'off:FreeUnitTypeName'};
#my $tot = $data->{'soapenv:Body'}->{'off:ConsumptionNotifyTOThirdPartyReqMsg'}->{'off:TotalAmount'};
#my $unsu = $data->{'soapenv:Body'}->{'off:ConsumptionNotifyTOThirdPartyReqMsg'}->{'off:UnUsedAmount'};
#my $expire = $data->{'soapenv:Body'}->{'off:ConsumptionNotifyTOThirdPartyReqMsg'}->{'off:ExpiryDate'};
#my $thv = $data->{'soapenv:Body'}->{'off:ConsumptionNotifyTOThirdPartyReqMsg'}->{'off:ThresholdValue'};

$dirlog="/var/www/cgi-bin/log/notificador/";

sub bl
{
  my $tt=shift;
  return ((length($tt)==1))? "0".$tt : $tt;
}

sub datalog{
my $error=shift;
(my $seg, my $min, my $hora, my $dia, my $mes, my $ao, my @zape) = localtime(time);
  $ao += 1900;
  $mes=$mes+1;
  $mes=&bl($mes);
  $dia=&bl($dia);
  $hora=&bl($hora);
  $min=&bl($min);
  $seg=&bl($seg);
  my $log_file="$dirlog/log-notif-$ao$mes$dia.log";
  open (LOG," >> $log_file");
  print LOG "$ao$mes$dia-$hora:$min:$seg - $error\n";
  close (LOG);
}

#if(length($msisdn)=='10' and ($be=='175' || $be=='130'))
#{
#Inserta info en BD
#$connect="DBI:mysql:database=$data;$host:$port";
#$dbh = DBI->connect($connect,$userid,$passwd);

#$inserta=" insert into notificador.notificador_proxy(id_company,msisdn,freedata,total_amount,unsused_amount,offeringid,threshold,validity,fecha_notificacion,id_status) values ($be,$msisdn,$free,$tot,$unsu,$off,$thv,$vali,sysdate(),'0')";

#$ejin = $dbh->prepare($inserta);
#$ejin->execute or die("Couldn't execute $inserta $DBI::errstr.\n");
#$re=$dbh->errstr;
#Consulta Endpoint en BD
#my $ty="select end_point, event_type from notificador.notificador_ws where id_company='$be'";
#my $sth = $dbh->prepare($ty);
#$sth->execute or die("Couldn't execute $ty $DBI::errstr.\n");
#while (@row = $sth->fetchrow_array) 
#{ 
#$call = $row[0];
#$etype = $row[1];
#}
#&datalog("$call");
#Envía gpiGee Gorila
#$cmd="perl /var/www/cgi-bin/bacth/funciones_gorilaV3.pl '' $be notificador '' '' '' $etype $call";
#print "---->>>>>>>>>>>>>>>>>>>>>>>>$cmd<----------------------\n";
#my $ty=qx($cmd);
#print "$ty \n";
#&datalog("$ty");

#else
#	{
#print "El msisdn o el id_company no es válido";
#print $json->encode({ status => nok});
#&datalog($json->encode({ status => nok}));
#	}

#valuesfinish;
#$dbh->disconnect();

