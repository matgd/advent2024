open(FH, '<', "input.txt") or die $!;
my $input = <FH>;

# Part 1
my @matches = $input =~ m/mul\((\d*),(\d*)\)/gx;
my $result = 0;
for (my $i = 0; $i < @matches; $i += 2) {
    $result += $matches[$i] * $matches[$i + 1];
}
print "Part 1: ". $result . "\n";

# Part 2
my @matches = $input =~ m/mul\((\d*),(\d*)\)|(don't\(\))|(do\(\))/gx;
my $result = 0, $on = 1;
for (my $i = 0; $i < @matches;) {
    if ($matches[$i] eq "do()") {
        $on = 1;
        $i++;
    } elsif ($matches[$i] eq "don't()") {
        $on = 0;
        $i++;
    } elsif ($on) {
        $result += $matches[$i] * $matches[$i + 1];
        $i += 2;
    } else {
        $i++;
    }
}
print "Part 2: " . $result . "\n";