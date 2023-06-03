<script>
    import MessageViewer from './MessageViewer.svelte';

    export let messages;
</script>

<div>
    <div class="container">
        {#each messages as message}
            <MessageViewer {...message}/>
        {/each}
    </div>
</div>


<style>
    .container {
        max-height: 45vh;
        overflow-x: scroll;
    }
</style>
