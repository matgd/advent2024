const std = @import("std");
const input = @embedFile("tinput.txt");
const print = std.debug.print;
const allocator = std.heap.page_allocator;

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

fn lineSafePart2(line: std.ArrayList(i32), found_error: bool) bool {
    var l: ?i32 = null;
    var r: ?i32 = null;
    var ascending = false;
    var descending = false;

    print("line.items: {any}\n", .{line.items});

    for (line.items, 0..) |number, i| {
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
            if (found_error) {
                return false;
            }
            var listc = std.ArrayList(i32, allocator);
            var listcc = std.ArrayList(i32, allocator);
            for (line.items, 0..) |n, j| {
                if (j == i - 1) {
                    continue;
                }
                _ = listc.append(n);
            }
            for (line.items, 0..) |n, j| {
                if (j == i) {
                    continue;
                }
                _ = listcc.append(n);
            }
            return lineSafePart2(listc, true) or lineSafePart2(listcc, true);
        }

        if (ascending and descending) {
            if (found_error) {
                return false;
            }
            var listc = std.ArrayList(i32, allocator);
            var listcc = std.ArrayList(i32, allocator);
            for (line.items, 0..) |n, j| {
                if (j == i - 1) {
                    continue;
                }
                _ = listc.append(n);
            }
            for (line.items, 0..) |n, j| {
                if (j == i) {
                    continue;
                }
                _ = listcc.append(n);
            }
            return lineSafePart2(listc, true) or lineSafePart2(listcc, true);
        }

        if (ascending and !safeIncrease(l.?, r.?)) {
            if (found_error) {
                return false;
            }
            var listc = line.clone();
            var listcc = line.clone();
            _ = listc.orderedRemove(i - 1);
            _ = listcc.orderedRemove(i);
            return lineSafePart2(listc, true) or lineSafePart2(listcc, true);
        } else if (descending and !safeDecrease(l.?, r.?)) {
            if (found_error) {
                return false;
            }
            var listc = line.clone();
            var listcc = line.clone();
            _ = try listc.orderedRemove(i - 1);
            _ = listcc.orderedRemove(i);
            return lineSafePart2(listc, true) or lineSafePart2(listcc, true);
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
    defer number_lines.deinit();

    var safe_sum: u16 = 0;
    var safe_sum_part2: u16 = 0;
    for (number_lines.items) |line| {
        safe_sum += if (lineSafe(line)) 1 else 0;
        safe_sum_part2 += if (lineSafePart2(line, false)) 1 else 0;
    }
    print("Part 1, safe sum: {}\n", .{safe_sum});
    print("Part 2, safe sum: {}\n", .{safe_sum_part2});

    for (number_lines.items) |line| {
        line.deinit();
    }
}
