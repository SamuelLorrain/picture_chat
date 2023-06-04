<div class="chat-container">
    <MessageList {messages}/>
    <Editor on:send={send}/>
</div>

<script>
    import { onMount } from 'svelte';
    import { useParams } from "svelte-navigator";
    import MessageList from './MessageList.svelte';
    import Editor from './Editor.svelte';
    const params = useParams();

    const url =  `ws://localhost:8000/ws`
    const chatSocket = new WebSocket(url);
    let messages = [];

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        messages = [...messages, data];
    }

    onMount(async () => {
        const response = await fetch(`http://localhost:8000/messages/${$params.roomUUID}`)
        const data = await response.json();
        messages = [...data];
    })

    function send(e) {
        e.detail.room_uuid = $params.roomUUID;
        chatSocket.send(JSON.stringify(e.detail));
    }
</script>
