<main>
    <div class="container">
        <div>
            <MessageList {messages}/>
            <Editor on:send={send}/>
        </div>
    </div>
</main>
<script>
    import { onMount } from 'svelte';
    import MessageList from './MessageList.svelte';
    import Editor from './Editor.svelte';
    let messages = [];
    const url =  `ws://localhost:8000/ws`
    const chatSocket = new WebSocket(url);

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        messages = [...messages, data];
    }


    onMount(async () => {
        const response = await fetch('http://localhost:8000/messages')
        const data = await response.json();
        messages = [...data];
    })

    function send(e) {
        chatSocket.send(JSON.stringify(e.detail));
    }
</script>

<style>
    .container {
        display: flex;
        justify-content:center;
        margin-top:10vh;
        margin-bottom:10vh;
    }
</style>
