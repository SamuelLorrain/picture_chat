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

    function createRoom(e) {
        e.preventDefault();
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

<div class="card">
    <header>
        <div>
            <h1>Rooms</h1>
            <p class="subtitle">Choose or create a room</p>
        </div>
    </header>
    <div class="rooms-list">
        {#each rooms as room}
            <Link to={`/chat/${room.uuid}`}>
                <div class="room-selection-box">
                    {room.name}
                </div>
            </Link>
        {/each}
    </div>
    <hr/>
    <form>
        <label for="new_room">New room</label>
        <input id="new_room" type="text" bind:value={newRoomName}/>
        <button on:click={createRoom} disabled={!canSend}>Create Room</button>
    </form>
</div>
