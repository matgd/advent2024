const input = await Bun.file(process.argv[2]).text();
const blinks = +process.argv[3];
const stoneState = {};
input.trim().split(' ').forEach(s => stoneState[s] === undefined ? stoneState[s] = 1 : stoneState[s]++);

function stoneDelta(stone, numberOfStones) {
    const delta = {[stone]: -numberOfStones};

    if (stone === '0') 
        return {...delta, '1': numberOfStones};

    else if (stone.length % 2 === 0) {
        const [s1, s2] = [stone.slice(0, stone.length / 2), (+stone.slice(stone.length / 2)) + ''];
        if (s1 === s2) 
            return {...delta, [s1]: numberOfStones*2};

        return {...delta, [s1]: numberOfStones, [s2]: numberOfStones};
    }

    return {...delta, [(+stone * 2024) + '']: numberOfStones};
}

for (let i = 0; i < blinks; i++) {
    for (let [k, v] of Object.entries(stoneState)) {
        for (let [k2, v2] of Object.entries(stoneDelta(k, +v))) {
            if (stoneState[k2] === undefined) stoneState[k2] = 0;
            stoneState[k2] += v2;
        }
    }
}

console.log(Object.values(stoneState).reduce((a, b) => a + b, 0));
