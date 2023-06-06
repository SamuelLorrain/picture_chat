<div class="message-viewer" bind:this={messageViewer}>
    <div class="message-viewer-header">
        <div class="username">
            {#if user && user.name}
                {user.name}
            {:else}
                user deleted
            {/if}
        </div>
        <div class="datetime">
            {formattedDatetime}
        </div>
    </div>
    <div class="message-viewer-text-space" bind:this={textSpace}></div>
    <canvas bind:this={canvas}></canvas>
</div>

<script>
    import { onMount } from 'svelte';
    import { cloneResizeCanvas } from './lib/utils';

    export let text;
    export let image;
    export let user;
    export let datetime;
    export let uuid;
    export let room;
    const CANVAS_DEFAULT_WIDTH = 600;
    const CANVAS_DEFAULT_HEIGHT = 200;
    const canvasSize = {
        width: CANVAS_DEFAULT_WIDTH,
        height: CANVAS_DEFAULT_HEIGHT
    }
    $: imgDataUrl = image;
    $: formattedDatetime = (new Date(datetime)).toLocaleDateString();
    let messageViewer;
    let canvas;
    let canvasResized = false;
    let textSpace;
    let ctx;
    let img = new Image();

    onMount(() => {
        if (window.innerWidth < canvasSize.width) {
            canvasSize.width = window.innerWidth;
            canvasSize.height = (window.innerWidth / 3.0);
            canvasResized = true;
        }
        ctx = canvas.getContext('2d');
        canvas.width = canvasSize.width;
        canvas.height = canvasSize.height;

        // create image
        img.src = imgDataUrl;
        img.onload = function() {
            ctx.drawImage(img, 0,0, canvasSize.width, canvasSize.height);
        }

        // create text:
        textSpace.innerHTML = text;
    })


</script>
