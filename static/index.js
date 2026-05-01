let profile = null;
const LOGIN_BUTTON = document.getElementById("login-button")
const USERNAME_ELEMENT = document.getElementById("profile-name")
const USERNAME_AREA = document.getElementById("profile-name-area")
const LOGOUT_BUTTON = document.getElementById("logout-button")
const HOST_SERVER = getCookie("host-server");

function getCookie(key) {
    var cookies = document.cookie.split(";")
    var value = cookies.find(element => element.trim().startsWith(key + "=")).trim()

    return value ? value.substring(key.length + 1, value.length) : null
}

async function loadProfile(token) {
    var resp = await fetch(`${HOST_SERVER}/profile`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        }
    })

    if (!resp.ok) {
        return null
    }

    return await resp.json()
}

addEventListener("load", async (e) => {
    if (!HOST_SERVER) {
        location.href = "./login.html"
        return
    }

    try {
        profile = await loadProfile(getCookie("token"))
        if (profile === null) {
            alert("セッションの有効期限が切れました。再度ログインしてください。")
            location.href = "./login.html"
            return
        }
    }
    catch {
        alert("このシステムを使用するには、ログインをしてください。")
        location.href = "./login.html"
        return
    }

    window.dispatchEvent(new CustomEvent("profileLoaded", {detail: profile}))

    LOGIN_BUTTON.style.display = "none"
    USERNAME_ELEMENT.innerText = profile.name
    USERNAME_AREA.style.display = "unset"
})

LOGOUT_BUTTON.addEventListener("click", (event) => {
    document.cookie = "token=; max-age=0"
    location.href = "./login.html"
})
