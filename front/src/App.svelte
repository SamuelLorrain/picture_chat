<main>
    <MessageList {messages}/>
    <Editor on:send={send}/>
    <button on:click={get}>GET</button>
</main>
<script>
    import MessageList from './MessageList.svelte';
    import Editor from './Editor.svelte';

    let messages = [];

    async function send(e) {
        try {
            await fetch('http://localhost:8000/message/', {
                method:'POST',
                body: JSON.stringify(e.detail),
            })
        } catch(error) {
            console.log(error);
        }
    }

    function get() {
        fetch('http://localhost:8000/message/', {
            method: 'GET'
        })
        .then((x) => x.json())
        .then((jsonData) => {
            console.log(jsonData);
            messages = jsonData.map((x) => x.fields);
            console.log(messages);
        })
        .catch((x) => console.error(x));
    }

</script>
