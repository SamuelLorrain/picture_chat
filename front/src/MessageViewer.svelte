<div class="message-viewer" bind:this={messageViewer}>
    <div class="text-space" bind:this={textSpace}>
        <div></div>
    </div>
    <canvas bind:this={canvas}></canvas>
</div>

<script>
    import { onMount } from 'svelte';

    export let text;
    export let image;
    export let user_uuid;
    export let datetime;
    const canvasSize = {
        width: 600,
        height: 200
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
        canvas.style.top = -canvasSize.y+'px';

        canvas.style.position = 'relative';
        textSpace.style.width = canvasSize.width+'px';
        textSpace.style.height = canvasSize.height+'px';
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
        height: 200px;
    }

    canvas {
        top:-200px;
        position:relative;
    }
    .text-space {
        position:relative;
        z-index:10;
    }
</style>
