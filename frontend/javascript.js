let darkbtn=document.querySelector(".dark");
let body=document.querySelector("body");
let maincontainer=document.querySelector(".maincontainer")
const API_BASE_URL =
    window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
        ? "http://127.0.0.1:8001"
        : "https://linkedin-post-genertor1-0-1.onrender.com";

darkbtn.addEventListener("click",function(){
    body.classList.toggle("dark-mode");
    if (body.classList.contains('dark-mode')) {
        darkbtn.textContent = '☀️';
    } else {
        darkbtn.textContent = '🌙';
    }
})
document.getElementById("copyBtn").addEventListener("click", function () {
    const postText = document.querySelector(".text").innerText;
    navigator.clipboard.writeText(postText).then(() => {
        const msg = document.getElementById("copyMsg");
        msg.style.display = "block";
        setTimeout(() => msg.style.display = "none", 20000);
    });
});

function getPost() {
    const payload = {
        role: document.getElementById("role").value,
        tone: document.getElementById("tone").value,
        purpose: document.getElementById("purpose").value,
        highlights: document.getElementById("highlights").value,
        insights: document.getElementById("insights").value,
        gratitude: document.getElementById("gratitude").value,
        tags: document.getElementById("tags").value,
        resources: document.getElementById("resources").value,
        reflection: document.getElementById("reflection").value,
        cta: document.getElementById("cta").value,
        hashtags: document.getElementById("hashtags").value,
        extras: document.getElementById("extras").value
    };

    fetch(`${API_BASE_URL}/generatePost/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector('.text').innerHTML = data.post;
    });
}
