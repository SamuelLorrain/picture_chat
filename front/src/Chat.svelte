<main>
    <div class="container">
        <div>
            <MessageList {messages}/>
            <Editor on:send={send}/>
            <button on:click={get}>GET</button>
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
    const url =  `ws://localhost:8000/ws/socket-server/`
    const chatSocket = new WebSocket(url);

    onMount(() => {
        if(!getToken()) {
            navigate('/', {replace:true});
        }
    });

    let messages = [];

    function send(e) {
        chatSocket.send(JSON.stringify(e.detail));
    }

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log(data);
        messages = data.map((x) => x.fields);
    }

    function get() {
        fetch('http://localhost:8000/messages/', {
            method: 'GET'
        })
        .then((x) => x.json())
        .then((jsonData) => {
            messages = jsonData.map((x) => x);
        })
        .catch((x) => console.error(x));
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
