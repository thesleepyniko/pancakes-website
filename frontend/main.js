const form = document.getElementById("commentForm")
form.addEventListener("submit", addComment);

function addComment(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const comment_div = document.getElementById("comments")

    const p = document.createElement("p");
    p.textContent = "Comment by " + formData.get("firstname")
        + " at " + Date() + ": " + formData.get("comment"); 
    comment_div.appendChild(p);
}

function exampleFunc(parameter) {
    //code here!
    console.log("the argument passed was" + parameter)
}
