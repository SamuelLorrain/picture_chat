<Router>
    <div>
        <nav>
            <Link to="/">Link</Link>
            <Link to="/chat">Chat</Link>
        </nav>

        <Route path="/">
            <Login/>
        </Route>
        <PrivateRoute path="/chat">
            <Chat/>
        </PrivateRoute>
    </div>
</Router>

<script>
    import { Link, Route, Router } from 'svelte-navigator';
    import Chat from './Chat.svelte';
    import Login from './Login.svelte';
    import PrivateRoute from './PrivateRoute.svelte';
</script>
