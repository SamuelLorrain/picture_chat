<Route path={path}>
    <slot/>
</Route>

<script>
    import { useNavigate, useLocation, Route } from 'svelte-navigator';
    import { onMount } from 'svelte';
    import getToken from './lib/login.js';

    export let path;

    let navigate = useNavigate();

    $: if(!getToken()) {
        navigate('/');
    }
</script>
