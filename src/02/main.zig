const std = @import("std");
const input = @embedFile("input.txt");
const print = std.debug.print;
const allocator = std.heap.page_allocator;

fn part1(number_lines: std.ArrayList(std.ArrayList(i32))) void {
    var safe_sum: u16 = 0;
    for (number_lines.items) |line| {
        safe_sum += if (lineSafe(line)) 1 else 0;
    }
    print("Part 1, safe sum: {}\n", .{safe_sum});
}

inline fn safeIncrease(lower: i32, higher: i32) bool {
    return higher - lower >= 1 and higher - lower <= 3;
}

inline fn safeDecrease(lower: i32, higher: i32) bool {
    return safeIncrease(higher, lower);
}

fn lineSafe(line: std.ArrayList(i32)) bool {
    var l: ?i32 = null;
    var r: ?i32 = null;
    var ascending = false;
    var descending = false;

    for (line.items) |number| {
        l = r;
        r = number;

        if (l == null or r == null) {
            continue;
        }

        if (l.? - r.? > 0) {
            descending = true;
        } else if (l.? - r.? < 0) {
            ascending = true;
        } else {
            return false;
        }

        if (ascending and descending) {
            return false;
        }

        if (ascending) {
            if (!safeIncrease(l.?, r.?)) {
                return false;
            }
        } else if (descending) {
            if (!safeDecrease(l.?, r.?)) {
                return false;
            }
        }
    }

    return true;
}

pub fn main() !void {
    var lines = std.mem.splitSequence(u8, std.mem.trim(u8, input, "\n"), "\n");

    var number_lines = std.ArrayList(std.ArrayList(i32)).init(allocator);
    while (lines.next()) |line| {
        var numbers = std.ArrayList(i32).init(allocator);
        var split_numbers = std.mem.splitSequence(u8, line, " ");
        while (split_numbers.next()) |number| {
            const number_i32 = try std.fmt.parseInt(i32, number, 10);
            try numbers.append(number_i32);
        }
        try number_lines.append(numbers);
    }

    part1(number_lines);

    // print arraylist
    // for (number_lines.items) |line| {
    //     for (line.items) |number| {
    //         print("{}, ", .{number});
    //     }
    //     print("\n", .{});
    // }
}
