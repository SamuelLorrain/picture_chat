<Route path={path}>
    <slot/>
</Route>

<script>
    import { useNavigate, Route } from 'svelte-navigator';
    import { onMount } from 'svelte';
    import getToken from './lib/login.js';
    let navigate = useNavigate();

    export let path;
    export let redirect;

    $: if(getToken()) {
        navigate(redirect);
    }
</script>
