document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("comicForm");

    const button = document.getElementById("generateButton");


    if (form && button) {

        form.addEventListener("submit", function () {

            button.disabled = true;

            button.innerHTML =
                "⏳ Generating Comic... Please Wait";

        });

    }

});