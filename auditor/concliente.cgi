#!/usr/bin/perl

use CGI ();
use Data::Dumper qw(Dumper);
use DBI;
use JSON qw(decode_json);

my $q  = CGI->new;
my $json  = JSON->new->utf8;


my $yu=$q->param('POSTDATA');
my $input=$json->decode($yu);

my $a = $input->{id_company};
my $b = $input->{msisdn};
my $c = $input->{imsi};




#$a=175;
#$b=525584612566;
if(length($b)>3)
{
$cmd="python3 /var/www/cgi-bin/bigd/conve_msisdn_imei.py 52$b 2> /dev/null";
$rt=qx($cmd);

}
if(length($c)>3)
{
$cmd="python3 /var/www/cgi-bin/bigd/conve_imsi_imei.py $c 2> /dev/null";
$rt=qx($cmd);

}
$rt =~ s/\n|\r//g;

my($bb,$cc,$dd)=split(" ",$rt);

$cmd="perl /opt/blackbird/funciones_gorilaV3.pl $b $a profile 2> /dev/null";
#print $cmd;
$rt=qx($cmd);
$rtx=0;
my($rtp,$im)=split(',',$rt);
if($rt=~'Active')
{
$rt="Active";
$rtx=1;
}

if($rt=~'Barring')
{
$rt="Barring";
$rtx=1;
}

if($rt=~'Suspended')
{
$rt="Suspended";
$rtx=1;
}
if($rt!='Active' && $rtx==0)
{
$rt="No Active";
}

print $q->header("application/json");
$fg= $json->encode({status=>$rt,imsi=>$cc,msisdn=>$bb,imei=>$dd});
$fg =~ s/\\n//g;

print "$fg";
#print $cmd;

