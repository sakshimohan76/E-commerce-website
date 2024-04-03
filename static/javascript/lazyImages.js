function lazyLoadImages(container) {
    const imgDivs = container.querySelectorAll(".common-img-container");
    imgDivs.forEach((container) => {
        const image = container.querySelector('img');

        const onLoaded = () => {
            container.classList.add("load-completed");
        }

        if (image.complete) {
            onLoaded();
        } else {
            image.addEventListener("load", onLoaded);
        }
    })
}
lazyLoadImages(document);
