<div class="chat-container">
    <MessageList {messages}/>
    <Editor on:send={send}/>
</div>

<script>
    import { onMount } from 'svelte';
    import { useParams, useNavigate } from "svelte-navigator";
    import getToken, { getTokenPayload, logout } from './lib/login.js';
    import MessageList from './MessageList.svelte';
    import Editor from './Editor.svelte';
    const params = useParams();

    const url =  `${import.meta.env.VITE_WEBSOCKET_URL}/ws/${$params.roomUUID}`
    const chatSocket = new WebSocket(url);
    let messages = [];
    let navigate = useNavigate();

    // handle connection closed event
    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        messages = [...messages, data];
    }

    onMount(async () => {
        try {
            const response = await fetch(
              `${import.meta.env.VITE_BACK_URL}/messages/${$params.roomUUID}`,
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
        } catch {
            logout();
            navigate('/');
        }
    })

    function send(e) {
        e.detail.room_uuid = $params.roomUUID;
        e.detail.user_uuid = getTokenPayload()['uuid'];
        e.detail.jwt = getToken()
        chatSocket.send(JSON.stringify(e.detail));
    }
</script>
