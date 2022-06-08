<main>
    <MessageList {messages}/>
    <Editor on:send={send}/>
</main>
<script>
    import MessageList from './MessageList.svelte';
    import Editor from './Editor.svelte';

    let messages;
        {
            text: 'test',
            date: Date.now(),
            image: 'image'
        },
        {
            text: 'toast',
            date: Date.now(),
            image: 'image'
        }
    ];

    function send() {
        fetch()
        .then()
        .catch();
    }

</script>
