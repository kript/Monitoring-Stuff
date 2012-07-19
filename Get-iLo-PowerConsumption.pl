#!/usr/bin/perl
# script to get iLo information for snmpd to graph in Cacti
# you'd think there would be a better way, huh?

use warnings;
use Net::ILO;
use strict;
use v5.10; #make use of the say command and other nifty perl 10.0 onwards goodness
#use Carp;
use YAML;

#load the username and password from a config file

my $account = YAML::LoadFile($ENV{HOME} . "/.ilo_login")
    or die "Failed to read $ENV{HOME}/.ilo_login - $!";

my $ilo = Net::ILO->new({
        address     => '192.168.1.117',
        username    => "$account->{username}",
        password    => "$account->{password}",
        debug		=> '0', #set up to 2 to get verbose XML & transcript of connection
});

my $power_status = $ilo->power or die $ilo->error;

# something like 340
say $ilo->power_consumption;
    
__END__
=head1 NOTES

<b> Note</b> The script expect to find a file called ~/.ilo_login and will fail if it can't.
It's a YAML file and follows the following format;

 ---
 username: ilo_username
 password: ilo_password
