export default () => {
    const token = window.localStorage.getItem('token')
    return JSON.parse(token);
}
