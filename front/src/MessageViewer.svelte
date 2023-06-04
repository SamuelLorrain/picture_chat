<div class="message-viewer" bind:this={messageViewer}>
    <div class="message-viewer-text-space" bind:this={textSpace}></div>
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
