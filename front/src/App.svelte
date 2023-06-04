<script>
    import { Router, Route, Link} from 'svelte-navigator';
    import Room from './Room.svelte';
    import Chat from './Chat.svelte';
</script>

<Router>
    <div class="app-container">
        <Route path="/chat/:roomUUID">
            <Chat/>
        </Route>
        <Route path="/room">
            <Room/>
        </Route>
        <Route path="/">
            <Room/>
        </Route>
    </div>
</Router>
