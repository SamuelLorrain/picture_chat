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

    export let text;
    export let image;
    export let user;
    export let datetime;
    export let uuid;
    export let room;
    const canvasSize = {
        width: 600,
        height: 200
    }
    $: imgDataUrl = image;
    $: formattedDatetime = (new Date(datetime)).toLocaleDateString();
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
