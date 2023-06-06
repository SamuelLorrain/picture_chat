export function getRandomColor() {
    const value = Math.floor(Math.random() * 16777214);
    return '#' + value.toString(16);
}

export function cloneResizeCanvas(canvas, targetX, targetY) {
    let copy = document.createElement('canvas');
    let context = copy.getContext('2d');
    copy.width = targetX;
    copy.height = targetY;
    context.drawImage(canvas,0 ,0, targetX, targetY);
    return copy;
}

export function resizeImageData(imageDataUrl, targetX, targetY) {

}
