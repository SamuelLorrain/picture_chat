<div>
    {#each messages as message}
        <MessageViewer {...message} :key={message.text+message.date}/>
    {/each}
</div>

<script>
    import MessageViewer from './MessageViewer.svelte';

    export let messages;
</script>
