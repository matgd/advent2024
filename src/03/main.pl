open(FH, '<', "input.txt") or die $!;
my $input = <FH>;

my @matches = $input =~ m/mul\((\d*),(\d*)\)/gx;
my $result = 0;
for (my $i = 0; $i < @matches; $i += 2) {
    print $matches[$i] . " * " . $matches[$i + 1] . "\n";
    $result += $matches[$i] * $matches[$i + 1];
}
print $result;