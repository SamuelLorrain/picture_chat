<Route path={path} redirect={redirect}>
    <slot/>
</Route>

<script>
    import { useNavigate, Route } from 'svelte-navigator';
    import { onMount } from 'svelte';
    import getToken from './lib/login.js';

    export let path;
    export let redirect;

    let navigate = useNavigate();

    $: if(!getToken()) {
        navigate(redirect);
    }
</script>
