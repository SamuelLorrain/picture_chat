<form>
    <label>
        Username
        <input type="text" name="username" bind:value={username}/>
    </label>
    <label>
        Password
        <input type="password" name="password" bind:value={password}/>
    </label>
    <button on:click={login}>Login</button>
</form>

<script>
    import { Link, Route, Router, useNavigate, useLocation } from 'svelte-navigator';
    import { onMount } from 'svelte';
    import getToken from './lib/login.js'

    const MAIN_LINK = 'chat/'
    let username;
    let password;
    const navigate = useNavigate();
    const location = useLocation();

    onMount(() => {
        if(getToken()) {
            navigate('/chat', {replace:true});
        }
    });

    function login(e) {
        e.preventDefault();
        let token = fetch('http://localhost:8000/tokens/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username,
                password
            }),
        })
        .then((x) => {
            if (x.status != 200) {
                throw new Error("Unable to connect");
            }
            return x.json();
        })
        .then(x => {
            window.localStorage.setItem(
                'token',
                JSON.stringify(x)
            );
            navigate(MAIN_LINK);
        })
        .catch(x => {
            console.error(x);
        })
    }
</script>
