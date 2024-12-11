const input = await Bun.file(process.argv[2]).text();
const blinks = +process.argv[3];
var stones = input.trim().split(' ');
const stoneState = {};

function stoneTransform(stone) {
    if (stone === '0')
        return ['1'];
    if (stone.length % 2 === 0)
        return [stone.slice(0, stone.length / 2), (+stone.slice(stone.length / 2)) + ''];
    return [(+stone * 2024) + ''];
}

function updateStoneState(newStones) {
    newStones.forEach(s => stoneState[s] === undefined ? stoneState[s] = 1 : stoneState[s]++);
}

updateStoneState(stones);
for (let i = 0; i < blinks; i++) {
    console.log(`${i}/${blinks}`);
    const stateClone = structuredClone(stoneState);
    Object.keys(stateClone).forEach(s => {
        for (let j = 0; j < stateClone[s]; j++) {
            stoneState[s]--;
            updateStoneState(stoneTransform(s));
        }
    });
}

console.log(stoneState);
console.log(Object.values(stoneState).reduce((a, b) => a + b, 0));

//  Part 1 199946
