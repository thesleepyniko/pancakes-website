const form = document.getElementById("commentForm");
form.addEventListener("submit", addComment);

async function updateComments() {
    const container = document.getElementById("comments");
    try {
        container.innerText = "reloading comments...";
        const response = await fetch("/api/comments");
        const data = await response.json();
        if (!data || data.length == 0) {
            container.innerText = "";
        }
        container.innerHTML = "";
        for (const c of data) {
            const p = document.createElement("p");
            p.textContent = "Comment by " + c.name
            + " at " + c.date + ": " + c.comment; 
            container.appendChild(p);
        }
        console.log(data);
    }    
    catch(err) {
        console.error("Fetch error:", err);
        container.innerHtml = ""
        container.innerText = "could not get comments, try again later"}
}

setInterval(updateComments, 10000)
window.addEventListener("DOMContentLoaded", updateComments);

function addComment(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const comment_div = document.getElementById("comments");

    const data = {
        name: formData.get("firstname"),
        comment: formData.get("comment"),
        date: new Date().toISOString()
    };

    fetch("/api/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => console.log("Success:", data))
    .catch(error => console.error("Error:", error));   

    const p = document.createElement("p");
    p.textContent = "Comment by " + formData.get("firstname")
        + " at " + Date() + ": " + formData.get("comment"); 
    comment_div.appendChild(p);
}