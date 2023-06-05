<div>
    <form>
        <label>
            Username
            <input type="text" name="username" bind:value={username}/>
        </label>
        <label>
            Password
            <input type="password" name="password" bind:value={password}/>
        </label>
        <button on:click={login} disabled={!canLogin}>Login</button>
    </form>
    <form>
        <label>
            Username
            <input type="text" name="username" bind:value={register_username}/>
        </label>
        <label>
            Password
            <input type="password" name="password" bind:value={register_password}/>
        </label>
        <button on:click={register} disabled={!canRegister}>Register</button>
    </form>
</div>

<script>
    import { Link, Route, Router, useNavigate, useLocation } from 'svelte-navigator';
    import getToken from './lib/login.js'

    const MAIN_LINK = 'room/'
    let username = "";
    let password = "";
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
        let new_user = fetch('http://localhost:8000/register', {
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
            return fetch('http://localhost:8000/login', {
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
        let token = fetch('http://localhost:8000/login', {
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
