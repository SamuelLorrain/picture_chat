<div>
    <div class="editor">
        <div class="text-space" contenteditable bind:this={textSpace}>
        </div>
        <canvas bind:this={canvas}>
        </canvas>
    </div>

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
        <button on:click={popHistory}>pop</button>
        <button on:click={reset}>reset</button>
        <button on:click={send}>send</button>
    </div>
</div>

<script>
    import { onMount, createEventDispatcher } from 'svelte';
    import { EditorHistory } from './lib/editor.js';

    let size = 1;
    let drawing = false;
    let canvas;
    let textSpace;
    let color;
    const canvasSize = {
        width: 600,
        height: 300
    }
    const paddingSize=10;
    const cursor = {
        x: null,
        y: null,
    }
    const editorHistory = new EditorHistory();
    const dispatch = createEventDispatcher();
    let ctx;

    onMount(() => {
        ctx = canvas.getContext('2d');
        const canvasPosition = canvas.getBoundingClientRect();

        canvas.width = canvasSize.width;
        canvas.height = canvasSize.height;
        textSpace.style.width = canvasSize.width+'px';
        textSpace.style.height = canvasSize.height+'px';
        textSpace.style.top = -canvasSize.y+'px';
        textSpace.style.left = -canvasSize.x+'px';
        textSpace.style.position = 'absolute';
        textSpace.style.padding=paddingSize+'px';

        window.addEventListener('pointermove', function(e) {
            const canvasPosition = canvas.getBoundingClientRect();
            cursor.x = e.clientX - canvasPosition.x - 5;
            cursor.y = e.clientY - canvasPosition.y - 5;
            if (drawing) {
                ctx.fillStyle = color ?? '#000';
                ctx.fillRect(cursor.x, cursor.y, size*10, size*10);
            }
        });
        window.addEventListener('pointerup', function(e) {
            drawing = false;
            canvas.style.cursor = "default";
            textSpace.style.cursor = "default";
        });
        textSpace.addEventListener('pointerdown', function(e) {
            storeHistory();
            drawing = true;
            canvas.style.cursor = "crosshair";
            textSpace.style.cursor = "crosshair";
        });
        textSpace.addEventListener('input', function(e) {
            if(e.data == ' ' || e.inputType == 'insertParagraph') {
                storeHistory();
            }
        })
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
        ctx.fillStyle = color;
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0,0, canvasSize.width, canvasSize.height);
    }

    function send() {
        // NOT GOOD ENOUGH IF
        // THE MESSAGE FAIL NO POSSIBILITY
        // TO HANDLE
        dispatch('send', {
            text: textSpace.innerHTML,
            canvas: canvas.toDataURL('image/jpeg'),
        });
        reset();
    }
</script>

<style>
    .text-space {
        border: 1px solid black;
        cursor: default;
    }

    .tools {
        margin-top:1rem;
    }
</style>
