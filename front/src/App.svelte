<Router>
    <div>
        <nav>
            <Link to="/">Link</Link>
            <Link to="/chat">Chat</Link>
        </nav>

        <Route path="/">
            <Login/>
            <Chat/>
        </Route>
    </div>
</Router>

<script>
    import { Link, Route, Router } from 'svelte-navigator';
    import Chat from './Chat.svelte';
    import Login from './Login.svelte';
</script>
