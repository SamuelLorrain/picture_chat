<script>
    import { Router, Route, Link} from 'svelte-navigator';
    import PrivateRoute from './PrivateRoute.svelte';
    import RedirectIfLoggedRoute from './RedirectIfLoggedRoute.svelte';
    import Room from './Room.svelte';
    import Chat from './Chat.svelte';
    import Login from './Login.svelte';

    const rootPath = "/";
</script>

<Router>
    <div class="app-container">
        <PrivateRoute path="/chat/:roomUUID" redirect={rootPath}>
            <Chat/>
        </PrivateRoute>
        <PrivateRoute path="/room" redirect={rootPath}>
            <Room/>
        </PrivateRoute>
        <RedirectIfLoggedRoute path={rootPath} redirect="/room">
            <Login/>
        </RedirectIfLoggedRoute>
    </div>
</Router>
