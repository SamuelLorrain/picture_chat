<script>
    // TODO
    // STORE HasData/HasDrawn in historyState
    import { useFocus } from 'svelte-navigator';
    import { onMount, createEventDispatcher, onDestroy } from 'svelte';
    import { getRandomColor, cloneResizeCanvas } from './lib/utils';
    import { EditorHistory } from './lib/editor.js';
    import ResetArrow from './icons/ResetArrow.svelte';
    import LeftArrow from './icons/LeftArrow.svelte';
    import RightArrow from './icons/RightArrow.svelte';

    let canvas;
    let textSpace;
    let color = getRandomColor();
    let size = 2;
    let drawing = false;
    let hasData = false;
    let hasDrawn = false;
    let canvasResized = false;
    const CANVAS_DEFAULT_WIDTH = 600;
    const CANVAS_DEFAULT_HEIGHT = 200;
    const canvasSize = {
        width: CANVAS_DEFAULT_WIDTH,
        height: CANVAS_DEFAULT_HEIGHT
    }
    const cursor = {
        x: null,
        y: null,
    }
    const editorHistory = new EditorHistory();
    const dispatch = createEventDispatcher();
    const BACKGROUND_COLOR = '#fff';
    let ctx;
    let registerFocus = useFocus();

    const pointerMoveEvent = function(e) {
        const canvasPosition = canvas.getBoundingClientRect();
        cursor.x = e.clientX - canvasPosition.x - 5;
        cursor.y = e.clientY - canvasPosition.y - 5;
        if (drawing) {
            ctx.fillStyle = color ?? '#000';
            ctx.fillRect(cursor.x, cursor.y, size*10, size*10);
            hasData = true;
        }
    };

    const pointerUpEvent = function(e) {
        drawing = false;
        canvas.style.cursor = "default";
        textSpace.style.cursor = "default";
    };

    const pointerDownEvent = function(e) {
        storeHistory();
        drawing = true;
        hasDrawn = true;
        canvas.style.cursor = "crosshair";
        textSpace.style.cursor = "crosshair";
    };

    const inputEvent = function(e) {
        if(e.data == ' ' || e.inputType == 'insertParagraph') {
            storeHistory();
        }
        hasData = true;
    }

    onMount(() => {
        if (window.innerWidth < canvasSize.width) {
            canvasSize.width = window.innerWidth - 2;
            canvasSize.height = (window.innerWidth / 3.0);
            canvasResized = true;
        }
        ctx = canvas.getContext('2d');
        canvas.width = canvasSize.width;
        canvas.height = canvasSize.height;
        textSpace.style.width = canvasSize.width + 'px';
        textSpace.style.height = canvasSize.height + 'px';

        ctx.fillStyle = BACKGROUND_COLOR;
        ctx.fillRect(0,0,canvasSize.width, canvasSize.height);

        window.addEventListener('pointermove', pointerMoveEvent);
        window.addEventListener('pointerup', pointerUpEvent);
        textSpace.addEventListener('pointerdown', pointerDownEvent);
        textSpace.addEventListener('input', inputEvent)
    });

    onDestroy(() => {
        window.removeEventListener('pointermove', pointerMoveEvent);
        window.removeEventListener('pointerup', pointerUpEvent);
        textSpace.removeEventListener('pointerdown', pointerDownEvent);
        textSpace.removeEventListener('input', inputEvent)

    });

    function storeHistory() {
        if (!canvasResized) {
            editorHistory.append({
                text: textSpace.innerHTML,
                canvas: ctx.getImageData(
                    0,
                    0,
                    CANVAS_DEFAULT_WIDTH,
                    CANVAS_DEFAULT_HEIGHT
                ),
            });
        } else {
            const resizedCanvas = cloneResizeCanvas(
                canvas,
                CANVAS_DEFAULT_WIDTH,
                CANVAS_DEFAULT_HEIGHT
            )
            const resizedCtx = resizedCanvas.getContext('2d');
            editorHistory.append({
                text: textSpace.innerHTML,
                canvas: resizedCtx.getImageData(
                    0,
                    0,
                    CANVAS_DEFAULT_WIDTH,
                    CANVAS_DEFAULT_HEIGHT
                ),
            });
        }
    }

    function popHistory() {
        if (!canvasResized) {
            editorHistory.apply(ctx, textSpace);
        } else {
            editorHistory.applyResized(
                ctx,
                textSpace,
                canvasSize.width,
                canvasSize.height
            )
        }
    }

    function reset() {
        storeHistory();
        textSpace.innerHTML = '';
        ctx.fillStyle = BACKGROUND_COLOR;
        ctx.fillRect(0,0, canvasSize.width, canvasSize.height);
        hasData = false;
    }

    function send() {
        if (!hasData) {
            return;
        }

        let canvasData = null;
        if (hasDrawn) {
            if (!canvasResized) {
                canvasData = canvas.toDataURL('image/jpeg')
            } else {
                canvasData = cloneResizeCanvas(canvas, 600, 200)
                    .toDataURL('image/jpeg');
            }
        }
        // NOT GOOD ENOUGH IF
        // THE MESSAGE FAIL NO POSSIBILITY
        // TO HANDLE
        dispatch('send', {
            text: textSpace.innerHTML,
            image: canvasData,
        });
        reset();
    }
</script>

<div class="editor-container">
    <div class="editor">
        <div class="editor-text-space" contenteditable bind:this={textSpace}>
        </div>
        <canvas class="editor-canvas" bind:this={canvas}>
        </canvas>
    </div>
    <div class="tools-container">
        <div class="tools">
            <input class="size size-small" type="radio" bind:group={size} name="size" value={1}/>
            <input class="size size-medium" type="radio" bind:group={size} name="size" value={2}/>
            <input class="size size-big" type="radio" bind:group={size} name="size" value={3}/>
            <input use:registerFocus class="color" type="color" bind:value={color}/>
            <button class="reset" on:click={reset}>
                <ResetArrow/>
            </button>
            <button class="undo" on:click={popHistory}>
                <LeftArrow/>
            </button>
            <button class="send" on:click={send} disabled={!hasData}>
                <RightArrow/>
            </button>
        </div>
    </div>
</div>

