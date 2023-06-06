<script>
    import { onMount, afterUpdate } from 'svelte';
    import MessageViewer from './MessageViewer.svelte';
    export let messages;
    let messageListContainer;

    function scrollBottom() {
        messageListContainer.scrollTo(
            0,
            messageListContainer.scrollHeight
        )
    }

    onMount(() => scrollBottom());
    afterUpdate(() => scrollBottom());
</script>

<div class="message-container" bind:this={messageListContainer}>
    {#each messages as message}
        <MessageViewer {...message}/>
    {/each}
</div>
