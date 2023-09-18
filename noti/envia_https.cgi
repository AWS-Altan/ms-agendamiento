#!/usr/bin/perl 
use strict; 
use CGI::Carp qw(fatalsToBrowser);
use CGI ();
use Data::Dumper qw(Dumper);

#use warnings; 
use HTTP::Response; 
use LWP::UserAgent;
use HTTP::Request;

use JSON qw(decode_json);

my $q  = CGI->new;
my $json  = JSON->new->utf8;

my $yu=$q->param('POSTDATA');
my $input=$json->decode($yu);

use JSON::XS;
my $j = JSON::XS->new->utf8->pretty(1);


#my $as1= $json->encode({be_id=>'103',status=>'no-ok',description=>'some data is not correct',id_transation_cudar=>'555',transationDate=>'20190212'});

print $q->header("application/json");
use JSON::XS;
my $j = JSON::XS->new->utf8->pretty(1);
#&datalog($input);

my $response = HTTP::Response->new( 200, 'OK', [ 'Content-Type' => 'application/json' ] ); 
$response->protocol('HTTP/1.1');
$response->date(time); 
print $response->as_string;
