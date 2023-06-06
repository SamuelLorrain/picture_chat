export const getTokenPayload = () => {
    const token = getToken();
    if (!token) {
        return undefined;
    }
    const parts = token.split('.');
    const payload = atob(parts[1]);
    return JSON.parse(payload);
}

export function logout() {
    return window.localStorage.removeItem('jwt');
}

export default function getToken() {
    return window.localStorage.getItem('jwt');
}
