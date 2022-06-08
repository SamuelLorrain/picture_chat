<div class="message-viewer" bind:this={messageViewer}>
    text: {text}
    image: {image}
</div>

<script>
    import { onMount } from 'svelte';

    export let text;
    export let date;
    export let image;
    let messageViewer;

    onMount(() => {
        messageViewer.style.backgroundImage = image;
    })
</script>

<style>
    .message-viewer {
        width: 600px;
        height: 300px;
    }
</style>
