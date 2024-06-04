document.addEventListener("DOMContentLoaded", function() {
    var div8 = document.querySelector(".div8");
    var content = document.querySelector(".content");

    setTimeout(function() {
        div8.style.display = "none";
        content.style.display = "block";
    }, 2000); // 5000 milliseconds = 5 seconds
});
