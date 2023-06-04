<script>
    // TODO
    // STORE HasData/HasDrawn in historyState
    import { onMount, createEventDispatcher, onDestroy } from 'svelte';
    import { EditorHistory } from './lib/editor.js';

    let canvas;
    let textSpace;
    let color;
    let size = 2;
    let drawing = false;
    let hasData = false;
    let hasDrawn = false;
    const canvasSize = {
        width: 600,
        height: 200
    }
    const cursor = {
        x: null,
        y: null,
    }
    const editorHistory = new EditorHistory();
    const dispatch = createEventDispatcher();
    const DEFAULT_COLOR = '#000';
    const BACKGROUND_COLOR = '#fff';
    let ctx;

    const pointerMoveEvent = function(e) {
        const canvasPosition = canvas.getBoundingClientRect();
        cursor.x = e.clientX - canvasPosition.x - 5;
        cursor.y = e.clientY - canvasPosition.y - 5;
        if (drawing) {
            ctx.fillStyle = color ?? DEFAULT_COLOR;
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
        ctx = canvas.getContext('2d');
        const canvasPosition = canvas.getBoundingClientRect();

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
        editorHistory.append({
            text: textSpace.innerHTML,
            canvas: ctx.getImageData(
                0,
                0,
                canvasSize.width,
                canvasSize.height
            ),
        });
    }

    function popHistory() {
        editorHistory.apply(ctx, textSpace);
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
            canvasData = canvas.toDataURL('image/jpeg')
        }

        // NOT GOOD ENOUGH IF
        // THE MESSAGE FAIL NO POSSIBILITY
        // TO HANDLE
        dispatch('send', {
            text: textSpace.innerHTML,
            image: canvasData,
            user_uuid: "fa7c57c2-f94d-41b0-85ad-e1143674eb65"
        });
        reset();
    }
</script>

<div class="editor-container">
    <div class="tools-container">
        <div class="tools">
            <label>
                <input type="radio" bind:group={size} name="size" value={1}/>
                Small
            </label>
            <label>
                <input type="radio" bind:group={size} name="size" value={2}/>
                Medium
            </label>
            <label>
                <input type="radio" bind:group={size} name="size" value={3}/>
                Large
            </label>
            <label>
                <input type="color" bind:value={color}/>
                Color
            </label>
            <button on:click={popHistory}>undo</button>
            <button on:click={reset}>reset</button>
            <button on:click={send} disabled={!hasData}>send</button>
        </div>
    </div>
    <div class="editor">
        <div class="editor-text-space" contenteditable bind:this={textSpace}>
        </div>
        <canvas class="editor-canvas" bind:this={canvas}>
        </canvas>
    </div>
</div>

