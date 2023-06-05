<div class="chat-container">
    <MessageList {messages}/>
    <Editor on:send={send}/>
</div>

<script>
    import { onMount } from 'svelte';
    import { useParams } from "svelte-navigator";
    import getToken, { getTokenPayload } from './lib/login.js';
    import MessageList from './MessageList.svelte';
    import Editor from './Editor.svelte';
    const params = useParams();

    const url =  `ws://localhost:8000/ws/${$params.roomUUID}`
    const chatSocket = new WebSocket(url);
    let messages = [];

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        messages = [...messages, data];
    }

    onMount(async () => {
        const response = await fetch(
          `http://localhost:8000/messages/${$params.roomUUID}`,
          {
            headers: {
              'Authorization': `Bearer ${getToken()}`
            }
          }
        )
        if (response.status > 400) {
          throw Error("Unable to create message");
        }
        const data = await response.json();
        messages = [...data];
    })

    function send(e) {
        e.detail.room_uuid = $params.roomUUID;
        e.detail.user_uuid = getTokenPayload()['uuid'];
        e.detail.jwt = getToken()
        chatSocket.send(JSON.stringify(e.detail));
    }
</script>
