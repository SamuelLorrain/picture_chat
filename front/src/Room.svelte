<script>
    import { Link } from 'svelte-navigator';
    import { onMount } from 'svelte';
    import getToken from './lib/login';
    let rooms = []
    let isLoading = false;
    $: canSend = !isLoading && newRoomName.length > 0;
    let newRoomName = ""

    onMount(async () => {
        const response = await fetch(`${import.meta.env.VITE_BACK_URL}/room`, {
            headers: {
              'Authorization': `Bearer ${getToken()}`
            }
        })
        const data = await response.json();
        rooms = [...data];
    })

    function createRoom() {
        isLoading = true;
        fetch(`${import.meta.env.VITE_BACK_URL}/room`, {
            method: 'POST',
            headers: {
             'Content-Type': 'application/json',
             'Authorization': `Bearer ${getToken()}`
            },
            body: JSON.stringify({
              name: newRoomName
            })
        })
        .then((data) => {
            if (data.status > 400) {
                throw Error("unable to create room");
            }
            return data.json()
        })
        .then((json) => {
            rooms = [...rooms, json];
            isLoading = false;
            newRoomName = "";
        })
        .catch((e) => {
            isLoading = false;
        })
    }
</script>

<div>
    Rooms:
    <div>
        {#each rooms as room}
            <div>
                <Link to={`/chat/${room.uuid}`}>{room.name}</Link>
            </div>
        {/each}
    </div>
    <div>
        <label>
            New room name
            <input type="text" bind:value={newRoomName}/>
        </label>
        <button on:click={createRoom} disabled={!canSend}>Create Room</button>
    </div>
</div>
