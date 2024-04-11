export function isUserLoggedIn() {
    return localStorage.getItem('token') !== null;
}

export function signOut() {
    localStorage.removeItem('token');
}