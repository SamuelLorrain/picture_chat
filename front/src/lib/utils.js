export function getRandomColor() {
    const value = Math.floor(Math.random() * 16777215);
    return '#' + value.toString(16);
}
