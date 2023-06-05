export const getTokenPayload = () => {
    const token = getToken();
    const parts = token.split('.');
    const payload = atob(parts[1]);
    return JSON.parse(payload);
}

export default function getToken() {
    return window.localStorage.getItem('jwt');
}
