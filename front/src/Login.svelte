<div class="card">
    <header>
        {#if loginForm}
            <h1>Login to your account</h1>
        {:else}
            <h1>Register a new account</h1>
        {/if}
        <button class="secondary-button" on:click={_ => loginForm = !loginForm}>
            {#if loginForm}
                Register instead
            {:else}
                Login
            {/if}
        </button>
    </header>
    {#if loginForm}
    <form>
        <label>Username</label>
        <input type="text" name="username" bind:value={username}/>
        <label>Password </label>
        <input type="password" name="password" bind:value={password}/>
        <button on:click={login} disabled={!canLogin}>Login</button>
    </form>
    {:else}
    <form>
        <label>Username</label>
        <input type="text" name="username" bind:value={register_username}/>
        <label>Password</label>
        <input type="password" name="password" bind:value={register_password}/>
        <button on:click={register} disabled={!canRegister}>Register</button>
    </form>
    {/if}
</div>

<script>
    import { Link, Route, Router, useNavigate, useLocation } from 'svelte-navigator';
    import getToken from './lib/login.js'

    const MAIN_LINK = 'room/'
    let username = "";
    let password = "";
    let loginForm = true;
    let loginIsLoading = false;
    $: canLogin = username.length > 0 && password.length > 0 && !loginIsLoading;

    let register_username = "";
    let register_password = "";
    let registerIsLoading = false;
    $: canRegister = register_username.length > 0 && register_password.length > 0 && !registerIsLoading;

    const navigate = useNavigate();
    const location = useLocation();

    function register(e) {
        registerIsLoading = true;
        e.preventDefault();
        let new_user = fetch(`${import.meta.env.VITE_BACK_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: register_username,
                password: register_password
            }),
        })
        .then((res) => {
            return res.json();
        })
        .then((data) => {
            registerIsLoading = false;
            return fetch(`${import.meta.env.VITE_BACK_URL}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: register_username,
                    password: register_password
                }),
            })
        })
        .then((x) => {
            if (x.status != 200) {
                throw new Error("Unable to connect");
            }
            return x.json();
        })
        .then(x => {
            window.localStorage.setItem(
                'jwt',
                x.jwt
            );
            registerIsLoading = false;
            register_username = "";
            register_password = "";
            navigate(MAIN_LINK);
        })
        .catch(x => {
            console.error(x);
            registerIsLoading = false;
        })
    }

    function login(e) {
        loginIsLoading = true;
        e.preventDefault();
        let token = fetch(`${import.meta.env.VITE_BACK_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: username,
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
                'jwt',
                x.jwt
            );
            loginIsLoading = false;
            username = "";
            password = "";
            navigate(MAIN_LINK);
        })
        .catch(x => {
            console.error(x);
            loginIsLoading = false;
        })
    }
</script>
