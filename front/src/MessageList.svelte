<div>
    <div class="container">
        {#each messages as message}
            <MessageViewer {...message} :key={message.text+message.image}/>
        {/each}
    </div>
</div>

<script>
    import MessageViewer from './MessageViewer.svelte';

    export let messages;
</script>

<style>
    .container {
        max-height: 45vh;
        overflow-x: scroll;
    }
</style>
