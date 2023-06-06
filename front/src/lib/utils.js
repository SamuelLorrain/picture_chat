export function getRandomColor() {
    const value = Math.floor(Math.random() * 16777214);
    return '#' + value.toString(16);
}
