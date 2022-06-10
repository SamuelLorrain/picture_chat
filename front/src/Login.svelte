<Router>
    <div>
        <Link to="/">Link</Link>
        <Link to="/chat">Chat</Link>

        <Route path="/">
            <form>
                <label>
                    Username
                    <input type="text" name="username" value={username}/>
                </label>
                <label>
                    Password
                    <input type="password" name="password" value={password}/>
                </label>
            </form>
        </Route>
        <Route path="/chat">
            <Chat/>
        </Route>
    </div>
</Router>

<script>
    import { Link, Route, Router } from 'svelte-navigator';
    import Chat from './Chat.svelte';

    let username = '';
    let password = '';
    function login() {
        let token = fetch('http://localhost:3000/tokens/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username,
                password
            }),

        })
    }
</script>
