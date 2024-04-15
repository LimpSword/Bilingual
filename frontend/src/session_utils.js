export function isUserLoggedIn() {
    return localStorage.getItem('token') !== null;
}

export function signOut() {
    localStorage.removeItem('token');
}

export function getUserName() {
    return localStorage.getItem('username');
}

export function getUserEmail() {
    return localStorage.getItem('email');
}