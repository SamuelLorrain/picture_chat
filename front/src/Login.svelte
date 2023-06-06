<div class="card">
    <header>
        {#if loginForm}
            <h1>Login to your account</h1>
        {:else}
            <h1>Register a new account</h1>
        {/if}
        <button class="secondary-button" on:click={changeForm}>
            {#if loginForm}
                Register instead
            {:else}
                Login
            {/if}
        </button>
    </header>
    {#if loginForm}
    <form>
        <label for="username">Username</label>
        <input id="username" type="text" name="username" bind:value={username} class:invalid={loginError} on:input={_ => loginError = false}/>
        <label for="password">Password </label>
        <input id="password" type="password" name="password" bind:value={password} class:invalid={loginError} on:input={_ => loginError = false}/>
        <button on:click={login} disabled={!canLogin}>Login</button>
    </form>
    {:else}
    <form>
        <label for="register_username">Username</label>
        <input id="register_username" type="text" name="username" bind:value={registerUsername} class:invalid={registerError} on:input={_ => registerError = false}/>
        <label for="register_password">Password</label>
        <input for="register_password" type="password" name="password" bind:value={registerPassword} class:invalid={registerError} on:input={_ => registerError = false}/>
        <button on:click={register} disabled={!canRegister}>Register</button>
    </form>
    {/if}
    {#if loginError}
    <div class="error">
        Unable to login, please enter good credentials or try again later.
    </div>
    {/if}
    {#if registerError}
    <div class="error">
        Unable to register, please enter others credentials or try again later.
    </div>
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
    let loginError = false;
    $: canLogin = username.length > 0 && password.length > 0 && !loginIsLoading && !loginError;

    let registerUsername = "";
    let registerPassword = "";
    let registerIsLoading = false;
    let registerError = false;
    $: canRegister = registerUsername.length > 0 && registerPassword.length > 0 && !registerIsLoading && !registerError;

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
                name: registerUsername,
                password: registerPassword
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
                    name: registerUsername,
                    password: registerPassword
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
            registerUsername = "";
            registerPassword = "";
            navigate(MAIN_LINK);
        })
        .catch(x => {
            console.error(x);
            registerIsLoading = false;
            registerError = true;
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
            loginError = true;
        })
    }

    function changeForm() {
        loginError = false;
        registerError = false;
        username = "";
        password = "";
        registerUsername = "";
        registerPassword = "";
        loginForm = !loginForm;
    }
</script>
