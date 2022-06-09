<template>
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

</template>

<script>
    let username;
    let password;
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
