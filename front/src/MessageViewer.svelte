<div class="message-viewer" bind:this={messageViewer}>
    <div class="text-space" contenteditable bind:this={textSpace}>
    </div>
    <canvas bind:this={canvas}>
    </canvas>
</div>

<script>
    import { onMount } from 'svelte';

    export let text;
    export let date;
    export let image;
    const canvasSize = {
        width: 600,
        height: 300
    }
    const paddingSize=10;
    $: imgDataUrl = image;
    let messageViewer;
    let canvas;
    let textSpace;
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

        // create image
        const img = new Image();
        img.onload = function() {
            ctx.drawImage(img, 0,0);
        }
        img.src = imgDataUrl;

        // create text:
        textSpace.innerHTML = text;
    })


</script>

<style>
    .message-viewer {
        width: 600px;
        height: 300px;
    }
</style>
