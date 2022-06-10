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
    import MessageList from './MessageList.svelte';
    import Editor from './Editor.svelte';

    let messages = [];

    async function send(e) {
        try {
            await fetch('http://localhost:8000/messages/', {
                method:'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(e.detail),
            })
        } catch(error) {
            console.log(error);
        }
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
