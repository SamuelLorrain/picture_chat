import { cloneResizeCanvas } from './utils';

export class EditorHistory {
    historyStack = [];
    historyIndex = null;

    append(historyElement) {
        this.historyIndex = this.historyStack.push(historyElement) - 1;
    }

    reset() {
        this.historyStack = [];
        this.historyIndex = null;
    }

    apply(canvasCtx, textElement) {
        if (this.historyIndex < 0) {
            return;
        }
        let historyElement = this.historyStack[this.historyIndex];
        if (!historyElement) {
            return;
        }
        textElement.innerHTML = historyElement.text;
        canvasCtx.putImageData(historyElement.canvas, 0, 0);
        if(this.historyIndex > -1) {
            this.historyIndex -= 1;
        }
    }

    applyResized(canvasCtx, textElement, targetWidth, targetHeight) {
        if (this.historyIndex < 0) {
            return;
        }
        let historyElement = this.historyStack[this.historyIndex];
        if (!historyElement) {
            return;
        }
        textElement.innerHTML = historyElement.text;
        const resizedCanvas = cloneResizeCanvas(
            historyElement.canvas,
            targetWidth,
            targetHeight,
        )
        canvasCtx.putImageData(resizedCanvas, 0, 0);
        if(this.historyIndex > -1) {
            this.historyIndex -= 1;
        }
    }
}
