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
    import { useNavigate } from 'svelte-navigator';
    import MessageList from './MessageList.svelte';
    import Editor from './Editor.svelte';
    import getToken from './lib/login.js'
    const navigate = useNavigate();
    let messages = [];
    const url =  `ws://localhost:8000/ws/socket-server/`
    const chatSocket = new WebSocket(url);

    onMount(() => {
        if(!getToken()) {
            navigate('/', {replace:true});
        }
    });

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        messages = data.map((x) => x.fields);
    }

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
