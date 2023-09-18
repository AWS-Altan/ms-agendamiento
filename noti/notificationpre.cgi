#!/usr/bin/perl



use DBI;


use CGI ();
use Data::Dumper qw(Dumper);

use JSON qw(decode_json);

my $q  = CGI->new;
my $json  = JSON->new->utf8;


my $yu=$q->param('POSTDATA');
my $input=$json->decode($yu);

my $a = $input->{a};
my $b = $input->{b};
my $c = $a + $b;

my $msisdn=$input->{'msisdn'};
my $free=$input->{'free_unit_type'};
my $tot=$input->{'total_amount'};
my $unsu=$input->{'unused_amount'};
my $vali=$input->{'validity'};
my $off=$input->{'offerind'};
my $thv=$input->{'threshold_value'};


print $q->header("application/json");
print $json->encode({ status => ok});
#print $rt;
#print "**************\n";
#print $yu;
#print Dumper $data;
##	$yu=~ s/\"/"\\"/g;
#$yu =~ s/"/\\/g;
#$gh='[{"body":"'.$yu.'"}]';


#$rty2=qq{curl -i -X POST -H 'Content-Type: application/json; charset=UTF-8' -d '$fg' http://10.10.0.220:41885 2>/dev/null};

#$rty=qq[$rty2];

#print $rty;


#$eje=qx($rty);

#print "";
#print "**************************************";
#print "-->$eje<--";
#qx($rt);
