const std = @import("std");
const input = @embedFile("input_sorted.txt");
const print = std.debug.print;

fn part1() !void {
    var lines = std.mem.splitSequence(u8, input, "\n");
    var left = std.mem.splitSequence(u8, lines.next().?, " ");
    var right = std.mem.splitSequence(u8, lines.next().?, " ");
    var numbers_left: [1000]i32 = undefined;
    var numbers_right: [1000]i32 = undefined;

    for (0..1000) |i| {
        numbers_left[i] = try std.fmt.parseInt(i32, left.next().?, 10);
        numbers_right[i] = try std.fmt.parseInt(i32, right.next().?, 10);
    }

    const vec_left = @as(@Vector(1000, i32), numbers_left);
    const vec_right = @as(@Vector(1000, i32), numbers_right);
    const res_vec = @abs(vec_left - vec_right);
    const sum = @reduce(.Add, res_vec);

    print("Sum: {}\n", .{sum});
}

pub fn main() !void {
    try part1();
}
