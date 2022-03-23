async function onClick(event){
    event.preventDefault();

    const likeLink = event.target;
    response = await fetch(likeLink.href);

    let responseData = await response.json()

    if (response.ok) {
        const articleId = likeLink.dataset.articleId;
        let likeCounter = document.getElementById(`like-counter-${articleId}`);
        likeCounter.innerText = `Лайкнуло: ${responseData.likes_count}`;

         for (likeLinkToToggle of document.querySelectorAll(`a[data-article-id="${articleId}"]`)) {
            likeLinkToToggle.classList.toggle("invisible");
        }

    } else {
        alert(responseData.error);
    }
}

function onLoad(){
    for (element of document.getElementsByClassName("like-link")) {
        element.addEventListener("click", onClick);
    }
}

window.addEventListener("load", onLoad);
