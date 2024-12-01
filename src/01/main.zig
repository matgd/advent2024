// Before in bash:
//   LEFT=$(cat input.txt | cut -d' ' -f1 | sort -n)
//   RIGHT=$(cat input.txt | cut -d' ' -f4 | sort -n)
//   MERGED=$(paste -d' ' <(echo "$LEFT") <(echo "$RIGHT"))
//   echo $MERGED | rs -t -C' ' 2 1000 > input_sorted.txt  # for some reason this works only in CLI

const std = @import("std");
const input = @embedFile("input_sorted.txt");
const print = std.debug.print;

fn part1(numbers_left: [1000]i32, numbers_right: [1000]i32) !void {
    const vec_left = @as(@Vector(1000, i32), numbers_left);
    const vec_right = @as(@Vector(1000, i32), numbers_right);
    const res_vec = @abs(vec_left - vec_right);
    const sum = @reduce(.Add, res_vec);

    print("Part 1, sum: {}\n", .{sum});
}

fn part2(numbers_left: [1000]i32, numbers_right: [1000]i32) !void {
    var left_pivot: u16 = 0;
    var right_pivot: u16 = 0;
    var sum: i32 = 0;

    while (left_pivot < numbers_left.len and right_pivot < numbers_right.len) {
        // We know that the numbers are sorted
        const l = numbers_left[left_pivot];
        var r = numbers_right[right_pivot];

        var similarity_score: u16 = 0;

        while (l == r) {
            similarity_score += 1;
            r = numbers_right[right_pivot + similarity_score];
        }
        sum += l * similarity_score;

        if (l < r) {
            left_pivot += 1;
        } else {
            right_pivot += 1;
        }
    }

    print("Part 2, sum: {}\n", .{sum});
}

pub fn main() !void {
    var lines = std.mem.splitSequence(u8, input, "\n");
    var left = std.mem.splitSequence(u8, lines.next().?, " ");
    var right = std.mem.splitSequence(u8, lines.next().?, " ");
    var numbers_left: [1000]i32 = undefined;
    var numbers_right: [1000]i32 = undefined;

    for (0..numbers_left.len) |i| {
        numbers_left[i] = try std.fmt.parseInt(i32, left.next().?, 10);
        numbers_right[i] = try std.fmt.parseInt(i32, right.next().?, 10);
    }

    try part1(numbers_left, numbers_right);
    try part2(numbers_left, numbers_right);
}
