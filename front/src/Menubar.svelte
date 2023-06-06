<menu>
    {#if hasReturnButton}
    <button class="secondary-button return-button" on:click={returnToRoom}>
        Return to rooms
    </button>
    {/if}
    {#if tokenPayload?.username}
        <p>Welcome <b>{tokenPayload.username}</b>!</p>
    {/if}
    {#if tokenPayload}
        <button on:click={processLogout}>Logout</button>
    {/if}
</menu>

<script>
    import { beforeUpdate } from 'svelte';
    import { getTokenPayload, logout } from './lib/login';
    import { useLocation, useNavigate } from 'svelte-navigator';
    import LeftArrow from './icons/LeftArrow.svelte';

    let tokenPayload = getTokenPayload();

    beforeUpdate(() => {
        tokenPayload = getTokenPayload();
    });

    const location = useLocation();
    const navigation = useNavigate();
    $: hasReturnButton = $location?.pathname?.startsWith('/chat/');

    function returnToRoom() {
        navigation('/room');
    }

    function processLogout() {
        logout();
        navigation('/');
    }
</script>
